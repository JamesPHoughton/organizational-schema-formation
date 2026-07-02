#!/usr/bin/env python3
"""
Competency-traps coordination-task dashboard — Study 1 AND Study 2 in one page,
in clearly separated sections, each fully interactive and independent.

Inspired by ../dialogue-levers/pilots/pilot_3.1_build_dashboard.py: standalone
Altair charts, each its own vega-embed, wired together by ONE shared focus
selection. The unit of analysis is the GROUP (dyad). In each study section:

  - CLICK a point / line  -> FOCUS that group: its trajectory goes bold across
    every chart in that section, and the section's INSPECTOR fills with the
    group's actual round-4 labels, recall + match status (green = unique matched
    name that counts toward accuracy, amber = reused name that earns no credit,
    red = mismatch), open-ended explanations, and demographics.
  - CLICK a cell / coding bar -> make every group in that bar the active GROUP
    SET; every chart fades to it and an ink diamond marks its mean.
  - CLICK empty space / Clear to reset.

The two studies share the entire pipeline (load -> exclude -> aggregate ->
group-level accuracy, mirroring each study's notebook) and all chart code; they
differ only in:
  * Study 1: schema vs non-schema, a single round-4 change (the schema-ambiguous
    change). Exclusions: 4 manually-flagged groups + total-blank cutoff.
  * Study 2: 2 x 2 (schema/non-schema x ambiguous/incompatible R4 change), plus
    human-coded R4 schema use -> the preregistered Fisher's-exact H1.

Each section gets its own set of vega views and its own JS controller, so a
click in one study never touches the other.

Run:  ../.venv/bin/python dashboard.py    (from analysis/)
Out:  dashboard.html  (single self-contained file)
"""
import glob, json, os, re
from datetime import date
from html import escape
from collections import defaultdict

import numpy as np
import pandas as pd
import altair as alt
from scipy.stats import fisher_exact, mannwhitneyu

# ── palette ───────────────────────────────────────────────────────────────────
SCHEMA_COL    = "#E85D75"
NONSCHEMA_COL = "#4A90E2"
MEAN_COL      = "#c77d11"
SEL_COL       = "#1f2937"
FOCUS_COL     = "#111827"
FAINT         = 0.16
COND_COL = {"schema": SCHEMA_COL, "nonschema": NONSCHEMA_COL}

IN_SET   = "length(groupIds) === 0 || indexof(groupIds, datum.gameId) >= 0"
IS_FOCUS = "focusGame !== '' && datum.gameId === focusGame"

ROUNDS = ["1a", "1b", "1c", "2", "3", "4"]
ROUND_MAX = {"1a": 2, "1b": 4, "1c": 8, "2": 8, "3": 8, "4": 8}
RECALL_N = dict(ROUND_MAX)

CELL_ORDER = ["ambiguous", "incompatible"]
CELL_LABEL = {"ambiguous": "Schema-ambiguous change", "incompatible": "Schema-incompatible change"}
TG_LABEL = {"schema": "Schema", "nonschema": "Non-schema"}

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_HTML = os.path.join(HERE, "dashboard.html")

# Shared Altair selection / param objects (chart specs only; each embed is an
# isolated Vega runtime, so reusing names across studies is harmless).
group_param = alt.param(name="groupIds", value=[])
focus_param = alt.param(name="focusGame", value="")
pick = alt.selection_point(name="pick", fields=["gameId"], on="click",
                           empty=False, clear="dblclick", toggle=False)
op_set = alt.condition(IN_SET, alt.value(0.65), alt.value(FAINT))


def cliffs_delta(x, y):
    x, y = np.asarray(x), np.asarray(y)
    if len(x) == 0 or len(y) == 0:
        return float("nan")
    return (np.sum(x[:, None] > y) - np.sum(x[:, None] < y)) / (len(x) * len(y))


# ─────────────────────────────────────────────────────────────────────────────
# Load + accuracy (shared; mirrors both notebooks' [load-data] cells)
# ─────────────────────────────────────────────────────────────────────────────
def pval(rec, key):
    v = (rec.get("prompts") or {}).get(key)
    return v.get("value") if isinstance(v, dict) else None

def demo(rec):
    d = (rec.get("surveys") or {}).get("survey_Demographics_exit_5_Demographics")
    return (d.get("responses") if isinstance(d, dict) else {}) or {}

def load_study(glob_pattern):
    filenames = sorted(glob.glob(glob_pattern))
    raw = []
    for fn in filenames:
        with open(fn) as f:
            for line in f:
                rec = json.loads(line)
                if rec.get("sampleId") != "missing":
                    raw.append(rec)

    ad = pd.DataFrame()
    ad["treatment"] = [r["treatment"]["name"] for r in raw]
    ad["treatmentGroup"] = [r["treatment"]["name"].split("_")[0] for r in raw]
    ad["changeType"] = ["incompatible" if "tangrams" in r["treatment"]["name"] else "ambiguous" for r in raw]
    ad["sampleId"] = [r["sampleId"] for r in raw]
    ad["gameId"] = [r["gameId"][-6:] for r in raw]
    ad["gameId_full"] = [r["gameId"] for r in raw]
    ad["position"] = [r["position"] for r in raw]
    ad["num_reports"] = [len(r["reports"]) for r in raw]
    coll = ad.groupby("gameId")["gameId_full"].nunique()
    assert coll.max() == 1, f"Truncated gameId collision(s): {coll[coll > 1].index.tolist()}"

    submit_times = pd.DataFrame([{k: v["time"] for k, v in r["stageSubmissions"].items()} for r in raw])
    submit_times.columns = ["time_" + "_".join(c.replace("submitButton_", "").split("_")[-3:]) for c in submit_times.columns]
    submit_times = submit_times[sorted(submit_times.columns)]
    labeling_times = [c for c in submit_times.columns if "labeling" in c]
    submit_times[labeling_times] = submit_times[labeling_times].fillna(300)
    ad = pd.concat([ad, submit_times[labeling_times]], axis=1)

    label_keys = [f"prompt_labeling_{r}" for r in ROUNDS]
    def get_labels(r):
        out = {}
        for key in label_keys:
            try:
                out[key.replace("prompt_", "")] = r["prompts"][key]["value"].strip()
            except (KeyError, TypeError, AttributeError):
                out[key.replace("prompt_", "")] = None
        return out
    ad = pd.concat([ad, pd.DataFrame([get_labels(r) for r in raw])], axis=1)

    recall = pd.DataFrame([{k: d["value"].lower().strip()
                            for k, d in r["prompts"].items() if "recall" in k} for r in raw])
    recall.columns = [c.replace("prompt_recall_", "recall_") for c in recall.columns]
    recall = recall[sorted(recall.columns)].fillna("")
    recall_cols = list(recall.columns)
    ad = pd.concat([ad, recall], axis=1)

    matches = ((ad.groupby("gameId")[recall_cols].nunique() == 1)
               & (ad.groupby("gameId")[recall_cols].count() == 2))
    matches.columns = [c.replace("recall_", "match_") for c in matches.columns]
    ad = pd.merge(ad, matches, left_on="gameId", right_index=True)
    for mc in [c for c in ad.columns if c.startswith("match_")]:
        ad[mc.replace("match_", "matched_recall_")] = ad[mc.replace("match_", "recall_")] * ad[mc]
    for r in ROUNDS:
        cols = [c for c in ad.columns if f"matched_recall_{r}_" in c]
        ad[f"accuracy_{r}"] = ad[cols].replace("", np.nan).nunique(axis=1).astype(float)

    conf = pd.DataFrame([{f"conf_{rr}": pval(r, f"prompt_confidence_{rr}") for rr in ROUNDS} for r in raw])
    ad = pd.concat([ad, conf], axis=1)
    ad["open_strategy"] = [pval(r, "prompt_strategy") for r in raw]
    ad["open_working"] = [pval(r, "prompt_working_together") for r in raw]
    ad["open_mistake"] = [pval(r, "prompt_mistake") for r in raw]
    ad["_demo"] = [demo(r) for r in raw]
    return raw, ad, recall_cols


