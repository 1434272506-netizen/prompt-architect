"""Set repository description and topics (strict UTF-8), then read back.

Token comes from env DSH_GH_TOKEN (never printed, never written to disk).
"""
import json
import os
import sys
import urllib.request
import urllib.error

REPO = "1434272506-netizen/prompt-architect"
DESCRIPTION = ("Prompt Architect \u2014 a traceable architecture for turning ambiguous "
               "user intent into controlled, adaptive AI interactions.")
TOPICS = [
    "prompt-engineering",
    "ai-agent",
    "llm",
    "agent-architecture",
    "human-ai-interaction",
    "adaptive-interview",
    "decision-making",
    "ai-assistant",
    "prompt-architect",
]


def opener():
    proxy = "http://127.0.0.1:12000"
    return urllib.request.build_opener(
        urllib.request.ProxyHandler({"https": proxy, "http": proxy}))


def call(method, url, token, payload=None):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "dsh-repo-meta",
        })
    with opener().open(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    token = os.environ.get("DSH_GH_TOKEN")
    if not token:
        print("FAIL: DSH_GH_TOKEN not set")
        return 2

    try:
        repo = call("PATCH", f"https://api.github.com/repos/{REPO}", token,
                    {"description": DESCRIPTION})
        print("PATCH description  = OK")
        topics = call("PUT", f"https://api.github.com/repos/{REPO}/topics", token,
                      {"names": TOPICS})
        print("PUT topics         = OK")
    except urllib.error.HTTPError as exc:
        print(f"HTTP {exc.code}: {exc.read().decode('utf-8', 'replace')[:600]}")
        return 1

    # read-back
    rb = call("GET", f"https://api.github.com/repos/{REPO}", token)
    got_desc = rb.get("description") or ""
    print(f"description set    = {got_desc == DESCRIPTION}")
    print(f"description len    = {len(got_desc)}")
    print(f"description        = {got_desc}")
    print(f"topics set         = {sorted(topics.get('names', [])) == sorted(TOPICS)}")
    print(f"topics             = {topics.get('names')}")
    print(f"visibility         = {rb.get('visibility')}  default_branch = {rb.get('default_branch')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
