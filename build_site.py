#!/usr/bin/env python3
"""
Compiles the 8 primary-source dossiers (619 KB, 8,100+ lines) in sources/01..08-*.md
alongside interactive verification matrices and briefings into unabridged, deeply
literate multi-tab HTML monographs across index.html, workload.html, proxies.html,
hardware.html, assurance.html, vision.html, and atlas.html.
"""
import html
import os
import re

ROOT = "/Users/ember/dev/whatember"
SOURCES = os.path.join(ROOT, "sources")

PUBLIC_GH_REPOS = {
    "breadstuffs": "https://github.com/emberian/breadstuffs/blob/main/",
    "minidregg": "https://github.com/emberian/minidregg/blob/main/",
    "zkml-research": "https://github.com/emberian/zkml-research/blob/main/",
    "degg-research": "https://github.com/emberian/degg-research/blob/main/",
    "redregg": "https://github.com/emberian/redregg/blob/main/",
    "plonky3-recursion": "https://github.com/emberian/plonky3-recursion/blob/main/",
    "fn": "https://github.com/emberian/fn/blob/main/",
    "dregg-posters": "https://github.com/emberian/dregg-posters/blob/main/",
    "verifereum": "https://github.com/verifereum/verifereum/blob/main/",
}


def read_lines(filename, start_line=1, end_line=None):
    path = os.path.join(SOURCES, filename)
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    if end_line is None:
        return "".join(lines[start_line - 1 :])
    return "".join(lines[start_line - 1 : end_line])


def slugify(text, counter):
    s = re.sub(r"`([^`]*)`", r"\1", text)
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    if not s:
        s = "section"
    return f"{s[:48]}-{counter}"


def format_inline(text):
    # Protect inline code spans first
    code_spans = []

    def save_code(m):
        idx = len(code_spans)
        code_spans.append(f"<code>{html.escape(m.group(1))}</code>")
        return f"\x00CODE{idx}\x00"

    text = re.sub(r"`([^`]+)`", save_code, text)

    # Protect math spans $...$
    math_spans = []

    def save_math(m):
        idx = len(math_spans)
        math_spans.append(html.escape(m.group(0)))
        return f"\x00MATH{idx}\x00"

    text = re.sub(r"\$\$[^$]+\$\$|\$[^$\n]+\$", save_math, text)

    # Convert markdown links [label](url)
    links = []

    def save_link(m):
        label_raw = m.group(1)
        url = m.group(2).strip()
        label_fmt = format_inline_basic(html.escape(label_raw))
        if url.startswith("file:///Users/ember/"):
            rel = url.replace("file:///Users/ember/dev/", "").replace("file:///Users/ember/src/", "")
            parts = rel.split("/", 1)
            repo = parts[0]
            rest = parts[1] if len(parts) > 1 else ""
            if repo in PUBLIC_GH_REPOS:
                gh_url = PUBLIC_GH_REPOS[repo] + rest
                link_html = f'<a href="{html.escape(gh_url)}" target="_blank" rel="noopener" title="{html.escape(rel)}">{label_fmt}</a>'
            else:
                link_html = f'<span class="src-loc" title="{html.escape(rel)}">{label_fmt}</span>'
        else:
            target = ' target="_blank" rel="noopener"' if url.startswith("http") else ""
            link_html = f'<a href="{html.escape(url)}"{target}>{label_fmt}</a>'
        idx = len(links)
        links.append(link_html)
        return f"\x00LINK{idx}\x00"

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", save_link, text)

    # Escape remaining HTML
    text = html.escape(text)
    text = format_inline_basic(text)

    # Restore links, math, code
    for idx, val in enumerate(links):
        text = text.replace(f"\x00LINK{idx}\x00", val)
    for idx, val in enumerate(math_spans):
        text = text.replace(f"\x00MATH{idx}\x00", val)
    for idx, val in enumerate(code_spans):
        text = text.replace(f"\x00CODE{idx}\x00", val)
    return text


def format_inline_basic(text):
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", text)
    return text


def render_markdown_to_monograph(md_text, prefix="sec", dossier_badge=None, raw_dossier_file=None):
    lines = md_text.splitlines()
    n = len(lines)
    i = 0
    out = []
    toc = []
    sec_counter = 0

    if dossier_badge and raw_dossier_file:
        branch_ref = "main"
        out.append(
            f'<div class="callout" style="margin-top:0;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">'
            f'<div><div class="callout-title">{html.escape(dossier_badge)}</div>'
            f'<div>Working field notes &amp; source index below, with theorem anchors, code pointers, git history, and open questions.</div></div>'
            f'<div style="display:flex;gap:8px;"><a class="btn btn-primary" href="https://github.com/emberian/whatember/blob/{branch_ref}/sources/{html.escape(raw_dossier_file)}" target="_blank" rel="noopener">View on GitHub ↗</a>'
            f'<a class="btn btn-ghost" style="color:var(--ink);border-color:var(--line);" href="sources/{html.escape(raw_dossier_file)}" target="_blank">Raw Markdown ↗</a></div>'
            f"</div>"
        )

    while i < n:
        line = lines[i]

        # Skip blank lines
        if not line.strip():
            i += 1
            continue

        # Horizontal rule
        if re.match(r"^\s*([-*_])\1\1+\s*$", line):
            out.append("<hr/>")
            i += 1
            continue

        # Fenced code block
        m_fence = re.match(r"^(\s*)```([^\s`]*)\s*$", line)
        if m_fence:
            lang = m_fence.group(2).strip() or "text"
            i += 1
            code_lines = []
            while i < n and not re.match(r"^\s*```\s*$", lines[i]):
                code_lines.append(lines[i])
                i += 1
            if i < n:
                i += 1
            raw_code = "\n".join(code_lines)
            if lang.lower() == "mermaid":
                out.append(f'<pre class="mermaid">{html.escape(raw_code)}</pre>')
            else:
                out.append(
                    f'<div class="code-block-wrap">'
                    f'<div class="code-header"><span>{html.escape(lang)}</span>'
                    f'<button class="code-copy-btn" type="button">Copy</button></div>'
                    f"<pre><code>{html.escape(raw_code)}</code></pre></div>"
                )
            continue

        # Display math block $$
        if line.strip().startswith("$$"):
            math_lines = [line]
            if not (line.strip().endswith("$$") and len(line.strip()) > 2):
                i += 1
                while i < n:
                    math_lines.append(lines[i])
                    if lines[i].strip().endswith("$$"):
                        break
                    i += 1
            i += 1
            out.append(f'<div class="math-block">{html.escape(chr(10).join(math_lines))}</div>')
            continue

        # Headings
        m_h = re.match(r"^(#{1,4})\s+(.+)$", line)
        if m_h:
            level = len(m_h.group(1))
            title_raw = m_h.group(2).strip()
            sec_counter += 1
            hid = f"{prefix}-{slugify(title_raw, sec_counter)}"
            if level == 1:
                # Render H1 as a prominent callout header inside the tab
                out.append(f'<h2 id="{hid}">{format_inline(title_raw)}</h2>')
            elif level == 2:
                out.append(f'<h2 id="{hid}">{format_inline(title_raw)}</h2>')
                toc.append(("h2", hid, format_inline(title_raw)))
            elif level == 3:
                out.append(f'<h3 id="{hid}">{format_inline(title_raw)}</h3>')
                toc.append(("h3", hid, format_inline(title_raw)))
            else:
                out.append(f'<h4 id="{hid}">{format_inline(title_raw)}</h4>')
            i += 1
            continue

        # Pipe Table
        if "|" in line and i + 1 < n and re.match(r"^\s*\|?[\s:|-]+\|[\s:|-]*$", lines[i + 1]):
            header_cells = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2  # skip header and separator
            rows = []
            while i < n and "|" in lines[i] and lines[i].strip():
                row_cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                rows.append(row_cells)
                i += 1
            thead = "<tr>" + "".join(f"<th>{format_inline(c)}</th>" for c in header_cells) + "</tr>"
            tbody_rows = []
            for r in rows:
                if len(r) < len(header_cells):
                    r += [""] * (len(header_cells) - len(r))
                tbody_rows.append("<tr>" + "".join(f"<td>{format_inline(c)}</td>" for c in r[: len(header_cells)]) + "</tr>")
            out.append(f'<div class="table-wrap"><table><thead>{thead}</thead><tbody>{"".join(tbody_rows)}</tbody></table></div>')
            continue

        # Blockquote
        if line.lstrip().startswith(">"):
            bq_lines = []
            while i < n and lines[i].lstrip().startswith(">"):
                cleaned = re.sub(r"^\s*>\s?", "", lines[i])
                bq_lines.append(cleaned)
                i += 1
            bq_text = "\n".join(bq_lines).strip()
            out.append(f"<blockquote><p>{format_inline(bq_text)}</p></blockquote>")
            continue

        # Lists (unordered or ordered)
        m_list = re.match(r"^(\s*)([-*+]|\d+\.)\s+(.+)$", line)
        if m_list:
            is_ordered = m_list.group(2)[0].isdigit()
            tag = "ol" if is_ordered else "ul"
            items = []
            while i < n:
                m_item = re.match(r"^(\s*)([-*+]|\d+\.)\s+(.+)$", lines[i])
                if m_item:
                    item_lines = [m_item.group(3)]
                    i += 1
                    while i < n and lines[i].strip() and not re.match(r"^(\s*)([-*+]|\d+\.)\s+", lines[i]) and not re.match(r"^(#{1,4}|\s*```|\s*>)", lines[i]):
                        item_lines.append(lines[i].strip())
                        i += 1
                    items.append(" ".join(item_lines))
                else:
                    break
            li_html = "".join(f"<li>{format_inline(it)}</li>" for it in items)
            out.append(f"<{tag}>{li_html}</{tag}>")
            continue

        # Standard Paragraph
        para_lines = [line.strip()]
        i += 1
        while (
            i < n
            and lines[i].strip()
            and not re.match(r"^(#{1,4}\s|\s*```|\s*>|\s*([-*_])\2\2+\s*$|\s*([-*+]|\d+\.)\s)", lines[i])
            and not ("|" in lines[i] and i + 1 < n and re.match(r"^\s*\|?[\s:|-]+\|[\s:|-]*$", lines[i + 1]))
        ):
            para_lines.append(lines[i].strip())
            i += 1
        out.append(f"<p>{format_inline(' '.join(para_lines))}</p>")

    toc_html = ""
    if toc:
        toc_items = []
        for lvl, hid, label in toc:
            cls = ' class="toc-h3"' if lvl == "h3" else ""
            toc_items.append(f'<li{cls}><a href="#{hid}">{label}</a></li>')
        toc_html = (
            f'<aside class="doc-toc" aria-label="Section table of contents">'
            f'<div class="doc-toc-title">On This Tab ({len(toc)} Sections)</div>'
            f'<ul>{"".join(toc_items)}</ul>'
            f"</aside>"
        )
        return f'<div class="doc-layout">{toc_html}<div class="doc-prose">{"".join(out)}</div></div>'
    else:
        return f'<div class="doc-prose">{"".join(out)}</div>'


