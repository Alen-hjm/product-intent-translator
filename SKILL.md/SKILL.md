---
name: product-intent-translator
description: Translate low-friction product intent into an explicit, reviewable coding-agent handoff. Preserve user intent, separate facts from assumptions, ask only decision-changing questions, and keep accepted UI choices and later changes traceable.
---
# Product Intent Translator
Use this skill when a user has a product idea, UI feedback, screenshots, references, an existing project, or a follow-up change and wants a coding agent to understand and implement it.
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
When machine integration is requested, also emit the JSON shape in schemas/product-intent.schema.json and adapter payloads described in integrations/pipeline.md.
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
For a complete handoff, produce:
- intent.json: normalized intent record.
- prompt.md: current coding-agent Prompt.
- prompts-chat.json: optional Prompt/Skill asset payload for prompts.chat.
- prompt-optimizer.json: optional optimization/test payload for prompt-optimizer.
The bundled script scripts/pipeline.py renders these files from a normalized intent JSON file without contacting external services. External calls remain opt-in and must be performed by the receiving tool with its own credentials and permissions.
