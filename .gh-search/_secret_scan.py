"""Pre-publish secret scan over full git history.

Scans every blob in the object database (all history, not just HEAD) for
credential-shaped strings. Prints only path/sha/rule/line/length -- never the
matched secret value itself.
"""
import re
import subprocess
import sys

PATTERNS = [
    ("private-key-block", re.compile(rb"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("github-pat", re.compile(rb"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b")),
    ("github-fine-grained-pat", re.compile(rb"\bgithub_pat_[A-Za-z0-9_]{20,}\b")),
    ("aws-access-key-id", re.compile(rb"\b(AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("aws-secret-assign", re.compile(rb"(?i)aws_secret_access_key\s*[:=]\s*\S{20,}")),
    ("openai-key", re.compile(rb"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("anthropic-key", re.compile(rb"\bsk-ant-[A-Za-z0-9_-]{20,}\b")),
    ("slack-token", re.compile(rb"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("google-api-key", re.compile(rb"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("jwt", re.compile(rb"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
    ("ssh-private-key-body", re.compile(rb"(?i)ssh-rsa\s+AAAA[A-Za-z0-9+/=]{100,}")),
    ("generic-password-assign", re.compile(rb"(?i)(password|passwd|secret|api[_-]?key|access[_-]?token)\s*[:=]\s*[\"']?[A-Za-z0-9!@#$%^&*_+=/-]{12,}")),
    ("dotenv-assign", re.compile(rb"(?m)^[A-Z0-9_]{3,}(KEY|TOKEN|SECRET|PASSWORD|PASSWD|CREDENTIAL)[A-Z0-9_]*\s*=\s*\S+")),
    ("bearer-token", re.compile(rb"(?i)bearer\s+[A-Za-z0-9._-]{20,}")),
    ("connection-string-cred", re.compile(rb"(?i)(mongodb|postgres|postgresql|mysql|redis|amqp)://[^/\s:@]+:[^/\s:@]{3,}@")),
    ("private-ip-or-host", re.compile(rb"\b(?:100\.(?:6[4-9]|[7-9]\d|1[0-2]\d)\.\d{1,3}\.\d{1,3}|172\.3[1-9]\.\d{1,3}\.\d{1,3})\b")),
    ("windows-user-path", re.compile(rb"C:\\\\Users\\\\[A-Za-z0-9._-]+")),
]

PREALLOW = re.compile(
    r"(?i)(example|placeholder|redacted|dummy|sample|fake|your[_-]?(key|token|password)|"
    r"<[a-z_-]+>|\$\{|\{\{|xxx+|\.\.\.|changeme|todo)"
)


def revision_blobs():
    out = subprocess.run(
        ["git", "rev-list", "--objects", "--all"],
        capture_output=True, check=True,
    ).stdout.decode("utf-8", "replace")
    seen = {}
    for line in out.splitlines():
        parts = line.split(" ", 1)
        if len(parts) != 2:
            continue
        sha, path = parts
        seen.setdefault(sha, path)
    return seen


def blob_paths():
    blobs = revision_blobs()
    out = subprocess.run(
        ["git", "cat-file", "--batch-check=%(objectname) %(objecttype)"],
        input="\n".join(blobs).encode(), capture_output=True, check=True,
    ).stdout.decode("utf-8", "replace")
    keep = {}
    for line in out.splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[1] == "blob":
            keep[parts[0]] = blobs[parts[0]]
    return keep


def main():
    blobs = blob_paths()
    print(f"blobs scanned: {len(blobs)}")
    findings = []
    for sha, path in blobs.items():
        raw = subprocess.run(["git", "cat-file", "blob", sha], capture_output=True, check=True).stdout
        for lineno, line in enumerate(raw.splitlines(), 1):
            for rule, rx in PATTERNS:
                for m in rx.finditer(line):
                    token = m.group(0)
                    if PREALLOW.search(token):
                        findings.append((path, sha[:10], lineno, rule, len(token), "ALLOWLISTED"))
                        continue
                    findings.append((path, sha[:10], lineno, rule, len(token), "REVIEW"))
    if not findings:
        print("RESULT: CLEAN -- no credential-shaped strings found in any blob")
        return 0
    review = [f for f in findings if f[5] == "REVIEW"]
    allow = [f for f in findings if f[5] == "ALLOWLISTED"]
    print(f"RESULT: {len(review)} REVIEW / {len(allow)} allowlisted")
    print("\n== REVIEW (human must look) ==")
    for path, sha, lineno, rule, ln, _ in review:
        print(f"{path}:{lineno}  [{rule}]  blob={sha}  match_len={ln}")
    print("\n== allowlisted (low signal) ==")
    seen = set()
    for path, sha, lineno, rule, ln, _ in allow:
        key = (path, rule)
        if key in seen:
            continue
        seen.add(key)
        print(f"{path}:{lineno}  [{rule}]  match_len={ln}")
    return 1 if review else 0


if __name__ == "__main__":
    sys.exit(main())
