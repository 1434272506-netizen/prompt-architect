import hashlib, re, io, os

p = 'SKILL.md'
lines = open(p, encoding='utf-8').read().split('\n')

def block(title_re, stop_at_sub=False):
    start = None
    for i, l in enumerate(lines):
        if re.match(title_re, l):
            start = i
            break
    assert start is not None, title_re
    out = [lines[start]]
    i = start + 1
    while i < len(lines):
        l = lines[i]
        if l.strip() == '---' or (stop_at_sub and re.match(r'^### ', l)) or re.match(r'^## ', l):
            break
        out.append(l)
        i += 1
    while out and out[-1].strip() == '':
        out.pop()
    return start + 1, i, '\n'.join(out)   # 1-based start, end(exclusive->last content line), text

specs = {
    '§2.1': (r'^### 2\.1 ', True),
    '§3':   (r'^## 3\. ', False),
    '§6.3': (r'^### 6\.3 ', True),
    '§6.4': (r'^### 6\.4 ', True),
    '§6.5': (r'^### 6\.5 ', True),
}
base = {
    '§2.1': ('83～151', '26e207d736b0ad747fa3bb69bded41fb1720b2fbf8b109a6634f96e8b4ad3d38'),
    '§3':   ('V0.3.3 新基线', '24efa40f9b64f335ba2b4dd5c2d053cadadef22a73bb1e697703cb25a122d1cd'),
    '§6.3': ('288～301', '8571705186f487b20712c2d8e2f25d96d9b799acf3be45d4248dfbb1d5c04b52'),
    '§6.4': ('303～311', '60315aa5681c0814193e1575c4b4792a22512c922944a465cf9d1212740d3e47'),
    '§6.5': ('313～350', 'aef796ad3a5bda6a5c2fc00480be083b33dbb02e5eb54a8780090511819792b0'),
}

print('%-6s %-14s %-14s %-8s %s' % ('sec', 'base_lines', 'now_lines', 'match', 'sha256'))
for k, (rx, sub) in specs.items():
    s, e, txt = block(rx, sub)
    h = hashlib.sha256(txt.encode('utf-8')).hexdigest()
    b = base[k]
    print('%-6s %-14s %-14s %-8s %s' % (k, b[0], '%d～%d' % (s, e - 1), 'MATCH' if h == b[1] else 'DIFF', h))
    if h != b[1]:
        print('        base=%s' % b[1])
