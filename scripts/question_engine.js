// scripts/question_engine.js

// --- Universal graph‑drawing helper with “nice” major + minor grid lines ---
function drawGraph(canvas, spec) {
  const ctx = canvas.getContext("2d");
  const w = canvas.width,
    h = canvas.height;
  const m = 40;
  const plotW = w - 2 * m,
    plotH = h - 2 * m;

  function niceStep(raw) {
    const exp = Math.floor(Math.log10(Math.abs(raw)));
    const base = Math.pow(10, exp);
    const frac = raw / base;
    const nf = frac <= 1 ? 1 : frac <= 2 ? 2 : frac <= 5 ? 5 : 10;
    return nf * base;
  }

  const xGraphMax = (() => {
    const step = spec.xStep || niceStep(spec.xMax / 5);
    return Math.ceil(spec.xMax / step) * step;
  })();
  const xDivs = Math.ceil(xGraphMax / (spec.xStep || niceStep(spec.xMax / 5)));

  const yGraphMax = (() => {
    const step = spec.yStep || niceStep(spec.yMax / 5);
    return Math.ceil(spec.yMax / step) * step;
  })();
  const yDivs = Math.ceil(yGraphMax / (spec.yStep || niceStep(spec.yMax / 5)));

  ctx.strokeStyle = "#f0f0f0";
  ctx.lineWidth = 1;
  for (let i = 0; i < xDivs; i++) {
    for (let k = 1; k <= 5; k++) {
      const x = m + (((i + k / 6) * (xGraphMax / xDivs)) / xGraphMax) * plotW;
      ctx.beginPath();
      ctx.moveTo(x, m);
      ctx.lineTo(x, m + plotH);
      ctx.stroke();
    }
  }
  for (let j = 0; j < yDivs; j++) {
    for (let k = 1; k <= 5; k++) {
      const y =
        m + plotH - (((j + k / 6) * (yGraphMax / yDivs)) / yGraphMax) * plotH;
      ctx.beginPath();
      ctx.moveTo(m, y);
      ctx.lineTo(m + plotW, y);
      ctx.stroke();
    }
  }

  ctx.strokeStyle = "#e0e0e0";
  for (let i = 0; i <= xDivs; i++) {
    const x = m + ((i * (xGraphMax / xDivs)) / xGraphMax) * plotW;
    ctx.beginPath();
    ctx.moveTo(x, m);
    ctx.lineTo(x, m + plotH);
    ctx.stroke();
  }
  for (let j = 0; j <= yDivs; j++) {
    const y = m + plotH - ((j * (yGraphMax / yDivs)) / yGraphMax) * plotH;
    ctx.beginPath();
    ctx.moveTo(m, y);
    ctx.lineTo(m + plotW, y);
    ctx.stroke();
  }

  ctx.strokeStyle = "#000";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(m, m + plotH);
  ctx.lineTo(m + plotW, m + plotH);
  ctx.lineTo(m + plotW, m);
  ctx.stroke();

  ctx.fillStyle = "#000";
  ctx.font = "12px sans-serif";
  for (let i = 0; i <= xDivs; i++) {
    const val = (i * xGraphMax) / xDivs;
    const x = m + (val / xGraphMax) * plotW;
    ctx.beginPath();
    ctx.moveTo(x, m + plotH - 5);
    ctx.lineTo(x, m + plotH + 5);
    ctx.stroke();
    ctx.fillText(Math.round(val).toString(), x - 10, m + plotH + 20);
  }
  for (let j = 0; j <= yDivs; j++) {
    const val = (j * yGraphMax) / yDivs;
    const y = m + plotH - (val / yGraphMax) * plotH;
    ctx.beginPath();
    ctx.moveTo(m - 5, y);
    ctx.lineTo(m + plotW, y);
    ctx.stroke();
    ctx.fillText(Math.round(val).toString(), m - 30, y + 4);
  }

  ctx.fillText(spec.xLabel, m + plotW / 2 - 20, h - 5);
  ctx.fillText(spec.yLabel, 10, m + plotH / 2);

  ctx.strokeStyle = spec.color || "blue";
  ctx.lineWidth = 2;
  ctx.beginPath();
  spec.points.forEach(([xv, yv], idx) => {
    const x = m + (xv / xGraphMax) * plotW;
    const y = m + plotH - (yv / yGraphMax) * plotH;
    idx === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
  });
  ctx.stroke();
}

