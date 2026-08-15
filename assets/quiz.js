(function () {
  document.querySelectorAll("[data-quiz]").forEach((quiz) => {
    const feedback = quiz.querySelector(".feedback");
    const okText = quiz.getAttribute("data-ok") || "回答正确。";
    const badText = quiz.getAttribute("data-bad") || "再想一想。";
    quiz.querySelectorAll("button").forEach((btn) => {
      btn.addEventListener("click", () => {
        quiz.querySelectorAll("button").forEach((b) => {
          b.classList.remove("correct", "wrong");
          b.disabled = true;
        });
        const ok = btn.dataset.correct === "true";
        btn.classList.add(ok ? "correct" : "wrong");
        if (!ok) {
          const right = quiz.querySelector('button[data-correct="true"]');
          if (right) right.classList.add("correct");
        }
        if (feedback) feedback.textContent = ok ? okText : badText;
      });
    });
  });
})();
