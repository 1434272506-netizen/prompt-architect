"""Update the existing GitHub Release with the real notes (strict UTF-8).

Reads the token from env DSH_GH_TOKEN (never printed, never written to disk).
Reads the notes body from .gh-search/_release-notes-v0.4.0-rc.2.md.
"""
import json
import os
import sys
import urllib.request
import urllib.error

REPO = "1434272506-netizen/prompt-architect"
RELEASE_ID = 402425378
NOTES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_release-notes-v0.4.0-rc.2.md")


def build_opener():
    """Prefer the local proxy that this machine's VPN exposes for github.com."""
    proxy = "http://127.0.0.1:12000"
    return urllib.request.build_opener(urllib.request.ProxyHandler({"https": proxy, "http": proxy}))


def main():
    token = os.environ.get("DSH_GH_TOKEN")
    if not token:
        print("FAIL: DSH_GH_TOKEN not set")
        return 2

    with open(NOTES, "r", encoding="utf-8-sig") as fh:
        body = fh.read().lstrip("\ufeff")

    payload = {
        "name": "Prompt Architect v0.4.0-rc.2 \u2014 Release Candidate",
        "body": body,
        "prerelease": True,
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/releases/{RELEASE_ID}",
        data=data,
        method="PATCH",
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "dsh-release-updater",
        },
    )
    try:
        with build_opener().open(req, timeout=60) as resp:
            out = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        print(f"HTTP {exc.code}: {exc.read().decode('utf-8', 'replace')[:800]}")
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL: {exc!r}")
        return 1

    print(f"OK release id      = {out['id']}")
    print(f"OK tag_name        = {out['tag_name']}")
    print(f"OK name            = {out['name']!r}")
    print(f"OK prerelease      = {out['prerelease']}")
    print(f"OK draft           = {out['draft']}")
    print(f"OK body_chars      = {len(out['body'])}")
    print(f"OK body_sha256     = {__import__('hashlib').sha256(out['body'].encode('utf-8')).hexdigest()[:16]}")
    print(f"OK html_url        = {out['html_url']}")
    print(f"OK target_commit   = {out.get('target_commitish')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
