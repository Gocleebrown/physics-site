// ─────────────────────────────────────────────────────────────────────────────
//  Universal graph-drawing helper with “nice” major + minor grid lines
// ─────────────────────────────────────────────────────────────────────────────
function drawGraph(canvas, spec) {
  const ctx = canvas.getContext("2d");
  const w = canvas.width, h = canvas.height;
  const m = 40;
  const plotW = w - 2 * m, plotH = h - 2 * m;

  function niceStep(raw) {
    if (!isFinite(raw) || raw <= 0) return 1;
    const exp = Math.floor(Math.log10(Math.abs(raw)));
    const base = Math.pow(10, exp);
    const frac = raw / base;
    return base * (frac <= 1 ? 1 : frac <= 2 ? 2 : frac <= 5 ? 5 : 10);
  }

  const xMin = isFinite(spec.xMin) ? spec.xMin : 0;
  const xStep = spec.xStep || niceStep(spec.xMax / 5);
  const xGraphMax = Math.ceil(spec.xMax / xStep) * xStep;
  const xDivs = Math.ceil(xGraphMax / xStep);

  const yStep = spec.yStep || niceStep(spec.yMax / 5);
  const yGraphMax = Math.ceil(spec.yMax / yStep) * yStep;
  const yDivs = Math.ceil(yGraphMax / yStep);

  // minor grid
  ctx.strokeStyle = "#f0f0f0";
  ctx.lineWidth = 1;
  for (let i = 0; i < xDivs; i++) {
    for (let k = 1; k <= 5; k++) {
      const x = m + (((i + k / 6) * xStep) / xGraphMax) * plotW;
      ctx.beginPath();
      ctx.moveTo(x, m);
      ctx.lineTo(x, m + plotH);
      ctx.stroke();
    }
  }
  for (let j = 0; j < yDivs; j++) {
    for (let k = 1; k <= 5; k++) {
      const y = m + plotH - (((j + k / 6) * yStep) / yGraphMax) * plotH;
      ctx.beginPath();
      ctx.moveTo(m, y);
      ctx.lineTo(m + plotW, y);
      ctx.stroke();
    }
  }

  // major grid
  ctx.strokeStyle = "#e0e0e0";
  for (let i = 0; i <= xDivs; i++) {
    const x = m + ((i * xStep) / xGraphMax) * plotW;
    ctx.beginPath();
    ctx.moveTo(x, m);
    ctx.lineTo(x, m + plotH);
    ctx.stroke();
  }
  for (let j = 0; j <= yDivs; j++) {
    const y = m + plotH - ((j * yStep) / yGraphMax) * plotH;
    ctx.beginPath();
    ctx.moveTo(m, y);
    ctx.lineTo(m + plotW, y);
    ctx.stroke();
  }

  // axes
  ctx.strokeStyle = "#000";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(m, m + plotH);
  ctx.lineTo(m + plotW, m + plotH);
  ctx.lineTo(m + plotW, m);
  ctx.stroke();

  // ticks & labels
  ctx.fillStyle = "#000";
  ctx.font = "12px sans-serif";
  for (let i = 0; i <= xDivs; i++) {
    const val = xMin + i * (xStep);
    const x = m + ((val - xMin) / (xGraphMax - xMin)) * plotW;
    ctx.beginPath();
    ctx.moveTo(x, m + plotH - 5);
    ctx.lineTo(x, m + plotH + 5);
    ctx.stroke();
    ctx.fillText(val.toString(), x - 10, m + plotH + 20);
  }
  for (let j = 0; j <= yDivs; j++) {
    const val = j * yStep;
    const y = m + plotH - (val / yGraphMax) * plotH;
    ctx.beginPath();
    ctx.moveTo(m - 5, y);
    ctx.lineTo(m + plotW, y);
    ctx.stroke();
    ctx.fillText(val.toString(), m - 30, y + 4);
  }

  // axis titles
  ctx.fillText(spec.xLabel || "", m + plotW / 2 - 20, h - 5);
  ctx.fillText(spec.yLabel || "", 10, m + plotH / 2);

  // plot data line
  ctx.strokeStyle = spec.color || "blue";
  ctx.lineWidth = 2;
  ctx.beginPath();
  const pts = Array.isArray(spec.points) ? spec.points : [];
  pts.forEach(([xv, yv], idx) => {
    const x = m + ((xv - xMin) / (xGraphMax - xMin)) * plotW;
    const y = m + plotH - (yv / yGraphMax) * plotH;
    idx === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
  });
  ctx.stroke();
}

