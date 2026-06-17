# -*- coding: utf-8 -*-
"""Generate the remaining 6 project detail pages on the established reader
template. Reuses the exact <style> block from 万物的客舍.html so styling is
identical; body content + nav/pager chain come from the data below."""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))

# --- pull the canonical stylesheet verbatim from the reference page ----------
with open(os.path.join(BASE, "万物的客舍.html"), encoding="utf-8") as f:
    ref = f.read()
STYLE = re.search(r"<style>.*?</style>", ref, re.S).group(0)

# --- fixed pieces ------------------------------------------------------------
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com" />\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />\n'
         '<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;500;700'
         '&family=Noto+Sans+SC:wght@300;400;500&family=Space+Mono:ital,wght@0,400;0,700;1,400'
         '&display=swap" rel="stylesheet" />')

TOC = [("01", "ch-overview", "项目概述"),
       ("02", "ch-role", "核心职责"),
       ("03", "ch-highlight", "设计亮点"),
       ("04", "ch-outcome", "成果")]

JS = r"""<script>
(function () {
  "use strict";
  /* ---------- custom cursor (inertial ring + instant dot) ---------- */
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
  /* ---------- back transition ---------- */
  var back = document.getElementById("navBack");
  if (back) back.addEventListener("click", function (e) {
    e.preventDefault();
    document.body.classList.add("leaving");
    setTimeout(function () { window.location.href = "index.html"; }, 480);
  });
  /* ---------- TOC smooth jump ---------- */
  document.querySelectorAll(".toc-link").forEach(function (link) {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      var el = document.getElementById(link.getAttribute("data-spy"));
      if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });
  /* ---------- scroll-spy (ids derived from the TOC, so this is generic) ---------- */
  (function () {
    var links = [].slice.call(document.querySelectorAll(".toc-link"));
    var els = links.map(function (l) { return document.getElementById(l.getAttribute("data-spy")); }).filter(Boolean);
    var raf = 0;
    function compute() {
      raf = 0;
      var line = innerHeight * 0.35;
      var current = els[0] ? els[0].id : null;
      els.forEach(function (el) { if (el.getBoundingClientRect().top <= line) current = el.id; });
      if (innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4) {
        current = els[els.length - 1] ? els[els.length - 1].id : current;
      }
      links.forEach(function (l) { l.classList.toggle("active", l.getAttribute("data-spy") === current); });
    }
    function onScroll() { if (!raf) raf = requestAnimationFrame(compute); }
    addEventListener("scroll", onScroll, { passive: true });
    addEventListener("resize", onScroll);
    compute();
  })();
  /* ---------- reveal on scroll ---------- */
  (function () {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    document.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });
  })();
})();
</script>"""


def logic(items):
    rows = "\n".join(
        '            <li>\n'
        '              <span class="lk">%s</span>\n'
        '              <span class="lt"><b>%s</b>%s</span>\n'
        '            </li>' % (k, lead, rest) for (k, lead, rest) in items)
    return '          <ul class="logic">\n%s\n          </ul>' % rows


def paras(ps):
    return "\n".join('          <p>%s</p>' % p for p in ps)


def fig(slot, ph, tool, cap, src="", fit="cover", cls=""):
    srcattr = (' src="%s"' % src) if src else ""
    figcls = "fig" + ((" " + cls) if cls else "")
    return ('\n          <figure class="%s">\n'
            '            <div class="fig-frame" data-hot>\n'
            '              <image-slot id="%s" class="fig-img" shape="rect" fit="%s"%s placeholder="%s"></image-slot>\n'
            '            </div>\n'
            '            <figcaption class="fig-cap"><b>%s</b><span>%s</span></figcaption>\n'
            '          </figure>' % (figcls, slot, fit, srcattr, ph, tool, cap))


