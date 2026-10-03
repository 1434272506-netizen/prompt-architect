import io
p = '.gh-search/freeze_v03.py'
lines = open(p, encoding='utf-8').read().split('\n')
# 删除旧的"整文档重写"块（从 "    if write:" 到 "        print('已重新登记基线" 那行）
start = next(i for i,l in enumerate(lines) if l.strip() == 'if write:')
end = next(i for i,l in enumerate(lines) if '已重新登记基线' in l)
new = lines[:start] + ["    if write:", "        replace_hashes()"] + lines[end+1:]
open(p, 'w', encoding='utf-8').write('\n'.join(new))
print('removed lines:', end - start + 1)
print('now around write block:')
print('\n'.join(new[start-2:start+4]))
