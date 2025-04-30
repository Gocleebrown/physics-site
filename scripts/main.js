// scripts/main.js

let totalMarksEarned = 0;
let totalMarksPossible = 0;
let sessionMarksEarned = 0;
let sessionMarksPossible = 0;

function resetQuestionScores() {
  sessionMarksEarned += totalMarksEarned;
  sessionMarksPossible += totalMarksPossible;
  totalMarksEarned = 0;
  totalMarksPossible = 0;
}

function updateScoreDisplay() {
  const div = document.getElementById("score-display");
  div.textContent =
    `Question Score: ${totalMarksEarned} / ${totalMarksPossible}` +
    ` | Session Score: ${sessionMarksEarned + totalMarksEarned} / ${
      sessionMarksPossible + totalMarksPossible
    }`;
}