# ── per-study exclusions (each mirrors its own notebook) ─────────────────────
def exclude_study1(ad, recall_cols):
    flagged = ["ES0E4B", "RHNS8Z", "DA5DS8", "WMJTSY"]  # audio/video/comm + cheating
    ad = ad[~ad["gameId"].isin(flagged)]
    ad = ad[ad["num_reports"] < 3]
    ad = ad[(ad[recall_cols] == "").sum(axis=1) < 26]           # total-blank cutoff (prereg)
    pc = (ad.groupby("gameId")[["accuracy_3", "accuracy_4"]].count() == 2).all(axis=1)
    ad = ad[ad["gameId"].isin(pc[pc].index)]
    ad = ad[ad["treatmentGroup"].isin(["schema", "nonschema"])]
    return ad

def exclude_study2(ad, recall_cols):
    flagged = []  # manual cheating flags — populate as needed
    ad = ad[~ad["gameId"].isin(flagged)]
    ad = ad[ad["num_reports"] < 3]
    round_cols = {r: [c for c in recall_cols if c.startswith(f"recall_{r}_")] for r in ROUNDS}
    def too_many_blanks(row):
        for r, cols in round_cols.items():
            if r in ("1a", "1b"):
                continue
            if sum(row[c] == "" for c in cols if c in row) > 2:
                return True
        return False
    bad = ad.loc[ad.apply(too_many_blanks, axis=1), "gameId"].unique()
    ad = ad[~ad["gameId"].isin(bad)]
    pc = (ad.groupby("gameId")[["accuracy_3", "accuracy_4"]].count() == 2).all(axis=1)
    ad = ad[ad["gameId"].isin(pc[pc].index)]
    ad = ad[ad["treatmentGroup"].isin(["schema", "nonschema"])]
    return ad


def aggregate(ad):
    acc_cols = [c for c in ad.columns if c.startswith("accuracy_")]
    time_cols = [c for c in ad.columns if c.startswith("time_labeling_")]
    assert ad.groupby(["treatment", "gameId"])[acc_cols].std().max().max() == 0
    return (ad.groupby(["treatment", "treatmentGroup", "changeType", "gameId"], as_index=False)
            [acc_cols + time_cols].max())


def age_of(d):
    try:
        y = int(str(d.get("birth_year")))
        if 1920 <= y <= 2026 - 13:
            return 2026 - y
    except (TypeError, ValueError):
        pass
    return None

def build_groupdata(ad, data, coding):
    su_map = {}
    if coding is not None:
        c = coding.copy()
        c["gameId"] = c["gameId"].astype(str).str[-6:]
        su_map = dict(zip(c["gameId"], c["schema_use_4"]))
    out = {}
    for gid, g in ad.groupby("gameId"):
        g = g.sort_values("position")
        row0 = g.iloc[0]
        members = []
        for _, m in g.iterrows():
            dd = m["_demo"] or {}
            members.append(dict(
                pos=int(m["position"]),
                labels={r: (m.get(f"labeling_{r}") or "") for r in ROUNDS},
                recall={r: [str(m.get(f"recall_{r}_{i}", "") or "") for i in range(RECALL_N[r])] for r in ROUNDS},
                conf={r: (m.get(f"conf_{r}") if pd.notna(m.get(f"conf_{r}")) else None) for r in ROUNDS},
                strategy=(m.get("open_strategy") or None),
                working=(m.get("open_working") or None),
                mistake=(m.get("open_mistake") or None),
                age=age_of(dd), gender=dd.get("gender"), education=dd.get("education_US"), race=dd.get("race_US"),
            ))
        match = {r: [bool(g.iloc[0].get(f"match_{r}_{i}", False)) for i in range(RECALL_N[r])] for r in ROUNDS}
        # cell status mirrors scoring: accuracy = # DISTINCT matched names; only the
        # first matched occurrence of a name counts ("unique"), repeats are "reuse".
        cellstatus = {}
        base = members[0]["recall"]
        for r in ROUNDS:
            seen, status = set(), []
            for i in range(RECALL_N[r]):
                v = base[r][i]
                if match[r][i] and v != "":
                    status.append("reuse" if v in seen else "unique"); seen.add(v)
                elif any(m["recall"][r][i] for m in members):
                    status.append("mismatch")
                else:
                    status.append("blank")
            cellstatus[r] = status
        su = su_map.get(gid)
        su = int(su) if su is not None and pd.notna(su) else None
        out[gid] = dict(gameId=gid, treatmentGroup=row0["treatmentGroup"], changeType=row0["changeType"],
                        treatment=row0["treatment"],
                        accuracy={r: float(row0[f"accuracy_{r}"]) for r in ROUNDS},
                        schema_use_4=su, cellstatus=cellstatus, members=members)
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Charts — registered into a per-study build context (sb)
# ─────────────────────────────────────────────────────────────────────────────
class StudyBuild:
    def __init__(self, key):
        self.key = key
        self.embeds = []  # {"id","spec","picks"}
        self.catmap = defaultdict(lambda: defaultdict(list))

def _dedupe_inline_data(spec):
    import hashlib
    datasets = spec.get("datasets", {})
    name_for = {}
    def walk(o):
        if isinstance(o, dict):
            for k, v in list(o.items()):
                if isinstance(v, dict) and isinstance(v.get("values"), list) and len(v["values"]) > 20:
                    h = hashlib.md5(json.dumps(v["values"], sort_keys=True).encode()).hexdigest()
                    if h not in name_for:
                        nm = f"d{len(name_for)}"; name_for[h] = nm; datasets[nm] = v["values"]
                    o[k] = {"name": name_for[h]}
                else:
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(spec)
    if datasets:
        spec["datasets"] = datasets
    return spec

