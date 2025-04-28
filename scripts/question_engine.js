function loadRandomQuestion() {
  const question = questions[Math.floor(Math.random() * questions.length)];
  const questionData = question.question();

  document.getElementById("question-title").innerHTML = questionData.text;

  if (questionData.drawDiagram) {
    questionData.drawDiagram(document.getElementById("diagram-canvas"));
  }
}

function checkAnswer() {
  // Placeholder for future checking logic
}
