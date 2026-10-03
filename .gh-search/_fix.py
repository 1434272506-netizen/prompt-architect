import re
p = 'docs/failure-map.md'
s = open(p, encoding='utf-8').read()
new, n = re.subn(r'§11\.1\s?[–-]\s?§?11\.8', '§11.1–§11.7', s)
open(p, 'w', encoding='utf-8', newline='').write(new)
print('replacements:', n)
for m in re.finditer(r'§11\.1[^\n]{0,14}', new):
    print('now:', repr(m.group(0)))
