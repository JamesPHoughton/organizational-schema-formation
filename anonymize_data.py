#!/usr/bin/env python3
"""
Anonymize the raw scienceData exports prior to public release.

Policy (decided 2026-06-11). Rather than dropping whole metadata blocks, we filter
at the FIELD level: keep coarse covariates that may plausibly influence behavior,
remove only the high-entropy fingerprints and pure recruitment metadata.

connectionInfo  -- KEEP: country, timezone, isKnownVpn, isLikelyVpn, effectiveType,
                         downlink, rtt, saveData   (region/norms, data quality,
                         network quality that affects the video call)
                -- DROP: timezoneOffset (duplicate of timezone)

browserInfo     -- KEEP: screenWidth, screenHeight, width, height (what the
                         participant sees), language (native language -> labeling)
                -- ADD : device  (coarse OS/form-factor/browser class parsed from UA)
                -- DROP: userAgent (exact build string = fingerprint; replaced by
                         the coarse `device`), referrer (recruitment source only),
                         timezone (duplicate of connectionInfo.timezone)

demographics    -- COARSEN birth_year -> birth-decade band (e.g. "1980-1989").
                   All other demographic categories kept (gender, race, income,
                   education, employment, etc.) for sample-description tables.

free text       -- REDACT participant/partner first names that leaked into open
                   responses (from a full audit of every free-text field), scoped
                   to the specific (gameId, position, field). Plus a defensive
                   email/phone/URL net (audit found none).

KEPT: sampleId and recording ids/room/path -- internally generated, no external link.

IDEMPOTENT; edits scienceData files IN PLACE. Originals remain in git history (this
script does not rewrite history). postFlightReport.jsonl (batch aggregates) and
preregistration.jsonl (anon sampleId + config) contain no PII and are not touched.
"""
import json
import glob
import re

# ---- field-level keep-lists for the metadata blocks --------------------------
CONNECTION_KEEP = {
    "country", "timezone", "isKnownVpn", "isLikelyVpn",
    "effectiveType", "downlink", "rtt", "saveData",
}
BROWSER_KEEP = {"screenWidth", "screenHeight", "width", "height", "language"}

# ---- free-text name redactions (from the PII audit) --------------------------
# (gameId last-6, position) -> names (lowercase) to redact in that participant's
# open responses + QC textExpansion only. Same token used as an image label by
# another participant is untouched (redaction is scoped per participant+field).
# position is stored as a string ("0"/"1") in the data, so keys use strings.
NAME_REDACTIONS = {
    ("P0JRKR", "1"): {"jessica", "mike"},   # own name + partner ("jane" is a label -> kept)
    ("WFFYV5", "1"): {"brit"},              # partner, in QC textExpansion
    ("7ZTEW8", "0"): {"eva"},               # partner
    ("5Y647G", "1"): {"lewis"},             # partner
    ("TJKZD2", "1"): {"tom"},               # partner (borderline; redacted conservatively)
}
FREE_TEXT_PROMPTS = {"prompt_strategy", "prompt_mistake", "prompt_working_together"}
QC_FREE_FIELDS = {"technicalDetail", "textExpansion", "joiningDetail"}

STRUCTURED_PII = [
    re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),                 # email
    re.compile(r"https?://\S+|www\.\S+"),                   # url
    re.compile(r"(?<!\d)\+?\d[\d\-\.\s]{7,}\d(?!\d)"),      # phone-ish
]


def coarse_device(ua):
    """Parse a userAgent into a low-entropy '<OS> <form-factor> / <browser>' class.
    Returns None if ua is empty/non-string. Idempotent: a string with no '/'
    version tokens (i.e. an already-coarsened device label) maps to 'Other ...'."""
    if not isinstance(ua, str) or not ua.strip():
        return None
    u = ua
    if "Windows" in u:
        os_ = "Windows"
    elif "Mac OS X" in u or "Macintosh" in u:
        os_ = "macOS"
    elif "Android" in u:
        os_ = "Android"
    elif "iPhone" in u or "iPad" in u or "iOS" in u:
        os_ = "iOS"
    elif "Linux" in u or "X11" in u or "CrOS" in u:
        os_ = "Linux"
    else:
        os_ = "Other"

    if "iPad" in u or "Tablet" in u:
        form = "tablet"
    elif "Mobile" in u or "Android" in u or "iPhone" in u:
        form = "mobile"
    else:
        form = "desktop"

    if "Edg/" in u or "Edge" in u:
        br = "Edge"
    elif "OPR/" in u or "Opera" in u:
        br = "Opera"
    elif "Firefox/" in u:
        br = "Firefox"
    elif "Chrome/" in u:
        br = "Chrome"
    elif "Safari/" in u:
        br = "Safari"
    else:
        br = "Other"
    return f"{os_} {form} / {br}"


