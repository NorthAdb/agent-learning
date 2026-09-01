(function () {
  /**
   * vscode:// 在同时装了 VS Code 的机器上会被 VS Code 抢走。
   * 书路径含空格时，未编码的 href 会在空格处截断。一律改成 cursor:// 并 encodeURI。
   */
  function encodeSourceFileHrefs() {
    document.querySelectorAll(
      'a[href^="vscode://file/"], a[href^="cursor://file/"]'
    ).forEach(function (a) {
      const href = a.getAttribute("href") || "";
      const m = href.match(/^(?:vscode|cursor):\/\/file\/(.+)$/);
      if (!m) return;
      const rest = m[1];
      const lineCol = rest.match(/(:\d+(?::\d+)?)$/);
      if (!lineCol) return;
      let path = rest.slice(0, -lineCol[1].length);
      try {
        path = decodeURI(path);
      } catch (e) {
        /* keep path */
      }
      a.setAttribute("href", "cursor://file/" + encodeURI(path) + lineCol[1]);
    });
  }
  encodeSourceFileHrefs();

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

  /** Path of a lesson file relative to lessons/. */
  function fileOf(lesson) {
    return lesson.file;
  }

  function dirSegs(file) {
    const i = file.lastIndexOf("/");
    if (i < 0) return [];
    return file.slice(0, i).split("/");
  }

  function basename(file) {
    const i = file.lastIndexOf("/");
    return i < 0 ? file : file.slice(i + 1);
  }

  /** Relative URL from one lessons/* file to another (or to lessons/index.html). */
  function relUrl(fromFile, toFile) {
    const from = dirSegs(fromFile);
    const toDir = dirSegs(toFile);
    const name = basename(toFile);
    let i = 0;
    while (i < from.length && i < toDir.length && from[i] === toDir[i]) i += 1;
    const up = from.length - i;
    const down = toDir.slice(i);
    const prefix =
      (up ? "../".repeat(up) : "./") + (down.length ? down.join("/") + "/" : "");
    return prefix + name;
  }

  function homeUrl(fromFile) {
    const depth = dirSegs(fromFile).length;
    return (depth ? "../".repeat(depth) : "./") + "index.html";
  }

  function renderNav(lessonId) {
    const i = byId(lessonId);
    if (i < 0) return "";
    const prev = list[i - 1];
    const next = list[i + 1];
    const cur = list[i];
    const here = fileOf(cur);
    return `
      <nav class="lesson-nav" aria-label="课件导航">
        <div class="lesson-nav-links">
          ${link(homeUrl(here), "首页", true)}
          <span class="nav-sep">·</span>
          ${link(prev ? relUrl(here, fileOf(prev)) : "#", "上一课", !!prev)}
          <span class="nav-sep">·</span>
          ${link(next ? relUrl(here, fileOf(next)) : "#", "下一课", !!next)}
        </div>
        <p class="meta lesson-nav-meta">Lesson ${cur.id} · 阶段 ${cur.phase} · 约 ${cur.duration}</p>
      </nav>`;
  }

  document.querySelectorAll("[data-lesson-id]").forEach((el) => {
    const id = el.getAttribute("data-lesson-id");
    el.outerHTML = renderNav(id);
  });

  document.querySelectorAll("[data-lesson-id-footer]").forEach((el) => {
    const id = el.getAttribute("data-lesson-id-footer");
    el.outerHTML = renderNav(id).replace(
      'aria-label="课件导航"',
      'aria-label="课件导航（文末）"'
    );
  });
})();
