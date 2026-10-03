#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
preflight_ship02.py — SHIP-02 Protocol Preflight（**只读**）

目的：**防止测试协议在运行前被意外编辑**，并确认被测物锚未被移动。
任何一项不一致 ⇒ ABORT（非零退出），**不得开始 A/B/C**。

检查项
  ① sha256(docs/release-ship-02/protocol.md)        == 当前 pin（protocol-pin.json）
  ② sha256(docs/release-ship-02/record-template.md) == 当前 pin
  ③ git rev-parse <runtime_base_tag>                == runtime_base_commit

退出码
  0  PASS（一致，可以开始 A/B/C）
  1  ABORT（不一致）
  2  环境/文件缺失
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

PIN_JSON = "docs/release-ship-02/protocol-pin.json"


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    pin_path = root / PIN_JSON
    if not pin_path.is_file():
        print(f"ABORT (exit 2): pin record missing -> {PIN_JSON}")
        return 2

    pin = json.loads(pin_path.read_text(encoding="utf-8"))
    cur = pin["current_pin"]

    print("=== SHIP-02 Protocol Preflight (READ-ONLY) ===")
    print(f"pin_id     : {cur.get('pin_id')}")
    print(f"pinned_at  : {cur.get('pinned_at')}\n")

    problems: list[str] = []

    for label, rel, expect in (
        ("protocol.md", cur["protocol_path"], cur["protocol_sha256"]),
        ("record-template.md", cur["template_path"], cur["template_sha256"]),
    ):
        f = root / rel
        if not f.is_file():
            problems.append(f"{label} missing -> {rel}")
            print(f"[MISSING] {rel}")
            continue
        got = sha256(f)
        ok = got == expect
        print(f"[{'OK   ' if ok else 'DIFF '}] {rel}")
        print(f"        pinned  {expect}")
        print(f"        current {got}")
        if not ok:
            problems.append(f"{label} sha256 mismatch ({rel})")

    # ③ 被测物锚
    tag, commit = cur["runtime_base_tag"], cur["runtime_base_commit"]
    try:
        out = subprocess.run(["git", "rev-list", "-n", "1", tag], cwd=str(root),
                             capture_output=True, text=True, timeout=60)
        got_commit = (out.stdout or "").strip()
    except Exception as exc:  # noqa: BLE001
        got_commit = ""
        print(f"[WARN ] git unavailable: {exc!r}")
    full_expect = cur.get("runtime_base_commit_full", commit)
    ok = got_commit.startswith(commit) or got_commit == full_expect
    print(f"[{'OK   ' if ok else 'DIFF '}] {tag} -> {got_commit or '(not found)'}")
    print(f"        expected {full_expect}")
    if not ok:
        problems.append(f"runtime base tag moved or missing ({tag})")

    print("\n--- Result ---")
    if problems:
        print("ABORT — do NOT start A/B/C:")
        for p in problems:
            print("  - " + p)
        return 1
    print("PASS — protocol pinned and runtime anchor intact; A/B/C may start")
    return 0


if __name__ == "__main__":
    sys.exit(main())