def vidfig(src, cap):
    return ('        <figure class="vid reveal">\n'
            '          <div class="vid-frame" data-hot>\n'
            '            <video src="%s" muted loop playsinline preload="metadata"></video>\n'
            '            <span class="vid-tag">Demo</span>\n'
            '            <button class="vid-btn" type="button" aria-label="声音">♪</button>\n'
            '          </div>\n'
            '          <figcaption class="fig-cap"><b>Demo</b><span>%s</span></figcaption>\n'
            '        </figure>' % (src, cap))


# --- per-page data -----------------------------------------------------------
# chapter bodies are pre-rendered html (paragraphs or .logic lists)
PAGES = [
    dict(
        file="随行公交.html", prog="03",
        eyebrow="Public Service&nbsp;&nbsp;/&nbsp;&nbsp;Smart City",
        title="随行公交", title_attr="随行公交",
        intro="针对天津滨海新区「职住分离」导致的通勤拥堵与公交空载，设计一套基于动态需求的公交调度系统——让每一趟车都贴着真实的人流走。",
        role_note="我承担<b>用户研究与算法逻辑</b>两块：通过 200+ 份问卷与深度访谈，定位职住分离下的真实通勤痛点；提炼出「随行模式」的<b>合并调度逻辑</b>（相近行程实时归并、动态调整班次），并完成候车亭信息屏的交互界面设计，把调度结果落到候车现场。",
        meta=[("类别 / Category", "Public Service <span>·</span> Smart City"),
              ("角色 / Role", "用户调研 <span>/</span> 算法逻辑 <span>/</span> 硬件交互"),
              ("属性 / Type", "市级大创立项")],
        overview=["天津滨海新区的<strong>职住分离</strong>，让通勤时段一边是挤不上的车，一边是空载折返的班次。随行公交以<span class=\"hot\">动态需求</span>为底层逻辑重新组织运力，覆盖 APP 端与站台硬件端两条触点。",
                  "系统不预设固定线路：先用 APP 收集真实出行需求，再由调度算法实时合并相近行程、动态生成班次；站台端同步显示候车信息，让「等多久、坐哪班」一目了然。运力随人流伸缩，既缓解高峰拥挤，也减少平峰空载。"],
        role=[("用户调研", "200+ 份有效样本", "通过问卷与深度访谈收集数据，定位职住分离下的真实通勤痛点。"),
              ("算法逻辑", "「随行模式」", "合并相似路线、按需动态调整班次密度，让运力随人流伸缩。"),
              ("硬件交互", "站台界面", "完成公交站台的硬件交互界面设计，把调度结果落到候车现场。")],
        highlight=[("动态线路", "拼车式公交", "用户在 APP 上发起需求，系统自动归并并生成最优路径。"),
                   ("站台交互", "实时反馈", "显示屏即时反馈车辆拥挤度与预计等待时间，候车不再盲等。")],
        outcome=["项目获<strong>市级大学生创新创业训练计划</strong>立项，完成了从需求分析、算法逻辑到高保真原型验证的<span class=\"hot\">全链路</span>设计。"],
        prev=("万物的客舍.html", "万物的客舍", "Everything's Inn"),
        nxt=("沉默玩家.html", "沉默玩家", "Silent Player")),

    dict(
        file="沉默玩家.html", prog="04",
        eyebrow="AIoT&nbsp;&nbsp;/&nbsp;&nbsp;Social Innovation",
        title="沉默玩家", title_attr="沉默玩家",
        intro="一套面向聋哑群体的共情云生态——以智能手环、APP 与公共设施联动，让「沉默」也能被听见、被回应。",
        role_note="作为团队成员，我负责<b>市场与商业运营、营销与社群运营</b>：参与产品定位与 PEST 分析、商业模式与盈利模式设计，制定营销组合策略与社群运营推广，推动「沉默玩家」从校园项目走向更广的受众。",
        meta=[("类别 / Category", "AIoT <span>·</span> Social Innovation"),
              ("角色 / Role", "商业模式 <span>/</span> 营销策略 <span>/</span> 交互反馈"),
              ("属性 / Type", "大创立项")],
        overview=["一项<strong>大创立项</strong>项目。沉默玩家试图打破聋哑人与健听人之间的<span class=\"hot\">沟通壁垒</span>，构建一个由智能手环、APP 与公共设施共同支撑的共情生态。",
                  "生态分三层协同：可穿戴的<strong>智能手环</strong>负责即时感知与震动 / 光效反馈，<strong>APP</strong> 承载手语识别与社群连接，<strong>公共设施</strong>（如「沉默咖啡馆」触点）把无障碍体验延伸到线下场景——让沟通不再依赖单一设备，而是融进日常的每一个环节。"],
        role=[("商业模式", "B / C / G 三端", "构建三端盈利模型，让公益属性与可持续运营并存。"),
              ("营销策略", "4P 框架", "制定产品、价格、渠道、推广的完整 4P 策略。"),
              ("交互反馈", "手环机制", "设计以震动频率与光效传递信息的反馈机制。")],
        highlight=[("AI 手势识别", "手语转语音", "手环摄像头捕捉手语，实时转化为语音播报，沟通即时发生。"),
                   ("共情反馈", "危险示警", "身处高分贝等危险环境时，手环以强震动与强光示警。")],
        outcome=["成功<span class=\"hot\">大创立项</span>，完成<strong>商业计划书</strong>撰写，并获校级创业比赛<strong>二等奖</strong>。"],
        prev=("随行公交.html", "随行公交", "Transit Companion"),
        nxt=("心流咖啡厅.html", "心流咖啡厅", "Flow Cafe")),

    dict(
        file="心流咖啡厅.html", prog="05",
        eyebrow="Spatial Design&nbsp;&nbsp;/&nbsp;&nbsp;Psychology",
        title="心流咖啡厅", title_attr="心流咖啡厅",
        intro="为考研党与上班族打造的沉浸式精神避难所——以心流理论组织空间，把「不被打断」做成一种可设计的体验。",
        role_note="我负责<b>空间策略与触点道具</b>：应用心流理论推导出「动 / 静线分离」的流线规划，确定 4000K–4500K 的中性光照区间；并设计了防烫、防打扰的系列触点道具（如带「勿扰」信号的<b>特制杯套</b>），把「不被打断」做成可感知的体验细节。",
        meta=[("类别 / Category", "Spatial Design <span>·</span> Psychology"),
              ("角色 / Role", "空间布局 <span>/</span> 流线规划 <span>/</span> 触点道具"),
              ("属性 / Type", "年度优秀方案 <span>·</span> 入选毕设展")],
        overview=["高压人群常被焦虑与频繁打断拖出专注。心流咖啡厅以<strong>心流理论（Flow Theory）</strong>为依据，把一处服务空间设计成可以稳定进入<span class=\"hot\">「心流」</span>的容器。",
                  "从进门动线、座位密度到声光环境，每个触点都围绕「减少打断」展开：清晰的动静分区让走动不打扰沉浸，中性色温与隔音舱降低感官负荷，连特制杯套这样的小物，也承担起「勿扰」的信号功能。"],
        role=[("空间布局", "心理学驱动", "应用心理学理论组织空间结构，匹配专注所需的心理节奏。"),
              ("流线规划", "动 / 静线分离", "让走动的人不打扰沉浸的人，两条动线互不交叠。"),
              ("触点道具", "系列设计", "设计防烫、防打扰的系列触点道具，如特制杯套。")],
        highlight=[("光照设计", "4000K–4500K", "严格控制色温于中性光区间，减少长时间停留的视觉疲劳。"),
                   ("干扰屏蔽", "勿扰模式", "「勿扰」挂牌配合物理隔音舱，从源头阻断外界打断。")],
        outcome=["方案获工作室<strong>年度优秀方案</strong>，并作为完整的服务系统设计落地——从空间布局、流线规划到触点道具，形成统一的<span class=\"hot\">体验闭环</span>。"],
        prev=("沉默玩家.html", "沉默玩家", "Silent Player"),
        nxt=("水轮机组AR.html", "水轮机组 AR", "Hydro Turbine AR")),

    dict(
        file="水轮机组AR.html", prog="06",
        eyebrow="Unity&nbsp;&nbsp;/&nbsp;&nbsp;AR Visualization",
        title="水轮机组 AR", title_attr="水轮机组 AR",
        intro="面向水电站维修培训的 AR 可视化应用——把高风险、难拆解的机组，搬进可缩放、可爆炸的虚实叠加视图里。",
        role_note="我负责<b>AR 交互界面与可视化呈现</b>：梳理缩放 / 旋转 / 爆炸视图的交互逻辑，设计故障菜单与<b>五类故障高亮演示</b>（气蚀、磨损、过热、泄漏、振动）的界面流程，配合 Rhino 三维模型完成虚实叠加的交互体验。",
        meta=[("类别 / Category", "Unity <span>·</span> AR Visualization"),
              ("角色 / Role", "3D 建模 <span>/</span> 交互逻辑 <span>/</span> 故障识别"),
              ("属性 / Type", "可运行 Demo")],
        overview=["水电站维修人员<strong>培训难、风险高</strong>。这款基于 Unity + Vuforia 的 AR 应用，让学员无需面对真实机组，也能<span class=\"hot\">直观理解</span>内部结构与拆解流程。",
                  "学员用平板扫描实体图纸，屏幕上即叠加 1:1 的三维机组；可缩放、旋转、爆炸拆解，逐层查看叶轮、主轴与导水机构，并在模拟故障时高亮对应部件，把抽象的机械原理变成可上手操作的练习。"],
        role=[("三维建模", "Rhino 高精度", "完成水轮机组的高精度 3D 建模，还原真实机械结构。"),
              ("交互逻辑", "Unity 实现", "实现缩放、旋转与爆炸视图的交互操作。"),
              ("故障识别", "高亮显示", "开发故障点识别与高亮显示功能，定位即所见。")],
        highlight=[("虚实融合", "实物识别", "用平板 / 手机识别实体模型或图纸，屏幕上即叠加 1:1 的三维机组。"),
                   ("故障模拟", "五类故障", "模拟气蚀、磨损、过热、泄漏、振动五类典型故障，逐一高亮对应部件，辅助学员理解机组运作与排查逻辑。")],
        outcome=["完成可运行 <span class=\"hot\">Demo</span>，能够流畅演示设备拆解与<strong>故障排查</strong>的完整流程。"],
        prev=("心流咖啡厅.html", "心流咖啡厅", "Flow Cafe"),
        nxt=("知绘APP.html", "知绘 APP", "ZhiHui")),

    dict(
        file="知绘APP.html", prog="07",
        eyebrow="Mobile UI&nbsp;&nbsp;/&nbsp;&nbsp;EdTech",
        title="知绘 APP", title_attr="知绘 APP",
        video_src="videos/zhihui.mp4",
        intro="面向 3–15 岁儿童的美术教育应用——用游戏化闯关与 AI 辅助创作，把艺术启蒙的门槛压到最低。",
        role_note="我建立了<b>「活力橘黄」设计系统</b>（配色、字体、组件规范），设计「动物馆」式游戏化闯关界面与每日勋章激励机制；并对接 <b>AI 绘画识别接口</b>，完成作业自动评分与家长端成长报告的界面流程。",
        meta=[("类别 / Category", "Mobile UI <span>·</span> EdTech"),
              ("角色 / Role", "设计系统 <span>/</span> 游戏化界面 <span>/</span> AI 接口"),
              ("属性 / Type", "高保真原型 <span>·</span> 满意度 90%+")],
        overview=["知绘面向 <strong>3–15 岁儿童</strong>，把游戏化学习与 AI 辅助创作结合，让没有美术基础的孩子也能<span class=\"hot\">轻松开始第一笔</span>。",
                  "课程按色彩、线描、特色分层，配合「动物馆」式闯关与每日勋章激励；AI 实时识别画作并给出鼓励式反馈，家长端则能查看学习报告与成长树——把启蒙、练习与陪伴串成一条完整的链路。"],
        role=[("设计系统", "活力橘黄", "建立配色、字体与组件规范的整套视觉系统。"),
              ("游戏化界面", "动物馆模式", "设计闯关式的游戏化学习界面，把练习变成探索。"),
              ("AI 接口", "自动评分", "集成 AI 绘画识别算法接口，实现作业自动评分。")],
        highlight=[("游戏化激励", "解锁画具", "收集虚拟画笔解锁新画具，持续提升使用粘性。"),
                   ("家长模式", "成长树", "提供学习报告与作品成长树，连接家校两端。")],
        outcome=["完成高保真交互原型并通过<strong>可用性测试</strong>，用户满意度达 <span class=\"hot\">90% 以上</span>。"],
        prev=("水轮机组AR.html", "水轮机组 AR", "Hydro Turbine AR"),
        nxt=("My Note.html", "My Note", "Productivity Tool")),

    dict(
        file="My Note.html", prog="08",
        eyebrow="Productivity&nbsp;&nbsp;/&nbsp;&nbsp;UX Design",
        title="My Note", title_attr="My Note",
        video_src="videos/mynote.mp4",
        intro="为信息过载的大学生与职场新人设计的极简信息管理工具——主打「无压力记录」，打开即写，回归书写本质。",
        role_note="我负责<b>视觉规范与多维视图交互</b>：制定深海蓝视觉系统与栅格，设计看板 / 日历 / 列表三种视图的<b>切换逻辑</b>；并优化「一键剪藏」「语音速记」的信息捕获流程，让「记录」与「整理」彻底解耦。",
        meta=[("类别 / Category", "Productivity <span>·</span> UX Design"),
              ("角色 / Role", "视觉规范 <span>/</span> 多维视图 <span>/</span> 信息捕获"),
              ("属性 / Type", "课程设计满分作品")],
        overview=["信息过载让记录本身变成负担。My Note 以<span class=\"hot\">「无压力记录」</span>为主张，剥掉复杂菜单，让捕捉想法这件事回到<strong>最轻的状态</strong>。",
                  "打开即写，先把想法接住，再按需整理：同一批内容可在<strong>看板 / 日历 / 列表</strong>三种视图间自由切换，配合一键剪藏与语音速记，让「记录」与「整理」彻底解耦，贴合 GTD 的收集—处理节奏。"],
        role=[("视觉规范", "深海蓝系统", "设计深海蓝视觉规范与配套栅格系统。"),
              ("多维视图", "三视图切换", "实现看板 / 日历 / 列表的多维视图切换。"),
              ("信息捕获", "捕获流程", "优化一键剪藏与语音速记的捕获流程。")],
        highlight=[("多维视图", "按需切换", "用户按任务属性自由切换查看模式，结构随需求而变。"),
                   ("极简输入", "打开即写", "没有复杂菜单干扰，回归书写本质。")],
        outcome=["作为<strong>课程设计满分作品</strong>，其交互逻辑被教授评价为<span class=\"hot\">「最符合 GTD 逻辑的设计方案」</span>。"],
        prev=("知绘APP.html", "知绘 APP", "ZhiHui"),
        nxt=("智采灵枢.html", "智采灵枢", "Intelligent Tea-Picker")),
]

