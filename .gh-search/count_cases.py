import re, os, io

os.chdir(r'C:\Users\Administrator\Desktop\prompt-architect')
OUT = io.StringIO()
def P(*a): OUT.write(' '.join(str(x) for x in a) + '\n')

# 1) 从破坏测试文件抽全部案例 ID + 用例级判定
files = {
    'F1': 'docs/v04/break-tests/show-silence.md',
    'F4': 'docs/v04/break-tests/multi-round-compaction.md',
    'C':  'docs/v04/break-tests/contradictory-feedback.md',
    'G':  'docs/v04/break-tests/goal-shift.md',
    'S':  'docs/v04/break-tests/skip-analysis-and-stopping.md',
    'F2': 'docs/v04/break-tests/low-quality-answer.md',
    'F3': 'docs/v04/break-tests/teach-rejection.md',
}
all_ids = {}
for grp, path in files.items():
    txt = open(path, encoding='utf-8').read()
    # 标题：### F1-01 · …
    heads = re.findall(r'^###\s+([A-Z]{1,2}\d?-\d+|[A-Z]{1,2}\d+)\s*·\s*(.+)$', txt, re.M)
    # 判定行：- **判定**：**接不住**…
    verdicts = re.findall(r'\*\*判定\*\*\s*[：:]\s*\**\s*(接得住|接不住)', txt)
    P('%-4s 标题数=%d 判定行数=%d' % (grp, len(heads), len(verdicts)))
    for i, (cid, title) in enumerate(heads):
        v = verdicts[i] if i < len(verdicts) else '?'
        all_ids[cid] = (grp, v, title[:40])

P('')
P('全部案例 ID 数 = %d' % len(all_ids))
bad = [k for k, v in all_ids.items() if v[1] == '接不住']
good = [k for k, v in all_ids.items() if v[1] == '接得住']
unk = [k for k, v in all_ids.items() if v[1] == '?']
P('接不住 = %d' % len(bad))
P('接得住 = %d   %s' % (len(good), sorted(good)))
P('未标判定 = %d   %s' % (len(unk), sorted(unk)))

# 2) 与 failure-inventory.md 中记录的 ID 对比
inv = open('docs/v04/failure-inventory.md', encoding='utf-8').read()
inv_ids = set(re.findall(r'\b((?:F1|F2|F4|F3|C|G|S)-\d{2})\b', inv))
P('')
P('failure-inventory 提到的 ID 数 = %d' % len(inv_ids))
missing_in_inv = sorted(set(all_ids) - inv_ids)
P('测试文件有、总账未提 = %s' % missing_in_inv)
extra_in_inv = sorted(inv_ids - set(all_ids))
P('总账有、测试文件无 = %s' % extra_in_inv)

open('.gh-search/_count.txt', 'w', encoding='utf-8').write(OUT.getvalue())
print(OUT.getvalue())