def page_shell(filename, title, description, hero_html, subtabs, panels_html, footer_note):
    nav_items = [
        ("index.html", "01 · Overview"),
        ("workload.html", "02 · Workload & Absence"),
        ("proxies.html", "03 · Merkle Proxies"),
        ("hardware.html", "04 · Hardware & Silicon"),
        ("assurance.html", "05 · Formal Kernels"),
        ("vision.html", "06 · Vision & Lineage"),
        ("atlas.html", "07 · Master Atlas"),
        ("deos.html", "08 · DeOS & Breadstuffs"),
        ("verticals.html", "09 · All Verticals"),
        ("triage.html", "10 · Metamanagement & Triage"),
    ]
    nav_links = []
    for href, label in nav_items:
        cur = ' aria-current="page"' if href == filename else ""
        nav_links.append(f'<a href="{href}"{cur}>{html.escape(label)}</a>')

    subtab_btns = []
    for idx, (tid, tlabel) in enumerate(subtabs):
        sel = "true" if idx == 0 else "false"
        subtab_btns.append(
            f'<button class="subtab-btn" role="tab" aria-selected="{sel}" data-tab-target="{tid}">{html.escape(tlabel)}</button>'
        )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}" />
  <link rel="stylesheet" href="assets/style.css" />
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" />
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <script src="assets/app.js" defer></script>
</head>
<body>
  <header class="topbar">
    <div class="wrap topbar-inner">
      <a class="brand" href="index.html">
        <span class="brand-mark">W</span>
        <span>whatember</span>
        <small>what ember is up to · Nov 2026</small>
      </a>
      <nav class="main-nav" aria-label="Primary navigation">
        {"".join(nav_links)}
        <button id="theme-toggle" class="theme-toggle" type="button" title="Toggle theme">◐</button>
      </nav>
    </div>
  </header>

  {hero_html}

  <div class="subtabs-wrap">
    <div class="wrap subtabs" role="tablist">
      {"".join(subtab_btns)}
    </div>
  </div>

  <main class="wrap">
    {panels_html}
  </main>

  <footer class="site-footer">
    <div class="wrap footer-grid">
      <div>
        <strong>whatember</strong> · {footer_note}<br/>
        Working notebook &amp; open map across <code>~/dev</code> — linking live prototypes, formal footholds, composted generations, and open cycles.
      </div>
      <div>
        <a href="https://github.com/emberian/whatember">GitHub Repo</a> ·
        <a href="atlas.html">Master Atlas</a>
      </div>
    </div>
  </footer>