def register(sb, chart, picks=("pick",)):
    if chart is None:
        return None
    cid = f'{sb.key}_vis_{len(sb.embeds)}'
    sb.embeds.append({"id": cid, "spec": _dedupe_inline_data(chart.to_dict()), "picks": list(picks)})
    return f'<div class="chart" id="{cid}"></div>'

def js_json(obj):
    return (json.dumps(obj).replace("</", "<\\/").replace("<!--", "<\\!--")
            .replace(" ", "\\u2028").replace(" ", "\\u2029"))


def cell_counts_chart(sb, data, cts):
    rows, cell_lbl = [], {}
    for _, r in data.iterrows():
        cell = f'{r["treatmentGroup"]}|{r["changeType"]}'
        lab = (f'{TG_LABEL[r["treatmentGroup"]]} · {CELL_LABEL[r["changeType"]]}'
               if len(cts) > 1 else TG_LABEL[r["treatmentGroup"]])
        cell_lbl[cell] = lab
        rows.append(dict(gameId=r["gameId"], cell=cell, cellL=lab))
    for r in rows:
        sb.catmap["cell"][r["cell"]].append(r["gameId"])
    if len(cts) > 1:
        order = [f'{TG_LABEL[tg]} · {CELL_LABEL[ct]}' for ct in cts for tg in ["schema", "nonschema"]]
    else:
        order = [TG_LABEL[tg] for tg in ["schema", "nonschema"]]
    sel = alt.selection_point(name="pick_cell", fields=["cell"], on="click", empty=False, clear="dblclick", toggle=False)
    b = alt.Chart(alt.Data(values=rows))
    y = alt.Y("cellL:N", title=None, sort=order, axis=alt.Axis(labelLimit=320))
    x = alt.X("count():Q", title="# groups")
    bar = b.mark_bar(color="#94a3b8").encode(
        x=x, y=y, opacity=alt.condition(IN_SET, alt.value(0.95), alt.value(0.25)),
        tooltip=[alt.Tooltip("cellL:N", title="cell"), alt.Tooltip("count():Q", title="# groups")]
    ).add_params(sel, group_param, focus_param)
    lbl = b.mark_text(align="left", dx=3, baseline="middle", fontSize=10, color="#334155").encode(x=x, y=y, text="count():Q")
    h = 40 + 26 * len(order)
    return (bar + lbl).properties(width=420, height=h), ["pick_cell"]


def r4_headline_chart(sb, data, cts):
    rng = np.random.default_rng(42)
    rows = []
    for _, r in data.iterrows():
        rows.append(dict(gameId=r["gameId"], tg=r["treatmentGroup"], tgL=TG_LABEL[r["treatmentGroup"]],
                         ct=CELL_LABEL[r["changeType"]], acc=float(r["accuracy_4"]),
                         accj=float(r["accuracy_4"]) + float(rng.uniform(-0.16, 0.16))))
    b = alt.Chart(alt.Data(values=rows))
    x = alt.X("ct:N", title=None, sort=[CELL_LABEL[c] for c in cts], axis=alt.Axis(labelAngle=0))
    xoff = alt.XOffset("tg:N", sort=["schema", "nonschema"])
    y = alt.Y("accj:Q", scale=alt.Scale(domain=[-0.5, 8.5]),
              axis=alt.Axis(values=list(range(0, 9)), title="Round 4 accuracy (0–8 images matched)"))
    col = alt.Color("tgL:N", scale=alt.Scale(domain=["Schema", "Non-schema"], range=[SCHEMA_COL, NONSCHEMA_COL]),
                    legend=alt.Legend(title=None, orient="top"))
    tip = [alt.Tooltip("gameId:N", title="group"), alt.Tooltip("tgL:N", title="condition"),
           alt.Tooltip("ct:N", title="R4 change"), alt.Tooltip("acc:Q", title="R4 accuracy")]
    dots = b.mark_point(filled=True, size=55, stroke="white", strokeWidth=0.5).encode(
        x=x, xOffset=xoff, y=y, color=col, opacity=op_set, tooltip=tip).add_params(pick, group_param, focus_param)
    mean_tick = b.mark_tick(thickness=3, size=26, color=MEAN_COL, opacity=0.95).encode(
        x=x, xOffset=xoff, y=alt.Y("mean(acc):Q", scale=alt.Scale(domain=[-0.5, 8.5])))
    sel_mean = b.transform_filter("indexof(groupIds, datum.gameId) >= 0").mark_point(
        shape="diamond", filled=True, size=95, color=SEL_COL, stroke="white", strokeWidth=1.2).encode(
        x=x, xOffset=xoff, y=alt.Y("mean(acc):Q"),
        tooltip=[alt.Tooltip("mean(acc):Q", title="selected-group mean", format=".2f")])
    focus_pt = b.transform_filter(IS_FOCUS).mark_point(
        shape="diamond", filled=True, size=200, color=FOCUS_COL, stroke="white", strokeWidth=1.5).encode(
        x=x, xOffset=xoff, y=y, tooltip=tip)
    w = 200 + 150 * len(cts)
    return (dots + mean_tick + sel_mean + focus_pt).resolve_scale(color="independent").properties(
        width=w, height=360, title="Round 4 accuracy  ·  amber tick = cell mean")


def trajectory_chart(sb, data, ct):
    rows = []
    for _, r in data.iterrows():
        if r["changeType"] != ct:
            continue
        for io, rr in enumerate(ROUNDS):
            rows.append(dict(gameId=r["gameId"], tg=r["treatmentGroup"], tgL=TG_LABEL[r["treatmentGroup"]],
                             rnd=rr, rnd_order=io, acc=float(r[f"accuracy_{rr}"]),
                             prop=float(r[f"accuracy_{rr}"]) / ROUND_MAX[rr]))
    if not rows:
        return None
    b = alt.Chart(alt.Data(values=rows))
    x = alt.X("rnd:N", sort=ROUNDS, title="Round", axis=alt.Axis(labelAngle=0))
    y = alt.Y("prop:Q", scale=alt.Scale(domain=[0, 1]), axis=alt.Axis(format="%", title="Proportion of images matched"))
    col = alt.Color("tgL:N", scale=alt.Scale(domain=["Schema", "Non-schema"], range=[SCHEMA_COL, NONSCHEMA_COL]),
                    legend=alt.Legend(title=None, orient="top"))
    tip = [alt.Tooltip("gameId:N", title="group"), alt.Tooltip("tgL:N", title="condition"),
           alt.Tooltip("rnd:N", title="round"), alt.Tooltip("acc:Q", title="accuracy"),
           alt.Tooltip("prop:Q", title="proportion", format=".0%")]
    faint = b.mark_line(strokeWidth=1).encode(
        x=x, y=y, detail="gameId:N", order="rnd_order:Q", color=col,
        opacity=alt.condition(IN_SET, alt.value(0.18), alt.value(0.04)))
    dots = b.mark_point(filled=True, size=22).encode(
        x=x, y=y, color=col, opacity=op_set, tooltip=tip).add_params(pick, group_param, focus_param)
    mean_line = b.mark_line(strokeWidth=3.5).encode(
        x=x, y=alt.Y("mean(prop):Q", scale=alt.Scale(domain=[0, 1])), color=col, detail="tg:N", order="rnd_order:Q")
    focus_line = b.transform_filter(IS_FOCUS).mark_line(strokeWidth=3, color=FOCUS_COL).encode(
        x=x, y=y, detail="gameId:N", order="rnd_order:Q")
    focus_pt = b.transform_filter(IS_FOCUS).mark_point(filled=True, size=80, color=FOCUS_COL, stroke="white", strokeWidth=1).encode(
        x=x, y=y, tooltip=tip)
    title = CELL_LABEL[ct] if (data["changeType"].nunique() > 1) else "Accuracy by round"
    return (faint + mean_line + dots + focus_line + focus_pt).resolve_scale(color="independent").properties(
        width=320, height=300, title=title)


