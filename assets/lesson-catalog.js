(function () {
  const list = window.LESSON_CURRICULUM || [];
  const root = document.querySelector("[data-lesson-catalog]");
  if (!root) return;

  if (!list.length) {
    root.innerHTML = "<p class='muted'>暂无课程。</p>";
    return;
  }

  const byPhase = {};
  list.forEach((l) => {
    (byPhase[l.phase] ||= []).push(l);
  });

  const phaseLabel = {
    "0": "阶段 0 · Python 地基（lessons/phase-0/）",
    "1": "阶段 1 · 心智模型（lessons/phase-1/）",
    "2": "阶段 2 · 最小 harness",
    "3": "阶段 3 · 上下文与记忆",
  };

  let html = "";
  Object.keys(byPhase)
    .sort()
    .forEach((phase) => {
      html += `<h2>${phaseLabel[phase] || "阶段 " + phase}</h2><ol class="catalog">`;
      byPhase[phase].forEach((l) => {
        html += `<li>
          <a href="./${l.file}"><strong>${l.id}</strong> · ${l.title}</a>
          <span class="muted"> · 约 ${l.duration}</span>
        </li>`;
      });
      html += "</ol>";
    });

  root.innerHTML = html;
})();
