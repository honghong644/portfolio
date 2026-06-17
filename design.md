# 设计规范 · 陶土与深岩 (Terracotta & Deep Rock)

> 刘思敏 个人作品集 — 统一设计系统
> 所有新页面**必须先读本文件**，严格沿用以下 token 与规则，保证全站风格一致。

## 0. 设计哲学（先记住这三条）

1. **杂志排版 (Editorial)**：小字号、大间距、长行长。拒绝"大字报"，标题克制（约 2–3rem，字重 500，**绝不用 700**）。
2. **线条，不是卡片**：用 1px 细线 + 留白分隔内容。**全站禁止 box-shadow、禁止带阴影的色块、禁止圆角卡片**。
3. **禁止渐变做装饰**：背景质感只用 SVG 噪点 (grain) 与极淡的径向光晕 (atmosphere)。唯一允许的渐变是图片上的"黑→透明"可读性遮罩。

直接复制下面的 `:root` 到任何新页面：

```css
:root{
  --rock:#1A1A1A;          /* 背景：深岩石灰 */
  --rock-deep:#151515;     /* 更深背景：嵌入框、坑位底色 */
  --terra:#C97B63;         /* 主强调色：暖陶土，热区 */
  --steel:#5b7385;         /* 辅助冷调：危机/理性主题的反差色 */
  --white:#F5F5F5;         /* 暖白：标题、强调正文 */
  --ink:rgba(245,245,245,.68);   /* 正文 */
  --mute:rgba(245,245,245,.40);  /* 次级文字、标签 */
  --faint:rgba(245,245,245,.13); /* 结构分隔线（meta、pager、story 边界）*/
  --hair:rgba(245,245,245,.08);  /* 更细的内部分隔线（list、blueprint）*/
  --serif:"Noto Serif SC", serif;
  --sans:"Noto Sans SC", sans-serif;
  --mono:"Space Mono", monospace;
  --ease-out:cubic-bezier(.16,1,.3,1);   /* 缓出，惯性收尾 */
  --ease-back:cubic-bezier(.34,1.4,.5,1); /* 回弹，悬停/光标 */
}
```

---

## 1. 配色

| 角色 | Token | 色值 | 用途 |
|---|---|---|---|
| 背景主色 | `--rock` | `#1A1A1A` | 全站哑光岩石底色 |
| 背景深色 | `--rock-deep` | `#151515` | 嵌入框 / 图坑 / 蓝图泳道底 |
| **主强调色** | `--terra` | `#C97B63` | 热区、链接高亮、章节序号、光标、FIG 标号、数据点缀 |
| 辅助冷调 | `--steel` | `#5b7385` | 冷色叙事（危机/理性主题）的图框 overlay 与光晕，与陶土形成张力 |
| 文字·标题 | `--white` | `#F5F5F5` | 标题、加粗强调 (`<strong>`) |
| 文字·正文 | `--ink` | `rgba(245,245,245,.68)` | 正文段落 |
| 文字·次级 | `--mute` | `rgba(245,245,245,.40)` | 标签、引言、说明、英文注解 |
| 线·结构 | `--faint` | `rgba(245,245,245,.13)` | 模块边界分隔线 |
| 线·内部 | `--hair` | `rgba(245,245,245,.08)` | 列表行、蓝图网格等更细的线 |

**禁区**：荧光绿、科技蓝、纯黑白灰等廉价 AI 模板色。陶土只用于"热区"，不要大面积铺。

选区高亮：`::selection{ background:rgba(201,123,99,.3); color:#F5F5F5; }`

---

## 2. 字体

三套字体各司其职：**Serif 中文标题（美学）/ Sans 中文正文 / Mono 英文标签（工程感）**。

