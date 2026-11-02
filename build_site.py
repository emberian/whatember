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
    "dregg-microsites": "https://github.com/emberian/dregg-microsites/blob/main/",
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
        out.append(
            f'<div class="callout" style="margin-top:0;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">'
            f'<div><div class="callout-title">{html.escape(dossier_badge)}</div>'
            f'<div>Complete primary-source monograph rendered inline below, with verbatim theorem statements, code blocks, git commit tables, and <code>cv</code> session transcripts.</div></div>'
            f'<div style="display:flex;gap:8px;"><a class="btn btn-primary" href="https://github.com/emberian/whatember/blob/main/sources/{html.escape(raw_dossier_file)}" target="_blank" rel="noopener">View on GitHub ↗</a>'
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
        <small>Verifiable Systems Monograph · Nov 2026</small>
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
        All claims anchored to primary-source git commits, zero-<code>sorry</code> Lean 4 / HOL4 / ACL2 / Isabelle theorems, and reproducible benchmarks.
      </div>
      <div>
        <a href="https://github.com/emberian/whatember">GitHub Repo</a> ·
        <a href="https://emberian.github.io/dregg-microsites/">Dregg Microsites</a> ·
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
    matrix_inner = m_mat.group(1) if m_mat else ""
    m_quinn = re.search(r'<section id="tab-quinn"[^>]*>(.*?)</section>', old_index, re.S)
    quinn_inner = m_quinn.group(1) if m_quinn else ""

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
        dossier_badge="Executive Synthesis Across Dossiers 01, 02, 04 & 07",
        raw_dossier_file="01-parsing-query-aggregation-absence.md",
    )
    tab_1d_monograph = render_markdown_to_monograph(
        read_lines("08-october-november-2026-stratum.md", 1),
        prefix="idx-octnov",
        dossier_badge="Dossier 08 · Complete October–November 2026 Stratum (72 KB)",
        raw_dossier_file="08-october-november-2026-stratum.md",
    )

    m_hero_idx = re.search(r'(<section class="hero">.*?</section>)', old_index, re.S)
    hero_idx = m_hero_idx.group(1)
    m_exec_cards = re.search(r'<section id="tab-exec"[^>]*>(.*?)</section>', old_index, re.S)
    exec_cards_html = m_exec_cards.group(1) if m_exec_cards else ""

    index_panels = f"""
    <section id="tab-exec" class="tab-panel active" role="tabpanel">
      {exec_cards_html}
      <hr style="margin:42px 0;border:0;border-top:2px solid var(--line);" />
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
    """
    index_html = page_shell(
        "index.html",
        "whatember — Verifiable Compute, Merkleized Agent Proxies & Formal Silicon Monograph",
        "Unabridged primary-source technical monograph and index of Ember's verifiable compute, training-set absence proofs, Merkleized agent proxies, multi-vendor TEEs, and Lean/HOL4/ACL2/Isabelle formal silicon systems.",
        hero_idx,
        [
            ("tab-exec", "1A · Architecture & Full-Stack Executive Monograph"),
            ("tab-matrix", "1B · Interactive Problem → Primitive → Proof Matrix"),
            ("tab-quinn", "1C · Briefing for Quinn & Lucid Computing"),
            ("tab-dossiers", "1D · Oct–Nov 2026 Stratum (svenvs, verekos, o7vn, fn2)"),
        ],
        index_panels,
        "01 · Overview & Full-Stack Executive Monograph",
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

    # 6. Build VISION.HTML (Full Sections 1–4 of Dossier 06 + Model Organisms/intmat/eshkol from Dossier 08 — ~95 KB)
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
        dossier_badge="Dossier 08 (§3, §4, §6) · `intmat`/`intmat2`, `negstab`, `formal-organisms`, `acl2aiguide` (23 `fn` Wound Lessons), `eshkol` & `torchship`",
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
        "Complete primary-source monograph tracing the 13-year trajectory from pre-1.0 Rust and NICTA/UNSW seL4 to O(1) Labs Mina, Elide, and Dregg/OBend, plus redregg swarm methodology and model organisms.",
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
    at_repos_filter = m_at_repos.group(1) if m_at_repos else ""
    m_at_papers = re.search(r'<section id="tab-papers"[^>]*>(.*?)</section>', old_at, re.S)
    at_papers_table = m_at_papers.group(1) if m_at_papers else ""

    at_7a_deep = render_markdown_to_monograph(
        read_lines("06-vision-origins-and-complete-project-atlas.md", 340, 459),
        prefix="at-repos-deep",
        dossier_badge="Dossier 06 (§5) · Complete Master Atlas Table & Verbatim Code / Theorem Signatures Across All Repositories",
        raw_dossier_file="06-vision-origins-and-complete-project-atlas.md",
    )
    at_7b_deep = render_markdown_to_monograph(
        read_lines("06-vision-origins-and-complete-project-atlas.md", 460, 509),
        prefix="at-microsites-deep",
        dossier_badge="Dossier 06 (§6.1–§6.2) · Complete `dregg-site` (`dregg.net`) & 19 `dregg-microsites` Visual Essay Atlas",
        raw_dossier_file="06-vision-origins-and-complete-project-atlas.md",
    )
    at_7c_deep = render_markdown_to_monograph(
        read_lines("06-vision-origins-and-complete-project-atlas.md", 510),
        prefix="at-posters-deep",
        dossier_badge="Dossier 06 (§6.3) · Complete `dregg-posters` Archive: Bilingual Typst Suites, HTML Broadsides & All 49 ASCII Posters",
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
        "07 · Searchable Master Atlas: 38+ Repos, 19 Microsites, 65+ Posters & Theorem Signatures — whatember",
        "Complete searchable index and primary-source theorem/code signature atlas of Ember's 38+ repositories, 19 interactive visual essays, 65+ technical posters, and 8 source dossiers.",
        hero_at,
        [
            ("tab-repos", "7A · 38+ Repositories & Primary-Source Code/Theorem Signatures"),
            ("tab-microsites", "7B · `dregg.net` & All 19 Interactive Microsites (`dregg-microsites`)"),
            ("tab-posters", "7C · 65+ Posters: Typst EN/ZH Series, HTML Broadsides & 49 ASCII Posters"),
            ("tab-papers", "7D · All 8 Raw Primary-Source Dossiers (`sources/01..08`)"),
        ],
        atlas_panels,
        "07 · Searchable Master Atlas (Full Dossier 06 §5–§6 · 110 KB)",
    )
    with open(os.path.join(ROOT, "atlas.html"), "w", encoding="utf-8") as f:
        f.write(atlas_html)

    print("Successfully compiled all 7 HTML monograph pages!")


if __name__ == "__main__":
    build_all()
