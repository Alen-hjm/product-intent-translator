#!/usr/bin/env python3
import argparse, json
from pathlib import Path
def render(r):
    def bullets(key):
        return \n.join("- " + str(x.get("text","")) + " [" + str(x.get("source","context")) + "]" for x in r.get(key, [])) or "- None recorded."
    qs = \n.join("- " + str(x.get("question","")) + " — " + str(x.get("impact","")) for x in r.get("open_questions", [])) or "- None."
    checks = \n.join("- " + str(x) for x in r.get("acceptance", [])) or "- Define observable checks."
    return "# Coding agent handoff\n\n## Intent\n" + str(r.get("intent","")) + "\n\n## Context\n" + bullets("context") + "\n\n## Requirements\n" + bullets("requirements") + "\n\n## Constraints\n" + bullets("constraints") + "\n\n## Suggestions and assumptions\n" + bullets("assumptions") + "\n\n## Acceptance checks\n" + checks + "\n\n## Open questions\n" + qs + "\n\nInspect the repository before choosing a stack. Do not add capabilities or permissions that are not stated. Report actual changes and verification.\n"
def main():
    p=argparse.ArgumentParser(); p.add_argument("intent",type=Path); p.add_argument("--out",type=Path,default=Path("dist")); a=p.parse_args()
    r=json.loads(a.intent.read_text(encoding="utf-8")); required=["schema_version","revision","intent","context","requirements","constraints","assumptions","open_questions","acceptance","readiness"]
    missing=[k for k in required if k not in r]
    if missing: raise SystemExit("missing: " + ", ".join(missing))
    prompt=r.get("prompt_markdown") or render(r); a.out.mkdir(parents=True,exist_ok=True)
    (a.out/"prompt.md").write_text(prompt,encoding="utf-8")
    (a.out/"prompts-chat.json").write_text(json.dumps({"title":r.get("title",r["intent"]),"description":"Traceable coding-agent handoff","content":prompt,"type":"prompt","tags":["product-intent","coding-agent","handoff"]},ensure_ascii=False,indent=2),encoding="utf-8")
    (a.out/"prompt-optimizer.json").write_text(json.dumps({"systemPrompt":"You are a coding agent. Follow the handoff faithfully and report evidence.","userPrompt":prompt,"variables":[],"testCases":[{"name":"baseline"}],"evaluationCriteria":r.get("acceptance",[])},ensure_ascii=False,indent=2),encoding="utf-8")
if __name__=="__main__": main()
