#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
probe_baseline_drift.py — BL-08 Governance Negative Probe（**只写临时目录**）

目的：证明 verifier **不是摆设** —— 故意在临时副本里制造 drift，要求：
    1) verifier 报 DIFF 且 **exit != 0**
    2) 恢复后必须重新 **MATCH 且 exit == 0**

本脚本不修改仓库内任何被冻结文件（只读取），所有改动发生在系统临时目录。
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
JSON_NAME = "v0.4-release-baseline.json"
VERIFIER = REPO / ".gh-search" / "verify_v04_release_baseline.py"


def main() -> int:
    manifest_path = REPO / "docs" / "v04" / JSON_NAME
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    victim = manifest["artifacts"][0]["path"]
    for a in manifest["artifacts"]:
        if a["class"] == "normative":
            victim = a["path"]
            break

    tmp = Path(tempfile.mkdtemp(prefix="v04probe_"))
    try:
        for a in manifest["artifacts"]:
            src = REPO / a["path"]
            dst = tmp / a["path"]
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        tmp_manifest = tmp / "docs" / "v04" / JSON_NAME
        tmp_manifest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(manifest_path, tmp_manifest)

        def verify() -> tuple[int, str]:
            p = subprocess.run([sys.executable, str(VERIFIER), "--root", str(tmp), "--no-v03"],
                               capture_output=True, text=True)
            return p.returncode, (p.stdout or "") + (p.stderr or "")

        print("=== BL-08 Governance Negative Probe ===")
        print(f"temp root : {tmp}")
        print(f"victim    : {victim}\n")

        # baseline sanity (temp copy must PASS before the probe)
        rc0, out0 = verify()
        ok0 = rc0 == 0 and "PASS" in out0
        print(f"[0] pristine temp copy      : exit={rc0}  {'PASS' if ok0 else 'UNEXPECTED'}")

        # step 1: inject drift
        target = tmp / victim
        target.write_bytes(target.read_bytes() + b"drift")
        rc1, out1 = verify()
        diff_line = [l for l in out1.splitlines() if l.startswith("[DIFF")]
        ok1 = rc1 != 0 and bool(diff_line)
        print(f"[1] drift injected          : exit={rc1}  DIFF lines={len(diff_line)}  "
              f"{'OK (non-zero)' if ok1 else 'FAIL'}")

        # step 2: restore
        shutil.copy2(REPO / victim, target)
        rc2, out2 = verify()
        ok2 = rc2 == 0 and "PASS" in out2
        print(f"[2] restored                : exit={rc2}  {'OK (PASS)' if ok2 else 'FAIL'}")

        print("\n--- Result ---")
        if ok0 and ok1 and ok2:
            print("BL-08 = PASS  (drift detected with non-zero exit; clean state passes)")
            return 0
        print("BL-08 = FAIL")
        return 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