def slope_chart(sb, data, ct):
    rows = []
    for _, r in data.iterrows():
        if r["changeType"] != ct:
            continue
        for rr in ["3", "4"]:
            rows.append(dict(gameId=r["gameId"], tg=r["treatmentGroup"], tgL=TG_LABEL[r["treatmentGroup"]],
                             phase=f"Round {rr}", acc=float(r[f"accuracy_{rr}"])))
    if not rows:
        return None
    b = alt.Chart(alt.Data(values=rows))
    x = alt.X("phase:N", sort=["Round 3", "Round 4"], title=None, axis=alt.Axis(labelAngle=0))
    y = alt.Y("acc:Q", scale=alt.Scale(domain=[-0.5, 8.5]), axis=alt.Axis(values=list(range(0, 9)), title="Accuracy (0–8)"))
    col = alt.Color("tgL:N", scale=alt.Scale(domain=["Schema", "Non-schema"], range=[SCHEMA_COL, NONSCHEMA_COL]),
                    legend=alt.Legend(title=None, orient="top"))
    tip = [alt.Tooltip("gameId:N", title="group"), alt.Tooltip("tgL:N", title="condition"),
           alt.Tooltip("phase:N"), alt.Tooltip("acc:Q", title="accuracy")]
    faint = b.mark_line(strokeWidth=1).encode(
        x=x, y=y, detail="gameId:N", color=col, opacity=alt.condition(IN_SET, alt.value(0.2), alt.value(0.05)))
    dots = b.mark_point(filled=True, size=40).encode(
        x=x, y=y, color=col, opacity=op_set, tooltip=tip).add_params(pick, group_param, focus_param)
    mean_line = b.mark_line(strokeWidth=4).encode(x=x, y=alt.Y("mean(acc):Q"), color=col, detail="tg:N")
    focus_line = b.transform_filter(IS_FOCUS).mark_line(strokeWidth=3, color=FOCUS_COL).encode(x=x, y=y, detail="gameId:N")
    focus_pt = b.transform_filter(IS_FOCUS).mark_point(filled=True, size=110, color=FOCUS_COL, stroke="white", strokeWidth=1.2).encode(
        x=x, y=y, tooltip=tip)
    title = CELL_LABEL[ct] if (data["changeType"].nunique() > 1) else "Round 3 → Round 4"
    return (faint + mean_line + dots + focus_line + focus_pt).resolve_scale(color="independent").properties(
        width=230, height=300, title=title)


def schema_use_chart(sb, data, coding):
    if coding is None:
        return None, []
    sch = data[data["treatmentGroup"] == "schema"].dropna(subset=["schema_use_4"])
    rows = []
    for _, r in sch.iterrows():
        rows.append(dict(gameId=r["gameId"], ct=CELL_LABEL[r["changeType"]], used=int(r["schema_use_4"]),
                         usedL=("Used schema in R4" if int(r["schema_use_4"]) else "Did not")))
    if not rows:
        return None, []
    for r in rows:
        sb.catmap["schemause"][r["usedL"]].append(r["gameId"])
    sel = alt.selection_point(name="pick_schemause", fields=["usedL"], on="click", empty=False, clear="dblclick", toggle=False)
    b = alt.Chart(alt.Data(values=rows))
    y = alt.Y("ct:N", title=None, sort=[CELL_LABEL[c] for c in CELL_ORDER], axis=alt.Axis(labelLimit=220))
    x = alt.X("count():Q", stack="normalize", title="share of Schema groups", axis=alt.Axis(format="%"))
    col = alt.Color("usedL:N", scale=alt.Scale(domain=["Used schema in R4", "Did not"], range=[SCHEMA_COL, "#cbd5e0"]),
                    legend=alt.Legend(title=None, orient="top"))
    bars = b.mark_bar().encode(
        x=x, y=y, color=col, order=alt.Order("used:Q", sort="descending"),
        tooltip=[alt.Tooltip("ct:N", title="R4 change"), alt.Tooltip("usedL:N", title="schema use"),
                 alt.Tooltip("count():Q", title="# groups")]
    ).add_params(sel, group_param, focus_param)
    return bars.properties(width=300, height=120, title="R4 schema use among Schema groups (prereg H1)"), ["pick_schemause"]


def time_chart(sb, data, ct):
    rows = []
    for _, r in data.iterrows():
        if r["changeType"] != ct:
            continue
        for io, rr in enumerate(ROUNDS):
            c = f"time_labeling_{rr}"
            if c in data.columns and pd.notna(r[c]):
                rows.append(dict(gameId=r["gameId"], tg=r["treatmentGroup"], tgL=TG_LABEL[r["treatmentGroup"]],
                                 rnd=rr, rnd_order=io, secs=float(r[c])))
    if not rows:
        return None
    b = alt.Chart(alt.Data(values=rows))
    x = alt.X("rnd:N", sort=ROUNDS, title="Round", axis=alt.Axis(labelAngle=0))
    y = alt.Y("secs:Q", scale=alt.Scale(domain=[0, 305]), axis=alt.Axis(title="Labeling time (s)"))
    col = alt.Color("tgL:N", scale=alt.Scale(domain=["Schema", "Non-schema"], range=[SCHEMA_COL, NONSCHEMA_COL]),
                    legend=alt.Legend(title=None, orient="top"))
    tip = [alt.Tooltip("gameId:N", title="group"), alt.Tooltip("tgL:N", title="condition"),
           alt.Tooltip("rnd:N", title="round"), alt.Tooltip("secs:Q", title="seconds", format=".0f")]
    dots = b.mark_point(filled=True, size=22).encode(
        x=x, y=y, color=col, opacity=op_set, tooltip=tip).add_params(pick, group_param, focus_param)
    mean_line = b.mark_line(strokeWidth=3.5).encode(x=x, y=alt.Y("mean(secs):Q"), color=col, detail="tg:N", order="rnd_order:Q")
    focus_line = b.transform_filter(IS_FOCUS).mark_line(strokeWidth=3, color=FOCUS_COL).encode(
        x=x, y=y, detail="gameId:N", order="rnd_order:Q")
    title = CELL_LABEL[ct] if (data["changeType"].nunique() > 1) else "Labeling time by round"
    return (mean_line + dots + focus_line).resolve_scale(color="independent").properties(width=320, height=240, title=title)


