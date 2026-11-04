##v8
# CIE 9702 Physics Practice Site — Complete Handover (read this first)

Last updated 4 Nov 2026. This file holds everything a fresh Claude session needs to carry on the work. It replaces the earlier `handover_rules.md` (v1–v6). Where this contradicts any older note, this file wins.

---

## 0. Who and what

- **Owner:** Guy Brown, physics teacher and pastoral leader, Huanui College, NZ (guy.brown@hc.school.nz). Timezone Pacific/Auckland.
- **Site:** `https://gocleebrown.github.io/physics-site` (GitHub Pages, deploys from `master` root on push).
- **Repo:** `https://github.com/Gocleebrown/physics-site` (use the `add_repo` tool with push access, then clone). Layout: `index.html`, `scripts/` (engine), `styles/`, `assets/` (PNG figures), `tools/` (this folder: tests and docs, never served as data).
- **Question bank:** Google Sheet `1mspkPndqlydcum52DiVx_oq0cbmV8F06igR8kISehTI`, tab **"read from here"** (sheetId 0). The site reads this tab as published CSV.
  - Other tabs: Sheet4, questions_import, old as questions, done sheet, and **"backup AS 26-21 to 26-24 (old)"** (sheetId 900189, a copy of the old rows 189–319 made 4 Nov 2026 before the rebuild).
- **Content:** CIE 9702 practice questions. AS papers `9702-26-21..24` (rows ≈189–319), A2 papers `9702_s26_p41..p44` (rows ≈320–512), and older papers (`9702-25-xx` etc.) in rows 2–188 (NOT yet audited).

## 1. THE GOAL AND THE STANDING REQUIREMENT

Every question loads as **one whole question** on one page (e.g. `9702-25-41-Q1` shows parts partIndex 0..10 together). Numbers are **random on every page load** but **identical throughout all parts** of that load, so the questions differ each time and never contradict themselves. Therefore:

- Any value that could be a parameter MUST be a parameter. Do not leave fixed paper numbers unless a figure/image depends on them.
- Every later part and every answer keyword/model answer/explanation must use `${...}` variables, never hard-coded paper numbers.
- Wording must read like a real CIE question. **Never add method hints** that CIE would not give (e.g. "Use the area under the graph to determine…" when CIE says "Determine the elastic strain energy…").
- Each figure/graph/table appears **once**, beside the part that needs it (not duplicated on neighbouring parts).
- Ids and partIndex follow Rule 8 (section 3).

The owner is training Claude to rebuild whole papers directly from the real question paper (QP) and mark scheme (MS) PDFs. **Current plan:** rebuild AS 26-21 as a pilot from its QP+MS, he reviews it on the live site, then 26-22, 26-23, 26-24. Never invent anything not in the PDFs; ask for missing PDFs/figures.

## 2. HOW THE PIPELINE WORKS (so you can reason about bugs)

