# UI 资源目录与可选设计机制

调研日期：2026-09-22。用途：为 `vibe-prompt-translator` 的视觉选择层提供参考资源和设计规则。

本轮整理 24 项资源。依据为作者官方文档、官方 GitHub 仓库及许可证页面；本轮没有安装组件、运行示例或实测跨库兼容性。以下“适用方向”为本项目的设计判断，并非作者保证的效果。资源目录与预览选择器尚未实现。

## 1. 资源分层

页面模板决定内容组织；组件提供交互和实现基础；主题控制视觉参数；动效提供反馈和表现。选中一种风格不等于选中一个 npm 包，也不意味着自动改变现有项目技术栈。

### 基础组件与页面区块

| ID | 官方资源 / 源码 | 可提供的候选材料 | 技术边界与使用记录 |
| --- | --- | --- | --- |
| U01 | [shadcn/ui](https://ui.shadcn.com/) · [GitHub](https://github.com/shadcn-ui/ui) | 可修改的组件、应用界面基础，适合建立统一基础后变化风格 | 核心仓库 MIT；按具体 registry 项检查依赖与版本，不能把第三方 registry 视为官方 |
| U02 | [Mantine](https://mantine.dev/) · [GitHub](https://github.com/mantinedev/mantine) | 表单、日期、通知、图表等应用组件；官方预制响应式区块 | React；核心 MIT；适合功能密集的应用界面，具体版本适配使用前核实 |
| U03 | [Ant Design](https://ant.design/) · [GitHub](https://github.com/ant-design/ant-design) | 企业应用、表格和管理界面方向 | React；[许可证入口](https://github.com/ant-design/ant-design/blob/master/LICENSE)，纳入时核对实际采用版本；不因使用它就强制采用默认蓝色后台样式 |
| U04 | [HeroUI](https://www.heroui.com/) · [GitHub](https://github.com/heroui-inc/heroui) | 现代应用组件、主题化的界面基础 | React；核心 MIT；旧名 NextUI，避免按旧名称检索后直接使用旧教程 |
| U05 | [Headless UI](https://headlessui.com/) · [GitHub](https://github.com/tailwindlabs/headlessui) | 无预设视觉的交互组件，便于高度定制 | React/Vue；MIT；本身不是现成风格模板，需要配合样式和布局 |
| U06 | [Nuxt UI](https://ui.nuxt.com/) · [GitHub](https://github.com/nuxt/ui) · [官方模板](https://github.com/nuxt-ui-templates) | Dashboard、Landing、Docs、SaaS、Chat、Portfolio 等页面原型来源 | Vue/Nuxt；核心 MIT；每个模板单独核对许可证和依赖；旧 nuxt-ui-pro 组织已指向模板新地址 |
| U07 | [Skeleton](https://www.skeleton.dev/) · [GitHub](https://github.com/skeletonlabs/skeleton) | Tailwind 设计系统、主题与应用界面材料 | 核心 MIT；针对具体框架适配读取当前文档，不把所有组件当成框架无关 |
| U08 | [daisyUI](https://daisyui.com/) · [主题预览](https://daisyui.com/docs/themes/) · [GitHub](https://github.com/saadeghi/daisyui) | 同一界面的主题切换；可选商务、复古、柔和、深色等色彩方向 | Tailwind/CSS；核心 MIT；主题变化主要服务视觉比较，不能冒充布局方案变化；商业模板另查 |
| U09 | [HyperUI](https://hyperui.dev/) · [GitHub](https://github.com/markmead/hyperui) | 营销、应用、电商的布局区块；可复制 HTML/Tailwind | MIT；没有统一包安装要求；复制外观后仍需补齐实际业务行为 |
| U10 | [Flowbite](https://flowbite.com/) · [GitHub](https://github.com/themesberg/flowbite) | Tailwind 组件与页面区块，作为后台、内容站与营销页候选 | 核心 MIT；Pro、付费模板与单独框架适配分别检查，不默认所有资源同一许可 |
| U11 | [PrimeVue 原仓库](https://github.com/primefaces/primevue) | 既有 Vue 项目的组件和界面参考 | **暂缓作为新项目默认选项**：查阅时原仓库公告仅继续安全修复，开发迁往 PrimeUI；原 MIT 版本仍 MIT，新发行渠道和条件须另查 |

### 动效组件与表现区块

| ID | 官方资源 / 源码 | 可提供的候选材料 | 技术边界与使用记录 |
| --- | --- | --- | --- |
| U12 | [Magic UI](https://magicui.design/) · [GitHub](https://github.com/magicuidesign/magicui) | 动态文字、背景、展示区块与细节效果 | React/Tailwind 生态；仓库 MIT；具体组件单独查依赖，商业产品另查 |
| U13 | [React Bits](https://reactbits.dev/) · [GitHub](https://github.com/DavidHDev/react-bits) | 个性化文字、背景、交互和微动效 | 原作者仓库为 **MIT + Commons Clause**；[许可原文](https://github.com/DavidHDev/react-bits/blob/main/LICENSE.md)对组件本身的转售、再许可和再分发有限制；可作为参考目录，不能默认将组件源码批量打包进 skill |
| U14 | [Aceternity UI](https://ui.aceternity.com/) · [分类预览](https://ui.aceternity.com/explore) | 首屏、Bento、导航、背景、卡片与营销模板 | React/Tailwind/Motion；官方有免费组件与付费区块、模板；按所选条目核对访问权限和条款；本轮未认定统一开源许可 |
| U15 | [Motion Primitives](https://motion-primitives.com/) · [GitHub](https://github.com/ibelick/motion-primitives) | 动态文字和组件过渡的参考实现 | Motion/Tailwind；MIT；README 提示 beta，需测试实际选中项 |

### 动画引擎与播放工具

| ID | 官方资源 / 源码 | 可提供的候选材料 | 技术边界与使用记录 |
| --- | --- | --- | --- |
| U16 | [Motion](https://motion.dev/) · [GitHub](https://github.com/motiondivision/motion) | 布局变化、进出场、弹簧、手势等可控动效 | 核心 MIT；JS/React/Vue 使用各自适配；Motion+ 是另一个付费范围 |
| U17 | [GSAP 文档](https://gsap.com/docs/v3/) · [标准许可](https://gsap.com/community/standard-license/) | 复杂时间线、滚动叙事、联动动画 | 使用自有标准许可，不标成 MIT；若产品涉及可视化动效编辑与生成能力，须核对许可中相关适用范围 |
| U18 | [Anime.js](https://animejs.com/) · [GitHub](https://github.com/juliangarnier/anime) | DOM、SVG、属性和时间线动画 | MIT；原生 JavaScript 路线；避免把旧版示例 API 当成当前接口 |
| U19 | [AutoAnimate](https://auto-animate.formkit.com/) · [GitHub](https://github.com/formkit/auto-animate) | 列表增删、重排等轻量过渡 | MIT；可用于多种 JS 框架；适合操作反馈，不承担整页设计 |
| U20 | [Lottie Web](https://github.com/airbnb/lottie-web) | 动画插画、加载和状态表现 | 播放器 MIT；动画文件、插画和字体的许可需单独核对，播放器许可不覆盖素材 |

### 配色与特殊风格

| ID | 官方资源 / 源码 | 可提供的候选材料 | 技术边界与使用记录 |
| --- | --- | --- | --- |
| U21 | [tweakcn](https://tweakcn.com/) · [GitHub](https://github.com/jnsahaj/tweakcn) | 可视化主题编辑、预设风格；参考其“边看边调整”方式 | 查阅时仓库标注 Apache-2.0；主要面向 shadcn/Tailwind；主题不等于页面布局 |
| U22 | [Radix Colors](https://www.radix-ui.com/colors) · [GitHub](https://github.com/radix-ui/colors) | 色阶与语义配色，帮助候选方案保持一致 | MIT；最终文字/背景组合仍需检测，不因使用色库就自动判定可访问性通过 |
| U23 | [NES.css](https://nostalgic-css.github.io/NES.css/) · [GitHub](https://github.com/nostalgic-css/NES.css) | 8-bit、复古像素方向 | CSS；代码 MIT、文档另有许可；README 指出推荐的英文字体不覆盖其他语言，中文候选必须检查字形和回退 |
| U24 | [Wired Elements](https://wiredjs.com/) · [GitHub](https://github.com/rough-stuff/wired-elements) | 手绘、草图、轻松有趣的控件风格 | Web Components；MIT；接入框架、表单行为和可访问性需实际验证 |

## 2. 从资源目录到用户可选的设计

目录中库名用于 agent 选材。用户看到的是适合自己产品的视觉方案和可操作预览。预览区分“官方素材示例”“本产品概念预览”“实际运行版本”，不把仓库 README 的效果描述当成已观察到的效果。

### 可组合维度

| 维度 | 候选方向举例 | 用户如何选择 |
| --- | --- | --- |
| 页面用途 | 营销首页、工作台、管理后台、内容阅读、作品集、电商、编辑器、移动工具 | 从已知需求推断，无须重复问；用户可切换 |
| 整体风格 | 克制工具感、企业专业、温暖自然、编辑排版、奢雅展示、明亮活泼、粗线条强对比、复古像素、手绘、工业仪表、暗色科技、沉浸影像 | 先看少量差异明显的完整方案，支持“更多风格”和自带参考 |
| 布局 | 左导航工作区、顶部导航、主次双栏、主从三栏、单列阅读、卡片网格、看板、分屏、全屏画布、移动底栏 | 用相同内容的线框或缩略预览比较，保持任务相同 |
| 配色 | 冷静蓝、自然绿、暖中性、黑白强调色、柔和粉彩、深色低饱和、高对比双色、自定义品牌色 | 同一页面即时换色；配色命名不代替具体色值 |
| 字体与密度 | 标题与正文搭配、中文优先字族、舒展/标准/紧凑、不同标题层级 | 看同一段真实长度文案；检查中文、数字和英文混排 |
| 组件外观 | 直角/小圆角/大圆角、实心/描边按钮、平面/分层卡片、图标线条与填充 | 局部组件对照，不必重画全部页面 |
| 动效 | 无装饰动效、轻反馈、表现增强、叙事动效 | 使用真实播放预览，支持暂停/重播；静态图片不能验证动效 |
| 素材语言 | 摄影、线性图标、扁平插画、手绘、纹理、3D | 使用适合产品的样例；素材来源与许可独立记录 |

这些是可扩展分类，不是限制用户只能选的枚举全集。框架相容、内容适配与基本可用性会限制某些组合；不能用维度数量相乘来宣称已有数万套有效模板。

### 选择流程

1. 依据用户需求和已有项目筛选，默认展示 3—4 套差异明显的完整方向；用户要看全部时提供分类浏览。每套使用相同产品内容、关键任务和视口，不能只换颜色冒充不同布局。
2. 每张方案卡显示稳定编号、可见预览、适合本需求的理由和主要取舍。用户可选择、排除、收藏、指定局部，也能说“都不喜欢”。
3. 支持“保留 A 的布局，用 B 的颜色，卡片像 C”。接收此表达后提取布局和设计参数，统一字号、间距、图标、边框、状态色，再生成融合后的预览；不直接堆叠多个完整组件库。
4. 用户可锁定已满意的维度。反馈只改变相关维度，给出相同内容的前后对比；改变锁定项时解释冲突并保留回退版本。
5. 用户表示满意后记录本轮选中组合，再把具体参数、组件出处、交互规则及验收方法写入 agent Prompt。点击喜欢一个参考只表明视觉偏好，不等于批准添加该模板中的账号、付费或其他功能。
6. 实施后用实际渲染与选定预览核对；动效、交互和移动布局分别检查。用户可回到任一步修改，未撤销的需求继续保留。

首批方案数是交互默认值，不是上限。用户可以直接给精确要求，跳过不需要的选择步骤；无预览工具时提供可访问的官方演示链接并明确尚未生成本产品预览，不能声称用户已经选过实物。

## 3. 给 agent 的视觉交接信息

内部拟记录：

- `selection_id`、`revision`、`preview_ref`：指向用户实际看过的版本。
- `layout`：内容次序、区域关系、宽度策略、移动端变化。
- `tokens`：语义色值、字族、字号层级、间距、圆角、阴影与边框。
- `components`：角色与行为、所选资源 ID、具体文档/组件地址、适配方式。
- `motion`：触发条件、目标属性、时长、缓动、取消/重播、减少动态效果时的替代。
- `locked_dimensions`、`rejected_directions`：已认可部分和不喜欢的方向及原因，只作用于当前项目。
- `provenance`：用户明确选择、默认建议、融合修正分别标记。
- `acceptance`：主任务路径、信息层级、窄屏、键盘、文字对比、溢出与动态效果检查。

示例交接语义：“采用方案 A-02 的左导航结构与 C-03 的语义配色；保持今日待办为主信息；保留现有数据和交互行为；只给列表变化增加轻过渡。预览引用与实际参数随 Prompt 一并提供。”实际色值与时长必须从选定预览提取，不能只交付 A/B/C 编号，也不凭空填入数值冒充用户选择。

## 4. 资源条目维护要求

收录单位应逐步细化到具体模板、区块或组件，而非只停留在库首页。每项记录：官方 URL、源码出处、组件路径、核验日期、版本/commit（使用时固定）、框架/依赖、适用任务、视觉标签、预览方式、价格/许可范围、已知限制、可替代项和实际测试状态。

本轮 24 项是发现层目录；没有记录的版本、性能和兼容性标记为未核验。真正生成候选时，只读取和验证相关的少量条目。对失效链接、迁移项目、许可变化或不兼容版本更新目录；不自动把全库文档、代码和素材下载到 skill 中，也不为“持续更新”创建定时任务。

## 5. 首版验证场景

- 同一后台任务的候选确实有不同信息结构，不能只是三种主色。
- 用户只更改配色时，已认可的布局和业务功能保持有效。
- 选择“布局 A + 配色 B + 动效 C”后，融合预览统一且能在既有技术栈实现。
- 用户说“都不喜欢”时，支持新方向和自带参考，不强迫选最接近的一个。
- 用户选了含登录的营销模板，最终 Prompt 不因此添加未请求的账号功能。
- 用户选择的某项是付费资源或许可不适合打包时，明确差异并给可用替代，不暗中换成不同效果。
- 中文长标题、空内容、长列表、窄屏、减少动态效果模式下均检查实际展示。
- 移交到没有当前聊天历史的 agent，仍可根据预览引用和参数还原方向。

以上为待执行的验证方案。本轮只完成资源研究和设计落盘。