# Drop-in image slots, keyed by chapter. Count varies per project on purpose —
# hardware / spatial / AR work earns more frames; a light tool gets one.
FIGS = {
    # 随行公交 — 公共交通服务设计展板 + 候车亭模型
    "随行公交.html": {
        "overview": fig("t-app", "项目展板 / 公共交通系统优化服务设计 · A1", "Service Design", "动态调度系统", "images/transit-board.jpg", "contain", "fig-r34"),
        "role": fig("t-survey", "场景渲染图", "场景渲染图", "随行公交 · 候车亭", "images/transit-render2.jpg"),
        "highlight": fig("t-station", "场景细节图", "场景细节图", "叶形顶棚 · 候车亭", "images/transit-detail2.jpg")},
    # 沉默玩家 — SILENT ODYSSEY 服务系统展板，2 张
    "沉默玩家.html": {
        "overview": fig("s-wear", "服务系统 / SILENT ODYSSEY · 16:9", "Service Design", "AIoT 共情生态", "images/silent-board.jpg"),
        "highlight": fig("s-app", "服务蓝图 / 用户旅程地图 · A1", "Service Map", "活动 · 触点 · 旅程", "images/silent-3.jpg", "contain", "fig-r34")},
    # 心流咖啡厅 — 空间设计，最视觉，3 张
    "心流咖啡厅.html": {
        "overview": fig("f-space", "空间概念 / 心流空间夜景模型 · 16:9", "Spatial", "沉浸式服务空间", "images/cafe-space.jpg"),
        "role": fig("f-plan", "空间布局 / 模型俯视 · 16:9", "Plan", "动 / 静线规划", "images/cafe-plan2.jpg"),
        "highlight": fig("f-light", "触点道具 / 特制杯套 · 16:9", "Detail", "防烫防打扰 · 杯套", "images/cafe-cup.jpg")},
    # 水轮机组AR — 三维 + AR，最视觉，3 张
    "水轮机组AR.html": {
        "overview": fig("h-model", "实物模型 + AR / 虚实融合 · 16:9", "AR Scan", "识别实物 · 叠加 3D", "images/hydro-scan.jpg"),
        "role": fig("h-unity", "AR 交互界面 / 故障菜单 · 16:9", "Unity / UI", "缩放 · 旋转 · 爆炸", "images/hydro-ui.jpg"),
        "highlight": fig("h-ar", "AR 故障模拟 / 五类故障 · 16:9", "Vuforia", "气蚀·磨损·过热·泄漏·振动", "images/hydro-ar.jpg")},
    # 知绘APP — 移动界面，完整显示（contain，3:2 适配 iPad UI）
    "知绘APP.html": {
        "overview": fig("z-system", "知绘 / 主界面 · 我的课程", "Figma / UI", "色彩 · 线描 · 特色", "images/zhihui-home2.png", "contain", "fig-r32"),
        "role": fig("z-game", "绘画界面 / 游戏化创作", "Mobile UI", "闯关式学习", "images/zhihui-game2.png", "contain", "fig-r32"),
        "highlight": fig("z-parent", "语音助手 / 小知 AI", "语音助手", "小知 · 语音识别", "images/zhihui-voice.png", "contain", "fig-r32")},
    # My Note — 全部界面效果图（dense montage，铺满列宽，fig-fit 自适应比例）
    "My Note.html": {
        "overview": fig("m-views", "MY NOTE 效果图 / 全部界面", "MY NOTE 效果图", "全部界面 · UI 总览", "images/mynote-effect.jpg")},
}


