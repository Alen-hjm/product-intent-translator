# 集成状态与接口说明

状态更新：2026-09-24。**当前仅有实验性离线导出，三项目自动链路尚未打通。** 直接导入现有两个 JSON 的说明已由实测结果纠正，见 [测试报告](../TEST_REPORT.md)。

## 分工

1. product-intent-translator 整理产品意图、证据、建议、未决问题、UI 决定和验收条件，形成完整的 Markdown 交接说明。
2. prompts.chat 提供 Prompt / Skill 资产的保存、检索和复用能力；本仓库尚未实现相应客户端。
3. prompt-optimizer 提供提示词优化和模型测试能力；本仓库尚未实现工具调用、评估结果回收或迭代编排。

## 当前离线输出

```sh
python scripts/pipeline.py examples/short-video-intent.json --out dist
```

脚本读取意图 JSON，生成 prompt.md、prompts-chat.json、prompt-optimizer.json，不访问网络。它目前不生成 intent.json，也不完整校验 Schema；会丢失状态，并可能让旧 prompt_markdown 遮盖新需求。因此这些输出只能用于排查和开发适配，不能作为完整、可靠的意图交接包。

## prompts.chat 接口差异

所测版本：`f78a1c5136fa080155d928e0d7e2b4a41ddef03e`。

| 入口 | 实测要求与结果 |
|---|---|
| REST POST /api/prompts | 现有 type="prompt" 非法，缺少 tagIds 和 isPrivate；标签名称不等于数据库标签 ID |
| MCP save_prompt | 现有 type="prompt" 非法；改用 type="TEXT" 并显式设置 isPrivate=true 的正对照通过字段校验，tags 可使用名称 |
| UI 导入 | 未验证存在接收本仓库 JSON 的通用入口；所查管理员导入使用服务端 prompts.csv |

以上正对照仅通过字段校验。REST 与 MCP 需要各自的适配；MCP 参数还需 tools/call 封装及实际部署的鉴权。未测试线上保存或发布。

## prompt-optimizer 接口差异

所测版本：`897e56bf8af774c38b54cb2df0ebe5348ebac24c`。

- 当前 systemPrompt/userPrompt/variables/testCases/evaluationCriteria 对象被原始导入器拒绝：`Unknown or unsupported data format. Detected: unknown`。
- 上下文导入使用 `format: "prompt-optimizer-standard"` 以及 `messages: [{role, content}, ...]` 的正对照通过导入服务校验。
- MCP 优化工具接收 `prompt` 参数；`iterate-prompt` 还要求 `requirements`。这与会话导入格式是两个入口。
- UI 导入组件只交接 messages/tools；附带 testCases 或 evaluationCriteria 不会自动建立评估流程。

尚未运行应用 UI 或真实模型调用，不能将格式校验通过表述为优化和评估已完成。

## 完成链路所需工作

1. 修复离线交接保真与 Schema 校验，保留 intent.json、readiness、revision 和选择状态，避免旧 Prompt 覆盖新约束。
2. 选定具体接入入口，按其实际契约实现适配，并保留来源意图与输出的对应关系。
3. 实现外部调用、错误处理与结果回收，再用真实服务验证检索、保存、优化和测试。
4. 将优化建议与用户原始意图区分，核对未撤销的约束，记录版本和实际验证证据。

`ready` 仅表示信息足够开始实施，不代表代码已构建、测试或发布。外部调用应遵循用户已授权的范围和目标服务权限，不得把文件生成成功当作接入成功。
