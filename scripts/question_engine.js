// scripts/question_engine.js

function loadRandomQuestion() {
  // Pick a random question
  const question = questions[Math.floor(Math.random() * questions.length)];
  const qData = question.question();

  // Reset and tally marks for this question
  totalMarksEarned = 0;
  totalMarksPossible = qData.parts.reduce((sum, p) => sum + p.marks.length, 0);
  sessionMarksPossible += totalMarksPossible;
  updateScoreDisplay();

  // Make current question available for marking
  window.currentQuestionData = qData;

  // Render the question
  const container = document.getElementById("question-container");
  container.innerHTML = "";

  const intro = document.createElement("h2");
  intro.textContent = qData.mainText;
  container.appendChild(intro);

  qData.parts.forEach((part, index) => {
    const partDiv = document.createElement("div");
    partDiv.classList.add("question-part");

    const partText = document.createElement("p");
    partText.innerHTML = part.partText;
    partDiv.appendChild(partText);

    const answerInput = document.createElement("textarea");
    answerInput.id = `answer-${index}`;
    answerInput.rows = 3;
    answerInput.cols = 60;
    partDiv.appendChild(answerInput);

    const checkButton = document.createElement("button");
    checkButton.textContent = "Check Answer";
    checkButton.onclick = function() {
      checkPartAnswer(
        index,
        part.answer,
        part.modelAnswer,
        part.explanation
      );
    };
    partDiv.appendChild(checkButton);

    const modelDiv = document.createElement("div");
    modelDiv.id = `model-${index}`;
    modelDiv.style.display = "none";
    modelDiv.style.marginTop = "10px";
    modelDiv.style.padding = "10px";
    modelDiv.style.borderRadius = "8px";
    partDiv.appendChild(modelDiv);

    container.appendChild(partDiv);
  });

  // Show or hide the diagram canvas
  const canvas = document.getElementById("diagram-canvas");
  if (typeof qData.diagram === "function") {
    canvas.style.display = "block";
    qData.diagram(canvas);
  } else {
    canvas.style.display = "none";
  }
}

// Award marks only once per part and show model/hint
function checkPartAnswer(index, correctAnswer, modelAnswer, explanation) {
  const input = document.getElementById(`answer-${index}`).value.trim();
  const modelDiv = document.getElementById(`model-${index}`);
  modelDiv.style.display = "block";

  // Award unawarded marks for this part
  const partMarks = window.currentQuestionData.parts[index].marks;
  partMarks.forEach(mark => {
    if (!mark.awarded) {
      mark.awarded = true;
      totalMarksEarned++;
    }
  });
  updateScoreDisplay();

  // Show feedback
// Determine match: single string or any entry in an array
  let isCorrect;
  if (Array.isArray(correctAnswer)) {
    isCorrect = correctAnswer.some(ans => input === ans.toLowerCase());
  } else {
    isCorrect = input === correctAnswer.toLowerCase();
  }
  if (isCorrect) {
    modelDiv.innerHTML =
      "<strong>Correct!</strong><br><br>Model Answer:<br>" + modelAnswer;
    modelDiv.style.border = "2px solid green";
  } else {
    modelDiv.innerHTML =
      "<strong>Not quite right.</strong><br><br><em>Hint:</em><br>" +
      explanation +
      "<br><br>Model Answer:<br>" +
      modelAnswer;
    modelDiv.style.border = "2px solid red";
  }
}

// Ensure the first question loads on page open
window.onload = loadRandomQuestion;