function loadRandomQuestion() {
  const def =
    window.questions[Math.floor(Math.random() * window.questions.length)];
  const qData = window.genericBuilder(def);
  resetQuestionScores();
  totalMarksPossible = qData.parts.reduce((sum, p) => sum + p.marks.length, 0);
  updateScoreDisplay();

  const container = document.getElementById("question-container");
  container.innerHTML = "";

  const h2 = document.createElement("h2");
  h2.innerHTML = qData.mainText;
  container.appendChild(h2);

  qData.parts.forEach((part, i) => {
    const div = document.createElement("div");
    div.classList.add("question-part");
    const p = document.createElement("p");
    p.innerHTML = part.partText + " ";
    const span = document.createElement("span");
    span.id = `score-${i}`;
    span.textContent = `(0/${part.marks.length})`;
    span.style.fontWeight = "bold";
    p.appendChild(span);
    div.appendChild(p);

    if (part.graphSpec) {
      const canvas = document.createElement("canvas");
      canvas.width = 300;
      canvas.height = 300;
      canvas.style.border = "1px solid #000";
      div.appendChild(canvas);
      drawGraph(canvas, part.graphSpec);
    }

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

    container.appendChild(div);
  });

  const nextBtn = document.createElement("button");
  nextBtn.textContent = "Next Question";
  nextBtn.style.display = "block";
  nextBtn.style.marginTop = "1rem";
  nextBtn.onclick = loadRandomQuestion;
  container.appendChild(nextBtn);

  document.getElementById("diagram-canvas").style.display = "none";
}

function checkPartAnswer(index, marks, modelAnswer, explanation) {
  const raw = document.getElementById(`answer-${index}`).value.trim();
  const input = raw.replace(/%/g, "").toLowerCase();

  // Numeric-only fallback (single A-mark or truly no marks)
  const numericOnly =
    marks.length === 0 || (marks.length === 1 && marks[0].type === "A");
  if (numericOnly && !isNaN(parseFloat(modelAnswer))) {
    // 1) Normalize any “M x 10^N” or “M×10^N” into “MeN”
    const rawNorm = raw
      .trim()
      .replace(
        /([0-9]+(?:\.[0-9]*)?)\s*[×x]\s*10\s*\^\s*([+\-]?\d+)/gi,
        "$1e$2"
      )
      .replace(/,/g, ""); // strip commas

    // 2) Now parse as a standard JS number
    const userNum = parseFloat(rawNorm);

    // 3) Compare within your 0.1% tolerance
    const correctNum = parseFloat(modelAnswer);
    const tol = Math.abs(correctNum) * 1e-3;
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
  let aBlocked = false,
    aAwarded = false,
    cAwarded = new Set();

  function matchesKeywordGroups(groups) {
    if (!Array.isArray(groups)) return false;
    if (
      Array.isArray(groups[0]) &&
      Array.isArray(groups[0][0]) &&
      Array.isArray(groups[0][0][0])
    ) {
      return groups.some((sub) => matchesKeywordGroups(sub));
    }
    if (groups.every((g) => typeof g === "string")) {
      return groups.some((kw) => input.includes(kw));
    }
    return groups.every((grp) => grp.some((kw) => input.includes(kw)));
  }

  // M/A/C/B logic (unchanged)
  marks
    .filter((m) => m.type === "M")
    .forEach((m) => {
      if (matchesKeywordGroups(m.keywords)) {
        if (!m.awarded) {
          m.awarded = true;
          totalMarksEarned++;
        }
      } else aBlocked = true;
    });
  if (!aBlocked) {
    const a = marks.find((m) => m.type === "A");
    if (a && matchesKeywordGroups(a.keywords)) {
      a.awarded = true;
      totalMarksEarned++;
      aAwarded = true;
      marks.forEach((m) => {
        if (m.type === "C" && !m.awarded) {
          m.awarded = true;
          totalMarksEarned++;
          cAwarded.add(m.level || 1);
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
          cAwarded.add(m.level || 1);
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
  marks
    .filter((m) => m.type === "B")
    .forEach((m) => {
      if (!m.awarded && matchesKeywordGroups(m.keywords)) {
        m.awarded = true;
        totalMarksEarned++;
      }
    });
  const earned = marks.filter((m) => m.awarded).length,
    possible = marks.length;
  document.getElementById(
    `score-${index}`
  ).textContent = `(${earned}/${possible})`;
  if (earned === possible) {
    fb.innerHTML = `<strong>Correct!</strong><br><br>Model Answer:<br>${modelAnswer}`;
    fb.style.border = "2px solid green";
  } else if (earned > 0) {
    fb.innerHTML = `<strong>You're nearly there!</strong><br><br><em>Key Idea:</em><br>${explanation}<br><br><strong>Model Answer:</strong><br>${modelAnswer}`;
    fb.style.border = "2px solid orange";
  } else {
    fb.innerHTML = `<strong>Not quite right.</strong><br><br><em>Key Idea:</em><br>${explanation}<br><br><strong>Model Answer:</strong><br>${modelAnswer}`;
    fb.style.border = "2px solid red";
  }
  updateScoreDisplay();
}

window.loadRandomQuestion = loadRandomQuestion;
