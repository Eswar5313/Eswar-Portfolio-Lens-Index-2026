#!/usr/bin/env python3
"""Rebuild Eswar-Portfolio-Lens-Index-2026 as a COMPACT repo (≤ 10 files) with the 20 new Codec projects added.
Inputs: old lens_index.json (83 projects), /tmp/tracks.json (50 Codec cards), old CSS. Output: /home/claude/work/lens/."""
import json, re, csv, html, os, shutil
E = html.escape
HANDLE = "Eswar5313"; REPO = "Eswar-Portfolio-Lens-Index-2026"; MASTER = "Eswar-Master-Project-Portfolio-2026"
CODEC = "Codec-Technologies-Internship-Portfolio-2026"; OWNER = "Eswar Mahalingam"
GH = f"https://github.com/{HANDLE}"; PAGES = f"https://{HANDLE.lower()}.github.io/{REPO}"
OUT = "/home/claude/work/lens"; shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
old = json.load(open("/root/.claude/uploads/4ad55d60-1b47-5ed5-8770-d68a3d79de72/7e7875f7-lens_index.json"))
tracks = json.load(open("/tmp/tracks.json"))
LENSES = [(l["key"], l["name"], l["desc"]) for l in old["lenses"]]
projects = [p for p in old["projects"]]
for p in projects:
    for k in ("master_folder", "master_page"): p[k] = p[k].replace("YOUR-USERNAME", HANDLE)

# ---- update Codec EV + Cyber entries: real titles, links into the Codec portfolio repo
codec = {t["id"]: t for t in tracks}
cy = {c["num"]: c for c in codec["cyber"]["cards"]}; ev = {c["num"]: c for c in codec["ev"]["cards"]}
CODEC_TRACK = "Codec Technologies — 4 tracks (EV 10 · Cyber 20 · VLSI 10 · Robotics 10)"
for p in projects:
    m = re.match(r"04-Codec-Technologies-EV-and-Cyber/(EV|CYBER)-(\d\d)", p["id"])
    if not m: continue
    kind, n = m.groups(); c = (ev if kind == "EV" else cy)[n]; tf = "Electric-Vehicle" if kind == "EV" else "Cyber-Security"
    p["title"] = f"{'EV' if kind=='EV' else 'Cyber'} {n} — {c['title']}"; p["summary"] = c["desc"]
    p["result"] = c["metrics"][0][1] + " tests" if kind == "CYBER" else (p["result"] or c["metrics"][0][1] + " tests")
    p["tools"] = sorted(set(p["tools"]) | set(c["chips"][:3])) if kind == "EV" else ["Python"] + c["chips"][:2]
    p["track"] = CODEC_TRACK; p["source_track"] = [CODEC_TRACK]
    p["master_folder"] = f"{GH}/{CODEC}/blob/main/{tf}/reports/{c['folder']}.pdf"
    p["master_page"] = f"https://{HANDLE.lower()}.github.io/{CODEC}/#{'ev' if kind=='EV' else 'cyber'}-{n}"
    p["deliverable"] = sorted(set(p["deliverable"]) | {"PDF report", "Code / notebook"})
    if kind == "CYBER" and p["skills"] == ["Python programming", "Security analysis (defensive)"]:
        blob = (c["title"] + " " + c["desc"]).lower()
        if any(w in blob for w in ("classif", "randomforest", "ml", "isolation")): p["skills"].append("Machine learning"); p["method"].append("Classification (RandomForest etc.)")
        if any(w in blob for w in ("flask", "web", "platform", "portal")): p["skills"].append("Web development"); p["deliverable"].append("Web app / site")
        if "forensic" in blob or "memory" in blob: p["skills"].append("Technical writing & documentation")

# ---- add VLSI + Robotics (20 new)
def mk(tid, c, domain, skills, sector, roles, methods, tools_extra, prov):
    t = codec[tid]; n = c["num"]
    return dict(id=f"04-Codec-Technologies/{t['folder']}/{c['folder']}", title=f"{'VLSI' if tid=='vlsi' else 'Robotics'} {n} — {c['title']}", summary=c["desc"],
        result=" · ".join(f"{k} {v}" for k, v in c["metrics"][:2]), tools=c["chips"][:4] + tools_extra, tags=c["chips"], track=CODEC_TRACK,
        master_folder=f"{GH}/{CODEC}/blob/main/{t['folder']}/reports/{c['folder']}.pdf", master_page=f"https://{HANDLE.lower()}.github.io/{CODEC}/#{tid}-{n}",
        domain=[domain], skills=skills, sector=sector, role=roles, deliverable=["PDF report", "Code / notebook", "Simulation output (waveforms / GIF)"],
        method=methods, provenance=[prov], programme=["Codec Technologies India"], source_track=[CODEC_TRACK])