// ─────────────────────────────────────────────────────────────────────────────
//  Helpers: placeholder resolution, robust graphSpec normalization, images
// ─────────────────────────────────────────────────────────────────────────────
function collectContext(ctx) {
  const bag = {};
  const add = (o) => {
    if (o && typeof o === "object") {
      Object.keys(o).forEach(k => {
        const v = o[k];
        if (typeof v !== "object" && typeof v !== "function") bag[k] = v;
      });
    }
  };
  add(ctx);
  add(ctx?.params);
  add(ctx?.computedValues);
  add(ctx?.computed);
  add(ctx?.values);
  add(ctx?.vars);
  return bag;
}

function resolvePlaceholdersInString(src, ctx) {
  if (typeof src !== "string") return src;
  const bag = collectContext(ctx);
  return src.replace(/\$\{([^}]+)\}/g, (_, key) => {
    const v = bag[key];
    return (v !== undefined && v !== null) ? String(v) : "";
  });
}

// Normalize graphSpec: resolve ${...}, parse JSON, coerce numbers, infer limits
function normalizeGraphSpec(s, ctx) {
  if (typeof s === "string") {
    const substituted = resolvePlaceholdersInString(s, ctx);
    try { s = JSON.parse(substituted); } catch { s = {}; }
  }
  const spec = { ...(s || {}) };

  const num = (v) => {
    if (typeof v === "number") return v;
    if (typeof v === "string") {
      const n = Number(v.trim());
      return isFinite(n) ? n : NaN;
    }
    return NaN;
  };

  const pts = Array.isArray(spec.points)
    ? spec.points
        .map(([x, y]) => [num(x), num(y)])
        .filter(([x, y]) => isFinite(x) && isFinite(y))
    : [];
  spec.points = pts;

  const xs = pts.map(p => p[0]);
  const ys = pts.map(p => p[1]);

  const xMinC = num(spec.xMin);
  const xMaxC = num(spec.xMax);
  const yMaxC = num(spec.yMax);

  spec.xMin = isFinite(xMinC) ? xMinC : 0;
  spec.xMax = isFinite(xMaxC) ? xMaxC : (xs.length ? Math.max(...xs) * 1.05 : 1);
  spec.yMax = isFinite(yMaxC) ? yMaxC : (ys.length ? Math.max(...ys) * 1.05 : 1);

  spec.xLabel = spec.xLabel || "";
  spec.yLabel = spec.yLabel || "";
  return spec;
}

// Asset resolver: supports absolute http(s), repo-relative, and root-relative on Pages
function resolveAsset(src) {
  if (!src) return "";
  if (/^https?:\/\//i.test(src)) return src; // absolute OK
  if (src.startsWith("/")) {
    // convert root-relative → repo root (/user/repo/)
    const root = location.pathname.split("/").slice(0, 2).join("/") + "/";
    return root + src.replace(/^\/+/, "");
  }
  return src; // relative
}

// accepts .png or .svg; item may be string or {src, alt}
function appendImage(target, item) {
  const src = typeof item === "string" ? item : (item?.src || "");
  if (!src) return;
  const img = document.createElement("img");
  img.src = resolveAsset(src);
  img.alt = (typeof item === "object" && item.alt) ? item.alt : "diagram";
  img.loading = "lazy";
  img.style.maxWidth = "320px";
  img.style.display = "block";
  img.style.margin = "8px 0";
  img.onerror = () => {
    const fallback = document.createElement("div");
    fallback.textContent = "[image unavailable]";
    fallback.style.color = "crimson";
    img.replaceWith(fallback);
  };
  target.appendChild(img);
}

function parseArrayMaybe(strOrArr) {
  if (!strOrArr) return [];
  if (Array.isArray(strOrArr)) return strOrArr;
  try { return JSON.parse(strOrArr); } catch { return []; }
}

// ─────────────────────────────────────────────────────────────────────────────
//  1) Load & render a random question
// ─────────────────────────────────────────────────────────────────────────────
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

    // images (png/svg) before graph
    parseArrayMaybe(part.imageBelowMain).forEach((item) => appendImage(div, item));

    // graph (parse placeholders from qData; appear once because you only include on partIndex 0)
    if (part.graphSpec && part.graphSpec !== "[]") {
      const canvas = document.createElement("canvas");
      canvas.width = 300; canvas.height = 300;
      canvas.style.border = "1px solid #000";
      div.appendChild(canvas);
      try {
        const spec = normalizeGraphSpec(part.graphSpec, qData);
        drawGraph(canvas, spec);
      } catch (e) {
        console.error("Graph error:", e);
        const fb = document.createElement("div");
        fb.textContent = "[graph unavailable]";
        fb.style.color = "crimson";
        div.appendChild(fb);
      }
    }

    // images after graph
    parseArrayMaybe(part.imageAfterPart).forEach((item) => appendImage(div, item));

    // answer box
    const ta = document.createElement("textarea");
    ta.id = `answer-${i}`;
    ta.rows = 3;
    ta.cols = 60;
    div.appendChild(ta);

    // check button
    const btn = document.createElement("button");
    btn.textContent = "Check Answer";
    btn.onclick = () =>
      checkPartAnswer(i, part.marks, part.modelAnswer, part.explanation);
    div.appendChild(btn);

    // feedback
    const fb = document.createElement("div");
    fb.id = `model-${i}`;
    fb.style.display = "none";
    fb.style.marginTop = "10px";
    fb.style.padding = "10px";
    fb.style.borderRadius = "8px";
    div.appendChild(fb);

    container.appendChild(div);
  });

  // next question
  const nextBtn = document.createElement("button");
  nextBtn.textContent = "Next Question";
  nextBtn.style.display = "block";
  nextBtn.style.marginTop = "1rem";
  nextBtn.onclick = loadRandomQuestion;
  container.appendChild(nextBtn);

  // hide stray canvas (legacy)
  const stray = document.getElementById("diagram-canvas");
  if (stray) stray.style.display = "none";
}

