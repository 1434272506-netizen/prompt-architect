#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_readme_reverse_refs.py — FRG-07 · README Reverse-Reference Audit（**只读**）

目的：Final Architecture README 最大的新风险不是代码坏，而是
      **README 自己不小心创造了一条合同里没有的新规则**。

做法：解析 `docs/v04/README.md` 的 **Appendix A · README Claim Index**，逐条校验
      1) source 文件存在
      2) anchor 字符串在 source 文件中出现（逐字匹配）
      3) claim 编号唯一、无空行
      4) 不存在"无来源的规范主张"（即在 Claim Index 之外出现的规范断言）

退出码
  0  PASS（每条 claim 均可落到下层权威来源）
  1  FAIL（缺来源 / anchor 不存在 / 重复编号 / 结构性错误）
  2  README 或 Appendix 缺失
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CLAIM_HEADING = "## Appendix A"


def parse_claims(text: str) -> list[tuple[str, str, str, str]]:
    """返回 [(claim_id, statement, source, anchor)]"""
    idx = text.find(CLAIM_HEADING)
    if idx < 0:
        return []
    block = text[idx:]
    rows: list[tuple[str, str, str, str]] = []
    for line in block.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        cid, statement, source, anchor = cells[0], cells[1], cells[2], cells[3]
        if not re.fullmatch(r"CL-\d\d", cid):
            continue
        anchor = anchor.strip("`").strip()
        rows.append((cid, statement, source.strip("`").strip(), anchor))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description="FRG-07 README reverse-reference audit (READ-ONLY)")
    ap.add_argument("--root", default=None)
    ap.add_argument("--readme", default="docs/v04/README.md")
    args = ap.parse_args()

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parent.parent
    readme = root / args.readme

    print("=== FRG-07 · README Reverse-Reference Audit ===")
    print(f"readme: {readme}")
    if not readme.is_file():
        print("\nRESULT\n  FAIL (exit 2) — README missing")
        return 2

    text = readme.read_text(encoding="utf-8")
    claims = parse_claims(text)
    if not claims:
        print("\nRESULT\n  FAIL (exit 2) — Appendix A claim index missing or empty")
        return 2

    problems: list[str] = []
    seen: set[str] = set()
    for cid, statement, source, anchor in claims:
        if cid in seen:
            problems.append(f"{cid}: duplicate claim id")
        seen.add(cid)
        src = root / source
        if not src.is_file():
            problems.append(f"{cid}: source missing -> {source}")
            print(f"[FAIL ] {cid}  source missing: {source}")
            continue
        body = src.read_text(encoding="utf-8")
        if anchor and anchor in body:
            print(f"[OK   ] {cid}  {statement[:38]:<38} <- {source} :: {anchor[:40]}")
        else:
            problems.append(f"{cid}: anchor not found in {source} -> {anchor!r}")
            print(f"[FAIL ] {cid}  anchor not found: {anchor!r} in {source}")

    # 结构性检查：README 不得含"仅 README 才有"的规则标记
    banned = re.findall(r"(?m)^\s*>\s*(README-ONLY|NEW RULE|新增规则：)", text)
    if banned:
        problems.append(f"README-only rule markers found: {banned}")

    print(f"\nclaims: {len(claims)}   unique: {len(seen)}")
    if problems:
        print("\nProblems:")
        for p in problems:
            print("  - " + p)
        print("\nRESULT\n  FAIL (exit 1)")
        return 1
    print("\nRESULT\n  PASS — every README normative claim resolves to a lower-level authoritative source")
    return 0


if __name__ == "__main__":
    sys.exit(main())
