"""Recompute the §2 hash-table rows affected by freeze exception #35.

Read-only: prints the replacement rows and the new total line count.
"""
import hashlib
import re

src = open('.gh-search/freeze_v03.py', encoding='utf-8').read()
m = re.search(r'FROZEN = \[(.*?)\]', src, re.S)
files = re.findall(r"'([^']+)'", m.group(1))

total = 0
changed = {}
for f in files:
    raw = open(f, 'rb').read()
    n = len(open(f, encoding='utf-8').read().split('\n'))
    total += n
    if f in ('README.md', 'tests/acceptance.md'):
        changed[f] = (n, hashlib.sha256(raw).hexdigest())

print('frozen files:', len(files))
for f, (n, h) in changed.items():
    print('ROW | `%s` | %d | `%s` |' % (f, n, h))
print('TOTAL LINE: **合计 %d 个受保护文件，%d 行。**' % (len(files), total))
