// scripts/question_engine.js

// ─────────────────────────────────────────────────────────────────────────────
//  Universal graph-drawing helper with “nice” major + minor grid lines
//  ‣ Expects spec as object with optional:
//    { xMin, xMax, yMax, xStep?, yStep?, xLabel?, yLabel?, color?, points: [[x,y], ...] }
//  ‣ You supply the exact points (include [0,0] yourself whenever physics demands it).
//  ‣ This draws y-axis on the LEFT and x-axis at the BOTTOM, with minor+major grids & labels.
// ─────────────────────────────────────────────────────────────────────────────
function drawGraph(canvas, spec) {
  const ctx = canvas.getContext("2d");
  const w = canvas.width, h = canvas.height;
  const m = 40;               // margin
  const plotW = w - 2 * m;
  const plotH = h - 2 * m;

  // Guard + defaults
  if (!spec || typeof spec !== "object") spec = {};
  const xMin = Number.isFinite(spec.xMin) ? Number(spec.xMin) : 0;
  const xMax = Number.isFinite(spec.xMax) ? Number(spec.xMax) : 1;
  const yMax = Number.isFinite(spec.yMax) ? Number(spec.yMax) : 1;

  // nice step helper
  function niceStep(raw) {
    if (!isFinite(raw) || raw <= 0) return 1;
    const exp = Math.floor(Math.log10(Math.abs(raw)));
    const base = Math.pow(10, exp);
    const frac = raw / base;
    return base * (frac <= 1 ? 1 : frac <= 2 ? 2 : frac <= 5 ? 5 : 10);
  }

  const xStep = Number.isFinite(spec.xStep) ? Number(spec.xStep) : niceStep((xMax - xMin) / 5);
  const yStep = Number.isFinite(spec.yStep) ? Number(spec.yStep) : niceStep(yMax / 5);

  const xGraphMax = Math.ceil(xMax / xStep) * xStep;
  const xGraphMin = Math.floor(xMin / xStep) * xStep; // in case you ever set negative xMin
  const yGraphMin = 0;                                // force baseline at 0 for typical F–x
  const yGraphMax = Math.ceil(yMax / yStep) * yStep;

  const nX = Math.max(1, Math.round((xGraphMax - xGraphMin) / xStep));
  const nY = Math.max(1, Math.round((yGraphMax - yGraphMin) / yStep));

  // helpers to map data → canvas
  const xToPx = (x) => m + ((x - xGraphMin) / (xGraphMax - xGraphMin)) * plotW;
  const yToPx = (y) => m + plotH - ((y - yGraphMin) / (yGraphMax - yGraphMin)) * plotH;

  // BACKGROUND
  ctx.clearRect(0, 0, w, h);

  // minor grid (5 subdivisions between majors)
  ctx.strokeStyle = "#f0f0f0";
  ctx.lineWidth = 1;
  for (let i = 0; i < nX; i++) {
    for (let k = 1; k <= 5; k++) {
      const x = xToPx(xGraphMin + (i + k / 6) * xStep);
      ctx.beginPath();
      ctx.moveTo(x, m);
      ctx.lineTo(x, m + plotH);
      ctx.stroke();
    }
  }
  for (let j = 0; j < nY; j++) {
    for (let k = 1; k <= 5; k++) {
      const y = yToPx(yGraphMin + (j + k / 6) * yStep);
      ctx.beginPath();
      ctx.moveTo(m, y);
      ctx.lineTo(m + plotW, y);
      ctx.stroke();
    }
  }

  // major grid
  ctx.strokeStyle = "#e0e0e0";
  for (let i = 0; i <= nX; i++) {
    const x = xToPx(xGraphMin + i * xStep);
    ctx.beginPath();
    ctx.moveTo(x, m);
    ctx.lineTo(x, m + plotH);
    ctx.stroke();
  }
  for (let j = 0; j <= nY; j++) {
    const y = yToPx(yGraphMin + j * yStep);
    ctx.beginPath();
    ctx.moveTo(m, y);
    ctx.lineTo(m + plotW, y);
    ctx.stroke();
  }

  // axes (LEFT y-axis and BOTTOM x-axis)
  ctx.strokeStyle = "#000";
  ctx.lineWidth = 2;
  ctx.beginPath();
  // y-axis at left margin
  ctx.moveTo(m, m + plotH);
  ctx.lineTo(m, m);
  // x-axis at bottom
  ctx.moveTo(m, m + plotH);
  ctx.lineTo(m + plotW, m + plotH);
  ctx.stroke();

  // ticks & labels
  ctx.strokeStyle = "#000";
  ctx.fillStyle = "#000";
  ctx.lineWidth = 1;
  ctx.font = "12px sans-serif";
  ctx.textBaseline = "top";
  ctx.textAlign = "center";

  // x-axis ticks & labels
  for (let i = 0; i <= nX; i++) {
    const val = xGraphMin + i * xStep;
    const x = xToPx(val);
    ctx.beginPath();
    ctx.moveTo(x, m + plotH - 5);
    ctx.lineTo(x, m + plotH + 5);
    ctx.stroke();
    ctx.fillText((Math.abs(val) < 1e-12 ? 0 : val).toString(), x, m + plotH + 8);
  }

  // y-axis ticks & labels
  ctx.textAlign = "right";
  ctx.textBaseline = "middle";
  for (let j = 0; j <= nY; j++) {
    const val = yGraphMin + j * yStep;
    const y = yToPx(val);
    // short tick on left axis only
    ctx.beginPath();
    ctx.moveTo(m - 5, y);
    ctx.lineTo(m + 5, y);
    ctx.stroke();
    ctx.fillText((Math.abs(val) < 1e-12 ? 0 : val).toString(), m - 8, y);
  }

  // axis titles
  if (spec.xLabel) {
    ctx.textAlign = "center";
    ctx.textBaseline = "alphabetic";
    ctx.fillText(spec.xLabel, m + plotW / 2, h - 8);
  }
  if (spec.yLabel) {
    ctx.save();
    ctx.translate(12, m + plotH / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.textAlign = "center";
    ctx.textBaseline = "top";
    ctx.fillText(spec.yLabel, 0, 0);
    ctx.restore();
  }

  // plot data line(s) — either a single line (spec.points, existing behaviour)
  // or multiple labelled lines (spec.series: [{points, color, label}, ...])
  const seriesList = Array.isArray(spec.series) && spec.series.length
    ? spec.series
    : [{ points: Array.isArray(spec.points) ? spec.points : [], color: spec.color }];

  seriesList.forEach((s) => {
    const pts = Array.isArray(s.points) ? s.points : [];
    if (!pts.length) return;
    ctx.strokeStyle = s.color || "black";
    ctx.lineWidth = 2;
    ctx.beginPath();
    pts.forEach(([xv, yv], idx) => {
      const x = xToPx(Number(xv));
      const y = yToPx(Number(yv));
      if (idx === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();
  });

  // series labels, drawn near the end of each line
  seriesList.forEach((s) => {
    if (!s.label || !Array.isArray(s.points) || !s.points.length) return;
    const [lx, ly] = s.points[s.points.length - 1];
    ctx.fillStyle = s.color || "black";
    ctx.font = "12px sans-serif";
    ctx.textAlign = "left";
    ctx.textBaseline = "middle";
    ctx.fillText(s.label, xToPx(Number(lx)) + 6, yToPx(Number(ly)));
  });
}

// Accept object or JSON string; coerce numeric fields (keeps old behaviour)
function normalizeGraphSpec(specLike) {
  let spec = specLike;
  if (typeof spec === "string") {
    try { spec = JSON.parse(spec); } catch { spec = {}; }
  }
  if (!spec || typeof spec !== "object") spec = {};

  const num = (v) =>
    (typeof v === "string" && v.trim() !== "" && !isNaN(v)) ? Number(v) : v;

  ["xMin", "xMax", "yMax", "xStep", "yStep"].forEach((k) => {
    if (k in spec) spec[k] = num(spec[k]);
  });

  if (Array.isArray(spec.points)) {
    spec.points = spec.points
      .map((pt) => {
        const [x, y] = pt || [];
        return [num(x), num(y)];
      })
      .filter(([x, y]) => Number.isFinite(x) && Number.isFinite(y));
  }

  if (Array.isArray(spec.series)) {
    spec.series = spec.series.map((s) => ({
      ...s,
      points: Array.isArray(s.points)
        ? s.points
            .map((pt) => {
              const [x, y] = pt || [];
              return [num(x), num(y)];
            })
            .filter(([x, y]) => Number.isFinite(x) && Number.isFinite(y))
        : [],
    }));
  }

  return spec;
}

// ─── 1) Load & render a random question ───
function loadRandomQuestion() {
  const def = window.questions[Math.floor(Math.random() * window.questions.length)];
  const qData = window.genericBuilder(def);

  // reset scores
  resetQuestionScores();
  totalMarksPossible = qData.parts.reduce((sum, p) => sum + p.marks.length, 0);
  updateScoreDisplay();

  const container = document.getElementById("question-container");
  container.innerHTML = "";

  // main text
  const h2 = document.createElement("h2");
  h2.innerHTML = qData.mainText;
  container.appendChild(h2);

  // each part
  qData.parts.forEach((part, i) => {
    const div = document.createElement("div");
    div.classList.add("question-part");

    // prompt + score
    const p = document.createElement("p");
    p.innerHTML = part.partText + " ";
    const span = document.createElement("span");
    span.id = `score-${i}`;
    span.textContent = `(0/${part.marks.length})`;
    span.style.fontWeight = "bold";
    p.appendChild(span);
    div.appendChild(p);

    // graph if given (accepts JSON string or object; coerces numbers)
    if (part.graphSpec) {
      const canvas = document.createElement("canvas");
      canvas.width = 300;
      canvas.height = 300;
      canvas.style.border = "1px solid #000";
      canvas.style.marginRight = "10px";
      div.appendChild(canvas);
      try {
        const spec = normalizeGraphSpec(part.graphSpec);
        drawGraph(canvas, spec);
      } catch (e) {
        console.error("Graph error:", e, part.graphSpec);
        const fb = document.createElement("div");
        fb.textContent = "[graph unavailable]";
        fb.style.color = "crimson";
        div.appendChild(fb);
      }
    }

    // optional second graph, shown alongside the first (e.g. two related
    // figures the student needs to read together)
    if (part.graphSpec2) {
      const canvas2 = document.createElement("canvas");
      canvas2.width = 300;
      canvas2.height = 300;
      canvas2.style.border = "1px solid #000";
      div.appendChild(canvas2);
      try {
        const spec2 = normalizeGraphSpec(part.graphSpec2);
        drawGraph(canvas2, spec2);
      } catch (e) {
        console.error("Graph 2 error:", e, part.graphSpec2);
        const fb = document.createElement("div");
        fb.textContent = "[second graph unavailable]";
        fb.style.color = "crimson";
        div.appendChild(fb);
      }
    }

    if (part.answerType === "imageChoice") {
      // ── clickable diagram/graph options instead of a text box ──
      const grid = document.createElement("div");
      grid.style.display = "flex";
      grid.style.flexWrap = "wrap";
      grid.style.gap = "10px";
      grid.style.marginTop = "8px";

      const options = Array.isArray(part.imageOptions) ? part.imageOptions : [];
      if (!options.length) {
        const warn = document.createElement("div");
        warn.textContent = "[no image options configured for this part]";
        warn.style.color = "crimson";
        div.appendChild(warn);
      }

      options.forEach((filename, optIdx) => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.style.padding = "4px";
        btn.style.border = "2px solid #999";
        btn.style.borderRadius = "6px";
        btn.style.background = "white";
        btn.style.cursor = "pointer";

        const img = document.createElement("img");
        img.src = window.resolveAssetSrc(filename);
        img.style.width = "160px";
        img.style.display = "block";
        img.onerror = () => {
          btn.style.borderColor = "crimson";
          btn.title = `Missing asset: ${filename}`;
        };
        btn.appendChild(img);

        btn.onclick = () =>
          checkImageChoice(i, optIdx, part.correctImageIndex, part.marks, grid, part.explanation);

        grid.appendChild(btn);
      });

      div.appendChild(grid);

      // feedback area (shared with the rest of the flow)
      const fb = document.createElement("div");
      fb.id = `model-${i}`;
      fb.style.display = "none";
      fb.style.marginTop = "10px";
      fb.style.padding = "10px";
      fb.style.borderRadius = "8px";
      div.appendChild(fb);
    } else if (part.answerType === "table") {
      // ── grid of inputs, row/col labelled, matching the paper's table ──
      const rows = Array.isArray(part.tableRowLabels) ? part.tableRowLabels : [];
      const cols = Array.isArray(part.tableColLabels) ? part.tableColLabels : [];

      const table = document.createElement("table");
      table.style.borderCollapse = "collapse";
      table.style.marginTop = "8px";

      const headRow = document.createElement("tr");
      headRow.appendChild(document.createElement("th"));
      cols.forEach((c) => {
        const th = document.createElement("th");
        th.textContent = c;
        th.style.border = "1px solid #999";
        th.style.padding = "6px";
        headRow.appendChild(th);
      });
      table.appendChild(headRow);

      rows.forEach((rLabel, r) => {
        const tr = document.createElement("tr");
        const th = document.createElement("th");
        th.textContent = rLabel;
        th.style.border = "1px solid #999";
        th.style.padding = "6px";
        tr.appendChild(th);

        cols.forEach((c, cIdx) => {
          const td = document.createElement("td");
          td.style.border = "1px solid #999";
          td.style.padding = "4px";
          const input = document.createElement("input");
          input.type = "text";
          input.id = `table-${i}-${r}-${cIdx}`;
          input.style.width = "160px";
          td.appendChild(input);
          tr.appendChild(td);
        });
        table.appendChild(tr);
      });

      div.appendChild(table);

      const btn = document.createElement("button");
      btn.textContent = "Check Answer";
      btn.style.marginTop = "8px";
      btn.onclick = () =>
        checkTableAnswer(i, part.marks, rows, cols, part.tableCellKeywords, part.tableCellAnswers, part.explanation);
      div.appendChild(btn);

      const fb = document.createElement("div");
      fb.id = `model-${i}`;
      fb.style.display = "none";
      fb.style.marginTop = "10px";
      fb.style.padding = "10px";
      fb.style.borderRadius = "8px";
      div.appendChild(fb);
    } else {
      // ── standard typed-answer flow (unchanged) ──
      const ta = document.createElement("textarea");
      ta.id = `answer-${i}`;
      ta.rows = 3;
      ta.cols = 60;
      div.appendChild(ta);

      const btn = document.createElement("button");
      btn.textContent = "Check Answer";
      btn.onclick = () =>
        checkPartAnswer(i, part.marks, part.modelAnswer, part.explanation);
      div.appendChild(btn);

      const fb = document.createElement("div");
      fb.id = `model-${i}`;
      fb.style.display = "none";
      fb.style.marginTop = "10px";
      fb.style.padding = "10px";
      fb.style.borderRadius = "8px";
      div.appendChild(fb);
    }

    container.appendChild(div);
  });

  // next question
  const nextBtn = document.createElement("button");
  nextBtn.textContent = "Next Question";
  nextBtn.style.display = "block";
  nextBtn.style.marginTop = "1rem";
  nextBtn.onclick = loadRandomQuestion;
  container.appendChild(nextBtn);

  // hide stray legacy canvas (if present)
  const stray = document.getElementById("diagram-canvas");
  if (stray) stray.style.display = "none";
}

// ─── 2) Check an imageChoice answer: single click = single attempt ───
function checkImageChoice(index, chosenIdx, correctIdx, marks, grid, explanation) {
  const buttons = grid.querySelectorAll("button");
  const correct = chosenIdx === correctIdx;

  buttons.forEach((btn, idx) => {
    btn.disabled = true;
    btn.style.cursor = "default";
    if (idx === correctIdx) btn.style.borderColor = "green";
    if (idx === chosenIdx && !correct) btn.style.borderColor = "crimson";
  });

  if (correct) {
    marks.forEach((m) => (m.awarded = true));
    totalMarksEarned += marks.length;
  }

  const earned = marks.filter((m) => m.awarded).length;
  document.getElementById(`score-${index}`).textContent = `(${earned}/${marks.length})`;

  const fb = document.getElementById(`model-${index}`);
  fb.style.display = "block";
  fb.style.border = correct ? "2px solid green" : "2px solid red";
  fb.innerHTML = correct
    ? `<strong>Correct!</strong><br><br>${explanation || ""}`
    : `<strong>Not quite right.</strong><br><br>${explanation || ""}`;

  updateScoreDisplay();
}

// Parses a number typed in any common student style: "3.4e22", "3.4E22",
// "3.4 x 10^22", "3.4×10^22", "3.4*10^22", or with trailing units/words
// ("3.4x10^22 molecules"). Returns NaN if nothing numeric is found.
function parseFlexibleNumber(str) {
  if (!str) return NaN;
  let s = String(str).trim().toLowerCase();
  s = s.replace(/\s*[x×*]\s*10\s*\^?\s*/g, "e");
  const match = s.match(/-?\d+\.?\d*(e[+-]?\d+)?/);
  return match ? parseFloat(match[0]) : NaN;
}

// Shared keyword-matching logic — used by both checkPartAnswer and
// checkTableAnswer. Supports flat OR, AND-of-ORs, and OR-of-(AND-of-ORs).
function matchesKeywordGroups(groups, input) {
  if (!Array.isArray(groups)) return false;
  // OR-of-ORs
  if (Array.isArray(groups[0]) && Array.isArray(groups[0][0]) && Array.isArray(groups[0][0][0])) {
    return groups.some((sub) => matchesKeywordGroups(sub, input));
  }
  // flat OR
  if (groups.every((g) => typeof g === "string")) {
    return groups.some((kw) => input.includes(kw));
  }
  // AND-of-ORs
  return groups.every((grp) => grp.some((kw) => input.includes(kw)));
}

// ─── 3.5) Check a table-style answer (grid of inputs, one mark per cell) ───
function checkTableAnswer(index, marks, rowLabels, colLabels, cellKeywords, cellAnswers, explanation) {
  let earned = 0;
  let anyBlank = false;
  let markIdx = 0;

  const fb = document.getElementById(`model-${index}`);
  fb.style.display = "block";

  let feedbackRows = "";
  rowLabels.forEach((rLabel, r) => {
    colLabels.forEach((cLabel, c) => {
      const el = document.getElementById(`table-${index}-${r}-${c}`);
      const raw = (el ? el.value : "").trim();
      const input = raw.toLowerCase();
      const kw = (cellKeywords && cellKeywords[r] && cellKeywords[r][c]) || [];
      const answer = (cellAnswers && cellAnswers[r] && cellAnswers[r][c]) || "";
      const mark = marks[markIdx];
      markIdx++;

      if (raw === "") anyBlank = true;

      const correct = raw !== "" && matchesKeywordGroups(kw, input);
      if (mark) mark.awarded = correct;
      if (correct) earned++;

      if (el) el.style.border = raw === "" ? "1px solid #999" : correct ? "2px solid green" : "2px solid crimson";

      feedbackRows += `<tr><td style="padding:2px 8px 2px 0;">${rLabel} &ndash; ${cLabel}:</td><td>${answer}</td></tr>`;
    });
  });

  totalMarksEarned += earned;
  document.getElementById(`score-${index}`).textContent = `(${earned}/${marks.length})`;

  fb.style.border = earned === marks.length ? "2px solid green" : earned > 0 ? "2px solid orange" : "2px solid red";
  fb.innerHTML =
    (anyBlank ? `<strong>Try to fill in every cell.</strong><br><br>` : earned === marks.length ? `<strong>Correct!</strong><br><br>` : `<strong>Not quite right yet.</strong><br><br>`) +
    `<em>Model answers:</em><table>${feedbackRows}</table>` +
    (explanation ? `<br>${explanation}` : "");

  updateScoreDisplay();
}

// ─── 3) Check answer with blank-guard, numeric fallback ±0.5%, and M/A/C/B ───
function checkPartAnswer(index, marks, modelAnswer, explanation) {
  const raw = document.getElementById(`answer-${index}`).value.trim();
  const input = raw.replace(/%/g, "").toLowerCase();

  // blank-guard
  if (raw === "") {
    const fb = document.getElementById(`model-${index}`);
    fb.style.display = "block";
    fb.style.border = "2px solid red";
    fb.innerHTML =
      `<strong>Try to always put something down.</strong><br><br>` +
      `<em>Key Idea:</em><br>${explanation}`;
    return;
  }

  // numeric-only fallback (single A-mark or no marks) with ±0.5%
  const numericOnly = marks.length === 0 || (marks.length === 1 && marks[0].type === "A");
  if (numericOnly && !isNaN(parseFlexibleNumber(modelAnswer))) {
    const correctNum = parseFlexibleNumber(modelAnswer);
    const userStr = raw.toLowerCase().trim();

    const variants = [
      correctNum.toPrecision(2),
      Number.isFinite(correctNum) ? Number(correctNum).toExponential(2) : "",
      Number.isFinite(correctNum) ? Number(correctNum).toExponential(2).replace(/e\+?/, "×10^") : "",
      Math.round(correctNum).toString(),
      Number.isFinite(correctNum) ? Number(correctNum).toFixed(1) : "",
      correctNum.toString(),
    ].map((v) => String(v).toLowerCase().trim());

    if (variants.includes(userStr)) {
      totalMarksEarned++;
      updateScoreDisplay();
      document.getElementById(`score-${index}`).textContent = `(1/1)`;
      const fb = document.getElementById(`model-${index}`);
      fb.style.display = "block";
      fb.style.border = "2px solid green";
      fb.innerHTML = `<strong>Correct!</strong><br>Model Answer: ${modelAnswer}`;
      return;
    }

    const userNum = parseFlexibleNumber(raw);
    const tol = Math.abs(correctNum) * 0.005;
    if (!isNaN(userNum) && Math.abs(userNum - correctNum) <= tol) {
      totalMarksEarned++;
      updateScoreDisplay();
      document.getElementById(`score-${index}`).textContent = `(1/1)`;
      const fb = document.getElementById(`model-${index}`);
      fb.style.display = "block";
      fb.style.border = "2px solid green";
      fb.innerHTML = `<strong>Correct!</strong><br>Model Answer: ${modelAnswer}`;
      return;
    }
  }

  // M/A/C/B keyword marking
  const fb = document.getElementById(`model-${index}`);
  fb.style.display = "block";
  let aBlocked = false, aAwarded = false;

  // STEP 1: M
  marks.filter((m) => m.type === "M").forEach((m) => {
    if (matchesKeywordGroups(m.keywords, input)) {
      if (!m.awarded) { m.awarded = true; totalMarksEarned++; }
    } else {
      aBlocked = true;
    }
  });

  // STEP 2: A (+auto-credit remaining C’s once A is earned)
  // An A-mark can be satisfied either by keyword match OR by the typed
  // answer being numerically close to modelAnswer (when modelAnswer is a
  // number) — this matters for any question worth more than 1 mark, which
  // doesn't get the single-mark numeric shortcut above but can still have
  // a large/awkward number (scientific notation etc.) as its final answer.
  if (!aBlocked) {
    const aMark = marks.find((m) => m.type === "A");
    if (aMark) {
      const byKeyword = matchesKeywordGroups(aMark.keywords, input);
      let byNumber = false;
      const correctNum = parseFlexibleNumber(modelAnswer);
      if (!isNaN(correctNum)) {
        const userNum = parseFlexibleNumber(raw);
        const tol = Math.abs(correctNum) * 0.005;
        byNumber = !isNaN(userNum) && Math.abs(userNum - correctNum) <= tol;
      }
      if (byKeyword || byNumber) {
        aMark.awarded = true; totalMarksEarned++; aAwarded = true;
        marks.forEach((m) => {
          if (m.type === "C" && !m.awarded) { m.awarded = true; totalMarksEarned++; }
        });
      }
    }
  }

  // STEP 3: C (with implicit lower-level C catch-up)
  if (!aAwarded) {
    marks
      .filter((m) => m.type === "C" && !m.awarded)
      .sort((a, b) => (b.level || 1) - (a.level || 1))
      .forEach((m) => {
        if (matchesKeywordGroups(m.keywords, input)) {
          m.awarded = true; totalMarksEarned++;
          if ((m.level || 1) > 1) {
            const imp = marks.find((o) => o.type === "C" && (o.level || 1) < (m.level || 1));
            if (imp && !imp.awarded) { imp.awarded = true; totalMarksEarned++; }
          }
        }
      });
  }

  // STEP 4: B (independent)
  marks.filter((m) => m.type === "B").forEach((m) => {
    if (!m.awarded && matchesKeywordGroups(m.keywords, input)) {
      m.awarded = true; totalMarksEarned++;
    }
  });

  // final score display
  const earned = marks.filter((m) => m.awarded).length;
  const possible = marks.length;
  document.getElementById(`score-${index}`).textContent = `(${earned}/${possible})`;

  // feedback
  if (earned === possible) {
    fb.innerHTML = `<strong>Correct!</strong><br><br>Model Answer:<br>${modelAnswer}`;
    fb.style.border = "2px solid green";
  } else if (earned > 0) {
    fb.innerHTML =
      `<strong>You're nearly there!</strong><br><br><em>Key Idea:</em><br>${explanation}` +
      `<br><br><strong>Model Answer:</strong><br>${modelAnswer}`;
    fb.style.border = "2px solid orange";
  } else {
    fb.innerHTML =
      `<strong>Not quite right.</strong><br><br><em>Key Idea:</em><br>${explanation}` +
      `<br><br><strong>Model Answer:</strong><br>${modelAnswer}`;
    fb.style.border = "2px solid red";
  }

  updateScoreDisplay();
}

// expose globally
window.loadRandomQuestion = loadRandomQuestion;