# ─────────────────────────────────────────────────────────────────────────────
# Stats fragments
# ─────────────────────────────────────────────────────────────────────────────
def cell_summary_of(data, cts):
    out = {}
    for tg in ["schema", "nonschema"]:
        for ct in cts:
            v = data[(data["treatmentGroup"] == tg) & (data["changeType"] == ct)]["accuracy_4"].values
            out[(tg, ct)] = dict(n=len(v), mean=float(np.mean(v)) if len(v) else float("nan"),
                                 sem=float(np.std(v, ddof=1) / np.sqrt(len(v))) if len(v) > 1 else 0.0)
    return out

def cell_means_table(cs, cts):
    head = '<tr><th></th>' + ''.join(f'<th>{escape(CELL_LABEL[c])}</th>' for c in cts) + '</tr>'
    body = ""
    for tg in ["schema", "nonschema"]:
        cells = ""
        for ct in cts:
            s = cs[(tg, ct)]
            cells += f'<td><b>{s["mean"]:.2f}</b> <span class="muted">±{1.96*s["sem"]:.2f} · n={s["n"]}</span></td>'
        body += f'<tr><th>{TG_LABEL[tg]}</th>{cells}</tr>'
    return f'<table class="celltab"><thead>{head}</thead><tbody>{body}</tbody></table>'

def r4_compare_html(data, cts):
    rows = ""
    for ct in cts:
        sv = data[(data["treatmentGroup"] == "schema") & (data["changeType"] == ct)]["accuracy_4"].values
        nv = data[(data["treatmentGroup"] == "nonschema") & (data["changeType"] == ct)]["accuracy_4"].values
        if len(sv) == 0 or len(nv) == 0:
            continue
        u, p = mannwhitneyu(sv, nv, alternative="two-sided")
        d = cliffs_delta(sv, nv)
        diff = sv.mean() - nv.mean()
        rows += (f'<tr><td>{escape(CELL_LABEL[ct])}</td><td>{sv.mean():.2f}</td><td>{nv.mean():.2f}</td>'
                 f'<td>{diff:+.2f}</td><td>{d:+.2f}</td><td>{p:.4f}</td></tr>')
    return ('<table class="summary"><thead><tr><th>R4 change</th><th>Schema</th><th>Non-schema</th>'
            '<th>Δ (S−NS)</th><th>Cliff δ</th><th>MWU p (2-sided)</th></tr></thead>'
            f'<tbody>{rows}</tbody></table>')

def fisher_html(data, coding):
    if coding is None:
        return ""
    sch = data[data["treatmentGroup"] == "schema"].dropna(subset=["schema_use_4"])
    nob = sch[sch["changeType"] == "ambiguous"]["schema_use_4"].astype(int)
    obv = sch[sch["changeType"] == "incompatible"]["schema_use_4"].astype(int)
    a, b = int(nob.sum()), int(len(nob) - nob.sum())
    c, d = int(obv.sum()), int(len(obv) - obv.sum())
    if not ((a + b) and (c + d)):
        return ""
    orr, p = fisher_exact([[a, b], [c, d]], alternative="greater")
    return (f'<div class="result"><b>Preregistered Fisher\'s exact</b> (one-tailed, ambiguous &gt; incompatible): '
            f'schema reused in R4 by <b>{a}/{a+b}</b> ({100*a/(a+b):.0f}%) of Schema×ambiguous groups vs '
            f'<b>{c}/{c+d}</b> ({100*c/(c+d):.0f}%) of Schema×incompatible. OR = {orr:.2f}, p = {p:.4f}.</div>')

def results_csv_table(path):
    if not path or not os.path.exists(path):
        return ""
    df = pd.read_csv(path)
    head = "".join(f"<th>{escape(c)}</th>" for c in df.columns)
    body = ""
    for _, r in df.iterrows():
        cls = ' class="prereg"' if "PREREG" in str(r[df.columns[0]]) else ""
        body += f"<tr{cls}>" + "".join(f"<td>{escape(str(r[c]))}</td>" for c in df.columns) + "</tr>"
    return (f'<details><summary>Full hypothesis-test table (from {escape(os.path.basename(path))})</summary>'
            f'<table class="summary"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></details>')