def decade_band(year_str):
    """'1985' -> '1980-1989'. Non-year / already-banded values pass through."""
    s = str(year_str).strip()
    if not (s.isdigit() and len(s) == 4):
        return year_str
    y = int(s)
    lo = (y // 10) * 10
    return f"{lo}-{lo + 9}"


def redact_names(text, names):
    for n in names:
        text = re.sub(rf"\b{re.escape(n)}\b", "[name]", text, flags=re.IGNORECASE)
    return text


def scrub_structured(text):
    for pat in STRUCTURED_PII:
        text = pat.sub("[redacted]", text)
    return text


def anonymize_record(r, unexpected):
    changed = {"conn": False, "browser": False, "birth_year": False, "names": 0, "structured": 0}

    # 1a. connectionInfo: keep allowlist
    ci = r.get("connectionInfo")
    if isinstance(ci, dict):
        unexpected["connection"].update(set(ci) - CONNECTION_KEEP - {"timezoneOffset"})
        new_ci = {k: v for k, v in ci.items() if k in CONNECTION_KEEP}
        if new_ci != ci:
            r["connectionInfo"] = new_ci
            changed["conn"] = True

    # 1b. browserInfo: keep allowlist + coarse device from userAgent
    bi = r.get("browserInfo")
    if isinstance(bi, dict):
        unexpected["browser"].update(set(bi) - BROWSER_KEEP - {"userAgent", "referrer", "timezone"})
        new_bi = {k: v for k, v in bi.items() if k in BROWSER_KEEP}
        dev = coarse_device(bi.get("userAgent")) if "userAgent" in bi else bi.get("device")
        if dev:
            new_bi["device"] = dev
        if new_bi != bi:
            r["browserInfo"] = new_bi
            changed["browser"] = True

    # 2. Coarsen demographics birth_year
    for sk, sv in r.get("surveys", {}).items():
        if "Demographics" not in sk or not isinstance(sv, dict):
            continue
        for block in ("responses", "result"):
            d = sv.get(block)
            if isinstance(d, dict) and "birth_year" in d:
                new = decade_band(d["birth_year"])
                if new != d["birth_year"]:
                    d["birth_year"] = new
                    changed["birth_year"] = True

    # 3 + 4. Free-text: targeted name redaction + structured-PII net
    gid6 = (r.get("gameId") or "")[-6:]
    names = NAME_REDACTIONS.get((gid6, str(r.get("position"))), set())

    for pk, pv in r.get("prompts", {}).items():
        if not isinstance(pv, dict):
            continue
        val = pv.get("value")
        if not isinstance(val, str) or not val:
            continue
        new = redact_names(val, names) if (names and pk in FREE_TEXT_PROMPTS) else val
        new2 = scrub_structured(new)
        changed["names"] += int(new != val)
        changed["structured"] += int(new2 != new)
        if new2 != val:
            pv["value"] = new2

    qc = r.get("QCSurvey")
    if isinstance(qc, dict):
        resp = qc.get("responses", {})
        for fk in QC_FREE_FIELDS:
            val = resp.get(fk)
            if not isinstance(val, str) or not val:
                continue
            new = redact_names(val, names) if names else val
            new2 = scrub_structured(new)
            changed["names"] += int(new != val)
            changed["structured"] += int(new2 != new)
            if new2 != val:
                resp[fk] = new2

    return changed


def main():
    files = sorted(glob.glob("data/study_*/*.scienceData.jsonl"))
    totals = {"files": 0, "records": 0, "conn": 0, "browser": 0, "birth_year": 0, "names": 0, "structured": 0}
    unexpected = {"connection": set(), "browser": set()}
    for fn in files:
        with open(fn) as f:
            recs = [json.loads(line) for line in f if line.strip()]
        for r in recs:
            c = anonymize_record(r, unexpected)
            totals["records"] += 1
            for k in ("conn", "browser", "birth_year"):
                totals[k] += int(c[k])
            totals["names"] += c["names"]
            totals["structured"] += c["structured"]
        with open(fn, "w") as f:
            for r in recs:
                f.write(json.dumps(r) + "\n")
        totals["files"] += 1
        print(f"  scrubbed {fn} ({len(recs)} records)")

    print("\n=== anonymization summary ===")
    print(f"  files processed                      : {totals['files']}")
    print(f"  records processed                    : {totals['records']}")
    print(f"  connectionInfo filtered (records)    : {totals['conn']}")
    print(f"  browserInfo filtered (records)       : {totals['browser']}")
    print(f"  birth_year coarsened (records)       : {totals['birth_year']}")
    print(f"  free-text name redactions            : {totals['names']}")
    print(f"  structured-PII redactions            : {totals['structured']}")
    if unexpected["connection"] or unexpected["browser"]:
        print("\n  NOTE unexpected (dropped) fields encountered:")
        print(f"    connectionInfo: {sorted(unexpected['connection'])}")
        print(f"    browserInfo   : {sorted(unexpected['browser'])}")


if __name__ == "__main__":
    main()
