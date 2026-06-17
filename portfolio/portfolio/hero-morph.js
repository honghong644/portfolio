/* ============================================================================
   hero-morph.js — Shrinking Hero Header (收缩式英雄标题)
   作品集详情页通用动效：巨大的中文标题（陶土色 #C97B63, 字重 700, Hero 中央）
   随页面上滚平滑缩小、上移，最终锁进顶部导航栏，变成暖白 (#F5F5F5)、字重 500
   的紧凑标题；下滚回顶部时反向丝滑还原。

   实现要点（对照需求）：
   · 滚动驱动：进度 = clamp(scrollY / 阈值, 0, 1)，严格绑定滚动距离。
   · 非线性：进度经 ease-out 三次曲线映射（开始快、结束慢，像刹车的惯性）。
   · 形变：scale 1.0 → 0.4、translateY 居中 → 顶部、字重 700 → 500、色 陶土 → 暖白，
     全程连续插值，无跳切、无透明度突变。
   · 只用 transform（标题为 position:fixed，脱离文档流），绝不改 height/width，
     不影响下方内容布局。
   · 视差：标题变形的同时，背景宣纸颗粒纹理随进度缓慢位移，形成视差感。
   尊重 prefers-reduced-motion（去缓动与视差，仍可随滚动还原）。
   用法：详情页 <body> 末尾 <script src="hero-morph.js"></script>
============================================================================ */
(function () {
  "use strict";
  var title = document.querySelector(".head-title");
  if (!title) return;

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var grain = document.querySelector(".grain");
  var paper = null; // .atmos-paper is injected by atmosphere.js (may not exist yet)

  // 陶土 #C97B63 → 暖白 #F5F5F5
  var C0 = [201, 123, 99], C1 = [245, 245, 245];
  var lerp = function (a, b, t) { return a + (b - a) * t; };
  // ease-out cubic — 开始快、结束慢（惯性/刹车感）
  var easeOut = function (p) { return 1 - Math.pow(1 - p, 3); };

  var THRESH = 1, contentLeft = 48, compactLeft = 160, heroY = 200;
  function recalc() {
    THRESH = Math.max(1, Math.min(innerHeight * 0.46, 420));
    // 左上角对齐：标题左边缘 = 内容列左边缘（shell max-width:1360 居中 + 内边距 clamp(20,4vw,48)）
    var pad = Math.min(48, Math.max(20, innerWidth * 0.04));
    contentLeft = Math.max(0, (innerWidth - 1360) / 2) + pad;
    // 锁定态：移到「← Back」右侧，仍在左侧（绝不居中）
    var navPad = Math.min(56, Math.max(20, innerWidth * 0.05));
    compactLeft = navPad + (innerWidth < 560 ? 84 : 104);
    heroY = innerHeight * 0.22; // Hero 区上部，位于 eyebrow 之下
  }
  recalc();

  var raf = 0;
  function update() {
    raf = 0;
    var p = Math.min(1, Math.max(0, window.scrollY / THRESH));
    var pe = reduce ? p : easeOut(p);

    var scale = lerp(1.0, 0.4, pe);                 // 1.0 → 0.4
    var tx = lerp(contentLeft, compactLeft, pe);    // 内容列左缘 → Back 右侧（始终靠左）
    var ty = lerp(heroY, 0, pe);                    // Hero 上部 → 顶部 (top:18px)
    var weight = Math.round(lerp(700, 500, pe));    // 700 → 500
    var col = "rgb(" + Math.round(lerp(C0[0], C1[0], pe)) + "," +
                       Math.round(lerp(C0[1], C1[1], pe)) + "," +
                       Math.round(lerp(C0[2], C1[2], pe)) + ")";

    title.style.transform = "translate(" + tx.toFixed(1) + "px," + ty.toFixed(1) + "px) scale(" + scale.toFixed(3) + ")";
    title.style.color = col;
    title.style.fontWeight = weight;

    // 背景宣纸颗粒视差 —— 与标题形变同步，缓慢位移（限幅，避免露边）
    if (!reduce) {
      if (grain) grain.style.transform = "translate3d(0," + (pe * 54).toFixed(1) + "px,0)";
      if (!paper) paper = document.querySelector(".atmos-paper");
      if (paper) paper.style.transform = "translate3d(0," + (pe * 30).toFixed(1) + "px,0)";
    }
  }

  function onScroll() { if (!raf) raf = requestAnimationFrame(update); }
  addEventListener("scroll", onScroll, { passive: true });
  addEventListener("resize", function () { recalc(); onScroll(); });
  update();
})();
