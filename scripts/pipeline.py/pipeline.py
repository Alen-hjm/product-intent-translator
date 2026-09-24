#!/usr/bin/env python3
"""Render one product-intent record into a coding prompt and adapter payloads.
This script is deliberately offline. It does not call an LLM, prompts.chat, or
prompt-optimizer. Those systems can consume the generated JSON files later.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any
def _lines(items: list[dict[str, Any]], *, include_source: bool = True) -> str:
    result: list[str] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        text = str(item.get("text", "")).strip()
        if not text:
            continue
        source = item.get("source", "context")
        status = item.get("status")
        suffix = f" [{source}]" if include_source else ""
        if status and status != "active":
            suffix += f" ({status})"
        result.append(f"- {text}{suffix}")
    return "\n".join(result) or "- None recorded."
def validate(record: dict[str, Any]) -> list[str]:
    required = [
        "schema_version", "revision", "intent", "context",
        "requirements", "constraints", "assumptions",
        "open_questions", "acceptance", "prompt_markdown", "readiness",
    ]
    errors = [f"missing required field: {key}" for key in required if key not in record]
    if record.get("readiness") not in {"draft", "ready"}:
        errors.append("readiness must be draft or ready")
    if not isinstance(record.get("revision"), int):
        errors.append("revision must be an integer")
    if not isinstance(record.get("open_questions"), list):
        errors.append("open_questions must be an array")
    return errors
def render_prompt(record: dict[str, Any]) -> str:
    open_questions = record.get("open_questions", [])
    question_lines = []
    for question in open_questions:
        if isinstance(question, dict):
            q = str(question.get("question", "")).strip()
            impact = str(question.get("impact", "")).strip()
            if q:
                question_lines.append(f"- {q} — impact: {impact or 'unspecified'}")
    question_text = "\n".join(question_lines) or "- None."
    return f"""# Coding agent handoff
## Intent
{record.get('intent', '').strip()}
## Context
{_lines(record.get('context', []))}
## Requirements
{_lines(record.get('requirements', []))}
## Constraints
{_lines(record.get('constraints', []))}
## Suggestions and assumptions
{_lines(record.get('assumptions', []))}
## Acceptance checks
{chr(10).join(f'- {item}' for item in record.get('acceptance', []) if str(item).strip()) or '- Define observable checks before implementation.'}
## Open questions
{question_text}
## Execution rules
- Inspect the current repository and runtime before choosing a stack or path.
- Do not add capabilities, permissions, external services, or data collection that are not stated above.
- Report what was actually changed and verified. Keep unverified items visible.
- Preserve existing behavior and accepted choices unless this handoff explicitly changes them.
Readiness: {record.get('readiness')}. Revision: {record.get('revision')}.
""".strip() + "\n"
def build_assets(record: dict[str, Any]) -> dict[str, Any]:
    prompt = record.get("prompt_markdown") or render_prompt(record)
    title = str(record.get("title") or record.get("intent") or "Product intent handoff").strip()
    tags = ["product-intent", "coding-agent", "handoff"]
    return {
        "prompt_markdown": prompt,
        "prompts_chat": {
            "title": title,
            "description": "A traceable coding-agent handoff rendered from product intent.",
            "content": prompt,
            "type": "prompt",
            "tags": tags,
            "metadata": {"source": "product-intent-translator", "revision": record.get("revision")},
        },
        "prompt_optimizer": {
            "systemPrompt": "You are a coding agent. Follow the handoff faithfully and report evidence.",
            "userPrompt": prompt,
            "variables": [],
            "testCases": [{"name": "baseline handoff", "input": "Use the repository and user context provided with this task."}],
            "evaluationCriteria": record.get("acceptance", []),
            "metadata": {"source": "product-intent-translator", "revision": record.get("revision")},
        },
    }
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("intent", type=Path, help="input normalized intent JSON")
    parser.add_argument("--out", type=Path, default=Path("dist"), help="output directory")
    args = parser.parse_args()
    record = json.loads(args.intent.read_text(encoding="utf-8"))
    errors = validate(record)
    if errors:
        for error in errors:
            print(f"error: {error}")
        return 2
    assets = build_assets(record)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "prompt.md").write_text(assets["prompt_markdown"], encoding="utf-8")
    (args.out / "prompts-chat.json").write_text(json.dumps(assets["prompts_chat"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.out / "prompt-optimizer.json").write_text(json.dumps(assets["prompt_optimizer"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.out / 'prompt.md'}")
    print(f"wrote {args.out / 'prompts-chat.json'}")
    print(f"wrote {args.out / 'prompt-optimizer.json'}")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
