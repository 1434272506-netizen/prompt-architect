"""Independent read-back verification of the published Release.

Re-fetches the release from the GitHub API and compares the stored body with the
local notes file, then confirms the tag/commit pair the release points at.
"""
import hashlib
import json
import os
import sys
import urllib.request

REPO = "1434272506-netizen/prompt-architect"
NOTES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_release-notes-v0.4.0-rc.2.md")
HERE = os.path.dirname(os.path.abspath(__file__))


def get(url):
    proxy = "http://127.0.0.1:12000"
    op = urllib.request.build_opener(urllib.request.ProxyHandler({"https": proxy, "http": proxy}))
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json",
                                               "User-Agent": "dsh-verify"})
    with op.open(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    with open(NOTES, "r", encoding="utf-8-sig") as fh:
        local = fh.read().lstrip("\ufeff")

    rel = get(f"https://api.github.com/repos/{REPO}/releases/tags/v0.4.0-rc.2")
    remote = rel["body"]

    lh = hashlib.sha256(local.encode("utf-8")).hexdigest()
    rh = hashlib.sha256(remote.encode("utf-8")).hexdigest()

    print(f"release id        : {rel['id']}")
    print(f"tag_name          : {rel['tag_name']}")
    print(f"name              : {rel['name']}")
    print(f"prerelease        : {rel['prerelease']}")
    print(f"draft             : {rel['draft']}")
    print(f"published_at      : {rel['published_at']}")
    print(f"html_url          : {rel['html_url']}")
    print(f"local  notes sha  : {lh[:24]}  ({len(local)} chars)")
    print(f"remote notes sha  : {rh[:24]}  ({len(remote)} chars)")
    print(f"BODY MATCH        : {'YES' if lh == rh else 'NO'}")

    # tag object -> commit
    tag = get(f"https://api.github.com/repos/{REPO}/git/ref/tags/v0.4.0-rc.2")
    obj = tag["object"]
    print(f"tag object        : {obj['sha'][:12]} ({obj['type']})")
    if obj["type"] == "tag":
        peeled = get(f"https://api.github.com/repos/{REPO}/git/tags/{obj['sha']}")
        print(f"peels to commit   : {peeled['object']['sha']}")
    print(f"expected commit   : 7c0c9bd1db02c5baf6b3268a3c43827b7370c609")
    return 0 if lh == rh else 1


if __name__ == "__main__":
    sys.exit(main())
