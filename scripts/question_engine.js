// scripts/question_engine.js

function loadRandomQuestion() {
  // Pick a random question
  const question = questions[Math.floor(Math.random() * questions.length)];
  const qData = question.question();

  // Reset totals
  totalMarksEarned = 0;
  totalMarksPossible = qData.parts.reduce((sum, p) => sum + p.marks.length, 0);
  updateScoreDisplay();

  // Store for marking
  window.currentQuestionData = qData;

  // Render
  const container = document.getElementById("question-container");
  container.innerHTML = "";

  // Main text
  const intro = document.createElement("h2");
  intro.textContent = qData.mainText;
  container.appendChild(intro);

  qData.parts.forEach((part, index) => {
    const partDiv = document.createElement("div");
    partDiv.classList.add("question-part");

    // Part text + per-part score display
    const partText = document.createElement("p");
    partText.innerHTML = part.partText + " ";
    const scoreSpan = document.createElement("span");
    scoreSpan.id = `score-${index}`;
    scoreSpan.textContent = `(0/${part.marks.length})`;
    scoreSpan.style.fontWeight = "bold";
    partText.appendChild(scoreSpan);
    partDiv.appendChild(partText);

    // Answer input
    const answerInput = document.createElement("textarea");
    answerInput.id = `answer-${index}`;
    answerInput.rows = 3;
    answerInput.cols = 60;
    partDiv.appendChild(answerInput);

    // Check button
    const checkButton = document.createElement("button");
    checkButton.textContent = "Check Answer";
    checkButton.onclick = () => {
      checkPartAnswer(index, part.answer, part.modelAnswer, part.explanation);
    };
    partDiv.appendChild(checkButton);

    // Model & feedback box
    const modelDiv = document.createElement("div");
    modelDiv.id = `model-${index}`;
    modelDiv.style.display = "none";
    modelDiv.style.marginTop = "10px";
    modelDiv.style.padding = "10px";
    modelDiv.style.borderRadius = "8px";
    partDiv.appendChild(modelDiv);

    container.appendChild(partDiv);
  });

  // Diagram if any
  const canvas = document.getElementById("diagram-canvas");
  if (typeof qData.diagram === "function") {
    canvas.style.display = "block";
    qData.diagram(canvas);
  } else {
    canvas.style.display = "none";
  }
}

function checkPartAnswer(index, correctAnswer, modelAnswer, explanation) {
  // Fetch input
  const inputRaw = document.getElementById(`answer-${index}`).value.trim();
  const input = inputRaw.replace("%", "").trim(); // strip % for numbers

  // Show model/feedback container
  const modelDiv = document.getElementById(`model-${index}`);
  modelDiv.style.display = "block";

  const lowerInput = input.toLowerCase();
  const partData = window.currentQuestionData.parts[index];
  const partMarks = partData.marks;

  // Flags
  let c1FirstAwarded = false;
  let c1SecondAwarded = false;
  let aMarkAwarded = false;

  // 1) Special percentage-uncertainty working checks
  if (partData.partText.includes("percentage uncertainty")) {
    const fractionRegex = /\d+(\.\d+)?\s*\/\s*\d+(\.\d+)?/;
    if (fractionRegex.test(lowerInput)) c1FirstAwarded = true;
    const plusCount = (lowerInput.match(/\+/g) || []).length;
    if (plusCount >= 2) c1SecondAwarded = true;
  } else {
    // 2) Keyword checking for definitions & method steps
    if (Array.isArray(partData.keywords)) {
      let allGroups = true;
      for (let group of partData.keywords) {
        if (!group.some((kw) => lowerInput.includes(kw.toLowerCase()))) {
          allGroups = false;
          break;
        }
      }
      if (allGroups) c1FirstAwarded = true;
    }
  }

  // 3) Final-answer (A1) check
  if (typeof correctAnswer === "string" && input === correctAnswer) {
    aMarkAwarded = true;
    c1FirstAwarded = true;
    c1SecondAwarded = true;
  }

  // 4) Award marks in one pass: B1/M1, C1, C1-sum, A1
  partMarks.forEach((mark) => {
    if (!mark.awarded) {
      if (
        (mark.point.includes("(B1)") || mark.point.includes("(M1)")) &&
        c1FirstAwarded
      ) {
        mark.awarded = true;
        totalMarksEarned++;
      }
      if (
        mark.point.includes("(C1)") &&
        ((mark.point.includes("fractional") && c1FirstAwarded) ||
          (mark.point.includes("sum") && c1SecondAwarded))
      ) {
        mark.awarded = true;
        totalMarksEarned++;
      }
      if (
        mark.point.includes("(C1)") &&
        !mark.point.includes("fractional") &&
        !mark.point.includes("sum") &&
        c1FirstAwarded
      ) {
        mark.awarded = true;
        totalMarksEarned++;
      }
      if (mark.point.includes("(A1)") && aMarkAwarded) {
        mark.awarded = true;
        totalMarksEarned++;
      }
    }
  });

  // 5) Update per-part score display
  const earned = partMarks.filter((m) => m.awarded).length;
  const possible = partMarks.length;
  document.getElementById(
    `score-${index}`
  ).textContent = `(${earned}/${possible})`;

  // 6) Feedback styling
  const hasSingle = partMarks.some(
    (m) => m.awarded && (m.point.includes("(B1)") || m.point.includes("(M1)"))
  );
  if (
    aMarkAwarded ||
    (c1FirstAwarded && possible === 1) ||
    (c1FirstAwarded && hasSingle)
  ) {
    modelDiv.innerHTML = `<strong>Correct!</strong><br><br>Model Answer:<br>${modelAnswer}`;
    modelDiv.style.border = "2px solid green";
  } else if (c1FirstAwarded || c1SecondAwarded) {
    modelDiv.innerHTML = `<strong>You're nearly there!</strong><br><br>You have correctly set up the method.<br>Now substitute or combine carefully to get the final answer.<br><br><strong>Model Answer:</strong><br>${modelAnswer}`;
    modelDiv.style.border = "2px solid orange";
  } else {
    modelDiv.innerHTML = `<strong>Not quite right.</strong><br><br><em>Hint:</em><br>${explanation}<br><br><strong>Model Answer:</strong><br>${modelAnswer}`;
    modelDiv.style.border = "2px solid red";
  }

  // 7) Update the TOTAL score display
  updateScoreDisplay();
}

// Auto-load first question
window.onload = loadRandomQuestion;
