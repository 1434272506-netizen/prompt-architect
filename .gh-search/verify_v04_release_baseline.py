#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_v04_release_baseline.py — V0.4 Release Baseline VERIFIER（**永远只读**）

职责（BL-07）
  1. 调用既有 V0.3 verification（.gh-search/freeze_v03.py）
  2. 读取 V0.4 JSON manifest（machine source of truth）
  3. 计算当前文件 SHA-256（raw bytes）并与 manifest 对照
  4. 输出 drift report（含 section 级**诊断**）
  5. **只读**：不写任何文件、不支持任何写入参数

退出码
  0  PASS   （无 DIFF / MISSING / UNREGISTERED，且 V0.3 通过）
  1  DRIFT  （任一 DIFF / MISSING / UNREGISTERED / 治理违规）
  2  MANIFEST 不可读或缺失
  3  V0.3 校验无法执行或未通过

纪律
  * 文件级 hash = 权威；section hash = 诊断
  * **绝不允许** "file DIFF + section MATCH ⇒ 整体通过"
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

JSON_NAME = "v0.4-release-baseline.json"


def file_hash(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def section_hashes(p: Path) -> dict:
    text = p.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    heads = [(ln.strip(), i) for i, ln in enumerate(lines) if ln.startswith("## ")]
    out = {}
    for idx, (title, start) in enumerate(heads):
        end = heads[idx + 1][1] if idx + 1 < len(heads) else len(lines)
        out[title[3:].strip()[:48]] = hashlib.sha256("".join(lines[start:end]).encode("utf-8")).hexdigest()
    return out


def run_v03(root: Path, script: Path) -> tuple[int, str]:
    """返回 (status, 文本)；status: 0 通过 / 1 漂移 / 2 无法执行"""
    if not script.is_file():
        return 2, f"V0.3 verifier not found: {script}"
    try:
        proc = subprocess.run([sys.executable, str(script)], cwd=str(root),
                              capture_output=True, text=True, timeout=300)
    except Exception as exc:  # noqa: BLE001
        return 2, f"V0.3 verifier failed to run: {exc!r}"
    out = (proc.stdout or "") + (proc.stderr or "")
    m = re.search(r"summary:\s*MATCH=(\d+)\s+DIFF=(\d+)\s+UNREGISTERED=(\d+)", out)
    if not m:
        if "MATCH=" in out:
            return 2, out
        return 2, "V0.3 summary not found:\n" + out[-800:]
    match, diff, unreg = (int(x) for x in m.groups())
    text = f"MATCH {match}  DIFF {diff}  UNREGISTERED {unreg}  (exit={proc.returncode})"
    ok = (diff == 0 and unreg == 0 and proc.returncode == 0)
    return (0 if ok else 1), text


def main() -> int:
    ap = argparse.ArgumentParser(description="V0.4 release baseline verifier (READ-ONLY)")
    ap.add_argument("--root", default=None, help="repo root (default: parent of .gh-search)")
    ap.add_argument("--no-v03", action="store_true", help="skip V0.3 aggregation (diagnostic use only)")
    ap.add_argument("--manifest", default=None, help="override manifest path")
    ap.add_argument("--skip-unregistered", action="store_true",
                    help="ignore docs/v04 UNREGISTERED scan (NOT for release use)")
    args = ap.parse_args()

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parent.parent
    manifest_path = Path(args.manifest).resolve() if args.manifest else root / "docs" / "v04" / JSON_NAME

    print("=== V0.4 Release Baseline Verification (READ-ONLY) ===")
    print(f"root     : {root}")
    print(f"manifest : {manifest_path}")

    if not manifest_path.is_file():
        print("\nRESULT\n  FAIL (exit 2) — manifest missing; baseline not established")
        return 2
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        print(f"\nRESULT\n  FAIL (exit 2) — manifest unreadable: {exc!r}")
        return 2

    print(f"baseline : {manifest.get('baseline_id')}  ({manifest.get('baseline_kind')})")
    print(f"effective: {manifest.get('effective_at')}")
    print(f"hash algo: {manifest.get('hash_algorithm')}")
    print(f"prospective-only: {manifest.get('prospective_only')}\n")

    violations: list[str] = []
    match = diff = missing = 0
    sec_match = sec_diff = 0

    for entry in manifest.get("artifacts", []):
        rel = entry["path"]
        p = root / rel
        if not p.is_file():
            missing += 1
            violations.append(f"MISSING  {rel}")
            print(f"[MISSING] {rel}")
            continue
        cur = file_hash(p)
        if cur == entry.get("sha256"):
            match += 1
            print(f"[MATCH  ] ({entry['class']}) {rel}")
        else:
            diff += 1
            violations.append(f"DIFF     {rel}")
            print(f"[DIFF   ] ({entry['class']}) {rel}")
            print(f"          manifest {entry.get('sha256')}")
            print(f"          current  {cur}")
            # section 级诊断（绝不参与通过判定）
            old_sec = entry.get("section_hashes") or {}
            new_sec = section_hashes(p)
            if old_sec:
                for key in old_sec:
                    same = new_sec.get(key) == old_sec[key]
                    sec_match += 1 if same else 0
                    sec_diff += 0 if same else 1
                    print(f"          § {key:<50} {'MATCH' if same else 'DIFF'}")
                print("          NOTE: file-level DIFF is authoritative — section MATCH never overrides it")

    # UNREGISTERED：docs/v04 下未登记且不在 out_of_scope 的文件
    unregistered = 0
    if not args.skip_unregistered:
        registered = {e["path"] for e in manifest.get("artifacts", [])}
        scope = set(manifest.get("out_of_scope", []))
        for p in sorted((root / "docs" / "v04").glob("*.md")):
            rel = p.relative_to(root).as_posix()
            if rel not in registered and rel not in scope:
                unregistered += 1
                violations.append(f"UNREGISTERED {rel}")
                print(f"[UNREG] {rel}")

    if not args.no_v03:
        print("\n--- V0.3 protected baseline ---")
        v03_root = Path(__file__).resolve().parent
        v03_script = v03_root / "freeze_v03.py"
        status, text = run_v03(root, v03_script)
        print(f"V0.3  {text}")
        if status != 0:
            violations.append("V0.3 baseline check FAILED")
    else:
        print("\n--- V0.3 protected baseline: SKIPPED (--no-v03) ---")

    print("\n--- Summary ---")
    print(f"V0.4  MATCH {match}  DIFF {diff}  MISSING {missing}  UNREGISTERED {unregistered}")
    if sec_match or sec_diff:
        print(f"SECTIONS (diagnostic)  MATCH {sec_match}  DIFF {sec_diff}")
    else:
        print("SECTIONS (diagnostic)  not needed — no file-level DIFF to localize")

    if violations:
        print("\nViolations:")
        for v in violations:
            print("  - " + v)
        print("\nRESULT\n  FAIL (exit 1) — drift / governance violation")
        return 1
    print("\nRESULT\n  PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
