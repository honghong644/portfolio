/* ============================================================================
   atmosphere.js — 宣纸 / 混凝土微距纹理层（陶土与深岩系统）
   在深岩石灰背景上叠加：
     1) 高分辨率宣纸/混凝土纤维纹理，透明度极低（~5%）。
     2) 极缓慢的「呼吸」——整层透明度在 4.5%–7.2% 之间微弱起伏（~9s）。
     3) 鼠标涟漪——光标附近的颗粒像被微风吹散一样向外排斥位移，再缓缓归位
        （「游鱼破水」）。canvas 仅在颗粒被扰动时绘制，静止时画布清空。
   单文件、自包含、幂等。尊重 prefers-reduced-motion 与触摸屏。
   用法：任意页面 <body> 末尾 <script src="atmosphere.js"></script>
============================================================================ */
(function () {
  "use strict";
  if (window.__atmos) return;
  window.__atmos = true;

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var coarse = window.matchMedia("(pointer: coarse)").matches;

  /* ---- 宣纸/混凝土纤维纹理：两层 fractalNoise（细颗粒 + 各向异性纤维）---- */
  var paperURI =
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E" +
    "%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E" +
    "%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E" +
    "%3Cfilter id='f'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.014 0.42' numOctaves='2' stitchTiles='stitch'/%3E" +
    "%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E" +
    "%3Crect width='100%25' height='100%25' filter='url(%23g)'/%3E" +
    "%3Crect width='100%25' height='100%25' filter='url(%23f)' opacity='0.4'/%3E%3C/svg%3E";

  var css =
    "@keyframes atmosBreath{0%,100%{opacity:.05}50%{opacity:.088}}" +
    ".atmos-paper{position:fixed;inset:-20px;z-index:1;pointer-events:none;" +
    "background-image:url(\"" + paperURI + "\");background-size:300px 300px;" +
    "mix-blend-mode:soft-light;opacity:.064;" +
    (reduce ? "" : "animation:atmosBreath 9s ease-in-out infinite;will-change:opacity;") + "}" +
    ".atmos-ripple{position:fixed;inset:0;z-index:1;pointer-events:none;}";
  var styleEl = document.createElement("style");
  styleEl.textContent = css;
  document.head.appendChild(styleEl);

  var paper = document.createElement("div");
  paper.className = "atmos-paper";
  paper.setAttribute("aria-hidden", "true");
  document.body.appendChild(paper);

  /* 触摸屏无光标、reduce 模式下只保留静态纹理，跳过涟漪 */
  if (reduce || coarse) return;

  /* ---- 鼠标涟漪：jittered 颗粒场，近光标向外排斥 + 弹簧归位 ---- */
  var cv = document.createElement("canvas");
  cv.className = "atmos-ripple";
  cv.setAttribute("aria-hidden", "true");
  document.body.appendChild(cv);
  var ctx = cv.getContext("2d");
  var dpr = Math.min(2, window.devicePixelRatio || 1);
  var S = 26;                 // 颗粒网格间距
  var W = 0, H = 0, parts = [];

  function build() {
    W = innerWidth; H = innerHeight;
    cv.width = W * dpr; cv.height = H * dpr;
    cv.style.width = W + "px"; cv.style.height = H + "px";
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.fillStyle = "#F5F5F5";
    parts = [];
    for (var y = 0; y <= H + S; y += S) {
      for (var x = 0; x <= W + S; x += S) {
        // home 位置加抖动，打散网格感，读起来像散落的纸纤维颗粒
        var hx = x + (Math.random() - 0.5) * S * 0.8;
        var hy = y + (Math.random() - 0.5) * S * 0.8;
        parts.push({ hx: hx, hy: hy, x: hx, y: hy, vx: 0, vy: 0, s: 0.8 + Math.random() * 0.9 });
      }
    }
  }
  build();
  addEventListener("resize", build);

  var mx = -9999, my = -9999, active = false, lastMove = 0;
  addEventListener("pointermove", function (e) {
    mx = e.clientX; my = e.clientY; active = true; lastMove = performance.now();
  });

  var R = 190, R2 = R * R;    // 影响半径
  function loop(now) {
    ctx.clearRect(0, 0, W, H);
    if (active && now - lastMove > 1400) active = false;  // 光标静止后涟漪归于平静
    for (var i = 0; i < parts.length; i++) {
      var p = parts[i];
      var ax = (p.hx - p.x) * 0.055, ay = (p.hy - p.y) * 0.055;  // 弹簧回家
      if (active) {
        var dx = p.x - mx, dy = p.y - my, d2 = dx * dx + dy * dy;
        if (d2 < R2) {
          var d = Math.sqrt(d2) || 1, f = 1 - d / R;
          var push = f * f * 3.2;                                // 越近推得越远
          ax += dx / d * push; ay += dy / d * push;
        }
      }
      p.vx = (p.vx + ax) * 0.85; p.vy = (p.vy + ay) * 0.85;
      p.x += p.vx; p.y += p.vy;
      var disp = Math.abs(p.x - p.hx) + Math.abs(p.y - p.hy);
      if (disp > 0.18) {                       // 仅被扰动的颗粒才显形 → 涟漪显隐
        var a = disp * 0.018; if (a > 0.16) a = 0.16;
        ctx.globalAlpha = a;
        ctx.fillRect(p.x, p.y, p.s, p.s);
      }
    }
    ctx.globalAlpha = 1;
    requestAnimationFrame(loop);
  }
  requestAnimationFrame(loop);
})();
