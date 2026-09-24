#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

def lines(items):
    return chr(10).join('- ' + str(x.get('text', '')) + ' [' + str(x.get('source', 'context')) + ']' for x in items) or '- None recorded.'

def render(record):
    questions = chr(10).join('- ' + str(x.get('question', '')) + ' — ' + str(x.get('impact', '')) for x in record.get('open_questions', [])) or '- None.'
    checks = chr(10).join('- ' + str(x) for x in record.get('acceptance', [])) or '- Define observable checks.'
    return '# Coding agent handoff' + chr(10) + chr(10) + '## Intent' + chr(10) + str(record.get('intent', '')) + chr(10) + chr(10) + '## Context' + chr(10) + lines(record.get('context', [])) + chr(10) + chr(10) + '## Requirements' + chr(10) + lines(record.get('requirements', [])) + chr(10) + chr(10) + '## Constraints' + chr(10) + lines(record.get('constraints', [])) + chr(10) + chr(10) + '## Suggestions and assumptions' + chr(10) + lines(record.get('assumptions', [])) + chr(10) + chr(10) + '## Acceptance checks' + chr(10) + checks + chr(10) + chr(10) + '## Open questions' + chr(10) + questions + chr(10) + chr(10) + 'Inspect the repository before choosing a stack. Do not add capabilities or permissions that are not stated. Report actual changes and verification.' + chr(10)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('intent', type=Path)
    parser.add_argument('--out', type=Path, default=Path('dist'))
    args = parser.parse_args()
    record = json.loads(args.intent.read_text(encoding='utf-8'))
    required = ['schema_version', 'revision', 'intent', 'context', 'requirements', 'constraints', 'assumptions', 'open_questions', 'acceptance', 'readiness']
    missing = [key for key in required if key not in record]
    if missing:
        raise SystemExit('missing: ' + ', '.join(missing))
    prompt = record.get('prompt_markdown') or render(record)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / 'prompt.md').write_text(prompt, encoding='utf-8')
    (args.out / 'prompts-chat.json').write_text(json.dumps({'title': record.get('title', record['intent']), 'description': 'Traceable coding-agent handoff', 'content': prompt, 'type': 'prompt', 'tags': ['product-intent', 'coding-agent', 'handoff']}, ensure_ascii=False, indent=2), encoding='utf-8')
    (args.out / 'prompt-optimizer.json').write_text(json.dumps({'systemPrompt': 'You are a coding agent. Follow the handoff faithfully and report evidence.', 'userPrompt': prompt, 'variables': [], 'testCases': [{'name': 'baseline'}], 'evaluationCriteria': record.get('acceptance', [])}, ensure_ascii=False, indent=2), encoding='utf-8')

if __name__ == '__main__':
    main()