VL = {"01": (["FSM design", "Debounce & synchronisation"], "Own build (no external dataset)"), "02": (["Clock gating & operand isolation", "Activity-based power estimation"], "Own build (no external dataset)"),
      "03": (["FSM design", "Debounce & synchronisation"], "Own build (no external dataset)"), "04": (["Fixed-point Q1.15 DSP", "Pipelining / transposed FIR"], "Own build (no external dataset)"),
      "05": (["FSM design", "16× oversampling UART"], "Own build (no external dataset)"), "06": (["Fixed-point Q1.15 DSP", "AT-command state machine"], "Declared-synthetic / substituted data"),
      "07": (["Golden-model verification", "Custom ISA / micro-op FSM"], "Own build (no external dataset)"), "08": (["RTL-to-GDSII (SA placement, maze routing)", "Static timing analysis"], "Own build (no external dataset)"),
      "09": (["Clock gating & operand isolation", "Register-mapped UART command interface"], "Declared-synthetic / substituted data"), "10": (["FSM design", "CRC-8 + I²C EEPROM write-verify"], "Own build (no external dataset)")}
RB = {"01": (["A* / Dijkstra path planning", "Pure-pursuit control"], "Declared-synthetic / substituted data"), "02": (["Classification (RandomForest etc.)", "Inverse kinematics (DLS / analytic)"], "Declared-synthetic / substituted data"),
      "03": (["MFCC + DTW keyword recognition", "Intent / slot parsing"], "Declared-synthetic / substituted data"), "04": (["Cascaded PID control", "Kalman / complementary filtering"], "Own build (no external dataset)"),
      "05": (["Background subtraction (MOG2) + HOG", "Waypoint navigation (WGS84 → ENU)"], "Declared-synthetic / substituted data"), "06": (["Vegetation indices (ExG / VARI / NDVI)", "Hysteresis irrigation control"], "Declared-synthetic / substituted data"),
      "07": (["Convexity-defect gesture recognition", "Levenberg–Marquardt inverse kinematics"], "Declared-synthetic / substituted data"), "08": (["Log-odds SLAM + scan matching / ICP", "Frontier exploration", "TDOA bearing estimation"], "Own build (no external dataset)"),
      "09": (["Discrete-event simulation", "Slot allocation strategies", "SAT collision checking"], "Declared-synthetic / substituted data"), "10": (["Colour / shape classification (Hu moments)", "Discrete-event simulation"], "Declared-synthetic / substituted data")}
for c in codec["vlsi"]["cards"]:
    m, prov = VL[c["num"]]
    projects.append(mk("vlsi", c, "Digital Electronics & VLSI", ["Digital design & RTL (Verilog/VHDL)", "FPGA synthesis, place-and-route & timing", "Verification (self-checking testbenches)", "Simulation & modelling", "Technical writing & documentation"],
        ["Semiconductors & Embedded (VLSI / FPGA)"] + (["Automotive & Electric Vehicles"] if c["num"] == "06" else []) + (["Construction & Infrastructure"] if c["num"] == "01" else []),
        ["Digital Design / FPGA Engineer", "EV / Embedded / Electrical Engineer", "QA / Test Engineer"], m, ["Icarus Verilog", "Yosys", "nextpnr-ice40"], prov))
for c in codec["robo"]["cards"]:
    m, prov = RB[c["num"]]
    projects.append(mk("robo", c, "Robotics & Automation", ["Robotics algorithms (planning, control, SLAM, kinematics)", "Python programming", "Machine learning" if c["num"] in ("02", "06") else "Simulation & modelling", "Software testing & QA", "Technical writing & documentation"],
        ["Robotics & Industrial Automation"] + (["Logistics & Supply Chain"] if c["num"] in ("01", "10") else []) + (["Manufacturing, Energy & Utilities"] if c["num"] in ("02", "10") else []) + (["Automotive & Electric Vehicles"] if c["num"] == "09" else []),
        ["Robotics / Automation Engineer", "Data Scientist / ML Engineer", "Software / Web Developer"] + (["Supply Chain / Operations Manager"] if c["num"] in ("01", "09", "10") else []), m, ["OpenCV", "NumPy/SciPy", "ROS 2 (pkg)"], prov))
