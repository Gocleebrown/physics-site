function loadRandomQuestion() {
  const question = questions[Math.floor(Math.random() * questions.length)];
  const questionData = question.question();

  const container = document.getElementById("question-container");
  container.innerHTML = ""; // Clear previous content

  // Main question heading
  const intro = document.createElement("h2");
  intro.textContent = questionData.mainText;
  container.appendChild(intro);

  // Loop through each sub-part
  questionData.parts.forEach((part, index) => {
    const partDiv = document.createElement("div");
    partDiv.classList.add("question-part");

    // Part prompt
    const partText = document.createElement("p");
    partText.innerHTML = part.partText;
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
    checkButton.onclick = function() {
      checkPartAnswer(index, part.answer, part.modelAnswer);
    };
    partDiv.appendChild(checkButton);

    // Model answer container
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
  if (typeof questionData.diagram === "function") {
    canvas.style.display = "block";
    questionData.diagram(canvas);
  } else {
    canvas.style.display = "none";
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
