#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_v04_baseline.py — V0.4 Release Baseline INITIALIZER / REBASELINE tool

用途
  BL-01..BL-06：分类 → 清点 → 哈希规格 → 候选哈希 → 批准来源 → 初始化 V0.4 baseline。
  本工具是**唯一**可写 V0.4 baseline 的入口，且必须显式给出模式参数。

模式
  --enumerate        只读：列出候选 artifact 与哈希，**不写文件、不声称 MATCH**（Phase A）
  --init             首次写入 baseline（Phase C；标记 INITIAL BASELINE）
  --rebaseline       经批准的重新基线（需 --reason；版本号 +1）

纪律
  * 文件级 SHA-256 = **权威冻结值**（raw bytes，不做任何归一化）
  * section hash = **诊断定位**，不构成第二套冻结真相
  * 绝不把本 baseline 写成"这些文件过去一直如此"（prospective-only）
  * V0.3 的 24 个 hash **不复制**进本 manifest，只引用既有 V0.3 baseline
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import sys
from pathlib import Path

BASELINE_ID_BASE = "v0.4.0-release-baseline"
HASH_ALGO = "sha256-raw-bytes"
JSON_NAME = "v0.4-release-baseline.json"
MD_NAME = "v0.4-release-baseline.md"

# ---------------------------------------------------------------- 分类（BL-01）

NORMATIVE = [
    "docs/v04/gap-ledger-proposal.md",
    "docs/v04/gap-ledger-interface.md",
    "docs/v04/pending-resolution-transition-contract.md",
    "docs/v04/priority-layer-contract.md",
    "docs/v04/scheduler-fairness-contract.md",
    "docs/v04/notification-policy-contract.md",
]

GOVERNANCE = [
    "docs/v04/README.md",                          # D01 Final Architecture README
    "docs/v04/historical-discovery-governance.md",
    "docs/v04/v04-defect-ledger.md",
    "docs/freeze-v0.3.md",
]

EVIDENCE = [
    "docs/v04/failure-inventory.md",
    "docs/v04/interface-v3-migration-manifest.md",
    "docs/v04/interface-v3-migration-test.md",
    "docs/v04/pending-resolution-second-challenge-discovery.md",
    "docs/v04/priority-model-discovery.md",
    "docs/v04/priority-hint-language-discovery.md",
    "docs/v04/scheduler-fairness-starvation-discovery.md",
    "docs/v04/notification-policy-discovery.md",
    "docs/v04/e2e-adaptive-replay.md",
    "docs/v04/full-adaptive-e2e-replay.md",
    "docs/v04/release-evidence-closure.md",
]

# 明确排除（BL-02 scope 声明）：这些文件**不属** V0.4 release baseline
OUT_OF_SCOPE = [
    "docs/v04/v05-architecture-candidates.md",     # V0.5 前瞻材料
    "docs/v04/gap-ledger-coverage.md",             # V0.2 期覆盖审计
    "docs/v04/gap-ledger-x-v11-compat.md",         # v1.1 兼容审计
    "docs/v04/gap-ledger-replay.md",               # Phase 1 replay 记录
    "docs/v04/feedback-semantics-discovery.md",    # Phase 2 中间设计记录（规范内容已并入 Interface §9/§10）
    "docs/v04/feedback-transition-design.md",
    "docs/v04/feedback-language-map.md",
    "docs/v04/feedback-state-extension-design.md",
    "docs/v04/feedback-responsibility-extension-design.md",
    "docs/v04/" + JSON_NAME,
    "docs/v04/" + MD_NAME,
]