# ─────────────────────────────────────────────────────────────────────────────
# Build one study section
# ─────────────────────────────────────────────────────────────────────────────
def build_section(cfg):
    raw, ad, recall_cols = load_study(cfg["glob"])
    n_raw_groups = ad["gameId"].nunique()
    ad = cfg["exclude"](ad, recall_cols)
    n_groups = ad["gameId"].nunique()
    n_participants = len(ad)
    data = aggregate(ad)
    coding = None
    if cfg.get("coding_csv") and os.path.exists(cfg["coding_csv"]):
        coding = pd.read_csv(cfg["coding_csv"])
        coding["gameId"] = coding["gameId"].astype(str).str[-6:]
        data = data.merge(coding[["gameId", "schema_use_4"]], on="gameId", how="left")
    else:
        data["schema_use_4"] = np.nan
    groupdata = build_groupdata(ad, data, coding)
    cts = [ct for ct in CELL_ORDER if (data["changeType"] == ct).any()]
    print(f"[{cfg['key']}] {n_groups} groups, {n_participants} participants; cells={cts}")

    sb = StudyBuild(cfg["key"])
    cell_block = register(sb, *cell_counts_chart(sb, data, cts))
    headline_block = register(sb, r4_headline_chart(sb, data, cts))
    traj_blocks = [register(sb, trajectory_chart(sb, data, ct)) for ct in cts]
    slope_blocks = [register(sb, slope_chart(sb, data, ct)) for ct in cts]
    su_chart, su_picks = schema_use_chart(sb, data, coding)
    su_block = register(sb, su_chart, su_picks) if su_chart is not None else None
    time_blocks = [register(sb, time_chart(sb, data, ct)) for ct in cts]

    cs = cell_summary_of(data, cts)
    iid = f'inspector_{cfg["key"]}'

    def blk(b):
        return b or '<p class="muted">No data.</p>'

    # Panel fragments, keyed so each study can place them under Preregistered vs
    # Exploratory in its own order. Panels a study doesn't tag are simply omitted.
    panels = {}
    panels["headline"] = f'''<h4>Round 4 accuracy</h4>
      <p class="lede">Each dot is one group; amber tick = cell mean. Competency-trap prediction: Schema groups do
      <i>worse</i> than Non-schema specifically under the <b>ambiguous</b> change, where the old schema looks like it
      still applies.</p>
      <div class="row">
        <div>{blk(headline_block)}</div>
        <div>
          <h5>Cell means (R4 accuracy, ±95% CI)</h5>
          {cell_means_table(cs, cts)}
          <h5>R4: Schema vs Non-schema</h5>
          {r4_compare_html(data, cts)}
        </div>
      </div>'''
    if su_block:
        panels["schemause"] = f'''<h4>Round-4 schema use (Fisher's exact, H1)</h4>
          <p class="lede">Human-coded: did a group keep using schema-based names in round 4? The prereg predicts Schema
          groups cling to the schema more under the <b>ambiguous</b> change than the <b>incompatible</b> one.
          Click a segment to highlight those groups.</p>
          {blk(su_block)} {fisher_html(data, coding)}'''
    panels["trajectory"] = f'''<h4>Accuracy across all rounds</h4>
      <p class="lede">Proportion of the round's images matched (rounds 1a/1b have 2/4 images; the rest have 8).
      Bold lines are condition means.</p>
      <div class="row">{''.join(blk(b) for b in traj_blocks)}</div>'''
    panels["slope"] = f'''<h4>Round 3 → Round 4</h4>
      <p class="lede">The within-group change as the round-4 environment shifts.</p>
      <div class="row">{''.join(blk(b) for b in slope_blocks)}</div>'''
    panels["time"] = f'''<h4>Labeling time across rounds</h4>
      <p class="lede">Seconds spent naming each round (5-min cap). A round-4 spike can signal a group noticing the change.</p>
      <div class="row">{''.join(blk(b) for b in time_blocks)}</div>'''

    def render(keys):
        return "\n".join(panels[k] for k in keys if k in panels)

    prereg_keys = cfg.get("prereg", [])
    exp_keys = cfg.get("exploratory", [])
    prereg_html = (f'<div class="phase">Preregistered analyses</div>{render(prereg_keys)}'
                   if any(k in panels for k in prereg_keys) else "")
    exp_html = (f'<div class="phase exp">Exploratory analyses</div>{render(exp_keys)}'
                if any(k in panels for k in exp_keys) else "")

    section = f'''
<section class="study" id="sec_{cfg['key']}">
  <h2>{escape(cfg['title'])}</h2>
  <p class="lede">{cfg['blurb']}</p>

  <div class="kpis">
    <div class="kpi"><div class="l">Participant records</div><div class="v">{len(raw)}</div></div>
    <div class="kpi"><div class="l">Groups (pre-exclusion)</div><div class="v">{n_raw_groups}</div></div>
    <div class="kpi"><div class="l">Groups analyzed</div><div class="v">{n_groups}</div></div>
    <div class="kpi"><div class="l">Participants analyzed</div><div class="v">{n_participants}</div></div>
  </div>

  <div class="inspector" id="{iid}"></div>

  <h3>{'Design — the 2×2 cells' if len(cts) > 1 else 'Conditions'}</h3>
  <p class="lede">Click a bar to highlight that condition's groups across this section.</p>
  {blk(cell_block)}

  {prereg_html}
  {exp_html}

  {results_csv_table(cfg.get("results_csv"))}
</section>'''

    return dict(section=section, embeds=sb.embeds, catmap={k: dict(v) for k, v in sb.catmap.items()},
                groupdata=groupdata, inspector_id=iid)


# ─────────────────────────────────────────────────────────────────────────────
# Studies
# ─────────────────────────────────────────────────────────────────────────────
STUDIES = [
    dict(key="study1", title="Study 1 — Schema vs Non-schema (existence proof)",
         glob=os.path.join(HERE, "..", "data", "study_1_schema_nonschema", "batch_*.scienceData.jsonl"),
         coding_csv=None, results_csv=None, exclude=exclude_study1,
         prereg=["headline", "time"], exploratory=["trajectory", "slope"],
         blurb=("Groups do four rounds of a coordination naming task. Schema groups' rounds 1–2 share a consistent "
                "feature structure that invites a shared schema; Non-schema groups' don't. Rounds 3–4 are identical "
                "across conditions; round 4 introduces a change that looks schema-compatible but isn't (the "
                "schema-ambiguous change). The existence-proof result: schemas help through round 3, then hurt in "
                "round 4.")),
    dict(key="study2", title="Study 2 — 2×2: change type × schema (mechanism test)",
         glob=os.path.join(HERE, "..", "data", "study*2", "batch_*.scienceData.jsonl"),
         coding_csv=os.path.join(HERE, "..", "data", "study_2", "schema_use_coding.csv"),
         results_csv=os.path.join(HERE, "study_2_analysis_results.csv"), exclude=exclude_study2,
         prereg=["schemause"], exploratory=["headline", "trajectory", "slope", "time"],
         blurb=("Replicates Study 1 and adds a second round-4 change that is clearly <b>incompatible</b> with the "
                "schema (tangrams), crossing Schema/Non-schema with ambiguous/incompatible change. If the trap is "
                "about apparent compatibility, the schema penalty should be larger under the <b>ambiguous</b> change. "
                "Round-4 schema use is human-coded for the preregistered Fisher's-exact test.")),
]

sections = [build_section(cfg) for cfg in STUDIES]

# ── assemble ────────────────────────────────────────────────────────────────
all_embeds = [e for s in sections for e in s["embeds"]]
vl_major = "6" if all_embeds and "/v6" in (all_embeds[0]["spec"].get("$schema", "")) else "5"
_vega_major, _embed_major = ("6", "7") if vl_major == "6" else ("5", "6")
vega_scripts = (f'<script src="https://cdn.jsdelivr.net/npm/vega@{_vega_major}"></script>'
                f'<script src="https://cdn.jsdelivr.net/npm/vega-lite@{vl_major}"></script>'
                f'<script src="https://cdn.jsdelivr.net/npm/vega-embed@{_embed_major}"></script>')

