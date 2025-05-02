// scripts/question_engine.js

// --- Universal graph‐drawing helper ---
function drawGraph(canvas, spec) {
  const ctx = canvas.getContext("2d");
  const w = canvas.width,
    h = canvas.height;

  // Axes
  ctx.beginPath();
  ctx.moveTo(40, h - 40);
  ctx.lineTo(w - 40, h - 40);
  ctx.lineTo(w - 40, 40);
  ctx.stroke();

  // Ticks & labels (optional)
  if (spec.xTicks)
    spec.xTicks.forEach((val) => {
      const x = 40 + (val / spec.xMax) * (w - 80);
      ctx.fillText(val, x, h - 30);
      ctx.beginPath();
      ctx.moveTo(x, h - 44);
      ctx.lineTo(x, h - 36);
      ctx.stroke();
    });
  if (spec.yTicks)
    spec.yTicks.forEach((val) => {
      const y = h - 40 - (val / spec.yMax) * (h - 80);
      ctx.fillText(val, 10, y);
      ctx.beginPath();
      ctx.moveTo(36, y);
      ctx.lineTo(44, y);
      ctx.stroke();
    });

  // Axis labels
  ctx.fillText(spec.xLabel, w / 2, h - 10);
  ctx.fillText(spec.yLabel, 10, h / 2);

  // Plot points
  ctx.beginPath();
  spec.points.forEach(([xv, yv], i) => {
    const x = 40 + (xv / spec.xMax) * (w - 80);
    const y = h - 40 - (yv / spec.yMax) * (h - 80);
    i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
  });
  ctx.strokeStyle = spec.color || "blue";
  ctx.stroke();
}

// 1) Load & render a random question
function loadRandomQuestion() {
  const def =
    window.questions[Math.floor(Math.random() * window.questions.length)];
  const qData = window.genericBuilder(def);

  // reset & tally
  resetQuestionScores();
  totalMarksPossible = qData.parts.reduce((sum, p) => sum + p.marks.length, 0);
  updateScoreDisplay();
  window.currentQuestionData = qData;

  // clear
  const container = document.getElementById("question-container");
  container.innerHTML = "";

  // heading
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

    // if graphSpec → draw graph
    if (part.graphSpec) {
      const canvas = document.createElement("canvas");
      canvas.width = 300;
      canvas.height = 300;
      canvas.style.border = "1px solid #000";
      div.appendChild(canvas);
      drawGraph(canvas, part.graphSpec);
    }

    // textarea for answer
    const ta = document.createElement("textarea");
    ta.id = `answer-${i}`;
    ta.rows = 3;
    ta.cols = 60;
    div.appendChild(ta);

    // Check Answer button
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

  // Next Question button
  const next = document.createElement("button");
  next.textContent = "Next Question";
  next.style.display = "block";
  next.style.marginTop = "1rem";
  next.onclick = loadRandomQuestion;
  container.appendChild(next);

  document.getElementById("diagram-canvas").style.display = "none";
}

// 2) Check answer (numeric fallback + M/A/C/B marking, Key Idea text)
function checkPartAnswer(index, marks, modelAnswer, explanation) {
  const raw = document.getElementById(`answer-${index}`).value.trim();
  const input = raw.replace("%", "").toLowerCase();

  // Numeric‐only fallback
  if (marks.length === 0 && !isNaN(parseFloat(modelAnswer))) {
    const user = parseFloat(raw),
      corr = parseFloat(modelAnswer),
      tol = Math.abs(corr) * 1e-3;
    if (Math.abs(user - corr) <= tol) {
      totalMarksEarned++;
      updateScoreDisplay();
      document.getElementById(`score-${index}`).textContent = "(1/1)";
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

  // STEP 1: M-marks
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

  // STEP 2: A-marks
  if (!aBlocked) {
    const aMark = marks.find((m) => m.type === "A");
    if (aMark && matchesKeywordGroups(aMark.keywords)) {
      aMark.awarded = true;
      totalMarksEarned++;
      aAwarded = true;
      // award all C
      marks.forEach((m) => {
        if (m.type === "C" && !m.awarded) {
          m.awarded = true;
          totalMarksEarned++;
          cAwarded.add(m.level || 1);
        }
      });
    }
  }

  // STEP 3: C-marks
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
            const implied = marks.find(
              (o) => o.type === "C" && (o.level || 1) < (m.level || 1)
            );
            if (implied && !implied.awarded) {
              implied.awarded = true;
              totalMarksEarned++;
            }
          }
        }
      });
  }

  // STEP 4: B-marks
  marks
    .filter((m) => m.type === "B")
    .forEach((m) => {
      if (!m.awarded && matchesKeywordGroups(m.keywords)) {
        m.awarded = true;
        totalMarksEarned++;
      }
    });

  // Final score update
  const earned = marks.filter((m) => m.awarded).length,
    possible = marks.length;
  document.getElementById(
    `score-${index}`
  ).textContent = `(${earned}/${possible})`;

  // Feedback styling (Key Idea)
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

window.loadRandomQuestion = loadRandomQuestion;
