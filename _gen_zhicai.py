# -*- coding: utf-8 -*-
"""Generate 智采灵枢.html — the project-01 reader. Reuses the canonical <style>
from 万物的客舍.html, adds 智采灵枢-specific rules (.rate-big + 16/10 figure),
two image-slot figures, and loads image-slot.js."""
import os, re
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "万物的客舍.html"), encoding="utf-8") as f:
    STYLE = re.search(r"<style>.*?</style>", f.read(), re.S).group(0)

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com" />\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />\n'
         '<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;500;700'
         '&family=Noto+Sans+SC:wght@300;400;500&family=Space+Mono:ital,wght@0,400;0,700;1,400'
         '&display=swap" rel="stylesheet" />')

# 智采灵枢-specific overrides (cascade after the shared block)
OVERRIDE = """<style>
  /* ---- 智采灵枢 specifics ---- */
  .chap .hot{ color:var(--terra); font-weight:500; }
  .chap .rate-big{
    color:var(--terra); font-weight:700; font-family:var(--mono); font-size:1.05em;
    letter-spacing:0; padding:0 .12em;
  }
  .fig-frame{ aspect-ratio:16/10; }
  .fig-frame::after{ display:none; }
  .fig-img::part(img){ filter:grayscale(.7) contrast(1.02); }
  .fig:hover .fig-img::part(img){ filter:grayscale(0); }
</style>"""

JS = r"""<script>
(function () {
  "use strict";
  (function () {
    var fine = window.matchMedia("(pointer: fine)").matches;
    document.documentElement.classList.toggle("cursor-custom", fine);
    if (!fine) return;
    var ring = document.querySelector(".cursor-ring");
    var dot = document.querySelector(".cursor-dot");
    var t = { x: innerWidth / 2, y: innerHeight / 2 };
    var rp = { x: t.x, y: t.y }, dp = { x: t.x, y: t.y };
    addEventListener("pointermove", function (e) { t.x = e.clientX; t.y = e.clientY; });
    document.querySelectorAll("[data-hot]").forEach(function (el) {
      el.addEventListener("pointerenter", function () { ring.classList.add("is-hot"); });
      el.addEventListener("pointerleave", function () { ring.classList.remove("is-hot"); });
    });
    (function loop() {
      rp.x += (t.x - rp.x) * 0.18; rp.y += (t.y - rp.y) * 0.18;
      dp.x += (t.x - dp.x) * 0.5;  dp.y += (t.y - dp.y) * 0.5;
      ring.style.transform = "translate3d(" + rp.x + "px," + rp.y + "px,0) translate(-50%,-50%)";
      dot.style.transform  = "translate3d(" + dp.x + "px," + dp.y + "px,0) translate(-50%,-50%)";
      requestAnimationFrame(loop);
    })();
  })();
  function goBack(e) { e.preventDefault(); document.body.classList.add("leaving"); setTimeout(function () { window.location.href = "index.html"; }, 480); }
  var back = document.getElementById("navBack"); if (back) back.addEventListener("click", goBack);
  var pgHome = document.getElementById("pgHome"); if (pgHome) pgHome.addEventListener("click", goBack);
  document.querySelectorAll(".toc-link").forEach(function (link) {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      var el = document.getElementById(link.getAttribute("data-spy"));
      if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });
  (function () {
    var links = [].slice.call(document.querySelectorAll(".toc-link"));
    var els = links.map(function (l) { return document.getElementById(l.getAttribute("data-spy")); }).filter(Boolean);
    var raf = 0;
    function compute() {
      raf = 0;
      var line = innerHeight * 0.35;
      var current = els[0] ? els[0].id : null;
      els.forEach(function (el) { if (el.getBoundingClientRect().top <= line) current = el.id; });
      if (innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4) current = els[els.length - 1] ? els[els.length - 1].id : current;
      links.forEach(function (l) { l.classList.toggle("active", l.getAttribute("data-spy") === current); });
    }
    function onScroll() { if (!raf) raf = requestAnimationFrame(compute); }
    addEventListener("scroll", onScroll, { passive: true });
    addEventListener("resize", onScroll);
    compute();
  })();
  (function () {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { threshold: 0.15 });
    document.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });
  })();
})();
</script>"""

