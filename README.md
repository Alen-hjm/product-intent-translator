# Product Intent Translator

产品经理与 coding agent 之间的产品意图翻译器。

目标：以尽可能低的表达和决策门槛，产出符合用户预期、能够持续演进的产品。

## 当前状态

仓库已提供首个可测试版本：

- 根目录 SKILL.md：可安装的意图翻译规则。
- schemas/product-intent.schema.json：统一的意图与交接数据结构。
- scripts/pipeline.py：离线渲染器，将意图记录输出为 coding Prompt、prompts.chat 资产和 prompt-optimizer 测试载荷。
- examples/short-video-intent.json：短视频产品测试样例。
- integrations/pipeline.md：三段链路的接入说明。

原型编辑、页面运行、真实模型调用和 UI 选择仍需要外部工具；本仓库不会把未执行的预览、测试或业务结果写成已完成。

## 三段链路

1. product-intent-translator 负责保留用户意图，区分事实、建议、假设和未决问题，并生成可核对的 coding-agent Prompt。
2. prompts.chat 可保存和检索生成的 Prompt/Skill 资产。
3. prompt-optimizer 可对生成的 Prompt 做真实执行、评估和版本比较。

离线生成示例：

    python scripts/pipeline.py examples/short-video-intent.json --out dist

## 核心方向

### UI 意图对齐

让用户通过自然语言、参考、方案选择、局部比较与 DIY 表达视觉和体验需求。将这些表达转换为可追溯的设计依据与 agent 可执行的要求，并在实际实现后核对结果。

### 持续演进能力

针对有依据的后续变化，保留合理的产品与代码结构。新增功能时延续已认可的视觉语言，保持旧功能与数据的有效性，同时避免提前堆积无用功能和复杂架构。

## 设计与研究

- [整体设计草案](docs/superpowers/specs/2026-09-22-vibe-coding-contract-design.md)
- [核心设计：视觉对齐与持续演进](docs/superpowers/specs/2026-09-22-product-intent-core-design.md)
- [24 项 UI 资源与选择机制](docs/research/2026-09-22-ui-library-catalog.md)