APPROVAL_PROVENANCE = {
    "closure_ledger": "docs/v04/v04-defect-ledger.md",
    "defect_closure": ["D02", "D03", "D04", "D05", "D06", "D07", "D08", "D09", "D10"],
    "adjudications": ["N08", "N09", "N10", "CS-04", "CS-05", "CS-06",
                      "ER-07", "ER-08", "ER-09"],
    "probes": ["NR-01..NR-07", "AR-01..AR-02", "EX-01..EX-03", "DL-01..DL-03",
               "EV-07..EV-09", "HG-10", "EL-02"],
    "freeze_exceptions": "#13..#35 (docs/freeze-v0.3.md §4)",
    "protocol_steps": ["BL-01", "BL-02", "BL-03", "BL-04", "BL-05", "BL-06",
                       "BL-07", "BL-08", "BL-09", "BL-10"],
}

V03_REFERENCE = {
    "baseline_doc": "docs/freeze-v0.3.md",
    "verifier": ".gh-search/freeze_v03.py",
    "protected_files": 24,
    "note": "V0.3 受保护集**不复制**进本 manifest；组合执行 = V0.3 校验 + V0.4 校验。",
}

PROSPECTIVE_ONLY_EN = (
    "This is the first traceable V0.4 release baseline established after architecture "
    "and defect closure. It is effective prospectively from the recorded baseline "
    "timestamp and does not prove that these files were historically identical before "
    "that point."
)
PROSPECTIVE_ONLY_ZH = (
    "本基线是在 V0.4 架构与缺陷闭合完成后建立的首个可追溯发布基线，自所记录的生效时刻起具有冻结验证效力；"
    "它不构成这些文件在此前历史时点始终保持相同内容的证明。"
)


# ---------------------------------------------------------------- 哈希（BL-03）

def file_hash(root: Path, rel: str) -> str:
    return hashlib.sha256((root / rel).read_bytes()).hexdigest()


def section_hashes(root: Path, rel: str) -> dict:
    """按 `## ` 二级标题切节做**诊断**哈希；不参与通过判定。"""
    text = (root / rel).read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    heads: list[tuple[str, int]] = []
    for i, ln in enumerate(lines):
        if ln.startswith("## "):
            heads.append((ln.strip(), i))
    out: dict[str, str] = {}
    for idx, (title, start) in enumerate(heads):
        end = heads[idx + 1][1] if idx + 1 < len(heads) else len(lines)
        blob = "".join(lines[start:end]).encode("utf-8")
        key = title[3:].strip()[:48]
        out[key] = hashlib.sha256(blob).hexdigest()
    return out


def classify(rel: str) -> str:
    if rel in NORMATIVE:
        return "normative"
    if rel in GOVERNANCE:
        return "governance"
    if rel in EVIDENCE:
        return "evidence"
    return "unknown"


def build_entries(root: Path) -> list[dict]:
    entries = []
    for rel in NORMATIVE + GOVERNANCE + EVIDENCE:
        p = root / rel
        entries.append({
            "path": rel,
            "class": classify(rel),
            "exists": p.is_file(),
            "sha256": file_hash(root, rel) if p.is_file() else None,
            "bytes": p.stat().st_size if p.is_file() else None,
            "section_hashes": section_hashes(root, rel) if p.is_file() else {},
        })
    return entries


def inventory_checks(root: Path, entries: list[dict]) -> list[str]:
    problems = []
    seen = set()
    for e in entries:
        if e["path"] in seen:
            problems.append(f"DUPLICATE: {e['path']}")
        seen.add(e["path"])
        if not e["exists"]:
            problems.append(f"MISSING: {e['path']}")
        if e["class"] == "unknown":
            problems.append(f"UNCLASSIFIED: {e['path']}")
    for rel in OUT_OF_SCOPE:
        if rel in seen:
            problems.append(f"SCOPE-CONFLICT (in both baseline and out-of-scope): {rel}")
    return problems


# ---------------------------------------------------------------- 输出