| 元素 | 字体 | 字号 | 字重 | 行高 | 字距 | 颜色 |
|---|---|---|---|---|---|---|
| 页面大标题 | serif | `clamp(2rem,3.6vw,2.75rem)` | 500 | 1.12 | .04em | white |
| 章节标题 | serif | `1.4rem` | 500 | 1.32 | .02em | white |
| 引言 (intro) | sans | `14px` | **300** | 2.05 | .01em | mute |
| 正文段落 | sans | `14.5px` | 400 | 2.05 | .012em | ink |
| 元数据值 | sans | `14px` | 400 | 1.7 | .01em | white |
| 英文小标签 (eyebrow) | mono | `11px` | 400 | — | .34em · 大写 | mute |
| 章节序号 / 标签 | mono | `11px` | 400 | — | .24–.26em · 大写 | terra / mute |
| TOC 链接 | sans | `13px` | 400 | — | .02em | mute→white |
| pager 中文 | serif | `clamp(1.3rem,2.4vw,1.85rem)` | 500 | — | .02em | white |
| pager 英文 | mono | `12px` | 400 | — | .16em · 大写 | mute |

**字重铁律**：严肃叙事用 Regular(400)，引言可用 Light(300)，标题最多 Medium(500)。**永远不要用 700。**
正文统一 `text-wrap:pretty`，开启 `-webkit-font-smoothing:antialiased`。

字体引入：
```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;500&family=Noto+Sans+SC:wght@300;400;500&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet" />
```

---

## 3. 间距

**节奏单位用 `vh` 控制大留白，用 `px` 控制组件内部。**

| 场景 | 值 |
|---|---|
| 内容容器 | `max-width:1120px; margin:0 auto;` |
| 容器左右内边距 | `clamp(20px,5vw,56px)`（全站统一，nav / shell / pager 一致）|
| 阅读正文列 | `max-width:680px` |
| 页首区上下留白 | `padding:20vh 0 8vh` |
| 模块大间距 | `padding-bottom:11vh ~ 13vh`（章节、meta 下方）|
| 正文双栏 | `grid-template-columns:20% 1fr; gap:clamp(40px,6vw,96px)`（侧栏导航 + 正文）|
| 段落间距 | `margin-bottom:20px` |
| 元数据单元格 | `padding:32px 0 32px 32px`（首格 `padding-left:0`）|
| 列表行 (logic) | `padding:22px 0` |
| 嵌入图上下 | `margin:38–40px 0 8–10px` |
| 滚动锚点偏移 | `scroll-margin-top:108px`（避开固定导航）|

侧边导航粘性定位：`position:sticky; top:120px;`

---

## 4. 组件样式

> 总原则：**无阴影、几乎无圆角、靠 1px 细线和毛玻璃区分层级。**

### 导航栏 (Nav)
- 固定顶部：`position:fixed; height:62px; z-index:50`
- 毛玻璃：`background:rgba(20,20,20,.62); backdrop-filter:blur(16px) saturate(1.2)`
- 仅底部 1px 线：`border-bottom:1px solid var(--hair)`
- **无圆角、无阴影**
- 左侧返回键 `← Back`（mono 11–12px，大写）：悬停箭头左移 6px + 文字转白；点击 `body.leaving` 淡出后跳转
- 右侧进度 `02 / 08`（mono，序号用 terra）

### "卡片"——其实是线框块 (Cards = 禁用，用以下替代)
本系统**不使用传统卡片**。需要分组信息时：
- **细线列表**：`border-top/bottom:1px solid var(--hair)`，行与行之间 `border-bottom`，无背景、无阴影、无圆角。
- **嵌入图框 (fig)**：`border:1px solid var(--hair); background:var(--rock-deep); aspect-ratio:16/9; overflow:hidden`。冷调主题叠 `rgba(91,115,133,.16)` overlay；图片默认 `grayscale(.5)`，hover 转彩。**直角，无圆角。**
- **数据/蓝图 (blueprint)**：网格用 `1px var(--hair)` 描线，相位格淡陶土底 `rgba(201,123,99,.05)`，泳道格 `var(--rock-deep)`。横向可滚动，像书里的插图，不占满全屏。