1. Sheet tab published as CSV → `scripts/questionLoader.js` (##v5) groups rows **by id**, takes `type`, `level`, `tags`, `params` from the **first row of that id in sheet order**.
2. `scripts/questionBuilders.js` (##v2) `genericBuilder` draws each param once per id: `[min,max]` → random, rounded to 3 s.f.; anything else = constant. Then `computedValues` (G) from **all rows of the id** are merged with `Object.assign` in order (a repeated name silently overwrites), each evaluated with `new Function` using earlier keys and params.
3. `mainRow` = the row with partIndex 0 (else the first part). **mainText (I), tableRequest (H) and imageBelowMain (L) are read from that row only.** Parts are sorted by partIndex. Each part's graphSpec is drawn on that part.
4. Text columns are interpolated: `${expr}` evaluated as JS (cannot contain `}`), numbers shown to 3 s.f., strings pass through. partText, mainText and the graph render with `innerHTML`, so HTML (`<br>`, `<sup>`, inline-flex spans) is allowed. Keyword cells are interpolated **before** parsing (so `${kw1}` may supply a `|`-separated list).
5. `scripts/question_engine.js` (##v4) marks answers (`applyCieMarking(marks, studentText)`); `main.js` unchanged.
6. Site exposes `loadQuestionsFromSheet()`, `genericBuilder`, `window.allDefinitions` (useful for live checks in the browser pane).

If files on the live site have lower version markers than above, they are not deployed.

## 3. THE RULES

**Working rules**
1. **Do not guess.** If a PDF/MS/figure needed is not in context, stop and ask. Never invent mark points, axes, figures or model answers.
2. Reword **calculation/numeric** questions from the CIE original (copyright; enables random params). Keep **definition/explain/conceptual** verbatim (only change a symbol that breaks encoding, with approval).
3. Do not change working site behaviour (engine) without approval: flag, explain, wait.
4. Every delivered code file has `##vN` on line 1. Deliver complete drop-in files, not diffs.
5. Be concise, fail loudly with plain-English diagnostics, be honest. Do not claim "done" without running the tests below. (Earlier over-confident "done" claims cost the owner many hours.)
6. Commit messages / PR bodies end with the attribution lines given in the session's system reminder.
7. Never ask the owner to hand-edit the sheet; write via Sheets MCP tools.

**Rule 8 — ONE ID PER WHOLE QUESTION**
- An id is a whole question: `9702-26-21-Q3` (AS) or `9702_s26_p44_q2` (A2), never `q2ai`, `Q1a`.
- partIndex runs 0..n across the whole question in paper order (a, b(i), b(ii), c …). Sheet row order does not matter; partIndex does.
- **F (params) and E (tags) go on the FIRST row of the id in sheet order** (the loader reads that row only). Tags = union over all parts.
- **I, H, L are read from the partIndex-0 row only.** Context belonging to a later part goes at the start of that part's K, separated with `<br><br>`. A figure for a later part goes in M (imageAfterPart).
- **G is merged across rows.** Never give a fixed param and a computed value the same name (past clashes: `k`→`k_s`, `v`→`v_c`, `I`→`I_c`). Put shared computed values on the first row.
- Part labels "(a)", "(b)(i)" are not auto-shown; many parts lack them (optional improvement: prefix K with the label).

**Randomisation (shared values)**
- Draw independent quantities as params; derive dependants in G and round to 3 s.f. (`Number(x.toPrecision(3))`) so what is displayed is exactly what the answers use.
- Chains: compute each answer from the **displayed** values, set `tolerance` 1 (3–5 where a 2 s.f. answer is acceptable) so students who round between steps are not marked wrong. SHC rule: if a rounded value is shown, compute from the rounded value.
- Images that carry numbers cannot follow random values → redraw symbolically (E, x₀, V₀) or generate from params. Graphs: build points in G (`"pts":"JSON.stringify(arr)"`) and put `"points":${pts}` in graphSpec; two curves = two entries in `series`.
- Genericise named bodies (Earth/Sun → a planet/a star) unless a real constant is the point.
- Symbolic JS helper pattern S(var) and a stacked-nuclide helper `st(a,b)` (inline-flex span, mass number over proton number) were used in p44 and 26-23 Q5; see those rows for examples.

## 4. MARKING (engine ##v4)

| Column | Header | Mark type |
|---|---|---|
| N | A_keywords | **A** accuracy; blocked if any M is missed |
| R | M_keywords | **M** method, mandatory |
| S, T, AE | B, B2, B3 | **B** independent marks (only three) |
| O, P, Q | C3, C2, C1 | **C** compensatory; higher C implies lower C; a correct A awards all C |

No ECF, no unit marking. Say "follow through from (c)(i)" in the explanation where CIE has ECF.

**Keyword cell syntax:** `a|b|c` = OR (use this for new rows). JSON array of strings = OR; **JSON array of arrays = AND of ORs** (`[["charge on one plate","charge on a plate"],["between the plates"]]`). Matching: substring, case-insensitive, spaces ignored, hyphen/dash variants and unicode minus normalised... **but Unicode minus ≠ hyphen in some contexts: give both.** `²` and `^2` match each other. Standalone "the/a/an" ignored (v4). Prefix `exact:` requires whole answer equality (stops substring leaks, e.g. `exact:V0`).
- Subscripts are NOT converted: give `g₀` and `g0`; `Φ/ϕ/φ`; `×` and `x`. (Subscript digits ₀ don't match 0; an optional `normaliseText` fix is pending approval.)
- Never put an apostrophe in a JSON cell (builder swaps `'`→`"`, breaks JSON; mark silently never awards). `/`, `(`, `)`, `OR`, `;` inside a keyword are literal and unmatchable by students. Short keywords leak (bare letters, `ps`); use phrases, AND-groups or `exact:`.
- Include the MS's own *Allow* wordings and synonyms.
- **Numbers:** a student's number matches when equal, or has ≥ the keyword's s.f. and is within half a unit of its last s.f., or is within `tolerance` % (col AJ). Fewer s.f. than the MS is wrong. Range keyword `0.30 to 0.45`. Unit powers (m s⁻²) are stripped. Rows with a graphSpec default to 5% tolerance.
- **Powers of ten:** use the `_ans` pattern: G `"L_ans":"L.toExponential(2)"`, N `${L_ans}`. Never put only the mantissa in N.
- **"Any N of M" marks** cannot be expressed exactly. Interim: split points across B/B2/B3 by topic, put a point in two columns where it could earn either (slightly generous). **Planned fix: column AK "max marks"** (engine ##v5, only active when the cell is filled): list all acceptable points as marks, and cap the part's total. Not built yet; flag before changing the engine.
- More than 3 B marks: put the fourth in C1 (acts as independent when there is no A).
- Independent C1 marks (neither implies the other) can't be expressed.

## 5. ANSWER WIDGETS

- Text box by default. **imageChoice** if AA=`imageChoice`, or D=`imageChoice`, or AB non-empty. **table** if AA=`table`, or D=`table` and AF non-empty.
- imageChoice: 4 PNGs `p##_q<id>_a.png` (correct) … `_d.png` in `/assets/`, pushed **before** encoding; AB = JSON array `["x_a.png","x_b.png","x_c.png","x_d.png"]` (correct first); AC = `0`; AD = marks for the part. Drawing questions are always converted to imageChoice.
- table: one mark per cell, row-major; AF row labels, AG col labels (JSON arrays), AH `tableCellKeywords` (**3-level JSON: rows → cells → flat array of alternatives**; a 2-level cell crashes the builder), AI model answers (2-D array). No tick-grids: convert to one row per quantity with a "Change" column.
- Types (col D) exactly: `definition`, `explain`, `conceptual`, `numeric`, `calculation`, `table`, `imageChoice`. Not `drawing`, `shortAnswer`, `written`, `longAnswer`, `show`, `derivation`.

## 6. SHEET COLUMNS (header row 1; 0-based index in brackets)

A level · B id · C paper · D type · E tags · F params · G computedValues · H tableRequest · I mainText · J partIndex · K partText · L imageBelowMain · M imageAfterPart · N A_keywords · O C3 · P C2 · Q C1 · R M · S B · T B2 · U modelAnswer · V explanation · W graphSpec · X graph_straight_line_spec · Y will not work alone · Z make image · AA answerType · AB imageOptions · AC correctImageIndex · AD imageChoiceMarks · AE B3 · AF tableRowLabels · AG tableColLabels · AH tableCellKeywords · AI tableCellAnswers · AJ tolerance · (AK reserved for max marks).

Tags (col E): exact Cambridge names, comma-separated. AS: Physical quantities and units, Kinematics, Dynamics, **Forces, density and pressure** (contains a comma; protected via `COMMA_TOPICS` in questionLoader.js), Work, energy and power, Deformation of solids, Waves, Superposition, Electricity, D.C. circuits, Particle physics. A2: Circular motion, Gravitational fields, Oscillations, Thermal physics, Electric fields, Capacitance, Magnetic fields, Alternating currents, Electromagnetic induction, Quantum physics, Medical physics, Nuclear physics, Cosmology.

graphSpec (col W): `{"xMin":0,"xMax":12,"yMin":-40,"yMax":0,"xStep":2,"yStep":10,"xLabel":"x / cm","yLabel":"ln(I/I₀)","points":[[0,0],[12,-36]]}`; same x twice = vertical step; `series:[{points,color,label}]` for several curves.

## 7. HOW TO WORK WITH THE SHEET AND SITE FROM THE SANDBOX

- Outbound HTTPS to docs.google.com is blocked. Use the Sheets/Drive MCP tools:
  - **Full local copy:** Drive `download_file_content` (CSV export) → JSON result with base64 `content`; decode, then `python3 tools/csv_to_json.py sheet.csv sheet.json`. In Python use `csv.field_size_limit(10**9)`.
  - **Writes:** `update_values`, `update_formulas`, `batch_clear_values`, and `update_spreadsheet` (batchUpdate: repeatCell, copyPaste, updateCells, addSheet). Trick for bulk edits: build formulas in scratch columns (AO:AU), copyPaste PASTE_VALUES over the target, clear scratch. Always **re-download and diff** after writing (past restructure verified 0 diffs). Transient "service unavailable" errors: retry.
- Browser pane (`mcp__remote-devices__Claude_Browser__navigate` + `javascript_tool`) can load the live site and run `loadQuestionsFromSheet()` / `genericBuilder` / read `window.allDefinitions` to test the live data. Playwright is installed in the sandbox for screenshots (deviceScaleFactor 2 if the owner will see it).
- Repo: clone to `/home/claude/gocleebrown/physics-site`; push to master deploys. Hard-refresh the site after deploy.

## 8. TESTING (do all of this before claiming a paper is done)

1. Export sheet → JSON (`tools/csv_to_json.py`).
2. `node tools/build_test.js scripts sheet.json <firstRow> result.json` → want 0 build failures, 0 bad text. Rows that don't reach full marks on their own model answer must each be understood (imageChoice and table rows are harness artefacts; the rest are real keyword gaps and must be fixed).
3. Student simulations per question (`tools/example_marking_test.js`): model answer = full marks; blank = 0; obviously wrong < full; a rounded-intermediate answer still gets the A mark. 150–300 random loads per id. Reset `marks[i].awarded=false` before each `applyCieMarking(marks, text)` call (second arg is the STUDENT answer).
4. Look at it: Playwright screenshot or the live site for anything with a graph, figure or special HTML.
5. Check against the QP+MS: every part present, in order, marks per part match MS, figures present once.

## 9. REBUILD CHECKLIST FOR A PAPER (the pilot procedure)

Inputs: QP PDF, MS PDF, any figure images. Steps:
1. Read QP and MS fully (pdf tooling); list every question/part, marks, figures, tables.
2. Save the figure images into `/assets/` (short names `p21_q3_fig.png`), push before the rows reference them.
3. Per question: id, tags, params (all numbers that can vary, with sensible ranges), G (derived values, `_ans` keys), mainText (reworded for calculations; verbatim for explain/define), parts in paper order, keywords per the MS mark by mark, modelAnswer and explanation with variables, tolerance, graphs from params.
4. Write the rows to the sheet (below the live rows or in a staging tab first; swap in only when the paper passes testing).
5. Run section 8 tests; fix; show the owner a screenshot or per-paper preview; he reviews on the live site.
6. Update the STATUS section of this file.

## 10. STATUS (4 Nov 2026)

**Sheet:**
- Rows 189–512 restructured to one id per whole question (63 questions: 26-21..24 AS, p41..p44 A2). Live site loads 99 definitions; all 63 build clean in 20× tests. Re-download diff = 0.
- 26-23 Q5 fixed (β⁺ equation with random nuclide, stacked notation, "two baryons" wording, 6 random charge pairs, labelled P/Q/R/S keywords).
- Duplicate graphs fixed: 26-21 Q1 (wire graph only on row 252; row 253 asks to "Determine the elastic strain energy stored in the wire when the extension is 0.80 mm."); 26-23 Q2 graph moved to row 265.
- A2 papers p41–p44: keywords audited against QP+MS, randomised, chains merged.
- **Backup:** tab "backup AS 26-21 to 26-24 (old)" = copy of old rows 189–319 (header + 131 rows). Live rows 189–319 still in place until each rebuilt paper replaces them.

**Open concerns (not fixed):**
- AS 26-21..26-24 are all rebuilt and randomised (26-23/26-24 done unattended 5 Nov 2026, awaiting the owner's review). The wire graph (F_max=12, x_max_mm=0.8) is static.
- 26-21 rows Q1bii (252) and Q1bv (253) are a wire force–extension graph sitting inside the rocket question Q1; Q4cii is a resistance graph in Q4 (probably OK). Check against the real paper.
- Row 266 (26-23 Q2, "Use Fig. 2.1 to determine the extension") has no graph beside it and 0% tolerance on a graph-read value; suggest 5%.
- Figures/graphs/tables referred to but missing: 26-21 Q3, 26-22 Q1, 26-24 Q4 (Fig. 4.1), "Table 9.1"/"figure" in p41, p43, p44 Q9.
- Reconstructed (unseen) graphs: p44 Q9(b)(ii), p43 Q3c.
- Approximate "any N of" marks: p44 9(b)(ii), 2(a)(ii), p42 Q8(c), p43 Q3c/Q4a.
- 59 rows still don't score full marks on their own model answer in the harness: 23 imageChoice + table rows are harness artefacts; the rest are real keyword gaps (e.g. 26-22 Q4(iii) with `${F.toFixed(0)}` keywords).
- Possible real-CIE wording flagged: 26-22 Q6 "Use conservation of momentum to calculate…" (row 248).
- Engine limits: 3 B columns; no unit/ECF marking; independent C1; no "any N of M"; `type` column unused for marking.
- p44: row 507 (Q9bii) needs B3; some `longAnswer` types remain; row 475 explanation has hard-coded numbers (check); Q4 numeric rows verbatim CIE (Rule 2); p44 q5a needs "charge divided by voltage / Q/V" alternatives.
- Live-site checks not yet done by eye: p42 Q8 graph, p43 Q3c graph, p44 Q4(c)/Q9(b)(ii) graphs, new images.
- **Public repo:** `StudentQuery (61/62).csv` files sit in `/assets` of the public repo — the owner must check whether they contain student data and remove them if so.
- Rows 2–188 (25-xx and others) not audited.

**Next actions:** (1) owner uploads 26-21 QP+MS PDFs → pilot rebuild; (2) then 26-22, 26-23, 26-24; (3) build the AK max-marks column (engine ##v5); (4) optional per-paper preview page; (5) optional part labels and subscript normalisation (approval needed); (6) audit rows 2–188.


## 12. LESSONS FROM THE 26-21 REBUILD (4 Nov 2026) — READ BEFORE REBUILDING 22–24
- **Source PDFs:** `pdftotext -layout` gives the text; figures are vector (no embedded images), so render pages with `pdftoppm -r 80 -png` and look at them.
- **Figures from parameters:** do NOT use graphSpec (small 300px canvas). Put an SVG helper in G (`gsvg` for grid graphs, `wave31` for a wave diagram; both in `tools/rebuild/jshelpers.py`), build the points from the params, and drop `${fig}` into the part text where the figure sits in the paper. innerHTML renders it. Each G must carry its own copy of the helper (G is merged per id only).
- **Sketch/drawing parts:** convert to imageChoice with 4 SVGs (generator `tools/rebuild/imglib.py`), axes labelled symbolically (A, T) so random values still fit. Put the correct image at a varying index (engine does not shuffle; correct-first is guessable).
- **Part labels:** every K starts `<b>(b)(ii)</b> ` and mainText is `Question N`, so references like “1(b)(iii)” make sense.
- **Numbers in keywords are numeric, not substrings.** `[["5.6"],["8.5"]]` with the student typing `8.5e28` fails; write `8.5e28`. Use `x.toExponential(n)` strings for anything with a power of ten. Display strings (`M6s`, `T2s` via toFixed/toPrecision) keep trailing zeros; keep the raw number for the keyword.
- **Ranges:** `lo to hi` as plain decimals (no exponents) works for graph readings; CIE’s 1 s.f. allowances are asymmetric, so use e.g. 0.8x to 1.3x.
- **Model answer shown to students may contain `<sup>`; tests convert it to `^`.** Show numbers with a `sci(x,n)` helper (in G).
- **Tests:** `tools/rebuild/t40.js` (model answers full marks, blank = 0, wrong number does not earn A, 100 loads/id), `tpaper21.js`/`tq5.js` (fix the params to the real paper’s values and mark mark-scheme-quality answers; partial and wrong answers). Always run MS-quality answers at the paper’s own values: it catches tolerance mistakes (e.g. 1800 vs 1742 m/s).
- **Engine gaps hit again:** “name two leptons” (any 2 of N) is approximated; “correct answer only” earns all C marks (AFC). A max-marks column (AK) would fix the first.
- **Writing rows:** `update_values` with the JSON of each question (`tools/rebuild/build21.py` shows how rows are assembled). Delete old rows (`deleteDimension`, bottom first), `insertDimension`, write, then re-download and diff: must be 0 diffs.
- **AS tag vocabulary in use on the live site:** Dynamics, Kinematics, Energy, Materials, Measurement, Units, Waves, Electricity, Pressure, Particle physics (not the exact Cambridge names; the filter lists whatever is in the sheet).
- **26-21 status: DONE** (rows 189–222, 5 questions, 34 parts, all 60 marks; figures drawn from parameters; assets `as2621_q3*.svg` pushed). Old rows are in the backup tab.

## 11. DECIDED — DON'T REVISIT
1. Drawing questions → imageChoice, 4 PNGs, correct first. 2. One id per WHOLE question (Rule 8) — this supersedes the earlier "one id per sub-part". 3. imageOptions = JSON array of short filenames. 4. Tags are exact Cambridge names. 5. "Define"/"State what is meant by" = `definition`. 6. `Uₐ`→`U` approved for p44 Q4ci/Q4cii only. 7. Precision follows CIE (≥ MS s.f. and same rounding; graph readings get extra tolerance). 8. Marks follow B/M/C/A/AFC rules. 9. ECF is not auto-marked (students compare with earlier answer).

- **26-22 status: DONE** (rows 223–254, 6 questions, 32 parts, 60 marks; assets `as2622_q1v_*.svg`; helpers for plank/ropes, wave interference, circuits are in `tools/rebuild/jshelpers.py`). Lessons: the engine's s.f. rule already accepts a correctly rounded answer, so an A-mark `tolerance` is relative to the ROUNDED key (use 0 when the mark scheme rejects a neighbouring value, e.g. 8.8 vs 8.7); a table cannot share one mark across cells, so scalar/vector (2 marks) was done as a text part with two AND-groups; use `sf(x,n)` (String(+x.toPrecision(n))) for answer keys, never raw toPrecision (gives 1.0e+2).

- **26-23 status: DONE** (rows 255–287, 5 questions; assets `as2623_*.svg`; `build23.py`, `svg23.py`, `tpaper23.js`).
- **26-24 status: DONE** (rows 288–319, 7 questions, 32 parts, 60 marks; assets `as2624_q3b/q3d/q5b_*.svg`; `build24.py`, `svg24.py`, `tpaper24.js`). Sheet re-downloaded and diffed against the builder (differences only the first-row type of Q4 and one duplicate keyword).

### Concerns for review (26-23 / 26-24)
- imageChoice options are static, so image-dependent parts have fixed geometry: 26-24 Q3 uses a fixed 4-loop string; Q5 uses E = 0.80 V fixed and a 40 Ω line in (b).
- 26-24 Q1(a) vector list: the AND of three names also passes a student who lists every item (no negative matching in the engine).
- The engine's "higher C implies lower C" rule can award C1 for a C2-only answer where the mark scheme has independent C marks (26-24 Q5(c), Q2(b)(ii)).
- Q1(b)(ii) acceleration requires the negative sign (MS answer is negative); a positive 3.2 scores 0.
- Hooke's law (Q2(a)) cannot accept "F = kx" alone (AND of three groups).
- Live-site visual check of 26-23 and 26-24 figures is still to be done by eye.