CSS = f"""<style>
  :root {{ --schema:{SCHEMA_COL}; --nonschema:{NONSCHEMA_COL}; --focus:{FOCUS_COL}; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
          color:#1a202c; max-width:1180px; margin:0 auto; padding:1.2em 1.4em 4em; line-height:1.45; }}
  h1 {{ font-size:1.7em; margin:.2em 0 .1em; }}
  h2 {{ font-size:1.45em; margin:.2em 0 .3em; }}
  h3 {{ font-size:1.15em; margin:1.4em 0 .3em; border-bottom:2px solid #edf2f7; padding-bottom:.2em; }}
  h4 {{ font-size:1.05em; margin:1.1em 0 .2em; }}
  h5 {{ font-size:.92em; margin:.4em 0 .2em; }}
  .phase {{ margin:1.5em 0 .2em; font-size:1.05em; font-weight:700; color:#0f172a; background:#eef2ff;
            border-left:5px solid #6366f1; padding:.45em .85em; border-radius:6px; }}
  .phase.exp {{ background:#f1f5f9; border-left-color:#94a3b8; }}
  .meta {{ color:#718096; font-size:.86em; }}
  .muted {{ color:#718096; font-size:.85em; font-weight:400; }}
  nav.studynav {{ position:sticky; top:0; z-index:80; background:#fff; border-bottom:1px solid #e2e8f0;
                  padding:.5em 0; margin-bottom:.6em; display:flex; gap:1em; align-items:center; }}
  nav.studynav a {{ text-decoration:none; color:#334155; font-weight:600; padding:.25em .7em; border-radius:6px;
                    background:#f1f5f9; }}
  nav.studynav a:hover {{ background:#e2e8f0; }}
  section.study {{ border:1px solid #e2e8f0; border-radius:12px; padding:1em 1.2em 1.6em; margin:1.2em 0 2.4em;
                   background:#fff; }}
  .kpis {{ display:flex; gap:.7em; flex-wrap:wrap; margin:1em 0; }}
  .kpi {{ background:#f7fafc; border:1px solid #e2e8f0; border-radius:8px; padding:.6em 1em; min-width:120px; }}
  .kpi .l {{ color:#718096; font-size:.78em; text-transform:uppercase; letter-spacing:.03em; }}
  .kpi .v {{ font-size:1.5em; font-weight:700; }}
  .row {{ display:flex; gap:1.2em; flex-wrap:wrap; align-items:flex-start; }}
  .chart {{ margin:.3em 0; }}
  p.lede {{ font-size:.95em; color:#4a5568; max-width:80ch; }}
  .how {{ background:#f7fafc; border-left:4px solid var(--schema); padding:.6em 1em; border-radius:6px;
          margin:1em 0; font-size:.92em; }}
  .sw {{ display:inline-block; width:.8em; height:.8em; border-radius:2px; vertical-align:middle; }}
  table.celltab, table.summary {{ border-collapse:collapse; font-size:.88em; margin:.4em 0; }}
  table.celltab td, table.celltab th, table.summary td, table.summary th {{ border:1px solid #e2e8f0; padding:.35em .6em; text-align:left; }}
  table.celltab th, table.summary th {{ background:#f7fafc; }}
  table.summary tr.prereg {{ background:#fef3c7; font-weight:600; }}
  details {{ margin:.6em 0; }}
  details summary {{ cursor:pointer; font-weight:600; color:#334155; }}
  .result {{ background:#f0fdf4; border-left:4px solid #16a34a; padding:.55em .9em; border-radius:6px; margin:.6em 0; font-size:.9em; }}
  .inspector {{ position:sticky; top:52px; z-index:60; background:#fff; border:1px solid #e2e8f0; border-radius:10px;
                box-shadow:0 2px 10px rgba(0,0,0,.06); padding:.7em 1em; margin:.6em 0 1.2em; }}
  .inspector .ihead {{ display:flex; justify-content:space-between; align-items:center; gap:1em; }}
  .inspector .ititle {{ font-weight:700; }}
  .inspector .badge {{ display:inline-block; padding:.1em .55em; border-radius:999px; font-size:.78em; color:#fff; font-weight:600; }}
  .inspector .ibody {{ margin-top:.6em; font-size:.86em; }}
  .clear-sel {{ border:1px solid #cbd5e0; background:#f7fafc; border-radius:6px; padding:.25em .8em; cursor:pointer; color:#4a5568; font:inherit; }}
  .clear-sel:hover {{ background:#edf2f7; }}
  .imgrow {{ display:grid; grid-template-columns:repeat(8, 1fr); gap:.25em; margin:.2em 0; }}
  .cellbox {{ border:1px solid #e2e8f0; border-radius:4px; padding:.15em .3em; font-size:.8em; min-height:1.4em;
              overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
  .cellbox.match {{ background:#dcfce7; border-color:#86efac; }}
  .cellbox.reuse {{ background:#fef3c7; border-color:#fcd34d; }}
  .cellbox.miss {{ background:#fee2e2; border-color:#fecaca; }}
  .open {{ background:#f8fafc; border-left:3px solid #cbd5e0; padding:.4em .7em; margin:.3em 0; border-radius:4px; font-size:.88em; white-space:pre-wrap; }}
  .twocol {{ display:grid; grid-template-columns:1fr 1fr; gap:.8em; }}
  .partbox {{ border:1px solid #e2e8f0; border-radius:6px; padding:.4em .6em; }}
</style>"""

