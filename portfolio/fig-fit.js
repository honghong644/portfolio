/* ============================================================================
   fig-fit.js — 图片自适应：让每个 .fig 图框采用图片真实宽高比，
   图片完整显示、不裁切、不变形、无黑边。对填了 src 的 image-slot 生效；
   空占位（无 src）保持默认 16:9 框。图片异步加载，故轮询若干次后停止。
   用法：详情页 <body> 末尾 <script src="fig-fit.js"></script>
============================================================================ */
(function () {
  "use strict";
  function apply() {
    var done = true;
    document.querySelectorAll("image-slot.fig-img[src]").forEach(function (s) {
      var frame = s.closest(".fig-frame");
      if (!frame) return;
      var img = s.shadowRoot && s.shadowRoot.querySelector("img");
      if (img && img.naturalWidth && img.naturalHeight) {
        var ar = img.naturalWidth + " / " + img.naturalHeight;
        if (frame.style.aspectRatio !== ar) frame.style.aspectRatio = ar;
      } else {
        done = false; // not loaded yet
      }
    });
    return done;
  }
  var n = 0;
  var iv = setInterval(function () { if (apply() || ++n >= 30) clearInterval(iv); }, 180);
  addEventListener("load", apply);
})();
