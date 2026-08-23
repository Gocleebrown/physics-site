// scripts/main.js

let totalMarksEarned = 0;
let totalMarksPossible = 0;
let sessionMarksEarned = 0;
let sessionMarksPossible = 0;
window.currentQuestionId = null;

function resetQuestionScores() {
  sessionMarksEarned += totalMarksEarned;
  sessionMarksPossible += totalMarksPossible;
  totalMarksEarned = 0;
  totalMarksPossible = 0;
}

// persistAttempt: true only when called after an actual answer check (not
// on initial question load) - otherwise every question would be recorded
// as "attempted at 0%" the instant it's displayed, before the student has
// done anything.
function updateScoreDisplay(persistAttempt) {
  const div = document.getElementById("score-display");
  div.textContent =
    `Question Score: ${totalMarksEarned} / ${totalMarksPossible}` +
    ` | Session Score: ${sessionMarksEarned + totalMarksEarned} / ${
      sessionMarksPossible + totalMarksPossible
    }`;

  if (persistAttempt && window.currentQuestionId && totalMarksPossible > 0) {
    const percent = (totalMarksEarned / totalMarksPossible) * 100;
    window.saveScoreForQuestion(window.currentQuestionId, percent);
  }
}