def cmd_enumerate(root: Path) -> int:
    entries = build_entries(root)
    problems = inventory_checks(root, entries)
    print("=== BL-04 Candidate Hash Run (READ-ONLY; no MATCH claim) ===")
    print(f"root: {root}")
    print(f"hash: {HASH_ALGO}\n")
    for e in entries:
        state = "OK" if e["exists"] else "MISSING"
        print(f"[{e['class']:>10}] {e['path']}")
        print(f"             {state}  bytes={e['bytes']}  sha256={e['sha256']}")
        if e["section_hashes"]:
            print(f"             sections={len(e['section_hashes'])} (diagnostic)")
    print(f"\ncandidates: {len(entries)}  "
          f"(normative={len(NORMATIVE)} governance={len(GOVERNANCE)} evidence={len(EVIDENCE)})")
    if problems:
        print("\nINVENTORY PROBLEMS:")
        for p in problems:
            print("  - " + p)
        return 1
    print("\ninventory: OK (paths unique, all present, classes assigned, scope disjoint)")
    print("NOTE: this is a candidate enumeration, NOT a verification result.")
    return 0


def write_manifest(root: Path, entries: list[dict], version: int, reason: str | None,
                   initial: bool, effective_at: str | None) -> int:
    problems = inventory_checks(root, entries)
    if problems:
        print("refuse to initialize: inventory problems")
        for p in problems:
            print("  - " + p)
        return 2

    out_json = root / "docs" / "v04" / JSON_NAME
    out_md = root / "docs" / "v04" / MD_NAME
    previous = None
    if out_json.is_file():
        previous = json.loads(out_json.read_text(encoding="utf-8"))

    eff = effective_at or _dt.datetime.now().astimezone().isoformat(timespec="seconds")
    manifest = {
        "baseline_id": f"{BASELINE_ID_BASE}-{version}",
        "baseline_kind": "INITIAL BASELINE" if initial else "REBASELINE",
        "effective_at": eff,
        "established_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "hash_algorithm": HASH_ALGO,
        "raw_bytes_no_normalization": True,
        "file_hash_role": "authoritative",
        "section_hash_role": "diagnostic",
        "prospective_only": True,
        "prospective_only_statement_en": PROSPECTIVE_ONLY_EN,
        "prospective_only_statement_zh": PROSPECTIVE_ONLY_ZH,
        "approval_provenance": APPROVAL_PROVENANCE,
        "v03_baseline_reference": V03_REFERENCE,
        "class_counts": {
            "normative": len(NORMATIVE),
            "governance": len(GOVERNANCE),
            "evidence": len(EVIDENCE),
        },
        "artifact_count": len(entries),
        "artifacts": entries,
        "out_of_scope": OUT_OF_SCOPE,
        "rebaseline_reason": reason,
        "supersedes": (previous or {}).get("baseline_id"),
    }
    out_json.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = []
    lines.append(f"# V0.4 Release Baseline — {manifest['baseline_id']}\n")
    lines.append(f"> {PROSPECTIVE_ONLY_EN}\n>\n> {PROSPECTIVE_ONLY_ZH}\n")
    lines.append("## Baseline 身份\n")
    lines.append("| 项 | 值 |")
    lines.append("|---|---|")
    lines.append(f"| baseline_id | `{manifest['baseline_id']}` |")
    lines.append(f"| kind | **{manifest['baseline_kind']}** |")
    lines.append(f"| effective_at | `{manifest['effective_at']}` |")
    lines.append(f"| hash_algorithm | `{HASH_ALGO}`（raw bytes，**不做任何归一化**） |")
    lines.append("| file hash | **权威冻结值** |")
    lines.append("| section hash | **诊断定位**（不得用于「以节代文件」通过判定） |")
    lines.append(f"| artifact_count | **{manifest['artifact_count']}**（normative {manifest['class_counts']['normative']} / governance {manifest['class_counts']['governance']} / evidence {manifest['class_counts']['evidence']}） |")
    lines.append(f"| supersedes | `{manifest['supersedes']}` |")
    lines.append("")
    lines.append("## A · Normative Baseline\n")
    lines.append("| path | sha256 | sections |")
    lines.append("|---|---|---|")
    for e in entries:
        if e["class"] == "normative":
            lines.append(f"| `{e['path']}` | `{e['sha256']}` | {len(e['section_hashes'])} |")
    lines.append("\n## B · Governance Baseline\n")
    lines.append("| path | sha256 | sections |")
    lines.append("|---|---|---|")
    for e in entries:
        if e["class"] == "governance":
            lines.append(f"| `{e['path']}` | `{e['sha256']}` | {len(e['section_hashes'])} |")
    lines.append("\n## C · Evidence Baseline\n")
    lines.append("| path | sha256 | sections |")
    lines.append("|---|---|---|")
    for e in entries:
        if e["class"] == "evidence":
            lines.append(f"| `{e['path']}` | `{e['sha256']}` | {len(e['section_hashes'])} |")
    lines.append("\n## 批准来源（approval provenance）\n")
    lines.append("```json")
    lines.append(json.dumps(APPROVAL_PROVENANCE, ensure_ascii=False, indent=2))
    lines.append("```")
    lines.append("\n## V0.3 关系\n")
    lines.append("```json")
    lines.append(json.dumps(V03_REFERENCE, ensure_ascii=False, indent=2))
    lines.append("```")
    lines.append("\n## 明确排除（out of scope）\n")
    for rel in OUT_OF_SCOPE:
        lines.append(f"- `{rel}`")
    lines.append("")
    lines.append("## 校验方式\n")
    lines.append("```")
    lines.append("python .gh-search/verify_v04_release_baseline.py          # 只读；V0.3 + V0.4 组合")
    lines.append("python .gh-search/verify_v04_release_baseline.py --no-v03 # 只读；仅 V0.4")
    lines.append("```")
    lines.append("**任何 DIFF / MISSING / UNREGISTERED / governance violation 必须非零退出。**\n")
    lines.append(f"_machine source of truth: `docs/v04/{JSON_NAME}`_\n")
    out_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"wrote {out_json.relative_to(root)}  ({len(entries)} artifacts, {manifest['baseline_kind']})")
    print(f"wrote {out_md.relative_to(root)}")
    print(f"effective_at = {eff}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="V0.4 Release Baseline initializer (writes manifest)")
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--enumerate", action="store_true", help="read-only candidate enumeration")
    mode.add_argument("--init", action="store_true", help="initialize baseline (first time)")
    mode.add_argument("--rebaseline", action="store_true", help="approved rebaseline (needs --reason)")
    ap.add_argument("--reason", default=None, help="rebaseline reason (required with --rebaseline)")
    ap.add_argument("--effective-at", default=None, help="override effective_at (ISO8601)")
    ap.add_argument("--root", default=None, help="repo root (default: parent of .gh-search)")
    args = ap.parse_args()

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parent.parent

    if args.enumerate:
        return cmd_enumerate(root)

    entries = build_entries(root)
    out_json = root / "docs" / "v04" / JSON_NAME

    if args.init:
        if out_json.is_file():
            print(f"refuse: {out_json.relative_to(root)} already exists — INITIAL BASELINE is one-shot.")
            print("use --rebaseline --reason \"...\" for an approved change set.")
            return 2
        return write_manifest(root, entries, version=1, reason=None, initial=True,
                              effective_at=args.effective_at)

    # rebaseline
    if not args.reason:
        print("refuse: --rebaseline requires --reason (governance: reason + approved change set)")
        return 2
    if not out_json.is_file():
        print("refuse: no existing baseline to rebaseline; use --init first.")
        return 2
    prev = json.loads(out_json.read_text(encoding="utf-8"))
    version = int(str(prev.get("baseline_id", "")).rsplit("-", 1)[-1]) + 1 \
        if str(prev.get("baseline_id", "")).rsplit("-", 1)[-1].isdigit() else 2
    return write_manifest(root, entries, version=version, reason=args.reason, initial=False,
                          effective_at=args.effective_at)


if __name__ == "__main__":
    sys.exit(main())