### 按钮 / 链接 (Buttons)
本系统的"按钮"基本是**文本链接 + 自定义光标热区**，不做实心药丸按钮：
- `a{ color:inherit; text-decoration:none; }`
- 交互元素加 `data-hot`，光标 ring 会放大吸附（见下）
- 悬停过渡统一 `transition: … .4s var(--ease-out)`；位移/回弹用 `var(--ease-back)`
- 箭头类（pager、back）hover 时平移 6px

### 圆角 / 阴影 / 边框 速查
| 属性 | 规则 |
|---|---|
| **border-radius** | 全站 **0**。例外仅：自定义光标 `50%`、滚动条 thumb `3px`。 |
| **box-shadow** | 全站 **禁用**。层级靠毛玻璃 + 细线，不靠投影。 |
| **border** | 只用 `1px solid`，颜色取 `--faint`（结构）或 `--hair`（内部）。 |

### 自定义光标 (Cursor)
- ring：`30px`，`1.5px solid var(--terra)`，惯性 lerp 0.18 跟随
- dot：`5px` 实心 terra，快速 lerp 0.5 跟随
- 悬停 `[data-hot]` 时 ring 放大到 `64px` 并填充 `color-mix(in srgb, var(--terra) 14%, transparent)`
- 触摸屏 / `pointer:coarse` 时隐藏，恢复系统光标

### 背景动效 (Atmosphere + Grain)
- `.atmos`：两团极淡径向光晕（steel + terra，opacity .035–.05），`blur(48px)`，`drift` 动画 46s 缓慢往返——"风吹过沙粒"的呼吸感。
- `.grain`：SVG `fractalNoise` 噪点，`opacity:.4; mix-blend-mode:soft-light`。
- `.reveal`：进入视口时 `translateY(22px)→0 + opacity 0→1`，`.8s var(--ease-out)`，IntersectionObserver 触发。
- **宣纸/混凝土纹理层 + 鼠标涟漪（`atmosphere.js`，全站共用，每页必引）**：在深岩背景上叠一层高分辨率宣纸/混凝土纤维纹理，透明度极低（~5%，`soft-light` 混合），并极缓慢「呼吸」（4.5%↔7.2%，~9s）。光标移动时，附近颗粒被向外排斥位移再弹簧归位，形成「游鱼破水」涟漪（canvas 颗粒场，仅扰动时显形）。自包含、幂等，z-index:1（在内容之下）。
- 全部尊重 `@media (prefers-reduced-motion:reduce)`（关动画/位移）与 `pointer:coarse`（触摸屏只留静态纹理，关涟漪）。

---

## 5. 响应式断点
- 主断点 `@media (max-width:820px)`：meta 三列→单列、story 双栏→单列、TOC 从粘性侧栏变横向 wrap、pager 上下堆叠。
- 容器内边距已用 `clamp()` 自适应，无需额外处理。

---

## 6. 新页面检查清单（动笔前过一遍）
- [ ] 复制了 `:root` token，没有硬编码色值
- [ ] 没有 box-shadow、没有圆角卡片、没有装饰性渐变
- [ ] 标题字重 ≤ 500，正文 14–14.5px、行高 ~2.0
- [ ] 容器 `max-width:1120px`、内边距 `clamp(20px,5vw,56px)`
- [ ] 交互元素加了 `data-hot`，过渡用了 `--ease-out` / `--ease-back`
- [ ] 顶部 nav（毛玻璃 + 进度）、底部 pager（细线分隔 + 上/下篇）齐全
- [ ] 引入了三套字体，做了 `prefers-reduced-motion` 降级
- [ ] `<body>` 末尾引入了 `atmosphere.js`（宣纸纹理 + 鼠标涟漪，全站统一）
- [ ] 陶土色只点在"热区"，没有大面积铺
