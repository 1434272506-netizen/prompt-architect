import io, re
p = 'docs/failure-map.md'
s = open(p, encoding='utf-8').read()
for m in re.finditer(r'§11\.1[–-]11\.8', s):
    ln = s[:m.start()].count('\n') + 1
    print('found at line', ln, '->', s.split('\n')[ln-1][:220])
