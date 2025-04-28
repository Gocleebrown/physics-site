+ // === Score Tracking Globals ===
 let totalMarksEarned = 0;
 let totalMarksPossible = 0;

 // Updates (or creates) the on‐page score display
 function updateScoreDisplay() {
   let scoreDiv = document.getElementById("score-display");
   if (!scoreDiv) {
     scoreDiv = document.createElement("div");
     scoreDiv.id = "score-display";
     scoreDiv.style.margin = "20px";
     document.body.insertBefore(scoreDiv, document.getElementById("question-container"));
   }
   scoreDiv.textContent = `Score: ${totalMarksEarned} / ${totalMarksPossible}`;
 }

  // Navigate from index.html → practice.html
  function startPractice() {
    window.location.href = "practice.html";
  }

// Navigate from index.html → practice.html
function startPractice() {
  window.location.href = "practice.html";
}

// (submitAnswer() is no longer used and can be removed)
