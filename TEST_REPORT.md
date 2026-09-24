# Product Intent Translator 测试报告

日期：2026-09-24。结论：**本地导出可运行，但被测版本未通过三项目集成验收。** 两个下游项目均拒绝当前原始导出；修正载荷后的正对照仅证明对应字段或导入格式可被接受，不证明当前导出兼容，也不证明线上链路已打通。

## 测试范围与方法

- 从已登录的 GitHub 浏览器读取测试时 main 的完整源码和示例，保存到 `snapshot/`，只规范化了文件末尾换行，没有缩短官方示例。
- 用 Python 3.12.14 实际启动仓库脚本；用 jsonschema 4.23.0 验证 Draft 2020-12 Schema。
- 用两个上游项目的实际源码执行输入校验和导入逻辑，无线上保存、API 鉴权、付费模型调用或代码实施。
- 测试阶段未修改远程仓库，也未执行线上写入。测试脚本、反例、产物与日志保存在测试证据归档中；本报告汇总其结果。

固定来源版本（以下结论针对这些版本，不代表后续修复后的状态）：

| 文件/项目 | 固定提交 |
|---|---|
| SKILL.md（行为模拟快照） | `10449093ced06be5944d8854f48795dcaa603f70` |
| scripts/pipeline.py | `177b3801960fe099f96cbeff134d4f1faea69644` |
| examples/short-video-intent.json | `75fdb7b5ebae168d2fe00b43c241a96e9f32af61` |
| schemas/product-intent.schema.json | `8fab7b20ee9348b5db92315822aeb65b13820e36` |
| prompts.chat | `f78a1c5136fa080155d928e0d7e2b4a41ddef03e` |
| prompt-optimizer | `897e56bf8af774c38b54cb2df0ebe5348ebac24c` |

## 本地脚本：13 项检查，6 通过、7 失败

| 检查 | 结果 | 实测证据 |
|---|---|---|
| Python 语法 | 通过 | 原始脚本可解析并执行 |
| Schema 定义合法性 | 通过 | Draft 2020-12 检查通过 |
| 官方示例符合 Schema | **失败** | `Additional properties are not allowed ('title' was unexpected)` |
| 官方示例生成三个文件 | 通过 | 子进程退出码 0，生成 prompt.md 和两个 JSON |
| 三份产物文本一致、JSON 可解析 | 通过 | 两个 JSON 内的 prompt 与 prompt.md 相同 |
| 原示例需求文字保留 | 通过 | 检查 16 段原始目标、要求、约束、验收、问题文字，无遗漏 |
| 输出完整 intent.json | **失败** | SKILL.md 列出的该交接产物没有生成 |
| 草稿状态与版本保留 | **失败** | 输入为 draft/revision 1，输出没有该标记或元数据 |
| 缺失 intent 时拒绝生成 | 通过 | 退出码非 0，无输出目录 |
| Schema 非法值被脚本拒绝 | **失败** | revision=-1、非法 source 和 readiness 仍退出 0 并生成输出 |
| 已拒绝需求不作为有效需求下发 | **失败** | status=rejected 的“每条视频强制付费”出现在普通 Requirements 列表中，拒绝状态消失 |
| 已锁定选择保留 | **失败** | 官方示例的 locked 状态被丢弃；why 也不渲染，且无原始记录交接 |
| 新意图不被旧 Prompt 静默覆盖 | **失败** | 非空 prompt_markdown 直接覆盖渲染；新加的“工作记录不得上传外部服务”约束消失 |

这些失败有共同原因：当前脚本只校验字段存在，忽略 Schema 的类型与枚举，并在渲染中丢失状态；已有 prompt_markdown 与结构化记录之间也没有同步或冲突检查。

## prompts.chat：当前导出不兼容

使用实际 `runs/official-example/dist/prompts-chat.json`，从固定上游源码提取原始 Zod 定义，用其 lockfile 中的 zod 4.2.1 执行 safeParse。

| 接入方式 | 当前输出 | 对照验证 |
|---|---|---|
| REST POST /api/prompts | **拒绝**：type="prompt" 非法，缺 tagIds 和 isPrivate | type="TEXT"、tagIds=[]、isPrivate=true 后通过字段校验 |
| MCP save_prompt | **拒绝**：type="prompt" 非法 | type="TEXT"、显式 isPrivate=true 后通过字段校验，tags 名称保留 |

当前输出也不是已验证的 UI 导入文件。源码中的管理员导入读取服务端 prompts.csv，并不接收这份 JSON。

对照通过只证明字段契约符合；没有验证账户登录、数据库标签 ID、真实保存和部署版本。MCP 参数文件仍需要 tools/call 请求封装与鉴权，不能直接当 HTTP 请求体发送。

源代码：

