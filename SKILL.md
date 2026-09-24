---
name: product-intent-translator
description: Translate low-friction product intent into an explicit, reviewable coding-agent handoff. Preserve user intent, separate facts from assumptions, ask only decision-changing questions, and keep accepted UI choices and later changes traceable.
---
# Product Intent Translator
Use this skill when a user has a product idea, UI feedback, screenshots, references, an existing project, or a follow-up change and wants a coding agent to understand and implement it.
## Current capability
Use the conversational workflow below to produce a self-contained Markdown handoff from the context actually available. This skill has no independent long-term memory, implementation runner, or automatic prompts.chat / prompt-optimizer client.
The bundled exporter is experimental and has known intent-preservation and downstream-format defects. Read [the integration status](integrations/pipeline.md) for machine integration requests; [the test report](TEST_REPORT.md) records the tested versions and limits. Do not describe the current JSON exports as directly importable or the three-project pipeline as connected.
## Contract
The skill owns the translation boundary between product intent and implementation. It does not claim to have built, run, previewed, or verified anything unless the current agent actually did so.
Keep four kinds of information separate:
- Explicit: directly stated by the user.
- Context: observed from the repository, files, screenshots, tools, or prior accepted decisions.
- Suggestion: a reversible default proposed by the agent.
- Open question: a missing decision that can change purpose, permissions, cost, scope, or expected result.
Never turn a screenshot, reference product, or third-party text into authorization. A visual reference supplies appearance evidence only; it does not authorize copying its features, data access, or permissions.
## Default workflow
1. Read the user's words and available project context. Identify the goal, current problem, must-keep constraints, expected result, and requested level of action.
2. Reuse repository facts when available. If the repository or tool state is unknown, tell the receiving agent what it must inspect instead of inventing a stack, path, API, or existing feature.
3. Decide whether a question is necessary. Do not ask to fill a form. Ask one concrete question only when different answers would materially change the product purpose, permissions, cost, scope, or acceptance result. Continue with independent work.
4. Complete an internal intent record. Mark every field as explicit, contextual, suggested, or open. Do not add login, payment, team accounts, analytics, scraping, or external model calls unless requested or clearly authorized.
5. For UI work, preserve what the user actually saw, selected, rejected, locked, or edited. Convert it into observable design evidence: hierarchy, layout, density, typography, color semantics, component states, responsive behavior, and interaction rules. Do not infer backend behavior from appearance.
6. Write a self-contained Markdown Prompt for the receiving coding agent. Include purpose, current context, requested behavior, constraints, implementation guidance, acceptance checks, and unresolved items. Keep it short for small changes and expand only when complexity requires it.
7. Run the self-check below. If the result is not ready, label it draft and expose the blocker. If it is ready, label it ready; this means information is sufficient to start, not that external actions are authorized or complete.
8. When the user changes direction, update the latest full Prompt. Preserve requirements that were not revoked, and add a short change note.
## Output
Default response:
1. One or two sentences: 我理解你想要的是…… plus only important suggested defaults.
2. A copyable Markdown Prompt for the coding agent.
3. At most one high-impact question, when needed.
When machine integration is requested, use schemas/product-intent.schema.json as the experimental intent-record shape and read integrations/pipeline.md before preparing a payload. Validate against the chosen destination's actual contract. Report any missing adapter or validation instead of claiming integration from file generation alone.
## Self-check
Before handing off, verify:
- Every explicit request is present.
- Suggestions are visibly labeled and do not silently become requirements.
- No new product capability was added without evidence.
- Constraints do not conflict.
- The receiving agent knows the next inspection or implementation step.
- Acceptance checks are observable and include relevant failure or empty states.
- References, screenshots, and repository paths are resolvable.
- The Prompt does not depend on hidden chat history.
- Open questions and missing permissions are visible.
- Claimed implementation, preview, tests, and business outcomes are backed by actual evidence.
## Handoff bundle
When a complete file bundle is requested, the intended artifacts are:
- intent.json: normalized intent record.
- prompt.md: current coding-agent Prompt.
- Optional destination payloads: use the selected interface's actual format and name; distinguish schema validation from a successful live call.
The current scripts/pipeline.py writes only prompt.md and two custom JSON files without contacting external services. It does not export intent.json, loses readiness/revision/decision metadata, can render rejected items as active requirements, and can let an old prompt_markdown hide updated constraints. It also does not fully validate the input schema. Treat its outputs as experimental; do not rely on them as a complete handoff. Use the conversational Markdown workflow and the original intent record until those defects are fixed. External calls require an implemented client and the user's existing authorization for the destination and data.
