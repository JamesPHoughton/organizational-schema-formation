"""Reusable CONSORT-style participant-flow diagrams.

A thin wrapper around Graphviz (`dot`) that lays out the standard CONSORT
flow: a vertical spine of "retained sample" boxes with exclusion boxes
branching to the right between stages, and an optional terminal split into
treatment arms. Renders to vector PDF (for the paper) and PNG (for preview).

Requires the `graphviz` Python package and the `dot` binary on PATH
(`brew install graphviz` / `conda install graphviz`).
"""

import graphviz


def consort_diagram(stages, exclusions=None, arms=None, path=None, dpi=300,
                    ranksep=0.28, nodesep=0.30, fontsize=11, size="6.5,9", ratio="compress"):
    """Build (and optionally render) a CONSORT flow diagram.

    Parameters
    ----------
    stages : list[str]
        Retained-sample box labels, top to bottom. Use ``\\n`` for line breaks.
    exclusions : list[str | None], optional
        Exclusion-reason boxes shown to the right, one per gap between
        consecutive stages (so ``len == len(stages) - 1``). ``None`` entries
        draw a plain arrow with no side box.
    arms : list[str] | None, optional
        Terminal boxes drawn side by side under the last stage (e.g. the two
        analyzed treatment arms).
    path : str | None, optional
        Output basename without extension. When given, writes ``{path}.pdf``
        and ``{path}.png``.
    dpi : int
        Raster resolution for the PNG.
    ranksep, nodesep : float
        Vertical gap between rows / horizontal gap between nodes (inches).
        ``ranksep`` is the main lever on total height — shrink it for a flatter,
        page-friendly diagram.
    fontsize : int
        Base font size for stage boxes (exclusion boxes are one point smaller).
    size : str | None
        Max drawing size "W,H" in inches. Graphviz scales the layout down to fit
        this box, so the figure prints within a single page. ``None`` disables.
    ratio : str | None
        Graphviz ``ratio`` (e.g. "compress" to pack a tall graph toward ``size``).
        ``None`` disables.

    Returns
    -------
    graphviz.Digraph
        The diagram (renders inline in Jupyter).
    """
    exclusions = exclusions or [None] * (len(stages) - 1)
    assert len(exclusions) == len(stages) - 1, (
        f"need one exclusion slot per gap: {len(exclusions)} != {len(stages) - 1}"
    )

    g = graphviz.Digraph("consort")
    g.attr(rankdir="TB", nodesep=str(nodesep), ranksep=str(ranksep), splines="ortho")
    if size:
        g.attr(size=size)
    if ratio:
        g.attr(ratio=ratio)
    g.attr(
        "node",
        shape="box",
        style="filled",
        fillcolor="white",
        color="#333333",
        fontname="Helvetica",
        fontsize=str(fontsize),
        margin="0.12,0.07",
    )
    g.attr("edge", color="#333333", arrowsize="0.7")

    for i, label in enumerate(stages):
        g.node(f"s{i}", label)

    for i, reason in enumerate(exclusions):
        if reason is None:
            g.edge(f"s{i}", f"s{i + 1}")
            continue
        # Invisible junction on the spine that the exclusion box hangs off of.
        j = f"j{i}"
        g.node(j, "", shape="point", width="0.02", style="invis")
        g.node(f"e{i}", reason, fillcolor="#f2f2f2", fontsize=str(fontsize - 1))
        g.edge(f"s{i}", j, arrowhead="none")
        g.edge(j, f"s{i + 1}")
        g.edge(j, f"e{i}", arrowhead="none", minlen="2")
        with g.subgraph() as same:
            same.attr(rank="same")
            same.node(j)
            same.node(f"e{i}")

    if arms:
        for k, arm in enumerate(arms):
            g.node(f"a{k}", arm, fillcolor="#eef4fb")
            g.edge(f"s{len(stages) - 1}", f"a{k}")

    if path:
        g.attr(dpi=str(dpi))
        g.render(path, format="png", cleanup=True)
        g.attr(dpi="")
        g.render(path, format="pdf", cleanup=True)
        print(f"Saved {path}.pdf and {path}.png")

    return g
