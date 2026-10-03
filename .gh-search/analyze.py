import os, re, json, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(ROOT, 'raw')
REF = os.path.join(os.path.dirname(ROOT), 'SKILL.md')

def norm(s):
    s = s.replace('\u3000', ' ')
    s = re.sub(r'\s+', '', s)
    return s.lower()

ref = norm(open(REF, encoding='utf-8').read())
ref3 = {ref[i:i+3] for i in range(len(ref)-2)}

FEATURES = {
    '触发判定(何时不采访)': [r'触发', r'不适用', r'未指定', r'under[- ]?specified', r'trigger', r'when not'],
    '分轮采访循环(1-3问)': [r'一轮', r'每轮', r'interview loop', r'clarify', r'1[~\-–]3', r'one to three', r'at most three'],
    '问题优先级(P0-P3/信息增益)': [r'P0', r'优先级', r'priorit', r'information gain', r'highest[- ]value'],
    '停止规则(信息够了就停)': [r'停止', r'停止规则', r'stop', r'when to stop', r'sufficient'],
    '默认/降级(用户说随便)': [r'随便', r'降级', r'default', r'degrade', r'fallback', r'assum'],
    '模糊词拆解(正交方向)': [r'模糊词', r'正交', r'vague term', r'orthogonal', r'ambiguous', r'cinematic', r'电影感'],
    '双轨标记(需求/假设分离)': [r'待确认假设', r'双轨', r'assumption', r'separate.*assumption', r'confirm'],
    '固定输出结构(5段)': [r'5 段', r'五段', r'输出格式', r'验收标准', r'acceptance criteria', r'success criteria', r'deliverable'],
    '用户侧话术(不泄露机制)': [r'用户侧', r'对外', r'人话', r'机制词', r'internal state', r'no jargon', r'plain language'],
    '冲突/修正处理(不重来)': [r'冲突', r'修正', r'revision', r'conflict', r'tension', r'update.*requirement'],
    '持久化/落盘产物': [r'落盘', r'brief\.md', r'persist', r'write.*file', r'需求简报', r'save'],
    '研究对象/产物类型清单': [r'七问', r'对象', r'deliverable type', r'checklist', r'七', r'taxonomy'],
}

def has(txt, pats):
    t = txt.lower()
    return sum(1 for p in pats if re.search(p, t, re.I))

rows = []
for fn in sorted(os.listdir(RAW)):
    if not fn.endswith('.md'):
        continue
    raw = open(os.path.join(RAW, fn), encoding='utf-8', errors='replace').read()
    n = norm(raw)
    n3 = {n[i:i+3] for i in range(len(n)-2)}
    inter = len(ref3 & n3)
    cov = inter / max(1, len(ref3))     # 候选覆盖了多少本文件的 3-gram
    prec = inter / max(1, len(n3))      # 候选自身有多少被本文件覆盖
    fhits = {k: has(n, v) for k, v in FEATURES.items()}
    rows.append({
        'file': fn, 'chars': len(raw), 'gram3_cov_ref': round(cov, 4),
        'gram3_prec_cand': round(prec, 4), 'features_hit': sum(1 for x in fhits.values() if x),
        'feat': {k: v for k, v in fhits.items() if v},
    })

rows.sort(key=lambda r: -r['gram3_cov_ref'])
out = os.path.join(ROOT, 'compare.json')
json.dump({'ref_chars': len(ref), 'ref_gram3': len(ref3), 'rows': rows}, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

print('REF grams3=%d  files=%d' % (len(ref3), len(rows)))
print('%-28s %7s %9s %9s %5s  %s' % ('file', 'chars', 'cov_ref', 'prec_cand', 'feat', 'top features'))
for r in rows:
    top = ', '.join(list(r['feat'].keys())[:4])
    print('%-28s %7d %9.4f %9.4f %5d  %s' % (r['file'], r['chars'], r['gram3_cov_ref'], r['gram3_prec_cand'], r['features_hit'], top))