N = len(projects); assert N == 103, N
vals = {k: sorted({v for r in projects for v in r[k]}) for k, _, _ in LENSES}
json.dump(dict(repo=REPO, master=MASTER, codec=CODEC, total=N, lenses=[dict(key=k, name=n, desc=d, values=vals[k]) for k, n, d in LENSES], projects=projects), open(f"{OUT}/lens_index.json", "w"), indent=1, ensure_ascii=False)
with open(f"{OUT}/project_lens_matrix.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["id", "title", "track", "evidence"] + [n for _, n, _ in LENSES])
    for r in projects: w.writerow([r["id"], r["title"], r["track"], r["master_folder"]] + ["; ".join(r[k]) for k, _, _ in LENSES])

CSS = open("/tmp/lens_css.txt").read() + """
.lens{display:flex;flex-wrap:wrap;gap:8px}.grp{margin:26px 0;scroll-margin-top:90px}.grp h2{font-size:22px;color:var(--navy);border-left:5px solid var(--gold);padding-left:12px;margin-bottom:12px}.grp .n{font-size:13px;color:var(--muted);font-weight:400;margin-left:8px}
.card .meta{font-size:11.5px;color:var(--muted)}.card .links{display:flex;gap:6px;margin-top:8px;flex-wrap:wrap}.card .links a{font-size:11.5px;font-weight:600;padding:4px 9px;border-radius:5px;background:var(--navy);color:#fff}.card .links a.alt{background:#fff;color:var(--navy);border:1px solid var(--navy)}
.new{display:inline-block;background:var(--gold);color:var(--navy);font-size:10px;font-weight:700;border-radius:4px;padding:1px 6px;margin-left:6px;vertical-align:middle}
.vals{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 4px}.vals a{font-size:12px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:3px 10px}.vals a:hover{border-color:var(--gold)}
.matrix{overflow-x:auto}.matrix table{border-collapse:collapse;font-size:12.5px;width:100%}.matrix th,.matrix td{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top;background:#fff}.matrix th{background:var(--navy);color:#fff;position:sticky;top:0}"""
FONTS = '<link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">'
def page(title, body): return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title>{FONTS}<style>{CSS}</style></head><body>{body}
<div class="foot"><div class="wrap">© 2026 {OWNER} · Lens index over the <a href="{GH}/{MASTER}">Master Project Portfolio</a> and the <a href="{GH}/{CODEC}">Codec Technologies Internship Portfolio</a> — every card links to the evidence file.</div></div></body></html>"""

chips = "".join(f'<button class="chip{" on" if i==0 else ""}" data-lens="{k}">{E(n)}</button>' for i, (k, n, _) in enumerate(LENSES))
new_ids = [p["id"] for p in projects if p["id"].startswith("04-Codec-Technologies/")]
root = f"""<header class="top"><div class="wrap"><div class="crumb">Portfolio Lens Index · 2026</div><h1>{OWNER} — Portfolio by Domain, Skills, Tools &amp; Sector</h1>
<p class="lead">{N} projects re-indexed through {len(LENSES)} lenses so a hiring manager can start from what they are hiring for — a skill, a tool, an industry, a role — and land on the evidence in two clicks. <span class="new">NEW</span> 20 Digital Electronics &amp; VLSI and Robotics &amp; Automation projects added Sep 2026.</p>
<div class="kpis"><div class="kpi"><b>{N}</b><span>Projects</span></div><div class="kpi"><b>{len(LENSES)}</b><span>Lenses</span></div><div class="kpi"><b>{len(vals['skills'])}</b><span>Skills</span></div><div class="kpi"><b>{len(vals['tools'])}</b><span>Tools</span></div><div class="kpi"><b>{len(vals['sector'])}</b><span>Sectors</span></div><div class="kpi"><b>{len(vals['role'])}</b><span>Target roles</span></div><div class="kpi"><b>{len(vals['method'])}</b><span>Methods</span></div></div>
<div class="btnrow"><a class="btn" href="{GH}/{MASTER}">Master repository (files)</a><a class="btn" href="{GH}/{CODEC}">Codec portfolio (50 engineering projects)</a><a class="btn ghost" href="README.md">README</a><a class="btn ghost" href="matrix.html">Full matrix</a></div></div></header>
<div class="bar"><div class="wrap"><input id="q" type="search" placeholder="Search a skill, tool, sector, method, role…"><div class="lens">{chips}</div><span style="font-size:13px;color:var(--muted)">Showing <b id="count"></b> · <a href="#" id="clear">clear value filter</a></span></div></div>
<main><div class="wrap"><div class="vals" id="vals"></div><div id="root"></div></div></main>
<script>const DATA={json.dumps(projects, ensure_ascii=False)};const LENSES={json.dumps([[k, n] for k, n, _ in LENSES])};const NEW=new Set({json.dumps(new_ids)});
const slug=s=>s.replace(/[^A-Za-z0-9]+/g,'-').replace(/^-|-$/g,'');
let lens='domain',val='';const q=document.getElementById('q');
function card(r){{return `<article class="card"><div class="id">${{r.track.split(' — ')[0]}}${{NEW.has(r.id)?'<span class="new">NEW</span>':''}}</div><h3>${{r.title}}</h3><p>${{r.summary}}</p>${{r.result?`<div class="res">▸ ${{r.result}}</div>`:''}}<div class="meta">${{r.sector.join(' · ')}}</div><div class="tags">${{r.tools.slice(0,5).map(t=>`<span>${{t}}</span>`).join('')}}</div><div class="links"><a href="${{r.master_folder}}">Evidence</a><a class="alt" href="${{r.master_page}}">Page</a></div></article>`}}
function render(){{const s=q.value.trim().toLowerCase();const groups={{}};let shown=0;
DATA.forEach(r=>{{const blob=(r.title+' '+r.summary+' '+r.tools.join(' ')+' '+LENSES.map(l=>r[l[0]].join(' ')).join(' ')).toLowerCase();if(s&&!blob.includes(s))return;const vs=r[lens].length?r[lens]:['(unclassified)'];if(val&&!vs.includes(val))return;shown++;vs.forEach(v=>{{if(val&&v!==val)return;(groups[v]=groups[v]||[]).push(r)}})}});
const all={{}};DATA.forEach(r=>(r[lens].length?r[lens]:['(unclassified)']).forEach(v=>all[v]=(all[v]||0)+1));
document.getElementById('vals').innerHTML=Object.keys(all).sort((a,b)=>all[b]-all[a]||a.localeCompare(b)).map(v=>`<a href="#${{lens}}/${{slug(v)}}" style="${{v===val?'background:var(--navy);color:#fff':''}}">${{v}} <b>${{all[v]}}</b></a>`).join('');
const keys=Object.keys(groups).sort((a,b)=>groups[b].length-groups[a].length||a.localeCompare(b));
document.getElementById('root').innerHTML=keys.length?keys.map(k=>`<section class="grp" id="g-${{slug(k)}}"><h2>${{k}}<span class="n">${{groups[k].length}} project${{groups[k].length>1?'s':''}}</span></h2><div class="grid">${{groups[k].map(card).join('')}}</div></section>`).join(''):'<div class="empty">No projects match.</div>';
document.getElementById('count').textContent=shown;document.querySelectorAll('.chip').forEach(x=>x.classList.toggle('on',x.dataset.lens===lens));}}
function route(){{const h=decodeURIComponent(location.hash.slice(1));if(!h){{val='';render();return}}const [l,v]=h.split('/');if(LENSES.some(x=>x[0]===l)){{lens=l;val='';if(v){{const all=new Set();DATA.forEach(r=>r[l].forEach(x=>all.add(x)));all.forEach(x=>{{if(slug(x)===v)val=x}})}}}}render();}}
document.querySelectorAll('.chip').forEach(b=>b.onclick=()=>{{location.hash='#'+b.dataset.lens}});document.getElementById('clear').onclick=e=>{{e.preventDefault();location.hash='#'+lens}};q.oninput=render;addEventListener('hashchange',route);route();</script>"""
open(f"{OUT}/index.html", "w").write(page(f"{OWNER} — Portfolio Lens Index", root)); open(f"{OUT}/.nojekyll", "w").write("")

th = "".join(f"<th>{E(n)}</th>" for _, n, _ in LENSES)
rows = "".join(f"<tr><td><a href='{r['master_folder']}'><b>{E(r['title'])}</b></a></td>" + "".join(f"<td>{E('; '.join(r[k]))}</td>" for k, _, _ in LENSES) + "</tr>" for r in projects)
open(f"{OUT}/matrix.html", "w").write(page("Project × Lens matrix", f"""<header class="top"><div class="wrap"><div class="crumb"><a href="index.html">← Lens dashboard</a></div><h1>Project × Lens matrix</h1><p class="lead">All {N} projects against all {len(LENSES)} lenses. Also available as <code>project_lens_matrix.csv</code> and <code>lens_index.json</code>.</p></div></header><main><div class="wrap matrix"><table><thead><tr><th>Project</th>{th}</tr></thead><tbody>{rows}</tbody></table></div></main>"""))

# ---- README (compact: tables link to hash routes on the live page, not folders)
slug = lambda s: re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-")
def badge(l, m, c): return f"![](https://img.shields.io/badge/{l.replace(' ','%20').replace('-','--')}-{m.replace(' ','%20').replace('-','--')}-{c}?style=for-the-badge)"
R = [f"""<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:C9A227,50:132B5C,100:0A1F44&height=190&section=header&text=Eswar%20Mahalingam&fontSize=46&fontColor=ffffff&fontAlignY=38&desc=Portfolio%20Lens%20Index%20%E2%80%A2%20{N}%20projects%20%C3%97%20{len(LENSES)}%20lenses&descAlignY=60&descSize=17&descColor=E4C56A" width="100%"/>

{badge("Projects",str(N),"0A1F44")} {badge("Lenses",str(len(LENSES)),"C9A227")} {badge("Skills",str(len(vals['skills'])),"0A1F44")} {badge("Tools",str(len(vals['tools'])),"C9A227")} {badge("Sectors",str(len(vals['sector'])),"0A1F44")} {badge("Target roles",str(len(vals['role'])),"C9A227")} {badge("Methods",str(len(vals['method'])),"0A1F44")}

[![Live lens dashboard](https://img.shields.io/badge/%E2%96%B6%20OPEN%20LENS%20DASHBOARD-C9A227?style=for-the-badge)]({PAGES}/)
[![Master repo](https://img.shields.io/badge/Master%20repo-all%20files-0A1F44?style=for-the-badge&logo=github&logoColor=C9A227)]({GH}/{MASTER})
[![Codec portfolio](https://img.shields.io/badge/Codec%20portfolio-50%20engineering%20projects-0A1F44?style=for-the-badge&logo=github&logoColor=C9A227)]({GH}/{CODEC})
[![LinkedIn](https://img.shields.io/badge/LinkedIn-eswar--mahalingam-0A66C2?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/eswar-mahalingam)

</div>

> **Start from what you are hiring for.** Pick a lens — a skill, a tool, an industry, a target role, a method — and every project that proves it is listed with a direct link to its evidence (PDF report, workbook, deck or code). Data and analytics work lives in the [master repository]({GH}/{MASTER}); the 50 engineering and security projects live in the [Codec Technologies portfolio]({GH}/{CODEC}) with a report PDF each.

## 🆕 Recent additions (September 2026)

| Added | Projects | Where |
|---|:-:|---|
| Digital Electronics & VLSI track — Verilog/VHDL RTL, Yosys + nextpnr place-and-route, own RTL-to-GDSII flow | 10 | [{CODEC}/Digital-Electronics-VLSI]({GH}/{CODEC}/tree/main/Digital-Electronics-VLSI) |
| Robotics & Automation track — A*/SLAM/PID/Kalman/IK simulations with OpenCV | 10 | [{CODEC}/Robotics-Automation]({GH}/{CODEC}/tree/main/Robotics-Automation) |
| Engineering-report PDFs for all 50 Codec projects (EV 10 · Cyber 20 · VLSI 10 · Robotics 10) | 50 | [Codec portfolio dashboard](https://{HANDLE.lower()}.github.io/{CODEC}/) |

## 🔍 Choose a lens

Each value below is a live filter on the dashboard (`index.html#lens/value`).

<table>"""]
tiles = [f"""<td align="center" width="20%"><a href="{PAGES}/#{k}"><img src="https://img.shields.io/badge/{E(n).replace(' ','%20').replace('-','--').replace('&','%26').replace('/','%2F')}-{len(vals[k])}-C9A227?style=for-the-badge&labelColor=0A1F44"/></a><br><sub>{E(d)}</sub></td>""" for k, n, d in LENSES]
for i in range(0, len(tiles), 5): R.append("<tr>\n" + "\n".join(tiles[i:i+5]) + "\n</tr>")
R.append("</table>\n")
for k, n, d in LENSES:
    R.append(f"""<details{' open' if k in ('domain','skills') else ''}>
<summary><b>By {n}</b> — {len(vals[k])} values · <i>{d}</i></summary>

<br>

| {n} | Projects | Examples |
|---|:-:|---|""")
    for v in sorted(vals[k], key=lambda v: -len([r for r in projects if v in r[k]])):
        rs = [r for r in projects if v in r[k]]
        ex = ", ".join(f"[{r['title'][:40]}]({r['master_folder']})" for r in rs[:3]) + (f" … +{len(rs)-3}" if len(rs) > 3 else "")
        R.append(f"| [**{v}**]({PAGES}/#{k}/{slug(v)}) | {len(rs)} | {ex} |")
    R.append(f"\n</details>\n")
R.append(f"""## 🗂️ What is in this repository (compact — {len(os.listdir(OUT)) + 2} files)

| Path | Purpose |
|---|---|
| `index.html` | Interactive lens dashboard — switch lens, click a value, search; every card links to the evidence file. Hash routes (`#skills/Python-programming`) replace the old one-folder-per-value layout, so the whole index is one page |
| `matrix.html` · `project_lens_matrix.csv` · `lens_index.json` | Every project against every lens (web, spreadsheet, machine-readable) |
| `_build_lens_compact.py` | Generator — edit `lens_index.json` or the rules and rebuild |

<div align="center">

**{OWNER}** · Ghaziabad, NCR, India · MBA · CSCMP SCPro · Six Sigma Black Belt<br>
[LinkedIn](https://linkedin.com/in/eswar-mahalingam) · eswarmba05313@gmail.com · +91-9360548243

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0A1F44,100:C9A227&height=100&section=footer" width="100%"/>

</div>
""")
open(f"{OUT}/README.md", "w").write("\n".join(R))
DESC = (f"Skills-first index of my {N}-project portfolio: the same work viewed by domain, skill, tool, sector, target role, deliverable, method, data provenance and programme — "
        "now including 50 engineering projects (VLSI, robotics, EV, cyber). Pick what you are hiring for and land on the evidence: every entry links to its report, workbook or code.")
assert len(DESC) <= 350, len(DESC)
open(f"{OUT}/REPO_NAME_AND_DESCRIPTION.txt", "w").write(f"REPOSITORY NAME\n{REPO}\n\nDESCRIPTION ({len(DESC)}/350 characters)\n{DESC}\n\nTOPICS\nportfolio skills-matrix data-analytics product-management excel python machine-learning cyber-security electric-vehicles vlsi fpga robotics industry-index career\n\nWEBSITE (after enabling GitHub Pages)\n{PAGES}/\n")
open(f"{OUT}/PUSH_TO_GITHUB.md", "w").write(f"""# Upload (GitHub web, one drag-and-drop — this repo is now {len(os.listdir(OUT)) + 2} files)
1. github.com → New repository → name `{REPO}` → paste description from REPO_NAME_AND_DESCRIPTION.txt → Public → "Add a README" UNTICKED → Create.
   (If the repo already exists with the old files: Settings → Delete this repository, then recreate — simplest way to clear the old by-*/ folders.)
2. "uploading an existing file" → drag ALL files in this folder (including `.nojekyll`) → Commit.
3. Settings → Pages → Deploy from a branch → main / (root) → Save → live at {PAGES}/
4. Links point to `{GH}/{MASTER}` (data/PM/Internship Studio work) and `{GH}/{CODEC}` (50 engineering projects). Push the Codec repo first; the master repo links resolve once that repo exists too.
""")
shutil.copy(__file__, f"{OUT}/_build_lens_compact.py")
print(N, {k: len(v) for k, v in vals.items()}, len(DESC), sorted(os.listdir(OUT)))
