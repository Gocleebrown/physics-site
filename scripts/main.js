// scripts/main.js

// Globals for current question marks
let totalMarksEarned = 0;
let totalMarksPossible = 0;

// Globals for session totals
let sessionMarksEarned = 0;
let sessionMarksPossible = 0;

// Updates (or creates) the on-page score display
function updateScoreDisplay() {
  let scoreDiv = document.getElementById("score-display");
  if (!scoreDiv) {
    scoreDiv = document.createElement("div");
    scoreDiv.id = "score-display";
    scoreDiv.style.margin = "20px";
    document.body.insertBefore(scoreDiv, document.getElementById("question-container"));
  }
  scoreDiv.textContent =
    `Question Score: ${totalMarksEarned} / ${totalMarksPossible}` +
    ` | Session Score: ${sessionMarksEarned + totalMarksEarned} / ${sessionMarksPossible + totalMarksPossible}`;
}

// Navigate from index.html → practice.html
function startPractice() {
  window.location.href = "practice.html";
}
