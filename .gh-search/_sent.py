p = 'docs/freeze-v0.3.md'
s = open(p, encoding='utf-8').read()
if '<!-- HASH-TABLE-START -->' not in s:
    s = s.replace('| 文件 | 行数 | sha256 |\n|---|---|---|\n', '<!-- HASH-TABLE-START -->\n| 文件 | 行数 | sha256 |\n|---|---|---|\n', 1)
    s = s.replace('\n\n**合计 24 个受保护文件', '\n<!-- HASH-TABLE-END -->\n\n**合计 24 个受保护文件', 1)
    open(p, 'w', encoding='utf-8').write(s)
print('sentinel:', '<!-- HASH-TABLE-START -->' in open(p, encoding='utf-8').read())
