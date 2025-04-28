function loadRandomQuestion() {
  const question = questions[Math.floor(Math.random() * questions.length)];
  const questionData = question.question();

  const container = document.getElementById("question-container");
  container.innerHTML = ""; // Clear previous question

  // Add the main intro text
  const intro = document.createElement("h2");
  intro.textContent = questionData.mainText;
  container.appendChild(intro);

  // Now loop over each part
  questionData.parts.forEach((part, index) => {
    // Create a div for each part
    const partDiv = document.createElement("div");
    partDiv.classList.add("question-part");
    partDiv.style.marginBottom = "30px";

    // Part text
    const partText = document.createElement("p");
    partText.innerHTML = part.partText;
    partDiv.appendChild(partText);

    // Student answer box
    const answerInput = document.createElement("textarea");
    answerInput.id = `answer-${index}`;
    answerInput.rows = 3;
    answerInput.cols = 60;
    partDiv.appendChild(answerInput);

    // Check button
    const checkButton = document.createElement("button");
    checkButton.textContent = "Check Answer";
    checkButton.style.display = "block";
    checkButton.style.marginTop = "10px";
    checkButton.onclick = function() {
      checkPartAnswer(index, part.answer, part.modelAnswer);
    };
    partDiv.appendChild(checkButton);

    // Div to show model answer after checking
    const modelDiv = document.createElement("div");
    modelDiv.id = `model-${index}`;
    modelDiv.style.display = "none";
    modelDiv.style.marginTop = "10px";
    modelDiv.style.backgroundColor = "#f9f9f9";
    modelDiv.style.padding = "10px";
    modelDiv.style.borderRadius = "8px";
    partDiv.appendChild(modelDiv);

    container.appendChild(partDiv);
  });

  // If the question has a diagram to draw
  if (questionData.diagram) {
    questionData.diagram(document.getElementById("diagram-canvas"));
  }
}

function checkPartAnswer(index, correctAnswer, modelAnswer) {
  const input = document.getElementById(`answer-${index}`).value.trim();
  const modelDiv = document.getElementById(`model-${index}`);

  modelDiv.style.display = "block";

  if (input.toLowerCase() === correctAnswer.toLowerCase()) {
    modelDiv.innerHTML = "<strong>Correct!</strong><br><br>Model Answer:<br>" + modelAnswer;
    modelDiv.style.border = "2px solid green";
  } else {
    modelDiv.innerHTML = "<strong>Not quite right.</strong><br><br>Model Answer:<br>" + modelAnswer;
    modelDiv.style.border = "2px solid red";
  }
}