// ─────────────────────────────────────────────────────────────────────────────
//  2) Check answer with blank-guard, numeric fallback + M/A/C/B
// ─────────────────────────────────────────────────────────────────────────────
function checkPartAnswer(index, marks, modelAnswer, explanation) {
  const raw = document.getElementById(`answer-${index}`).value.trim();
  const input = raw.replace(/%/g, "").toLowerCase();

  if (raw === "") {
    const fb = document.getElementById(`model-${index}`);
    fb.style.display = "block";
    fb.style.border = "2px solid red";
    fb.innerHTML =
      `<strong>Try to always put something down.</strong><br><br>` +
      `<em>Key Idea:</em><br>${explanation}`;
    return;
  }

  const numericOnly = marks.length === 0 || (marks.length === 1 && marks[0].type === "A");
  if (numericOnly && !isNaN(parseFloat(modelAnswer))) {
    const correctNum = parseFloat(modelAnswer);
    const userStr = raw.toLowerCase().trim();

    const variants = [
      correctNum.toPrecision(2),
      correctNum.toExponential(2),
      correctNum.toExponential(2).replace(/e\+?/, "×10^"),
      Math.round(correctNum).toString(),
      correctNum.toFixed(1),
      correctNum.toString(),
    ].map((v) => v.toLowerCase().trim());

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

    const userNum = parseFloat(raw);
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

  const fb = document.getElementById(`model-${index}`);
  fb.style.display = "block";
  let aBlocked = false, aAwarded = false;

  function matchesKeywordGroups(groups) {
    if (!Array.isArray(groups)) return false;
    if (Array.isArray(groups[0]) && Array.isArray(groups[0][0]) && Array.isArray(groups[0][0][0])) {
      return groups.some((sub) => matchesKeywordGroups(sub));
    }
    if (groups.every((g) => typeof g === "string")) {
      return groups.some((kw) => input.includes(kw));
    }
    return groups.every((grp) => grp.some((kw) => input.includes(kw)));
  }

  marks.filter((m) => m.type === "M").forEach((m) => {
    if (matchesKeywordGroups(m.keywords)) {
      if (!m.awarded) {
        m.awarded = true;
        totalMarksEarned++;
      }
    } else aBlocked = true;
  });

  if (!aBlocked) {
    const aMark = marks.find((m) => m.type === "A");
    if (aMark && matchesKeywordGroups(aMark.keywords)) {
      aMark.awarded = true;
      totalMarksEarned++;
      aAwarded = true;
      marks.forEach((m) => {
        if (m.type === "C" && !m.awarded) {
          m.awarded = true;
          totalMarksEarned++;
        }
      });
    }
  }

  if (!aAwarded) {
    marks
      .filter((m) => m.type === "C" && !m.awarded)
      .sort((a, b) => (b.level || 1) - (a.level || 1))
      .forEach((m) => {
        if (matchesKeywordGroups(m.keywords)) {
          m.awarded = true;
          totalMarksEarned++;
          if ((m.level || 1) > 1) {
            const imp = marks.find(
              (o) => o.type === "C" && (o.level || 1) < (m.level || 1)
            );
            if (imp && !imp.awarded) {
              imp.awarded = true;
              totalMarksEarned++;
            }
          }
        }
      });
  }

  marks.filter((m) => m.type === "B").forEach((m) => {
    if (!m.awarded && matchesKeywordGroups(m.keywords)) {
      m.awarded = true;
      totalMarksEarned++;
    }
  });

  const earned = marks.filter((m) => m.awarded).length;
  const possible = marks.length;
  document.getElementById(`score-${index}`).textContent = `(${earned}/${possible})`;

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