TOC = [("01", "ch-pain", "痛点与机会"),
       ("02", "ch-struct", "机械结构设计"),
       ("03", "ch-ui", "双端交互系统"),
       ("04", "ch-result", "核心成果")]
toc = "\n".join(
    '          <li><a class="toc-link%s" href="#%s" data-hot data-spy="%s"><span class="tn">%s</span>%s</a></li>'
    % (" active" if i == 0 else "", cid, cid, no, label)
    for i, (no, cid, label) in enumerate(TOC))

HTML = f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>智采灵枢 — 项目详情 / 刘思敏</title>
{FONTS}
{STYLE}
{OVERRIDE}
</head>
<body>
  <div class="atmos" aria-hidden="true"></div>
  <div class="grain" aria-hidden="true"></div>

  <nav class="nav">
    <a class="nav-back" href="index.html" data-hot id="navBack">
      <span class="ba">&larr;</span> Back
    </a>
    <div class="nav-right">
      <a class="nav-about" href="about.html" data-hot>关于</a>
      <span class="nav-prog"><b>01</b> / 08</span>
    </div>
  </nav>

  <h1 class="head-title">智采灵枢</h1>

  <div class="shell">
    <header class="head reveal">
      <div class="head-eyebrow">Graduation Project&nbsp;&nbsp;/&nbsp;&nbsp;Hardware Interaction</div>
      <p class="head-intro">一台为名优茶量身设计的智能采摘设备。以骑跨式履带底盘与温控保鲜舱，把机械化采摘的效率与手工采摘的品质留在同一台机器里。</p>
    </header>

    <div class="meta reveal">
      <div class="meta-cell">
        <div class="meta-k">时间 / Timeline</div>
        <div class="meta-v">2025.01 <span>—</span> 2025.06</div>
      </div>
      <div class="meta-cell">
        <div class="meta-k">角色 / Role</div>
        <div class="meta-v">项目负责人 <span>/</span> 交互设计师</div>
      </div>
      <div class="meta-cell">
        <div class="meta-k">工具 / Tools</div>
        <div class="meta-v">Rhino · Keyshot · Figma · Arduino</div>
      </div>
    </div>

    <div class="role-note reveal">
      <div class="role-note-k">个人贡献 / My Role</div>
      <p class="role-note-t">作为<b>项目负责人</b>，我主导了从用户研究到落地的全流程：独立完成采茶机的<b>机械结构建模</b>（骑跨式履带底盘、双温区保鲜舱），并设计了<b>操作员端 / 管理员端双端交互系统</b>；统筹团队推进 Rhino 建模、Keyshot 渲染与 Figma 界面的整合，最终把鲜叶红变率从 &gt;15% 压到 &lt;5%。</p>
    </div>

    <div class="story">
      <aside class="toc">
        <div class="toc-label">Contents</div>
        <ul class="toc-list">
{toc}
        </ul>
      </aside>

      <div class="main">
        <section class="chap reveal" id="ch-pain">
          <span class="chap-no">01 — Pain &amp; Opportunity</span>
          <h2 class="chap-h">痛点与机会</h2>
          <p>名优茶讲究「一芽一两叶」的手工采摘，但采茶季高度集中、用工成本逐年攀升，熟练采茶工日益短缺。靠人，已经越来越难。</p>
          <p>传统机械采摘「一刀切」，鲜叶破损严重；离开茶树后若不及时降温，<span class="hot">红变率常超过 15%</span>，直接拉低成品等级与售价。机会因此清晰——做一台能「轻拿轻放」并即时保鲜的设备，把效率与品质同时留下。</p>
          <figure class="fig">
            <div class="fig-frame" data-hot>
              <image-slot id="r-hero" class="fig-img" shape="rect" fit="cover" src="images/zhicai-field2.jpg" placeholder="采茶机整机 / 工业渲染 · 16:10"></image-slot>
            </div>
            <figcaption class="fig-cap"><b>Field</b><span>茶园实采 · 应用场景</span></figcaption>
          </figure>
        </section>

        <section class="chap reveal" id="ch-struct">
          <span class="chap-no">02 — Mechanical</span>
          <h2 class="chap-h">机械结构设计</h2>
          <p>整机采用<strong>骑跨式履带底盘</strong>，跨越田垄行进；重做履带齿距与张紧机构，抑制松软茶园里的打滑。采摘端以柔性夹持配合切割分离，减少对芽叶的挤压损伤。</p>
          <p>采下的鲜叶经输送通道进入<strong>温控保鲜舱</strong>——舱体分两个温区，先快速降温锁鲜，再恒温暂存，从源头压制红变的发生。</p>
          <figure class="fig">
            <div class="fig-frame" data-hot>
              <image-slot id="r-structure" class="fig-img" shape="rect" fit="cover" src="images/zhicai-render.jpg" placeholder="机械结构 / 爆炸图 · Rhino 截图"></image-slot>
            </div>
            <figcaption class="fig-cap"><b>Keyshot</b><span>整机形态 · 履带底盘</span></figcaption>
          </figure>
        </section>

        <section class="chap reveal" id="ch-ui">
          <span class="chap-no">03 — Interaction</span>
          <h2 class="chap-h">双端交互系统</h2>
          <p>设备配套<strong>操作员端</strong>与<strong>管理员端</strong>两套界面，按「现场执行 / 全局管理」分层。</p>
          <p>操作员端服务田间作业：实时显示行进路径、采净率与舱温，关键操作放大、可单手完成，开机即用。管理员端沉淀产量、设备状态与作业数据，支持多机调度与历史回溯。信息各取所需，互不干扰。</p>
          <figure class="fig">
            <div class="fig-frame" data-hot>
              <image-slot id="r-interface" class="fig-img" shape="rect" fit="cover" src="images/zhicai-ui.jpg" placeholder="双端界面 · Figma 深色模式截图"></image-slot>
            </div>
            <figcaption class="fig-cap"><b>Figma / Dark Mode</b><span>操作员端 + 管理员后台</span></figcaption>
          </figure>
        </section>

        <section class="chap reveal" id="ch-result">
          <span class="chap-no">04 — Outcome</span>
          <h2 class="chap-h">核心成果</h2>
          <p>通过结构与温控的协同，鲜叶红变率由传统机械采摘的 &gt;15% 压制到 <span class="rate-big">&lt;5%</span>，结构方案经验证 100% 可行。</p>
          <p>项目作为毕业设计完整落地，覆盖从用户研究、机械建模到双端交互的全流程——也是我对「工程逻辑与美学体验平衡」最完整的一次实践。</p>
        </section>
      </div>
    </div>
  </div>

  <nav class="pager">
    <a class="pg-prev" href="index.html" data-hot id="pgHome">
      <span class="pg-k"><span class="pa">&larr;</span> 上一页</span>
      <div class="pg-cn">主页</div>
      <div class="pg-en">Homepage</div>
    </a>
    <a class="pg-next" href="万物的客舍.html" data-hot>
      <span class="pg-k">下一页 <span class="pa">&rarr;</span></span>
      <div class="pg-cn">万物的客舍</div>
      <div class="pg-en">Everything&apos;s Inn</div>
    </a>
  </nav>

  <div class="cursor-ring" aria-hidden="true"></div>
  <div class="cursor-dot" aria-hidden="true"></div>

  <script src="image-slot.js"></script>
  <script src="atmosphere.js"></script>
  <script src="hero-morph.js"></script>
  <script src="fig-fit.js"></script>
{JS}
</body>
</html>
"""

with open(os.path.join(BASE, "智采灵枢.html"), "w", encoding="utf-8") as f:
    f.write(HTML)
print("wrote 智采灵枢.html")
