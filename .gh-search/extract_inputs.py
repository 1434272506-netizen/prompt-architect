import re, io, os, json

os.chdir(r'C:\Users\Administrator\Desktop\prompt-architect')

def parse(path):
    lines = open(path, encoding='utf-8').read().split('\n')
    cases, cur = [], None
    for i, l in enumerate(lines):
        m = re.match(r'^#{2,4}\s+([A-Z]{1,2}\d+)\s*[·:：\-–—]?\s*(.*)$', l)
        if m:
            cur = {'id': m.group(1), 'title': m.group(2).strip(), 'raw': []}
            cases.append(cur)
            continue
        if cur is not None:
            if re.match(r'^#{1,4}\s+(?!\S*[A-Z]{1,2}\d+\s*[·:：\-–—])', l):
                cur = None
                continue
            cur['raw'].append(l)
    out = []
    for c in cases:
        body = '\n'.join(c['raw'])
        def field(names):
            for n in names:
                m = re.search(r'[-*]\s*\*\*' + n + r'\*\*\s*[：:]\s*(.+)', body)
                if m:
                    return m.group(1).strip()
            return ''
        inp = field(['输入', '用户输入', '用户'])
        # 输入可能跨行（引号块）
        m = re.search(r'[-*]\s*\*\*(?:输入|用户输入|用户)\*\*\s*[：:]\s*(.+?)(?=\n[-*]\s|\n\n|$)', body, re.S)
        if m:
            inp = re.sub(r'\s+', ' ', m.group(1)).strip()
        out.append({'id': c['id'], 'title': c['title'], 'input': inp})
    return out

a = parse('tests/adversarial-question-selection.md')
b = parse('tests/adversarial-merge-questions.md')

buf = io.StringIO()
buf.write('## A. V0.2 问题选择 23 例 —— 原始输入\n\n')
buf.write('| ID | 标题 | 原始用户输入 |\n|---|---|---|\n')
for c in a:
    buf.write('| %s | %s | %s |\n' % (c['id'], c['title'], c['input'] or '（见原文：该例输入为多轮/上文）'))
buf.write('\n共 %d 例\n' % len(a))
buf.write('\n## B. 合并提问 12 例（M1–M12）—— 原始输入\n\n')
buf.write('| ID | 标题 | 原始用户输入 |\n|---|---|---|\n')
for c in b:
    buf.write('| %s | %s | %s |\n' % (c['id'], c['title'], c['input'] or '（见原文）'))
buf.write('\n共 %d 例\n' % len(b))

open('.gh-search/migration_inputs.md', 'w', encoding='utf-8').write(buf.getvalue())
print('A cases:', len(a), 'B cases:', len(b))
print(buf.getvalue()[:6000])