</body>
</html>
"""


def build_all():
    # 1. Read existing index.html to extract the rich interactive Problem->Primitive->Proof matrix & Quinn briefing
    with open(os.path.join(ROOT, "index.html"), "r", encoding="utf-8") as f:
        old_index = f.read()

    # Extract Tab 1B (matrix) and Tab 1C (quinn) inner HTML from old_index
    m_mat = re.search(r'<section id="tab-matrix"[^>]*>(.*?)</section>', old_index, re.S)
    matrix_inner = m_mat.group(1).strip() if m_mat else ""
    m_quinn = re.search(r'<section id="tab-quinn"[^>]*>(.*?)</section>', old_index, re.S)
    quinn_inner = m_quinn.group(1).strip() if m_quinn else ""

    # Build INDEX.HTML
    exec_synth_md = (
        read_lines("01-parsing-query-aggregation-absence.md", 1, 56)
        + "\n\n---\n\n"
        + read_lines("02-merkle-agent-proxies-and-dataplanes.md", 1, 61)
        + "\n\n---\n\n"
        + read_lines("04-workload-verification-zkml-vfhe-selvage.md", 1, 48)
        + "\n\n---\n\n"
        + read_lines("07-obend-silicon-fpga-and-latest-dregg.md", 1, 30)
    )
    tab_1a_monograph = render_markdown_to_monograph(
        exec_synth_md,
        prefix="idx-exec",
        dossier_badge="Field Notes Across Dossiers 01, 02, 04 & 07",
        raw_dossier_file="01-parsing-query-aggregation-absence.md",
    )
    tab_1d_monograph = render_markdown_to_monograph(
        read_lines("08-october-november-2026-stratum.md", 1),
        prefix="idx-octnov",
        dossier_badge="Dossier 08 · Complete October–November 2026 Stratum (72 KB)",
        raw_dossier_file="08-october-november-2026-stratum.md",
    )
    with open(os.path.join(ROOT, "PROGRAM-2026-11-12-obend-cathedral-and-trimodel-roadmap.md"), "r", encoding="utf-8") as f:
        prog_nov12_md = f.read()
    with open(os.path.join(ROOT, "INITIATIVES.md"), "r", encoding="utf-8") as f:
        init_nov12_md = f.read()
    tab_1e_header = (
        '<div class="callout" style="margin-top:0;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">'
        '<div><div class="callout-title">Active Master Charter · November 12, 2026 Convergence (<code>obend</code> + <code>obb v2</code> + Tri-Model Campaign)</div>'
        '<div>Consolidated cathedral architecture (<code>O1</code>–<code>O7</code>), <code>obb quarry</code> donor surgery (<code>refs/quarry/*</code>), <code>Oracle7</code> severance, Waves 1–3.8 ground truth, and Wave-4 <code>Gemini</code> × <code>Claude Fable</code> × <code>Codex Astra</code> peer engineering.</div></div>'
        '<div style="display:flex;gap:8px;">'
        '<a class="btn btn-primary" href="https://github.com/emberian/whatember/blob/main/PROGRAM-2026-11-12-obend-cathedral-and-trimodel-roadmap.md" target="_blank" rel="noopener">Program Charter ↗</a>'
        '<a class="btn btn-ghost" style="color:var(--ink);border-color:var(--line);" href="https://github.com/emberian/whatember/blob/main/INITIATIVES.md" target="_blank" rel="noopener">Initiatives Register ↗</a>'
        "</div></div>"
    )
    tab_1e_monograph = tab_1e_header + render_markdown_to_monograph(
        prog_nov12_md + "\n\n---\n\n" + init_nov12_md,
        prefix="idx-cathedral",
    )
    nov12_banner_html = (
        '<div class="callout" style="margin:0 0 28px 0;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">'
        '<div><div class="callout-title">Nov 12, 2026 Update · <code>obend</code> Cathedral + <code>obb v2</code> Metaharness &amp; Tri-Model Roadmap</div>'
        '<div>Active work across <code>breadstuffs</code>, <code>minidregg</code>, <code>svenvs</code>, and <code>lean-transport</code> now converges into <code>obend</code> (<code>dev</code>, 785+ Lean 4.35 modules) under <code>obb v2</code> (<code>cone</code>, <code>apex</code>, <code>pipeline</code>, <code>quarry</code>, <code>broker</code>), severing <code>Oracle7</code> and advancing Organs <code>O1</code>–<code>O7</code> via <code>Gemini</code> × <code>Claude claude-fable-5-2</code> × <code>Codex gpt-6-astra</code>.</div></div>'
        '<div style="display:flex;gap:8px;">'
        '<a class="btn btn-primary" href="https://github.com/emberian/whatember/blob/main/PROGRAM-2026-11-12-obend-cathedral-and-trimodel-roadmap.md" target="_blank" rel="noopener">Read Nov 12 Charter ↗</a>'
        '<a class="btn btn-ghost" style="color:var(--ink);border-color:var(--line);" href="https://github.com/emberian/whatember/blob/main/INITIATIVES.md" target="_blank" rel="noopener">Initiatives Register ↗</a>'
        "</div></div>"
    )

    m_hero_idx = re.search(r'(<section class="hero">.*?</section>)', old_index, re.S)
    hero_idx = m_hero_idx.group(1)
    m_exec_cards = re.search(r'<section id="tab-exec"[^>]*>(.*?)</section>', old_index, re.S)
    exec_cards_html = m_exec_cards.group(1).split('<hr style="margin:42px 0;')[0].strip() if m_exec_cards else ""

    index_panels = f"""
    <section id="tab-exec" class="tab-panel active" role="tabpanel">
      {exec_cards_html}
      <hr style="margin:42px 0;border:0;border-top:2px solid var(--line);" />
      {nov12_banner_html}
      {tab_1a_monograph}
    </section>
    <section id="tab-matrix" class="tab-panel" role="tabpanel">
      {matrix_inner}
    </section>
    <section id="tab-quinn" class="tab-panel" role="tabpanel">
      {quinn_inner}
    </section>
    <section id="tab-dossiers" class="tab-panel" role="tabpanel">
      {tab_1d_monograph}
    </section>
    <section id="tab-cathedral" class="tab-panel" role="tabpanel">
      {tab_1e_monograph}
    </section>
    """
    index_html = page_shell(
        "index.html",
        "whatember — what ember is up to",
        "Working notebook and open map of what Ember is up to across verifiable compute, DeOS, OBend silicon, neurobiology, deductive neural organs, and swarm continuity.",
        hero_idx,
        [
            ("tab-exec", "1A · Workshop Map & Open Directions"),
            ("tab-matrix", "1B · Interactive Problem → Primitive → Foothold Matrix"),
            ("tab-quinn", "1C · Briefing for Quinn & Lucid Computing"),
            ("tab-dossiers", "1D · Oct–Nov 2026 Stratum (svenvs, verekos, o7vn, fn2)"),
            ("tab-cathedral", "1E · Nov 12 Cathedral Roadmap (obend + obb v2)"),
        ],
        index_panels,
        "01 · Overview & Workshop Map",
    )
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    # 2. Build WORKLOAD.HTML (Full Dossiers 01 & 04 — ~144 KB of primary sources)
    with open(os.path.join(ROOT, "workload.html"), "r", encoding="utf-8") as f:
        old_workload = f.read()
    hero_wl = re.search(r'(<section class="hero">.*?</section>)', old_workload, re.S).group(1)

    wl_2a = render_markdown_to_monograph(
        read_lines("01-parsing-query-aggregation-absence.md", 1, 394),
        prefix="wl-deriv",
        dossier_badge="Dossier 01 (§0–§1) · Verified Regex-Complement DFAs & Symbolic Derivatives (`dregg-dfa` & `Dregg2/Crypto/Deriv/*`)",
        raw_dossier_file="01-parsing-query-aggregation-absence.md",
    )
    wl_2b = render_markdown_to_monograph(
        read_lines("01-parsing-query-aggregation-absence.md", 395, 570),
        prefix="wl-cfg",
        dossier_badge="Dossier 01 (§2) · Context-Free Parsing Certificates, Guarded Templates & 8-Lane Welded STARK Guards (`Cfg.lean`, `AttestedAutomatonWeld8.lean`)",
        raw_dossier_file="01-parsing-query-aggregation-absence.md",
    )
    wl_2c = render_markdown_to_monograph(
        read_lines("01-parsing-query-aggregation-absence.md", 571),
        prefix="wl-query",
        dossier_badge="Dossier 01 (§3–§5) · Attested MMR Queries, Non-Omission Theorems & End-to-End Training-Set Absence Protocol",
        raw_dossier_file="01-parsing-query-aggregation-absence.md",
    )
    wl_2d = render_markdown_to_monograph(
        read_lines("04-workload-verification-zkml-vfhe-selvage.md", 1, 318),
        prefix="wl-selvage",
        dossier_badge="Dossier 04 (§0–§2) · Selvage Commit-Then-Audit (`AuditSampling.lean`) & 1.56 TB Frontier Weight Registry",
        raw_dossier_file="04-workload-verification-zkml-vfhe-selvage.md",
    )
    wl_2e = render_markdown_to_monograph(
        read_lines("04-workload-verification-zkml-vfhe-selvage.md", 319, 408),
        prefix="wl-mxfp4",
        dossier_badge="Dossier 04 (§3) · Bit-Exact Native OCP `MXFP4` Arithmetization & 0.72%-Overhead MoE Router Binding",
        raw_dossier_file="04-workload-verification-zkml-vfhe-selvage.md",
    )
    wl_2f = render_markdown_to_monograph(
        read_lines("04-workload-verification-zkml-vfhe-selvage.md", 409),
        prefix="wl-vfhe",
        dossier_badge="Dossier 04 (§4–§6) · $p_{61}$ Verifiable FHE (`CyclotomicInertia.lean`), Dark Continual Learning & GPU/TPU/FPGA Proving Physics",
        raw_dossier_file="04-workload-verification-zkml-vfhe-selvage.md",
    )

    workload_panels = f"""
    <section id="tab-absence" class="tab-panel active" role="tabpanel">{wl_2c}</section>
    <section id="tab-deriv" class="tab-panel" role="tabpanel">{wl_2a}</section>
    <section id="tab-cfg" class="tab-panel" role="tabpanel">{wl_2b}</section>
    <section id="tab-selvage" class="tab-panel" role="tabpanel">{wl_2d}</section>
    <section id="tab-mxfp4" class="tab-panel" role="tabpanel">{wl_2e}</section>
    <section id="tab-vfhe" class="tab-panel" role="tabpanel">{wl_2f}</section>
    """
    workload_html = page_shell(
        "workload.html",
        "02 · Workload Verification, Training-Set Absence Proofs, zkML & vFHE Monograph — whatember",
        "Complete primary-source monograph for training-set absence proofs, 3,522-line Lean 4 regex-complement DFAs, 4M-token/40ms welded parsing certificates, Selvage commit-then-audit, MXFP4, and vFHE.",
        hero_wl,
        [
            ("tab-absence", "2A · Attested MMR Queries & Training-Set Absence Protocol"),
            ("tab-deriv", "2B · Regex-Complement DFAs & Symbolic Derivatives (3,522 LOC Lean 4)"),
            ("tab-cfg", "2C · Parsing Certificates & Welded STARK Guards (`Cfg.lean`)"),
            ("tab-selvage", "2D · Selvage Commit-Then-Audit & 1.56 TB Weight Registry"),
            ("tab-mxfp4", "2E · Native `MXFP4` Dot Products & 0.72% MoE Router Binding"),
            ("tab-vfhe", "2F · Verifiable FHE ($p_{61}$), Dark Training & GPU/TPU/FPGA Physics"),
        ],
        workload_panels,
        "02 · Workload Verification, Training-Set Absence Proofs, zkML & vFHE (Full Dossiers 01 & 04 · 144 KB)",
    )
    with open(os.path.join(ROOT, "workload.html"), "w", encoding="utf-8") as f:
        f.write(workload_html)

    # 3. Build PROXIES.HTML (Full Dossier 02 — 82 KB)
    with open(os.path.join(ROOT, "proxies.html"), "r", encoding="utf-8") as f:
        old_proxies = f.read()
    hero_pr = re.search(r'(<section class="hero">.*?</section>)', old_proxies, re.S).group(1)

    pr_3a = render_markdown_to_monograph(
        read_lines("02-merkle-agent-proxies-and-dataplanes.md", 350, 595)
        + "\n\n---\n\n"
        + read_lines("02-merkle-agent-proxies-and-dataplanes.md", 897),
        prefix="pr-engines",
        dossier_badge="Dossier 02 (§2 & §5) · The 4 Merkleization Engines (`grain-turn`, `inclusion-availability` MMR, `grain-fork`, `FullForestAuth.lean`, `AuthTrie.lean`)",
        raw_dossier_file="02-merkle-agent-proxies-and-dataplanes.md",
    )
    pr_3b = render_markdown_to_monograph(
        read_lines("02-merkle-agent-proxies-and-dataplanes.md", 1, 349),
        prefix="pr-gateways",
        dossier_badge="Dossier 02 (§0–§1) · Tool-Call, ACP & Keyless BYOK Intercepting Proxies (`ToolGateway`, `deos-hermes`, `mini-keys`, `secS-magik`)",
        raw_dossier_file="02-merkle-agent-proxies-and-dataplanes.md",
    )
    pr_3c = render_markdown_to_monograph(
        read_lines("02-merkle-agent-proxies-and-dataplanes.md", 596, 825),
        prefix="pr-orb",
        dossier_badge="Dossier 02 (§3) · Formally Verified HTTP/Proxy Dataplane (`Orb`, `dregg-serve-spec`, `orb-compiler`, `dreggnetArenaScript.sml`)",
        raw_dossier_file="02-merkle-agent-proxies-and-dataplanes.md",
    )
    pr_3d = render_markdown_to_monograph(
        read_lines("02-merkle-agent-proxies-and-dataplanes.md", 826, 896),
        prefix="pr-arch",
        dossier_badge="Dossier 02 (§4) · Chronological Git Commit Spine & Primary-Source `cv` Design Provenance",
        raw_dossier_file="02-merkle-agent-proxies-and-dataplanes.md",
    )

    proxies_panels = f"""
    <section id="tab-engines" class="tab-panel active" role="tabpanel">{pr_3a}</section>
    <section id="tab-gateways" class="tab-panel" role="tabpanel">{pr_3b}</section>
    <section id="tab-orb" class="tab-panel" role="tabpanel">{pr_3c}</section>
    <section id="tab-zkoracle" class="tab-panel" role="tabpanel">{pr_3d}</section>
    """
    proxies_html = page_shell(
        "proxies.html",
        "03 · Merkleized Agent Proxies, Capabilities & Verified Dataplanes Monograph — whatember",
        "Complete primary-source monograph for the 4-layer Merkleized agent proxy stack, grain-turn MMR/heap roots, inclusion-availability equivocation proofs, mini-keys SO_PEERCRED, and the verified Orb HTTP dataplane.",
        hero_pr,
        [
            ("tab-engines", "3A · The 4 Merkleization Engines (`grain-turn`, MMR, `FullForestAuth`, `AuthTrie`)"),
            ("tab-gateways", "3B · Tool Gateways, ACP (`deos-hermes`), Keyless BYOK (`mini-keys`) & `secS-magik`"),
            ("tab-orb", "3C · Verified HTTP Proxy Dataplane (`Orb`, Pancake x86-64 & HOL4 Arena)"),
            ("tab-zkoracle", "3D · Git Commit Spine & Primary-Source `cv` Session Archaeology"),
        ],
        proxies_panels,
        "03 · Merkleized Agent Proxies, Capabilities & Verified Dataplanes (Full Dossier 02 · 82 KB)",
    )
    with open(os.path.join(ROOT, "proxies.html"), "w", encoding="utf-8") as f:
        f.write(proxies_html)

    # 4. Build HARDWARE.HTML (Full Dossiers 07 & 03 — ~155 KB)
    with open(os.path.join(ROOT, "hardware.html"), "r", encoding="utf-8") as f:
        old_hw = f.read()
    hero_hw = re.search(r'(<section class="hero">.*?</section>)', old_hw, re.S).group(1)

    hw_4a = render_markdown_to_monograph(
        read_lines("07-obend-silicon-fpga-and-latest-dregg.md", 1, 340),
        prefix="hw-obend1",
        dossier_badge="Dossier 07 (§1–§4) · `obend` Core4, Metatheory & The Silicon Elaborator (`ExprCAM`, `DiscrTreeLUT`, Futamura, 3-Phase `ICAP` DPR)",
        raw_dossier_file="07-obend-silicon-fpga-and-latest-dregg.md",
    )
    hw_4b = render_markdown_to_monograph(
        read_lines("07-obend-silicon-fpga-and-latest-dregg.md", 341),
        prefix="hw-obend2",
        dossier_badge="Dossier 07 (§5–§9) · `obend` Physical Silicon Flow, Sky130 PDK DRC, 6-Stage FPGA/CDNA3/FP4 Equivalence, Next-Mathematica & DeOS",
        raw_dossier_file="07-obend-silicon-fpga-and-latest-dregg.md",
    )
    hw_4c = render_markdown_to_monograph(
        read_lines("03-hardware-tee-sel4-and-capabilities.md", 1, 356),
        prefix="hw-tee",
        dossier_badge="Dossier 03 (§1–§3) · Multi-Vendor TEE Verifier (`NitroVerifier`, `SnpVerifier`, `TdxVerifier`), GPU E2EE & 377/1,125 Residual Trust Proof",
        raw_dossier_file="03-hardware-tee-sel4-and-capabilities.md",
    )
    hw_4d = render_markdown_to_monograph(
        read_lines("03-hardware-tee-sel4-and-capabilities.md", 357),
        prefix="hw-sel4",
        dossier_badge="Dossier 03 (§4–§6) · Bare-Metal `seL4` Microkit 2.2.0, Firmament Capability Calculus & Post-Quantum Credential Stack",
        raw_dossier_file="03-hardware-tee-sel4-and-capabilities.md",
    )

    hardware_panels = f"""
    <section id="tab-obend" class="tab-panel active" role="tabpanel">{hw_4a}</section>
    <section id="tab-obend-phys" class="tab-panel" role="tabpanel">{hw_4b}</section>
    <section id="tab-tee" class="tab-panel" role="tabpanel">{hw_4c}</section>
    <section id="tab-sel4" class="tab-panel" role="tabpanel">{hw_4d}</section>
    """
    hardware_html = page_shell(
        "hardware.html",
        "04 · Hardware Roots of Trust, Multi-Vendor TEEs, seL4 & OBend Silicon Monograph — whatember",
        "Complete primary-source monograph for OBend (452 Lean 4 modules, 0 sorryAx, 64-bit ExprCAM, 3-phase ICAP DPR, 6-stage FPGA/CDNA3/FP4 equivalence), multi-vendor TEE verification, and seL4 Microkit.",
        hero_hw,
        [
            ("tab-obend", "4A · `obend` Core4 & Silicon Elaborator (`ExprCAM`, Futamura, 3-Phase `ICAP` DPR)"),
            ("tab-obend-phys", "4B · `obend` Physical Flow, Sky130 DRC, 6-Stage FPGA/CDNA3/FP4 & DeOS"),
            ("tab-tee", "4C · Multi-Vendor TEEs (Nitro, SEV-SNP, TDX), GPU E2EE & 377/1,125 Proof"),
            ("tab-sel4", "4D · Bare-Metal `seL4` Microkit, Firmament Cap Calculus & PQ Credentials"),
        ],
        hardware_panels,
        "04 · Hardware Roots of Trust, Multi-Vendor TEEs, seL4 & OBend Silicon (Full Dossiers 07 & 03 · 155 KB)",
    )
    with open(os.path.join(ROOT, "hardware.html"), "w", encoding="utf-8") as f:
        f.write(hardware_html)

    # 5. Build ASSURANCE.HTML (Full Dossier 05 + svenvs/verekos/o7vn/forensics from Dossier 08 — ~115 KB)
    with open(os.path.join(ROOT, "assurance.html"), "r", encoding="utf-8") as f:
        old_as = f.read()
    hero_as = re.search(r'(<section class="hero">.*?</section>)', old_as, re.S).group(1)

    as_5a = render_markdown_to_monograph(
        read_lines("05-formal-assurance-kernels-and-redteaming.md", 1, 483),
        prefix="as-sub",
        dossier_badge="Dossier 05 (§1) · The Formal Methods Substrates in Production (Lean 4, HOL4/CakeML/Pancake, `verifereum`, ACL2 `fn`, TLA+/Kani/MIR)",
        raw_dossier_file="05-formal-assurance-kernels-and-redteaming.md",
    )
    as_5b = render_markdown_to_monograph(
        read_lines("08-october-november-2026-stratum.md", 52, 271)
        + "\n\n---\n\n"
        + read_lines("08-october-november-2026-stratum.md", 441, 464)
        + "\n\n---\n\n"
        + read_lines("08-october-november-2026-stratum.md", 524),
        prefix="as-svenvs",
        dossier_badge="Dossier 08 (§1, §2, §5, §8) · `hol-reflection`, `svenvs` (Löb Reduction & In-Place x64 Self-Upgrade), `verekos`, `o7vn` & `fn2`",
        raw_dossier_file="08-october-november-2026-stratum.md",
    )
    as_5c = render_markdown_to_monograph(
        read_lines("05-formal-assurance-kernels-and-redteaming.md", 484, 655)
        + "\n\n---\n\n"
        + read_lines("08-october-november-2026-stratum.md", 487, 523),
        prefix="as-red",
        dossier_badge="Dossier 05 (§2) & Dossier 08 (§7.1) · Anti-Vacuity Gates (`CarrierCensus.lean`), Plonky3 `52e1fab` Red-Team, Nockchain & `forensics`",
        raw_dossier_file="05-formal-assurance-kernels-and-redteaming.md",
    )
    as_5d = render_markdown_to_monograph(
        read_lines("05-formal-assurance-kernels-and-redteaming.md", 656),
        prefix="as-law",
        dossier_badge="Dossier 05 (§3–§4) · Computable Law, `OPERATORLESS_AGENTS.md`, `leakage-lab` & The 5 August 2026 CFTC/SEC Filings",
        raw_dossier_file="05-formal-assurance-kernels-and-redteaming.md",
    )

    assurance_panels = f"""
    <section id="tab-substrates" class="tab-panel active" role="tabpanel">{as_5a}</section>
    <section id="tab-kernels" class="tab-panel" role="tabpanel">{as_5b}</section>
    <section id="tab-redteam" class="tab-panel" role="tabpanel">{as_5c}</section>
    <section id="tab-law" class="tab-panel" role="tabpanel">{as_5d}</section>
    """
    assurance_html = page_shell(
        "assurance.html",
        "05 · Formal Assurance Kernels, Anti-Vacuity Gates, Red-Teaming & Computable Law Monograph — whatember",
        "Complete primary-source monograph for our 5 formal verification substrates, svenvs reflective self-upgrading x64 compiler, Farkas SysCert, anti-vacuity gates, Plonky3 red-teaming, and computable law.",
        hero_as,
        [
            ("tab-substrates", "5A · Production Prover Substrates (Lean 4, HOL4/CakeML, `verifereum`, ACL2 `fn`, TLA+)"),
            ("tab-kernels", "5B · Self-Verifying HOL (`svenvs` Löb Reduction), `verekos`, `o7vn` & `fn2`"),
            ("tab-redteam", "5C · Anti-Vacuity (`CarrierCensus`), Plonky3 `52e1fab`, Nockchain & `forensics`"),
            ("tab-law", "5D · Computable Law, Operatorless Agents, `leakage-lab` & 5 CFTC/SEC Filings"),
        ],
        assurance_panels,
        "05 · Formal Assurance Kernels, Anti-Vacuity Gates, Red-Teaming & Computable Law (Full Dossiers 05 & 08 · 115 KB)",
    )
    with open(os.path.join(ROOT, "assurance.html"), "w", encoding="utf-8") as f:
        f.write(assurance_html)

    # 6. Build VISION.HTML (Full Sections 1–4 of Dossier 06 + Model Organisms/intmat/torchship from Dossier 08 — ~95 KB)
    with open(os.path.join(ROOT, "vision.html"), "r", encoding="utf-8") as f:
        old_vi = f.read()
    hero_vi = re.search(r'(<section class="hero">.*?</section>)', old_vi, re.S).group(1)

    vi_6a = render_markdown_to_monograph(
        read_lines("06-vision-origins-and-complete-project-atlas.md", 1, 136),
        prefix="vi-lineage",
        dossier_badge="Dossier 06 (§1) · The Continuous Decade-Long Thread (2013–2026) & Philosophical Pillars in Ember's Words",
        raw_dossier_file="06-vision-origins-and-complete-project-atlas.md",
    )
    vi_6b = render_markdown_to_monograph(
        read_lines("06-vision-origins-and-complete-project-atlas.md", 137, 339),
        prefix="vi-swarm",
        dossier_badge="Dossier 06 (§2–§4) · Swarm Engineering Methodology, `CLAUDE.md` Stratigraphy, `redregg`, `dregg-assortia` & `aidev` Synthesis",
        raw_dossier_file="06-vision-origins-and-complete-project-atlas.md",
    )
    vi_6c = render_markdown_to_monograph(
        read_lines("08-october-november-2026-stratum.md", 272, 440)
        + "\n\n---\n\n"
        + read_lines("08-october-november-2026-stratum.md", 465, 486),
        prefix="vi-organisms",
        dossier_badge="Dossier 08 (§3, §4, §6) · `intmat`/`intmat2`, `negstab`, `formal-organisms`, `acl2aiguide` (23 `fn` Wound Lessons) & `torchship`",
        raw_dossier_file="08-october-november-2026-stratum.md",
    )

    vision_panels = f"""
    <section id="tab-pillars" class="tab-panel active" role="tabpanel">{vi_6a}</section>
    <section id="tab-lineage" class="tab-panel" role="tabpanel">{vi_6b}</section>
    <section id="tab-swarm" class="tab-panel" role="tabpanel">{vi_6c}</section>
    """
    vision_html = page_shell(
        "vision.html",
        "06 · The Vision, Decade Lineage (2013–2026) & Swarm Engineering Monograph — whatember",
        "Complete primary-source monograph tracing the 13-year trajectory from pre-1.0 Rust and NICTA/UNSW seL4 to O(1) Labs Mina and Dregg/OBend, plus redregg swarm methodology and model organisms.",
        hero_vi,
        [
            ("tab-pillars", "6A · The Decade-Long Thread (2013–2026) & Philosophical Pillars"),
            ("tab-lineage", "6B · Swarm Engineering, `CLAUDE.md` Stratigraphy, `redregg` & `dregg-assortia`"),
            ("tab-swarm", "6C · Model Organisms (`negstab`, `formal-organisms`), `acl2aiguide` & `intmat2`"),
        ],
        vision_panels,
        "06 · The Vision, Decade Lineage (2013–2026) & Swarm Engineering (Full Dossiers 06 & 08 · 95 KB)",
    )
    with open(os.path.join(ROOT, "vision.html"), "w", encoding="utf-8") as f:
        f.write(vision_html)

    # 7. Build ATLAS.HTML (Interactive Repo Filter + Full Sections 5 & 6 of Dossier 06)
    with open(os.path.join(ROOT, "atlas.html"), "r", encoding="utf-8") as f:
        old_at = f.read()
    hero_at = re.search(r'(<section class="hero">.*?</section>)', old_at, re.S).group(1)
    m_at_repos = re.search(r'<section id="tab-repos"[^>]*>(.*?)</section>', old_at, re.S)
    at_repos_filter = m_at_repos.group(1).split('<hr style="margin:42px 0;')[0].strip() if m_at_repos else ""
    m_at_papers = re.search(r'<section id="tab-papers"[^>]*>(.*?)</section>', old_at, re.S)
    at_papers_table = m_at_papers.group(1) if m_at_papers else ""

    at_7a_deep = render_markdown_to_monograph(
        read_lines("06-vision-origins-and-complete-project-atlas.md", 340, 455),
        prefix="at-repos-deep",
        dossier_badge="Dossier 06 (§5) · Complete Master Atlas Table & Verbatim Code / Theorem Signatures Across All Repositories",
        raw_dossier_file="06-vision-origins-and-complete-project-atlas.md",
    )
    at_7b_deep = render_markdown_to_monograph(
        read_lines("06-vision-origins-and-complete-project-atlas.md", 456, 475),
        prefix="at-microsites-deep",
        dossier_badge="Dossier 06 (§6.1) · Complete `dregg-site` (`dregg.net`) Route & Information Architecture Atlas",
        raw_dossier_file="06-vision-origins-and-complete-project-atlas.md",
    )
    at_7c_deep = render_markdown_to_monograph(
        read_lines("06-vision-origins-and-complete-project-atlas.md", 476),
        prefix="at-posters-deep",
        dossier_badge="Dossier 06 (§6.2) · Complete `dregg-posters` Archive: Bilingual Typst Suites, HTML Broadsides & All 49 ASCII Posters",
        raw_dossier_file="06-vision-origins-and-complete-project-atlas.md",
    )

    atlas_panels = f"""
    <section id="tab-repos" class="tab-panel active" role="tabpanel">
      {at_repos_filter}
      <hr style="margin:42px 0;border:0;border-top:2px solid var(--line);" />
      {at_7a_deep}
    </section>
    <section id="tab-microsites" class="tab-panel" role="tabpanel">{at_7b_deep}</section>
    <section id="tab-posters" class="tab-panel" role="tabpanel">{at_7c_deep}</section>
    <section id="tab-papers" class="tab-panel" role="tabpanel">{at_papers_table}</section>
    """
    atlas_html = page_shell(
        "atlas.html",
        "07 · Searchable Master Atlas: Repositories, Posters & Theorem Signatures — whatember",
        "Complete searchable index and primary-source theorem/code signature atlas of Ember's repositories, 65+ technical posters, and 27 source dossiers.",
        hero_at,
        [
            ("tab-repos", "7A · Repositories & Primary-Source Code/Theorem Signatures"),
            ("tab-microsites", "7B · `dregg.net` Route & Information Architecture Atlas"),
            ("tab-posters", "7C · 65+ Posters: Typst EN/ZH Series, HTML Broadsides & 49 ASCII Posters"),
            ("tab-papers", "7D · All 27 Raw Primary-Source Dossiers (`sources/01..27`)"),
        ],
        atlas_panels,
        "07 · Searchable Master Atlas (Full Dossier 06 §5–§6 · 105 KB)",
    )
    with open(os.path.join(ROOT, "atlas.html"), "w", encoding="utf-8") as f:
        f.write(atlas_html)

    # 8. Build DEOS.HTML (Dossier 09 + Breadstuffs Diaspora 16..19 + OBend Language 22 + Mini/Nano/DelveTalk2 Lanes 23 — ~450 KB of primary sources)
    hero_deos = """
  <section class="hero">
    <div class="wrap">
      <div class="eyebrow">08 · DeOS, MiniDregg, NanoDregg, DelveTalk, OBend Language &amp; The Breadstuffs Diaspora</div>
      <h1>From the 2.89M-LOC <code>breadstuffs</code> Monorepo to Verified <code>minidregg</code>, <code>nanodregg</code>, <code>delvetalk2</code> &amp; Objective Bend (<code>obend</code>)</h1>
      <p class="lead">
        Complete primary-source archaeology across the <strong>100+ crates</strong> and <strong>21,511 commits</strong> of <code>~/dev/breadstuffs</code>, the <strong>Objective Bend (<code>obend</code>)</strong> language &amp; Amadio–Cardelli equi-recursive bisimulation, and the <strong>273 worktree lanes of <code>minidregg-lanes</code></strong>, <strong>67 recovered lanes of <code>claudesplosion</code></strong>, <strong>27 scouts of <code>nanodregg-scout</code></strong>, <strong>66 lanes of <code>delvetalk2-lanes</code></strong>, <code>drorb</code>, and <code>DreggCloud</code>.
      </p>
    </div>
  </section>"""

    deos_8a = render_markdown_to_monograph(
        read_lines("strands/09-deos-minidregg-nanodregg-delvetalk-deep-dive.md", 1),
        prefix="deos-deep",
        dossier_badge="Dossier 09 · DeOS, MiniDregg, NanoDregg, DelveTalk, Spween, Preoscript & OBend Deep Dive (64 KB)",
        raw_dossier_file="strands/09-deos-minidregg-nanodregg-delvetalk-deep-dive.md",
    )
    deos_8b = render_markdown_to_monograph(
        read_lines("strands/16-breadstuffs-kernel-circuits-crypto-diaspora.md", 1),
        prefix="deos-bs-kernel",
        dossier_badge="Dossier 16 · Breadstuffs Kernel, Circuits & Cryptography Diaspora (`dregg-*`, `fhegg-*`, `crypto-*`, `uc-crypthol` · 48 KB)",
        raw_dossier_file="strands/16-breadstuffs-kernel-circuits-crypto-diaspora.md",
    )
    deos_8c = render_markdown_to_monograph(
        read_lines("strands/17-breadstuffs-deos-surfaces-starbridge-diaspora.md", 1),
        prefix="deos-bs-ui",
        dossier_badge="Dossier 17 · Breadstuffs DeOS Surfaces, Starbridge 32-App Ecosystem & Moldable Inspector Diaspora (46 KB)",
        raw_dossier_file="strands/17-breadstuffs-deos-surfaces-starbridge-diaspora.md",
    )
    deos_8d = render_markdown_to_monograph(
        read_lines("strands/18-breadstuffs-dreggnet-games-worlds-diaspora.md", 1),
        prefix="deos-bs-worlds",
        dossier_badge="Dossier 18 · Breadstuffs DreggNet, Inhabited Worlds, Games (`dungeon-on-dregg`, `automatafl`) & PoA Diaspora (70 KB)",
        raw_dossier_file="strands/18-breadstuffs-dreggnet-games-worlds-diaspora.md",
    )
    deos_8e = render_markdown_to_monograph(
        read_lines("strands/19-breadstuffs-federation-chains-commons-diaspora.md", 1),
        prefix="deos-bs-fed",
        dossier_badge="Dossier 19 · Breadstuffs Federation, Cross-Chain Light Clients, `pg-dregg`, `fhir` & Polisware Diaspora (50 KB)",
        raw_dossier_file="strands/19-breadstuffs-federation-chains-commons-diaspora.md",
    )
    deos_8f = render_markdown_to_monograph(
        read_lines("strands/22-obend-language-astra-equirec-and-ltuo.md", 1),
        prefix="deos-obend-lang",
        dossier_badge="Dossier 22 · Objective Bend (`obend`) Language, LTUO (`fareoo`), Equi-Recursive Bisimulation, Astra Effect Laws & 11 Spine Modules (86 KB)",
        raw_dossier_file="strands/22-obend-language-astra-equirec-and-ltuo.md",
    )
    deos_8g = render_markdown_to_monograph(
        read_lines("strands/23-minidregg-lanes-claudesplosion-drorb-dreggcloud.md", 1),
        prefix="deos-mini-lanes",
        dossier_badge="Dossier 23 · Direct Source Re-Scout: `minidregg-lanes` (273 Entries), `claudesplosion` (67 Lanes), `nanodregg-scout` (27 Scouts), `delvetalk2-lanes` (66 Entries), `drorb` & `DreggCloud` (110 KB)",
        raw_dossier_file="strands/23-minidregg-lanes-claudesplosion-drorb-dreggcloud.md",
    )

    deos_panels = f"""
    <section id="tab-deos-deep" class="tab-panel active" role="tabpanel">{deos_8a}</section>
    <section id="tab-bs-kernel" class="tab-panel" role="tabpanel">{deos_8b}</section>
    <section id="tab-bs-ui" class="tab-panel" role="tabpanel">{deos_8c}</section>
    <section id="tab-bs-worlds" class="tab-panel" role="tabpanel">{deos_8d}</section>
    <section id="tab-bs-fed" class="tab-panel" role="tabpanel">{deos_8e}</section>
    <section id="tab-obend-lang" class="tab-panel" role="tabpanel">{deos_8f}</section>
    <section id="tab-mini-lanes" class="tab-panel" role="tabpanel">{deos_8g}</section>
    """
    deos_html = page_shell(
        "deos.html",
        "08 · DeOS, MiniDregg, NanoDregg, DelveTalk, OBend Language & Breadstuffs Diaspora Monograph — whatember",
        "Complete primary-source monograph covering DeOS, MiniDregg (273 lanes), NanoDregg (27 scouts), DelveTalk2 (66 lanes), Objective Bend (obend language & equirecursive types), Drorb, DreggCloud, and the 4-part Breadstuffs Diaspora.",
        hero_deos,
        [
            ("tab-deos-deep", "8A · DeOS, MiniDregg, NanoDregg, DelveTalk & Preoscript Overview"),
            ("tab-bs-kernel", "8B · Breadstuffs Kernel, Circuits & Crypto Diaspora (`dregg-*`, `fhegg-*`, `uc-crypthol`)"),
            ("tab-bs-ui", "8C · Breadstuffs DeOS Surfaces, Starbridge (32 Apps) & Moldable Inspector"),
            ("tab-bs-worlds", "8D · Breadstuffs DreggNet, Worlds, Games (`dungeon-on-dregg`) & PoA"),
            ("tab-bs-fed", "8E · Breadstuffs Federation, Light Clients, `pg-dregg`, `fhir` & Polisware"),
            ("tab-obend-lang", "8F · Objective Bend (`obend`) Language, Equi-Recursive Types, Astra & LTUO (`fareoo`)"),
            ("tab-mini-lanes", "8G · `minidregg-lanes` (273), `claudesplosion` (67), `nanodregg-scout`, `delvetalk2-lanes`, `drorb` & `DreggCloud`"),
        ],
        deos_panels,
        "08 · DeOS, MiniDregg, NanoDregg, DelveTalk, OBend Language & Breadstuffs Diaspora (Full Dossiers 09, 16–19, 22–23 · 474 KB)",
    )
    with open(os.path.join(ROOT, "deos.html"), "w", encoding="utf-8") as f:
        f.write(deos_html)

    # 9. Build VERTICALS.HTML (Dossiers 10..14 + Direct Source Re-Scouts 20, 21, 24, 25, 26 — ~850 KB of primary sources)
    hero_vert = """
  <section class="hero">
    <div class="wrap">
      <div class="eyebrow">09 · All Other Verticals Across <code>~/dev</code> (Direct Source Excavations)</div>
      <h1>Cognitive Learning, Formal Organs (<code>clairnets</code>), <em>Drosophila</em> Connectomes (<code>chreatures</code>), Markets (<code>dragons-clutch</code>/<code>dclutch</code>), Verified Minds (<code>fn</code>/<code>stella</code>/<code>h</code>) &amp; Physics/Audio (<code>spindle</code>/<code>audec</code>)</h1>
      <p class="lead">
        Unabridged primary-source monographs across ten complete engineering and research verticals excavated directly from source repositories: <strong>Cognitive Learning &amp; EKOS</strong> (<code>abcdeez</code>, <code>verekos</code>), <strong>Custom RISC ISAs &amp; Math</strong> (<code>absass</code>, <code>intmat2</code>, <code>graphplay</code>, <code>birkhoff-asa</code>), <strong>Checked Neural Deduction &amp; Seam Weaving</strong> (<code>clairnets</code>/GLaDOS, <code>leanuweave</code>), <strong><em>Drosophila</em> Connectome Embodiment &amp; Physiology</strong> (<code>chreatures</code>, <code>brorb</code>, <code>luteastress</code>, <code>febart</code>), <strong>Markets &amp; Mechanism Design</strong> (<code>dragons-clutch</code>, <code>dclutch</code>, all 10 <code>degg-research</code> experiments, <code>passwap</code>, <code>joshibot</code>), <strong>Formal Minds &amp; Interpretability</strong> (<code>fn</code>/<code>fn2</code>, <code>veri7vn</code>, <code>stella</code>, <code>h ghost</code>, <code>mediateor</code>), and <strong>Rotating-Frame Sports, Games, Audio &amp; Nuclear Physics</strong> (<code>spindle</code>, <code>don</code>, <code>blackwing</code>, <code>resequence-rs</code>, <code>audec</code>, <code>kitforge</code>, <code>vidbox</code>, <code>plymouth-rock</code>).
      </p>
    </div>
  </section>"""

    vert_9a = render_markdown_to_monograph(
        read_lines("strands/10-cognitive-learning-abcdeez-factshift-ekos.md", 1),
        prefix="vert-cog",
        dossier_badge="Dossier 10 · Cognitive Learning, Adaptive Spaced Repetition, Spw & Verified EKOS (`abcdeez`, `factshift`, `EKOS` · 78 KB)",
        raw_dossier_file="strands/10-cognitive-learning-abcdeez-factshift-ekos.md",
    )
    vert_9b = render_markdown_to_monograph(
        read_lines("strands/11-isa-compilers-physics-math-substrates.md", 1),
        prefix="vert-isa",
        dossier_badge="Dossier 11 · Custom RISC ISAs (`absass`), Living Materials (`intmat2`), Quantum Walks (`graphplay`) & Proof Complexity (`birkhoff-asa` · 86 KB)",
        raw_dossier_file="strands/11-isa-compilers-physics-math-substrates.md",
    )
    vert_9c = render_markdown_to_monograph(
        read_lines("strands/12-markets-dclutch-solana-joshi-mina-zk.md", 1),
        prefix="vert-mkt",
        dossier_badge="Dossier 12 · Markets, Auction Engines, Solana/DEX Systems & Mina ZK (`dclutch`, `joshi`, `ltshitcoims`, OpenMina/Snarky · 77 KB)",
        raw_dossier_file="strands/12-markets-dclutch-solana-joshi-mina-zk.md",
    )
    vert_9d = render_markdown_to_monograph(
        read_lines("strands/13-residents-bots-games-worlds-audec.md", 1),
        prefix="vert-res",
        dossier_badge="Dossier 13 · Resident Minds (`allgame`, `tulip`), Verified World Engines (`fn`, `don`, `automatafl`) & Audio (`audec`, `kitforge` · 85 KB)",
        raw_dossier_file="strands/13-residents-bots-games-worlds-audec.md",
    )
    vert_9e = render_markdown_to_monograph(
        read_lines("strands/14-interiority-bridge-interpretability-organisms.md", 1),
        prefix="vert-int",
        dossier_badge="Dossier 14 · Machine Interiority, The Bridge (`comp-theo`), Interpretability (`gowexp`, `negneg`, `h`) & Model Organisms (`negstab`, `formal-organisms` · 87 KB)",
        raw_dossier_file="strands/14-interiority-bridge-interpretability-organisms.md",
    )
    vert_9f = render_markdown_to_monograph(
        read_lines("strands/20-clairnets-glados-leanuweave-birkhoff-formal-organs.md", 1),
        prefix="vert-clairnets",
        dossier_badge="Dossier 20 · Direct Source Re-Scout: `clairnets` (GLaDOS 4-Leg LDT), `leanuweave` (Seam Solver), `birkhoff-asa` (`asagolf`), `navier-stokes-proof` & `ergolang` (105 KB)",
        raw_dossier_file="strands/20-clairnets-glados-leanuweave-birkhoff-formal-organs.md",
    )
    vert_9g = render_markdown_to_monograph(
        read_lines("strands/21-chreatures-drosophila-connectome-and-physiology.md", 1),
        prefix="vert-chreatures",
        dossier_badge="Dossier 21 · Direct Source Re-Scout: `chreatures` (165K-Neuron MaleCNS v1.0 Drosophila Connectome & 12 Native Crates), `brorb`, `luteastress` & `febart` (84 KB)",
        raw_dossier_file="strands/21-chreatures-drosophila-connectome-and-physiology.md",
    )
    vert_9h = render_markdown_to_monograph(
        read_lines("strands/24-dragons-clutch-dclutch-degg-research-deep-rescout.md", 1),
        prefix="vert-dclutch-deep",
        dossier_badge="Dossier 24 · Direct Source Re-Scout: `dragons-clutch` (11,176 Commits), `dclutch` (6,864 Commits, 256 Lean 4 Files), All 10 `degg-research` Experiments & `passwap` (74 KB)",
        raw_dossier_file="strands/24-dragons-clutch-dclutch-degg-research-deep-rescout.md",
    )
    vert_9i = render_markdown_to_monograph(
        read_lines("strands/25-fn-veri7vn-stella-h-ghost-and-mechinterp-rescout.md", 1),
        prefix="vert-fn-stella-h",
        dossier_badge="Dossier 25 · Direct Source Re-Scout: `fn` (18,807 Commits, 652K LOC ACL2) & `fn2`, `veri7vn` (`o7vn`), `stella` (252 Commits), `h ghost` (268 Commits) & `mediateor` (79 KB)",
        raw_dossier_file="strands/25-fn-veri7vn-stella-h-ghost-and-mechinterp-rescout.md",
    )
    vert_9j = render_markdown_to_monograph(
        read_lines("strands/26-spindle-blackwing-audec-vidbox-physics-and-games-rescout.md", 1),
        prefix="vert-spindle-audec",
        dossier_badge="Dossier 26 · Direct Source Re-Scout: `spindle` (`RIG`), `don` (`DataWalk` & `i686` Oracle), `blackwing`, `resequence-rs`, `audec`, `kitforge`, `vidbox` & `plymouth-rock` (96 KB)",
        raw_dossier_file="strands/26-spindle-blackwing-audec-vidbox-physics-and-games-rescout.md",
    )

    verticals_panels = f"""
    <section id="tab-cog" class="tab-panel active" role="tabpanel">{vert_9a}</section>
    <section id="tab-isa" class="tab-panel" role="tabpanel">{vert_9b}</section>
    <section id="tab-mkt" class="tab-panel" role="tabpanel">{vert_9c}</section>
    <section id="tab-res" class="tab-panel" role="tabpanel">{vert_9d}</section>
    <section id="tab-int" class="tab-panel" role="tabpanel">{vert_9e}</section>
    <section id="tab-clairnets" class="tab-panel" role="tabpanel">{vert_9f}</section>
    <section id="tab-chreatures" class="tab-panel" role="tabpanel">{vert_9g}</section>
    <section id="tab-dclutch-deep" class="tab-panel" role="tabpanel">{vert_9h}</section>
    <section id="tab-fn-stella-h" class="tab-panel" role="tabpanel">{vert_9i}</section>
    <section id="tab-spindle-audec" class="tab-panel" role="tabpanel">{vert_9j}</section>
    """
    verticals_html = page_shell(
        "verticals.html",
        "09 · All Verticals: Cognitive Learning, Formal Organs, Connectomes, Markets, Verified Minds & Physics Monograph — whatember",
        "Complete primary-source monographs across Cognitive Learning (abcdeez/verekos), ISAs/Math (absass/intmat2/graphplay), Formal Organs (clairnets/leanuweave/birkhoff-asa), Drosophila Connectomes (chreatures/brorb), Markets (dragons-clutch/dclutch/degg-research), Formal Minds (fn/veri7vn/stella/h), and Physics/Audio/Games (spindle/don/audec/kitforge/vidbox/plymouth-rock).",
        hero_vert,
        [
            ("tab-cog", "9A · Cognitive Learning & EKOS (`abcdeez`, `factshift`, `EKOS`, `verekos`)"),
            ("tab-isa", "9B · Custom ISAs, Living Matter & Quantum Walks (`absass`, `intmat2`, `graphplay`)"),
            ("tab-mkt", "9C · Markets, Auctions & Mina ZK Overview (`dclutch`, `joshi`, Mina)"),
            ("tab-res", "9D · Resident Minds, Bots, Games & Audio Overview (`allgame`, `tulip`, `fn`, `don`, `audec`)"),
            ("tab-int", "9E · Machine Interiority, Interpretability & Organisms (`comp-theo`, `gowexp`, `negneg`, `negstab`)"),
            ("tab-clairnets", "9F · Deep Re-Scout: `clairnets` (GLaDOS), `leanuweave`, `birkhoff-asa` (`asagolf`) & `ergolang`"),
            ("tab-chreatures", "9G · Deep Re-Scout: `chreatures` (165K-Neuron Drosophila Connectome), `brorb`, `luteastress` & `febart`"),
            ("tab-dclutch-deep", "9H · Deep Re-Scout: `dragons-clutch` (11K Commits), `dclutch` (64K LOC Lean 4) & 10 `degg-research` Exps"),
            ("tab-fn-stella-h", "9I · Deep Re-Scout: `fn` (652K LOC ACL2) & `fn2`, `veri7vn`, `stella` (252 Commits), `h ghost` & `mediateor`"),
            ("tab-spindle-audec", "9J · Deep Re-Scout: `spindle` (`RIG`), `don`, `blackwing`, `resequence-rs`, `audec`, `kitforge`, `vidbox` & `plymouth-rock`"),
        ],
        verticals_panels,
        "09 · All Other Verticals Across ~/dev (Full Dossiers 10–14, 20–21, 24–26 · 851 KB)",
    )
    with open(os.path.join(ROOT, "verticals.html"), "w", encoding="utf-8") as f:
        f.write(verticals_html)

    # 10. Build TRIAGE.HTML (Dossier 15 + Direct Source Re-Scout Dossier 27 — ~190 KB)
    hero_tri = """
  <section class="hero">
    <div class="wrap">
      <div class="eyebrow">10 · Swarm Metamanagement, <code>cv</code>/<code>wesvet</code> Empirical Science, <code>breadstuffs/docs</code> (252 Docs) &amp; Triage</div>
      <h1>How to Metamanage Multi-Wave Swarms (<code>cv</code>, <code>wesvet</code>, <code>redregg</code>), Relative Maturities (<code>L0</code>–<code>L4</code>), Unclosed Cycles (<code>C1</code>–<code>C15</code>) &amp; Revival/Triage Queues</h1>
      <p class="lead">
        Empirical synthesis from <strong>3,852 commits of <code>cv</code></strong> (OpenSession 0.3 IR, <code>&gt;3,000×</code> JSONL heap cut, <code>cv prune</code> &amp; <code>cv distill</code>), the <strong><code>wesvet</code> ("Veterans at the Front") study</strong> across 156 successions (<code>sharpen.py</code> <strong>98.6% recall</strong> at <code>-63.1%</code> tokens; 22.3M tokens lost to 350K park wakes), <code>redregg/cxo</code> (34.0M $\to$ 0.3M build-wait tokens), the <strong>252 internal design/audit documents of <code>breadstuffs/docs</code></strong>, the <strong>Maturity Matrix</strong>, <strong>15 Unclosed Cycles</strong>, <strong>Top 15 Revival Queue</strong>, and <strong>15 Needs-Ember Blockers</strong>.
      </p>
    </div>
  </section>"""

    tri_10a = render_markdown_to_monograph(
        read_lines("strands/15-metamanagement-open-cycles-revival-triage.md", 1, 450),
        prefix="tri-manual",
        dossier_badge="Dossier 15 (§0–§1) · Swarm Metamanagement Manual (`cv`, `tokeman`, `mission-control` → `cv task`, `board/seats`, Rules M1–M8)",
        raw_dossier_file="strands/15-metamanagement-open-cycles-revival-triage.md",
    )
    tri_10b = render_markdown_to_monograph(
        read_lines("strands/15-metamanagement-open-cycles-revival-triage.md", 451, 594),
        prefix="tri-matrix",
        dossier_badge="Dossier 15 (§2) · Master Portfolio Maturity & Lifecycle Matrix (`L0`–`L4`, `Frozen-for-Rethink`, `Compost/Superseded`)",
        raw_dossier_file="strands/15-metamanagement-open-cycles-revival-triage.md",
    )
    tri_10c = render_markdown_to_monograph(
        read_lines("strands/15-metamanagement-open-cycles-revival-triage.md", 595, 717),
        prefix="tri-cycles",
        dossier_badge="Dossier 15 (§3) · Unclosed Cycles (`C1`–`C15`): Exact Blockers, Closure Pathways & Next-Move Owners",
        raw_dossier_file="strands/15-metamanagement-open-cycles-revival-triage.md",
    )
    tri_10d = render_markdown_to_monograph(
        read_lines("strands/15-metamanagement-open-cycles-revival-triage.md", 718),
        prefix="tri-revival",
        dossier_badge="Dossier 15 (§4–§5 & Appendices) · High-Leverage Revival Queue (`#1`–`#15`), Needs-Ember Triage (`H1`–`H15`) & Key Numbers",
        raw_dossier_file="strands/15-metamanagement-open-cycles-revival-triage.md",
    )
    tri_10e = render_markdown_to_monograph(
        read_lines("strands/27-cv-wesvet-breadstuffs-253-docs-and-swarm-science-rescout.md", 1),
        prefix="tri-cv-wesvet",
        dossier_badge="Dossier 27 · Direct Source Re-Scout: `cv` (3,852 Commits, OpenSession 0.3, `>3,000×` Heap Cut), `wesvet` (Veterans at the Front), `redregg`/`cxo`, `phoenix` & All 252 `breadstuffs/docs` Entries (103 KB)",
        raw_dossier_file="strands/27-cv-wesvet-breadstuffs-253-docs-and-swarm-science-rescout.md",
    )

    triage_panels = f"""
    <section id="tab-manual" class="tab-panel active" role="tabpanel">{tri_10a}</section>
    <section id="tab-maturity" class="tab-panel" role="tabpanel">{tri_10b}</section>
    <section id="tab-cycles" class="tab-panel" role="tabpanel">{tri_10c}</section>
    <section id="tab-revival" class="tab-panel" role="tabpanel">{tri_10d}</section>
    <section id="tab-cv-wesvet" class="tab-panel" role="tabpanel">{tri_10e}</section>
    """
    triage_html = page_shell(
        "triage.html",
        "10 · Swarm Metamanagement, cv/wesvet Science, breadstuffs/docs (252 Docs) & Human Triage Monograph — whatember",
        "Complete primary-source metamanagement manual, cv (3,852 commits) & wesvet empirical swarm science, 252 breadstuffs/docs design excavations, portfolio maturity matrix, 15 unclosed cycles (C1-C15), top 15 revival candidates, and 15 human-attention blockers (H1-H15).",
        hero_tri,
        [
            ("tab-manual", "10A · Swarm Metamanagement Manual (`cv`, `tokeman`, `board/seats`, Rules M1–M8)"),
            ("tab-maturity", "10B · Master Portfolio Maturity Matrix (`L0`–`L4`, `Frozen`, `Compost`)"),
            ("tab-cycles", "10C · Unclosed Cycles (`C1`–`C15`) & Closure Pathway Map"),
            ("tab-revival", "10D · Top 15 Revival Queue (`#1`–`#15`) & Needs-Ember Triage (`H1`–`H15`)"),
            ("tab-cv-wesvet", "10E · Deep Re-Scout: `cv` (3,852 Commits), `wesvet` (Veterans), `redregg`/`cxo` & 252 `breadstuffs/docs`"),
        ],
        triage_panels,
        "10 · Swarm Metamanagement, cv/wesvet Science, breadstuffs/docs & Human Triage (Full Dossiers 15 & 27 · 190 KB)",
    )
    with open(os.path.join(ROOT, "triage.html"), "w", encoding="utf-8") as f:
        f.write(triage_html)

    print("Successfully compiled all 10 HTML monograph pages across all 27 dossiers!")


if __name__ == "__main__":
    build_all()
