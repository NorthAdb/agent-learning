(function () {
  const list = window.LESSON_CURRICULUM || [];
  if (!list.length) return;

  function byId(id) {
    return list.findIndex((l) => l.id === id);
  }

  function link(href, text, enabled) {
    if (!enabled) {
      return `<span class="nav-disabled">${text}</span>`;
    }
    return `<a href="${href}">${text}</a>`;
  }

  function renderNav(lessonId) {
    const i = byId(lessonId);
    if (i < 0) return "";
    const prev = list[i - 1];
    const next = list[i + 1];
    const cur = list[i];
    return `
      <nav class="lesson-nav" aria-label="课件导航">
        <div class="lesson-nav-links">
          ${link("./index.html", "首页", true)}
          <span class="nav-sep">·</span>
          ${link(prev ? "./" + prev.file : "#", "上一课", !!prev)}
          <span class="nav-sep">·</span>
          ${link(next ? "./" + next.file : "#", "下一课", !!next)}
        </div>
        <p class="meta lesson-nav-meta">Lesson ${cur.id} · 阶段 ${cur.phase} · 约 ${cur.duration}</p>
      </nav>`;
  }

  document.querySelectorAll("[data-lesson-id]").forEach((el) => {
    const id = el.getAttribute("data-lesson-id");
    el.outerHTML = renderNav(id);
  });

  // bottom nav: duplicate if marker present
  document.querySelectorAll("[data-lesson-id-footer]").forEach((el) => {
    const id = el.getAttribute("data-lesson-id-footer");
    el.outerHTML = renderNav(id).replace(
      'aria-label="课件导航"',
      'aria-label="课件导航（文末）"'
    );
  });
})();
