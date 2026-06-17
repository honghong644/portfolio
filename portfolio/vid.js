/* ============================================================================
   vid.js — 详情页演示视频控制：
   · .vid-hero  视频英雄区（标题/简介叠在视频上）—— 始终铺满，进出视口播放/暂停
   · .vid-frame 普通视频图位 —— 按视频真实比例自适应（横屏铺满 / 竖屏手机尺寸居中）
   共同：滚入视口自动静音循环播放、滚出暂停、点击 ♪ 切换声音。无视频时不做任何事。
   用法：详情页 <body> 末尾 <script src="vid.js"></script>
============================================================================ */
(function () {
  "use strict";
  var blocks = document.querySelectorAll(".vid-hero, .vid-frame");
  if (!blocks.length) return;

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      var v = e.target.querySelector("video");
      if (!v) return;
      if (e.isIntersecting) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
      else v.pause();
    });
  }, { threshold: 0.25 });

  blocks.forEach(function (f) {
    var v = f.querySelector("video");
    if (!v) return;
    v.muted = true; v.loop = true; v.setAttribute("playsinline", "");

    // only .vid-frame adapts its frame to the video's aspect ratio
    if (f.classList.contains("vid-frame")) {
      var fit = function () {
        if (v.videoWidth && v.videoHeight) {
          f.style.aspectRatio = v.videoWidth + " / " + v.videoHeight;
          f.classList.toggle("portrait", v.videoHeight > v.videoWidth);
        }
      };
      if (v.readyState >= 1) fit(); else v.addEventListener("loadedmetadata", fit);
    }

    io.observe(f);

    var btn = f.querySelector(".vid-btn");
    if (btn) btn.addEventListener("click", function (e) {
      e.stopPropagation();
      v.muted = !v.muted;
      f.classList.toggle("sound", !v.muted);
      if (!v.muted) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
    });
  });
})();
