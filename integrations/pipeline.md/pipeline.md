# Pipeline integration
The handoff is intentionally split into three stages:
1. product-intent-translator owns product intent, evidence, assumptions, open questions, UI decisions, acceptance checks, and change history.
2. prompts.chat can store or search the rendered coding prompt as a reusable prompt or skill asset. The adapter file is prompts-chat.json.
3. prompt-optimizer can execute and compare the rendered prompt against real models. The adapter file is prompt-optimizer.json.
## Offline first
scripts/pipeline.py only reads a normalized intent JSON file and writes local artifacts. It does not send user data to a third party and it does not require API keys.
    python scripts/pipeline.py examples/short-video-intent.json --out dist
## External adapters
- Import dist/prompts-chat.json through the prompts.chat UI/API or adapt its title, description, content, type, and tags fields to the current endpoint.
- Import dist/prompt-optimizer.json into the prompt-optimizer UI/MCP. Use userPrompt as the candidate prompt, evaluationCriteria as the evaluation rubric, and testCases as baseline inputs.
- Keep the original intent.json beside every result. Optimized wording must not overwrite the source intent or silently change requirements.
- When an optimizer proposes a change, record it as a suggestion or open question first. Promote it to an active requirement only after the product owner accepts it.
## Readiness
ready means the receiving agent has enough information to start. It does not mean the code has been built, tested, published, or authorized to access external data.