# One JS controller per study; shared helpers live at top level.
controller_js = f"""<script>
  const ROUNDS = {js_json(ROUNDS)};
  const RECALL_N = {js_json(RECALL_N)};
  const TG_LABEL = {{schema:"Schema", nonschema:"Non-schema"}};
  const CT_LABEL = {{ambiguous:"Schema-ambiguous change", incompatible:"Schema-incompatible change"}};
  const COND_COL = {{schema:"{SCHEMA_COL}", nonschema:"{NONSCHEMA_COL}"}};
  const SEL_COL = "{SEL_COL}";
  const STATUS_CLS = {{unique:" match", reuse:" reuse", mismatch:" miss", blank:""}};
  const STATUS_TITLE = {{unique:"unique matched name — counts toward accuracy",
                         reuse:"reused name — already used this round, no credit",
                         mismatch:"partners gave different names", blank:""}};
  function esc(s) {{ return (s == null ? "" : String(s)).replace(/[&<>"]/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c])); }}
  function labelLines(text) {{
    const out = [];
    (text || "").split(/\\n/).forEach(line => {{ const m = line.match(/image\\s*\\d+\\s*[:\\-]?\\s*(.*)/i); if (m) out.push(m[1].trim()); }});
    return out;
  }}
  function imgRow(vals, status, n) {{
    let h = '<div class="imgrow">';
    for (let i = 0; i < n; i++) {{
      const v = vals[i] || ""; const st = status ? status[i] : null;
      const cls = st ? STATUS_CLS[st] : ""; const tip = st ? (esc(v) + " — " + STATUS_TITLE[st]) : esc(v);
      h += '<div class="cellbox' + cls + '" title="' + tip + '">' + (esc(v) || "&middot;") + '</div>';
    }}
    return h + '</div>';
  }}

  function makeStudy(cfg) {{
    const {{EMBEDS, CATMAP, GROUPDATA, inspectorId}} = cfg;
    const inspector = document.getElementById(inspectorId);
    const views = [];
    let groupIds = [], focusGame = "", syncing = false;

    function pushAll() {{
      views.forEach(o => {{
        try {{ o.view.signal('groupIds', groupIds.slice()); }} catch (e) {{}}
        try {{ o.view.signal('focusGame', focusGame); }} catch (e) {{}}
        o.view.runAsync();
      }});
    }}
    function idle() {{
      return '<div class="ihead"><span class="ititle">Group inspector</span></div>'
        + '<div class="ibody muted">Click any point or line to inspect one group — its actual round-4 labels, '
        + 'recall &amp; match status, and open-ended explanations.</div>';
    }}
    function wireClear() {{
      const b = inspector.querySelector('.clear-sel');
      if (b) b.addEventListener('click', () => {{
        syncing = true;
        try {{ views.forEach(o => o.picks.forEach(pp => {{ try {{ o.view.data(pp + '_store', []); o.view.run(); }} catch (e) {{}} }})); }}
        finally {{ syncing = false; }}
        clearSel();
      }});
    }}
    function clearSel() {{ groupIds = []; focusGame = ""; pushAll(); inspector.innerHTML = idle(); }}
    function setGroupSet(field, cat) {{
      const ids = (CATMAP[field] && CATMAP[field][cat]) ? CATMAP[field][cat] : [];
      focusGame = ""; groupIds = ids.slice(); pushAll();
      inspector.innerHTML = '<div class="ihead"><span class="ititle">Group set: ' + esc(cat) + '</span>'
        + '<button class="clear-sel">Clear</button></div>'
        + '<div class="ibody muted">' + ids.length + ' groups highlighted; the '
        + '<span style="color:' + SEL_COL + '">◆</span> ink diamond marks its mean. Click a single point to inspect one group.</div>';
      wireClear();
    }}
    function memberCol(m, g) {{
      let h = '<div class="partbox"><b>Participant ' + m.pos + '</b>';
      const dem = []; if (m.age) dem.push("age " + m.age); if (m.gender) dem.push(esc(m.gender));
      if (Array.isArray(m.race) && m.race.length) dem.push(esc(m.race.join(", ")));
      if (dem.length) h += ' <span class="muted">' + dem.join(" · ") + '</span>';
      h += '<div class="muted" style="margin-top:.3em">Round-4 labels typed:</div>' + imgRow(labelLines(m.labels["4"]), null, 8);
      h += '<div class="muted" style="margin-top:.3em">Round-4 recall '
         + '(<span style="color:#16a34a">green</span>=unique match, '
         + '<span style="color:#b45309">amber</span>=reused name (no credit), '
         + '<span style="color:#dc2626">red</span>=mismatch):</div>' + imgRow(m.recall["4"], g.cellstatus["4"], 8);
      if (m.strategy) h += '<details style="margin-top:.4em"><summary>Strategy</summary><div class="open">' + esc(m.strategy) + '</div></details>';
      if (m.working)  h += '<details><summary>Dividing the work</summary><div class="open">' + esc(m.working) + '</div></details>';
      if (m.mistake)  h += '<details><summary>Mistakes</summary><div class="open">' + esc(m.mistake) + '</div></details>';
      return h + '</div>';
    }}
    function setFocus(gid) {{
      const g = GROUPDATA[gid]; if (!g) {{ clearSel(); return; }}
      focusGame = gid; groupIds = [gid]; pushAll();
      const colr = COND_COL[g.treatmentGroup] || "#64748b";
      const accSeq = ROUNDS.map(r => '<b>' + g.accuracy[r] + '</b>/' + RECALL_N[r]).join(' &middot; ');
      let su = "";
      if (g.schema_use_4 === 1) su = '<span class="badge" style="background:{SCHEMA_COL}">used schema in R4</span>';
      else if (g.schema_use_4 === 0) su = '<span class="badge" style="background:#94a3b8">no schema in R4</span>';
      let h = '<div class="ihead"><span class="ititle">Group ' + esc(gid)
        + ' <span class="badge" style="background:' + colr + '">' + TG_LABEL[g.treatmentGroup] + '</span> '
        + '<span class="badge" style="background:#64748b">' + CT_LABEL[g.changeType] + '</span> ' + su + '</span>'
        + '<button class="clear-sel">Clear</button></div>';
      h += '<div class="ibody"><div>Accuracy by round (1a·1b·1c·2·3·4): ' + accSeq + '</div>';
      h += '<div class="twocol" style="margin-top:.5em">' + g.members.map(m => memberCol(m, g)).join('') + '</div></div>';
      inspector.innerHTML = h; wireClear();
    }}
    function readSel(view, name) {{
      try {{ const st = view.data(name + '_store'); return (st && st.length) ? st[0].values[0] : null; }} catch (e) {{ return null; }}
    }}
    function handlePick(view, p) {{
      if (syncing) return; syncing = true;
      try {{
        const val = readSel(view, p);          // point selection keyed on `fields` => scalar at values[0]
        if (val == null) clearSel();
        else if (p === 'pick') setFocus(String(val));
        else setGroupSet(p.slice(5), String(val));
        views.forEach(o => o.picks.forEach(pp => {{
          if (o.view === view && pp === p) return;
          try {{ o.view.data(pp + '_store', []); o.view.run(); }} catch (e) {{}} }}));
      }} finally {{ syncing = false; }}
    }}
    inspector.innerHTML = idle();
    EMBEDS.forEach(e => {{
      vegaEmbed('#' + e.id, e.spec, {{actions: false}}).then(res => {{
        const o = {{view: res.view, picks: (e.picks && e.picks.length) ? e.picks : ['pick']}};
        views.push(o);
        o.picks.forEach(p => {{ try {{ res.view.addSignalListener(p, () => handlePick(res.view, p)); }} catch (err) {{}} }});
      }}).catch(console.error);
    }});
  }}

  const STUDY_CFGS = {js_json([{"EMBEDS": s["embeds"], "CATMAP": s["catmap"], "GROUPDATA": s["groupdata"], "inspectorId": s["inspector_id"]} for s in sections])};
  STUDY_CFGS.forEach(makeStudy);
</script>"""

nav = ('<nav class="studynav"><span class="muted">Jump to:</span>'
       + ''.join(f'<a href="#sec_{c["key"]}">{escape(c["title"].split(" — ")[0])}</a>'
                 for c in STUDIES) + '</nav>')

html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Competency Traps — Study 1 &amp; Study 2 Dashboard</title>
{CSS}
{vega_scripts}
</head><body>
<h1>Competency traps — shared schemas under environmental change</h1>
<p class="meta">Generated {date.today().isoformat()} · unit of analysis = <b>group (dyad)</b> ·
two studies, each independently interactive.</p>

<div class="how">
  <b>Click a point or line</b> to <b>focus one group</b> — its trajectory goes
  <span class="sw" style="background:{FOCUS_COL}"></span> bold across that study's charts and its <b>inspector</b>
  fills with the group's actual round-4 labels and recall (<span class="sw" style="background:#86efac"></span> unique
  match · <span class="sw" style="background:#fcd34d"></span> reused name, no credit ·
  <span class="sw" style="background:#fecaca"></span> mismatch), plus open-ended explanations.
  <b>Click a bar</b> to highlight a whole group set. Colors:
  <span class="sw" style="background:{SCHEMA_COL}"></span> Schema ·
  <span class="sw" style="background:{NONSCHEMA_COL}"></span> Non-schema.
  Each study is self-contained — selections never cross between sections.
</div>

{nav}
{''.join(s["section"] for s in sections)}

{controller_js}
</body></html>"""

with open(OUT_HTML, "w") as f:
    f.write(html)
print(f"Wrote {OUT_HTML} ({len(html):,} bytes) · {len(all_embeds)} interactive charts across {len(sections)} studies (vl=v{vl_major})")
