#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""V0.3 冻结基线复算器（安全版）

设计原则（2026-10-01 事故后修订）：
  1. **默认只读、只比对、只报告** —— 绝不修改 docs/freeze-v0.3.md
  2. 发现漂移 → 打印 DIFF 并以 **非零退出码** 结束（可被 CI 直接拦住）
  3. 只有显式传入 `--write` 才重新登记基线；且写入前要求每条漂移都有对应说明

事故背景：旧版 freeze_v03.py 每次运行都会把当前文件状态写成"新基线"，
导致"任何人跑一次复算命令就能把任意改动洗成基线"，冻结语义事实上失效。
"""
import hashlib, os, re, sys, datetime

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

FROZEN = [
    'SKILL.md',
    'core/uncertainty-classifier.md',
    'strategies/ask.md',
    'strategies/show.md',
    'strategies/inspect.md',
    'strategies/teach.md',
    'strategies/discover.md',
    'docs/failure-map.md',
    'tests/acceptance.md',
    'tests/cases.md',
    'tests/unknown-known.md',
    'tests/evidence-unknown.md',
    'tests/blind-spot.md',
    'tests/high-risk-c.md',
    'tests/adversarial-2.1.md',
    'tests/adversarial-question-selection.md',
    'tests/adversarial-merge-questions.md',
    'tests/adversarial-interview-core.md',
    'examples/case-01-vague-video.md',
    'examples/case-02-enough-info.md',
    'examples/case-03-no-idea.md',
    'examples/case-04-stop-rules.md',
    'examples/case-05-vague-website.md',
    'README.md',
]

BASELINE_DOC = 'docs/freeze-v0.3.md'


def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def read_doc_hashes():
    """从基线文档 §2 表格解析已登记的哈希（只读）。"""
    if not os.path.exists(BASELINE_DOC):
        return {}
    txt = open(BASELINE_DOC, encoding='utf-8').read()
    out = {}
    for m in re.finditer(r'\|\s*`([^`]+)`\s*\|\s*(\d+)\s*\|\s*`([0-9a-f]{64})`\s*\|', txt):
        out[m.group(1)] = m.group(3)
    return out


def section_hashes():
    """按冻结章节口径取块计算，并与文档 §3 登记的哈希比对。"""
    sec = [('§2.1', r'^### 2\.1 ', True), ('§3', r'^## 3\. ', False),
           ('§6.3', r'^### 6\.3 ', True), ('§6.4', r'^### 6\.4 ', True),
           ('§6.5', r'^### 6\.5 ', True)]
    sk = open('SKILL.md', encoding='utf-8').read().split('\n')
    res = []
    for name, rx, sub in sec:
        s = next(i for i, l in enumerate(sk) if re.match(rx, l))
        out = [sk[s]]; i = s + 1
        while i < len(sk):
            l = sk[i]
            if l.strip() == '---' or re.match(r'^## ', l) or (sub and re.match(r'^### ', l)):
                break
            out.append(l); i += 1
        while out and out[-1].strip() == '':
            out.pop()
        h = hashlib.sha256('\n'.join(out).encode('utf-8')).hexdigest()
        res.append((name, s + 1, i - 1, h))
    return res


def main():
    write = '--write' in sys.argv
    doc = read_doc_hashes()
    print('== V0.3 冻结基线复算（默认只读） ==')
    print('%-44s %5s %-10s %s' % ('file', 'lines', 'status', 'sha256'))

    drifted, added, same = [], [], 0
    for f in FROZEN:
        if not os.path.exists(f):
            print('%-44s %5s %-10s %s' % (f, '-', 'MISSING', ''))
            drifted.append(f)
            continue
        h = sha(f)
        n = len(open(f, encoding='utf-8').read().split('\n'))
        old = doc.get(f)
        if old is None:
            st = 'UNREGISTERED'
            added.append(f)
        elif old == h:
            st = 'MATCH'
            same += 1
        else:
            st = 'DIFF'
            drifted.append(f)
        print('%-44s %5d %-10s %s' % (f, n, st, h))

    print()
    print('== 冻结章节哈希 ==')
    for name, s, e, h in section_hashes():
        print('%-6s %4d～%-4d %s' % (name, s, e, h))

    print()
    print('summary: MATCH=%d  DIFF=%d  UNREGISTERED=%d' % (same, len(drifted), len(added)))
    if drifted or added:
        print('!! 检测到漂移 —— 冻结基线不再成立。')
        print('   处理顺序：① 登记异常修改（docs/freeze-v0.3.md §4）→ ② 全量回归 → ③ 再跑本脚本 --write 重新冻结')
        if not write:
            print('   （本次未写入；确认无误后显式执行：python .gh-search/freeze_v03.py --write）')
            sys.exit(1)

    if write:
        replace_hashes()


def replace_hashes():
    """只替换 §2 哈希表区域，**绝不重写正文**。写前自动备份。"""
    txt = open(BASELINE_DOC, encoding='utf-8').read()
    rows = []
    total = 0; cnt = 0
    for f in FROZEN:
        if not os.path.exists(f):
            continue
        n = len(open(f, encoding='utf-8').read().split('\n'))
        total += n; cnt += 1
        rows.append('| `%s` | %d | `%s` |' % (f, n, sha(f)))
    new_table = '<!-- HASH-TABLE-START -->\n' + '\n'.join(rows) + \
        '\n\n**合计 %d 个受保护文件，%d 行。**\n<!-- HASH-TABLE-END -->' % (cnt, total)

    m = re.search(r'(<!-- HASH-TABLE-START -->\n)(.*?)(\n<!-- HASH-TABLE-END -->)', txt, re.S)
    if not m:
        print('!! 未找到哈希表哨兵区（<!-- HASH-TABLE-START/END -->），拒绝写入以免破坏文档：%s' % BASELINE_DOC)
        sys.exit(2)
    bak = BASELINE_DOC + '.bak'
    open(bak, 'w', encoding='utf-8').write(txt)
    out = txt[:m.start(2)] + new_table + txt[m.end(2):]
    open(BASELINE_DOC, 'w', encoding='utf-8').write(out)
    print('已只替换 §2 哈希表（正文未动）；备份 -> %s' % bak)


if __name__ == '__main__':
    main()
