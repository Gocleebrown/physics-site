// scripts/question_engine.js

// 1) Load & render a random question
function loadRandomQuestion() {
  const qDef =
    window.questions[Math.floor(Math.random() * window.questions.length)];
  const qData = typeof qDef.question === "function" ? qDef.question() : qDef;

  // Reset and tally
  resetQuestionScores();
  totalMarksPossible = qData.parts.reduce((s, p) => s + p.marks.length, 0);
  updateScoreDisplay();
  window.currentQuestionData = qData;

  // Clear & render container
  const container = document.getElementById("question-container");
  container.innerHTML = "";

  // Main question text
  const h2 = document.createElement("h2");
  h2.innerHTML = qData.mainText;
  container.appendChild(h2);

  // Render each part
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

  document.getElementById("diagram-canvas").style.display = "none";
}

// 2) Check answer using unified marking system (with numeric fallback)
function checkPartAnswer(index, marks, modelAnswer, explanation) {
  const raw = document.getElementById(`answer-${index}`).value.trim();
  const input = raw.replace("%", "").toLowerCase();

  // —— Numeric-only fallback ——
  if (marks.length === 0 && !isNaN(parseFloat(modelAnswer))) {
    const userNum = parseFloat(raw);
    const correctNum = parseFloat(modelAnswer);
    const tol = Math.abs(correctNum) * 1e-3; // 0.1% tolerance

    if (Math.abs(userNum - correctNum) <= tol) {
      totalMarksEarned++;
      updateScoreDisplay();
      document.getElementById(`score-${index}`).textContent = `(1/1)`;
      const fb = document.getElementById(`model-${index}`);
      fb.style.display = "block";
      fb.style.border = "2px solid green";
      fb.innerHTML = `<strong>Correct!</strong><br>Model Answer: ${modelAnswer}`;
      return;
    }
    // else fall through
  }

  const fb = document.getElementById(`model-${index}`);
  fb.style.display = "block";

  let aBlocked = false;
  let aAwarded = false;
  let cAwarded = new Set();

  // Match flat, grouped, or OR-of-groups-of-groups keywords
  function matchesKeywordGroups(groups) {
    if (!Array.isArray(groups)) return false;

    // Depth-3: OR-of-branches-of-groups
    if (
      Array.isArray(groups[0]) &&
      Array.isArray(groups[0][0]) &&
      Array.isArray(groups[0][0][0])
    ) {
      return groups.some((subgroups) => matchesKeywordGroups(subgroups));
    }

    // Flat array: OR logic
    if (groups.every((g) => typeof g === "string")) {
      return groups.some((kw) => input.includes(kw));
    }

    // Depth-2: AND-of-ORs
    return groups.every(
      (group) => Array.isArray(group) && group.some((kw) => input.includes(kw))
    );
  }

  // STEP 1: M Marks (method gating)
  marks
    .filter((m) => m.type === "M")
    .forEach((m) => {
      if (matchesKeywordGroups(m.keywords)) {
        if (!m.awarded) {
          m.awarded = true;
          totalMarksEarned++;
        }
      } else {
        aBlocked = true;
      }
    });

  // STEP 2: A Marks (final answer)
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

  // STEP 3: C Marks
  if (!aAwarded) {
    marks
      .filter((m) => m.type === "C" && !m.awarded)
      .sort((a, b) => (b.level || 1) - (a.level || 1))
      .forEach((m) => {
        if (matchesKeywordGroups(m.keywords)) {
          m.awarded = true;
          totalMarksEarned++;
          cAwarded.add(m.level || 1);
          // if C2 then also C1
          if ((m.level || 1) > 1) {
            const implied = marks.find(
              (other) =>
                other.type === "C" && (other.level || 1) < (m.level || 1)
            );
            if (implied && !implied.awarded) {
              implied.awarded = true;
              totalMarksEarned++;
            }
          }
        }
      });
  }

  // STEP 4: B Marks
  marks
    .filter((m) => m.type === "B")
    .forEach((m) => {
      if (!m.awarded && matchesKeywordGroups(m.keywords)) {
        m.awarded = true;
        totalMarksEarned++;
      }
    });

  // Final display
  const earned = marks.filter((m) => m.awarded).length;
  const possible = marks.length;
  document.getElementById(
    `score-${index}`
  ).textContent = `(${earned}/${possible})`;

  // Feedback styling
  if (earned === possible) {
    fb.innerHTML = `<strong>Correct!</strong><br><br>Model Answer:<br>${modelAnswer}`;
    fb.style.border = "2px solid green";
  } else if (earned > 0) {
    fb.innerHTML =
      `<strong>You're nearly there!</strong><br><br><em>Hint:</em><br>${explanation}` +
      `<br><br><strong>Model Answer:</strong><br>${modelAnswer}`;
    fb.style.border = "2px solid orange";
  } else {
    fb.innerHTML =
      `<strong>Not quite right.</strong><br><br><em>Hint:</em><br>${explanation}` +
      `<br><br><strong>Model Answer:</strong><br>${modelAnswer}`;
    fb.style.border = "2px solid red";
  }

  updateScoreDisplay();
}

// Expose to global
window.loadRandomQuestion = loadRandomQuestion;