def render(p):
    figs = FIGS[p["file"]]
    toc = "\n".join(
        '          <li><a class="toc-link%s" href="#%s" data-hot data-spy="%s"><span class="tn">%s</span>%s</a></li>'
        % (" active" if i == 0 else "", cid, cid, no, label)
        for i, (no, cid, label) in enumerate(TOC))

    meta = "\n".join(
        '      <div class="meta-cell">\n'
        '        <div class="meta-k">%s</div>\n'
        '        <div class="meta-v">%s</div>\n'
        '      </div>' % (k, v) for (k, v) in p["meta"])

    rolenote = ('    <div class="role-note reveal">\n'
                '      <div class="role-note-k">个人贡献 / My Role</div>\n'
                '      <p class="role-note-t">%s</p>\n'
                '    </div>' % p["role_note"])

    chapters = "\n\n".join([
        '        <section class="chap reveal" id="ch-overview">\n'
        '          <span class="chap-no">01 — Overview</span>\n'
        '          <h2 class="chap-h">项目概述</h2>\n%s%s\n        </section>' % (paras(p["overview"]), figs.get("overview", "")),
        '        <section class="chap reveal" id="ch-role">\n'
        '          <span class="chap-no">02 — Role</span>\n'
        '          <h2 class="chap-h">核心职责</h2>\n%s%s\n        </section>' % (logic(p["role"]), figs.get("role", "")),
        '        <section class="chap reveal" id="ch-highlight">\n'
        '          <span class="chap-no">03 — Highlights</span>\n'
        '          <h2 class="chap-h">设计亮点</h2>\n%s%s\n        </section>' % (logic(p["highlight"]), figs.get("highlight", "")),
        '        <section class="chap reveal" id="ch-outcome">\n'
        '          <span class="chap-no">04 — Outcome</span>\n'
        '          <h2 class="chap-h">成果</h2>\n%s\n        </section>' % paras(p["outcome"]),
    ])

    # video pages (知绘 / My Note): Aura-style hero — full-width demo video with the
    # big title + intro overlaid on the left (no morph title / no normal header).
    # other pages: the shrinking morph title + the normal header.
    if p.get("video_src"):
        top = ('  <section class="vid-hero reveal">\n'
               '    <video src="%s" muted loop playsinline preload="metadata"></video>\n'
               '    <span class="vid-tag">Demo</span>\n'
               '    <button class="vid-btn" type="button" aria-label="声音">♪</button>\n'
               '  </section>' % p["video_src"])
        head_block = ('    <div class="vid-head reveal">\n'
                      '      <div class="head-eyebrow">%s</div>\n'
                      '      <h1 class="vid-head-title">%s</h1>\n'
                      '      <p class="vid-head-intro">%s</p>\n'
                      '    </div>\n' % (p["eyebrow"], p["title"], p["intro"]))
        morph = ""
    else:
        top = '  <h1 class="head-title">%s</h1>' % p["title"]
        head_block = ('    <header class="head reveal">\n'
                      '      <div class="head-eyebrow">%s</div>\n'
                      '      <p class="head-intro">%s</p>\n'
                      '    </header>\n' % (p["eyebrow"], p["intro"]))
        morph = '  <script src="hero-morph.js"></script>\n'

    return """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>%s — 项目详情 / 刘思敏</title>
%s
%s
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
      <span class="nav-prog"><b>%s</b> / 08</span>
    </div>
  </nav>

%s

  <div class="shell">
%s
    <div class="meta reveal">
%s
    </div>

%s
    <div class="story">
      <aside class="toc">
        <div class="toc-label">Contents</div>
        <ul class="toc-list">
%s
        </ul>
      </aside>

      <div class="main">
%s
      </div>
    </div>
  </div>

  <nav class="pager">
    <a class="pg-prev" href="%s" data-hot>
      <span class="pg-k"><span class="pa">&larr;</span> 上一篇</span>
      <div class="pg-cn">%s</div>
      <div class="pg-en">%s</div>
    </a>
    <a class="pg-next" href="%s" data-hot>
      <span class="pg-k">下一篇 <span class="pa">&rarr;</span></span>
      <div class="pg-cn">%s</div>
      <div class="pg-en">%s</div>
    </a>
  </nav>

  <div class="cursor-ring" aria-hidden="true"></div>
  <div class="cursor-dot" aria-hidden="true"></div>

  <script src="image-slot.js"></script>
  <script src="atmosphere.js"></script>
%s  <script src="fig-fit.js"></script>
  <script src="vid.js"></script>
%s
</body>
</html>
""" % (p["title_attr"], FONTS, STYLE, p["prog"], top, head_block,
       meta, rolenote, toc, chapters,
       p["prev"][0], p["prev"][1], p["prev"][2],
       p["nxt"][0], p["nxt"][1], p["nxt"][2], morph, JS)


for p in PAGES:
    out = os.path.join(BASE, p["file"])
    with open(out, "w", encoding="utf-8") as f:
        f.write(render(p))
    print("wrote", p["file"], "(%d/08)" % int(p["prog"]))
print("done:", len(PAGES), "pages")
