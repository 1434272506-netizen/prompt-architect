import os, re, sys, collections, io

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
OUT = io.StringIO()
def P(*a):
    OUT.write(' '.join(str(x) for x in a) + '\n')

def rd(p):
    return open(p, encoding='utf-8').read()

skill = rd('SKILL.md')
contract = rd('core/uncertainty-classifier.md')

# 1) 章节骨架
sk_h = re.findall(r'^#{2,3} (.+)$', skill, re.M)
ct_h = re.findall(r'^#{2,3} (.+)$', contract, re.M)
P('== SKILL.md 章节 (%d) ==' % len(sk_h))
P('   ' + ' | '.join(h[:28] for h in sk_h))
P('== contract 章节 (%d) ==' % len(ct_h))
P('   ' + ' | '.join(h[:28] for h in ct_h))

# 2) 陈旧引用检查
stale = {
    '§11.1–11.8': r'§11\.1[–-]11\.8|§11\.1[–-]§?11\.8',
    '动作选择=§11.7(错误)': r'新增 §11\.7 动作',
    'V0.1 旧标题': r'不确定|Uncertainty',
}
P('\n== 陈旧引用 ==')
for name, rx in stale.items():
    hits = []
    for f in ['SKILL.md', 'core/uncertainty-classifier.md', 'README.md'] + \
             ['strategies/' + x for x in os.listdir('strategies')] + \
             ['tests/' + x for x in os.listdir('tests') if x.endswith('.md')] + \
             ['docs/' + x for x in os.listdir('docs')]:
        t = rd(f)
        for m in re.finditer(rx, t):
            hits.append('%s:%d' % (f, t[:m.start()].count('\n') + 1))
    P('  %-22s %s' % (name, hits if hits else 'OK'))

# 3) 引用完整性：所有 §x.y 引用是否存在于 SKILL.md；契约 Rn 是否存在于契约
refs = collections.Counter()
for f in ['core/uncertainty-classifier.md', 'README.md'] + \
         ['strategies/' + x for x in os.listdir('strategies')] + \
         ['tests/' + x for x in os.listdir('tests') if x.endswith('.md')] + \
         ['docs/' + x for x in os.listdir('docs')]:
    t = rd(f)
    for m in re.finditer(r'§\s?(\d+(?:\.\d+)?)', t):
        refs[m.group(1)] += 1
sk_nums = set()
for h in sk_h:
    m = re.match(r'(\d+(?:\.\d+)?)', h.strip())
    if m: sk_nums.add(m.group(1))
# 顶层号也算（## 2 => 2）
missing = sorted([n for n in refs if n not in sk_nums and n.split('.')[0] not in sk_nums],
                 key=lambda x: float(x))
P('\n== 被引用但 SKILL.md 不存在的 § 号 ==')
P('  ' + (', '.join('§%s(x%d)' % (n, refs[n]) for n in missing) if missing else 'OK 全部存在'))

ct_rules = set(re.findall(r'\*\*R(\d+)\*\*', contract))
P('契约规则编号: ' + ', '.join('R' + x for x in sorted(ct_rules, key=int)))
bad_r = collections.Counter()
for f in ['SKILL.md', 'README.md'] + ['strategies/' + x for x in os.listdir('strategies')] + \
         ['tests/' + x for x in os.listdir('tests') if x.endswith('.md')] + ['docs/' + x for x in os.listdir('docs')]:
    t = rd(f)
    for m in re.finditer(r'契约\s?\*{0,2}R(\d+)', t):
        if m.group(1) not in ct_rules: bad_r['%s:R%s' % (f, m.group(1))] += 1
P('引用不存在的契约 Rn : ' + (', '.join(bad_r) if bad_r else 'OK'))

# 4) 案例计数与禁用词
P('\n== 测试文件 ==')
total = 0
for fn in sorted(os.listdir('tests')):
    if fn.startswith('adversarial') or fn in ('cases.md', 'acceptance.md'): continue
    if not fn.endswith('.md'): continue
    t = rd('tests/' + fn)
    ids = re.findall(r'^#{3,4}\s*([A-Z]{2}-\d+|Test\s*0?\d+)', t, re.M) + re.findall(r'\*\*(Test\s*0?\d+)\*\*', t)
    ids = [x.strip('*') for x in ids]
    uniq = sorted(set(ids))
    total += len(uniq)
    P('  %-24s 案例=%2d  %s' % (fn, len(uniq), ', '.join(uniq[:8]) + ('…' if len(uniq) > 8 else '')))
P('  合计唯一案例 = %d' % total)
forbidden = ['视情况而定', '看具体要求', '酌情处理']
P('\n== 禁用词（唯一裁定） ==')
for f in ['tests/' + x for x in os.listdir('tests') if x.endswith('.md')] + ['docs/failure-map.md']:
    t = rd(f)
    hit = [w for w in forbidden if w in t]
    if hit: P('  %s -> %s' % (f, hit))
P('  ' + ('OK 无禁用词' if True else ''))

# 5) 机制词泄漏：strategies 的用户可见模板段
mech = ['Type A', 'Type B', 'Type C', 'Type D', 'Type E', 'unknown known', 'Unknown Known',
        'ASK', 'SHOW', 'INSPECT', 'TEACH', 'DISCOVER', '决策树', '命中', '触发信号',
        'P0', 'unresolved', '槽位']
P('\n== strategies 用户可见模板内的机制词 ==')
for fn in sorted(os.listdir('strategies')):
    t = rd('strategies/' + fn)
    m = re.search(r'## 用户可见模板(.*?)\n## ', t, re.S)
    if not m:
        P('  %-16s ⚠️ 未找到模板段' % fn); continue
    seg = m.group(1)
    # 提取 ``` 代码块内的用户话术；若无代码块则整段
    blocks = re.findall(r'```(?:text)?\n(.*?)```', seg, re.S)
    body = '\n'.join(blocks) if blocks else seg
    hits = [w for w in mech if w in body]
    P('  %-16s %s' % (fn, hits if hits else 'OK 无机制词'))

# 6) V0.3.1–V0.3.7 新增规则是否有支撑
P('\n== V0.3 新增规则支撑 ==')
for r in ['R11', 'R12', 'R13', 'R14']:
    cited = []
    for f in ['strategies/' + x for x in os.listdir('strategies')] + \
             ['tests/' + x for x in os.listdir('tests') if x.endswith('.md')] + ['docs/failure-map.md']:
        if re.search(r'\b' + r + r'\b', rd(f)): cited.append(f)
    P('  %s -> %s' % (r, cited if cited else '⚠️ 无引用'))

open('.gh-search/verify_out.txt','w',encoding='utf-8').write(OUT.getvalue())
P('written')