- [REST 输入定义](https://github.com/f/prompts.chat/blob/f78a1c5136fa080155d928e0d7e2b4a41ddef03e/src/app/api/prompts/route.ts#L12)
- [MCP save_prompt 输入定义](https://github.com/f/prompts.chat/blob/f78a1c5136fa080155d928e0d7e2b4a41ddef03e/src/pages/api/mcp.ts#L578)

测试证据归档中的执行记录为 `prompts-chat/contract-test/results.json`，同目录保存提取的 Schema、测试脚本和修正后的正对照载荷。

## prompt-optimizer：当前导出不兼容

直接执行固定上游版本的 DataImportExportManager、PromptDataConverter 和 ParameterValidator，对实际 `runs/official-example/dist/prompt-optimizer.json` 进行检查。

- 导入器返回 `success: false`，错误为 `Unknown or unsupported data format. Detected: unknown`。
- MCP 优化需要 `prompt` 参数，现有 systemPrompt/userPrompt 不是对应工具参数；iterate-prompt 另外需要 requirements。
- 将输入映射为 `format: "prompt-optimizer-standard"` 与 `messages: [{role, content}, ...]` 后，导入服务正对照成功。
- UI 导入组件实际只交接 messages/tools；附带 variables/testCases/evaluationCriteria 不代表它们会自动进入测试和评估流程。

测试脚本的 9 个断言通过表示“成功复现拒绝，并验证修正格式的正对照”，不表示现有导出兼容。没有运行应用界面或真实模型。

源代码：

- [导入格式识别](https://github.com/linshenkx/prompt-optimizer/blob/897e56bf8af774c38b54cb2df0ebe5348ebac24c/packages/ui/src/services/DataImportExportManager.ts#L164)
- [MCP 接口](https://github.com/linshenkx/prompt-optimizer/blob/897e56bf8af774c38b54cb2df0ebe5348ebac24c/packages/mcp-server/src/index.ts#L88)
- [UI 实际导入载荷](https://github.com/linshenkx/prompt-optimizer/blob/897e56bf8af774c38b54cb2df0ebe5348ebac24c/packages/ui/src/components/context-mode/ImportExportDialog.vue#L522)

测试证据归档中的执行记录为 `optimizer/contract-results.json`。

## Skill 行为模拟：三例符合核心预期

加载快照中的完整 SKILL.md，由一个 agent 对三个固定输入各生成一次回复，并保存输入、回复和 intent.json；主 agent 另行阅读了三份回复。本次结果与脚本的 13 项检查分开统计。

| 输入场景 | 实际行为 | 结果 |
|---|---|---|
| 只修改导出按钮文案 | 不追问；保留布局和数据处理约束；不把“导出 CSV”推导成重写导出功能 | 核心预期满足 |
| 数据来源未知的周报工具 | 只问一个影响接入实现的问题；标记 draft，公开来源和权限缺口 | 核心预期满足 |
| 已确认需求上追加分类筛选 | 不追问；继续保留浅色主题、无需登录和本地存储，交互默认值明确标为建议 | 核心预期满足 |

三份 intent.json 均通过 Draft 2020-12 Schema 校验。发现一处轻微问题：第一例将用户直接陈述和本轮执行上下文合并为一条 context 证据，应按来源拆开。

这只是一次明确加载规则、提供上下文后的 agent 模拟。生成和初步评价由同一 agent 完成，没有独立模型评委；第三例的历史决定已经包含在输入中，不能证明长期记忆或跨轮存储。没有验证安装后自动触发、真实模型优化、资料检索或线上集成。保存回复的 run_behavior.py 不调用模型，重跑不会产生新样本。

测试证据归档中的行为记录为 `behavior/evaluation.md`、`behavior/validation.json`，以及 `behavior/` 下三个用例目录中的输入和输出。

## 复现条件与证据索引

完整原始证据保存在本次本地测试工作区，未随本次文档同步上传。本节文件名只作本地证据索引，不表示本仓库已包含这些测试脚本和产物。

- 本地脚本测试使用 Python 3.12.14 和 jsonschema 4.23.0，测试依赖安装在隔离目录 `test-deps/`。对固定源码快照执行 `run_tests.py`，本次预期退出码为 1，因为 13 项验收中有 7 项失败。
- `test-results.json` 保存具体检查结果与快照 SHA-256；`runs/*/execution.json` 保存每次子进程命令、退出码和 stderr。
- `runs/official-example/dist/` 保存使用完整官方示例实际生成的三个输出文件。
- `runs/rejected-requirement/` 保存已拒绝需求被重新作为普通需求下发的反例。
- `runs/stale-prompt-after-change/` 保存旧 Prompt 遮盖新约束的反例。
- prompts.chat 合约测试使用固定源码中的原始 Zod 定义及其 lockfile 中的 zod 4.2.1，对原始导出执行校验，并另行验证修正载荷的正对照。
- prompt-optimizer 合约测试直接执行固定上游源码的导入器、转换器和参数校验器。测试脚本 `contract-check.mjs` 以原始 `prompt-optimizer.json` 为输入，通过 Node 的 `--experimental-transform-types` 加载相关 TypeScript 源码。
- `behavior/run_behavior.py` 只重建已记录的模拟回复并验证其 JSON；重复运行不构成新增行为样本。

## 修复优先级

1. 先修意图保真：保留 readiness、revision、锁定与拒绝状态；导出 intent.json；在生成前检查结构化记录与已有 Prompt 是否一致。
2. 让 Schema、官方示例和 CLI 共用验证规则，补 title 定义；非法输入应给出清楚错误。
3. 将两个自定义 JSON 改成具体接口的载荷：prompts.chat MCP 参数和 REST 参数分别适配；optimizer 区分会话导入与 MCP 优化参数。
4. 再接入真实服务，补齐检索、优化、测试结果回收、意图核对和迭代。加载两个 JSON 不等于这些步骤已完成。

本次结果不能证明线上全链路或产品实现质量；当前源码尚无两个外部服务的自动调用和结果回收，因此不是只补 API key 就能完成联调。
