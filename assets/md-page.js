(function () {
  const script = document.currentScript;
  const src = script.getAttribute("data-md");
  const targetSel = script.getAttribute("data-target") || "#md-body";

  function escapeHtml(s) {
    return s
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function inline(s) {
    s = escapeHtml(s);
    s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
    s = s.replace(/`([^`]+)`/g, "<code>$1</code>");
    s = s.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    s = s.replace(/_([^_]+)_/g, "<em>$1</em>");
    return s;
  }

  function render(md) {
    const lines = md.replace(/\r\n/g, "\n").split("\n");
    let html = "";
    let para = [];
    function flushPara() {
      if (!para.length) return;
      html += "<p>" + inline(para.join(" ")) + "</p>";
      para = [];
    }
    for (const line of lines) {
      if (/^### /.test(line)) {
        flushPara();
        html += "<h3>" + inline(line.slice(4)) + "</h3>";
      } else if (/^## /.test(line)) {
        flushPara();
        html += "<h2>" + inline(line.slice(3)) + "</h2>";
      } else if (/^# /.test(line)) {
        flushPara();
        html += "<h1>" + inline(line.slice(2)) + "</h1>";
      } else if (line.trim() === "") {
        flushPara();
      } else {
        para.push(line);
      }
    }
    flushPara();
    return html;
  }

  const mount = document.querySelector(targetSel);
  if (!mount || !src) return;

  fetch(src)
    .then(function (r) {
      if (!r.ok) throw new Error(String(r.status));
      return r.text();
    })
    .then(function (md) {
      mount.innerHTML = render(md);
    })
    .catch(function () {
      mount.innerHTML =
        "<p>这边无法渲染 Markdown。请打开 <a href=\"" +
        src +
        "\">" +
        src +
        "</a>（用本地 HTTP 服务打开本站即可，不要直接双击 HTML）。</p>";
    });
})();
