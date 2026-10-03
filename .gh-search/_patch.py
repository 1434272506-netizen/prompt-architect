import re, io
p = '.gh-search/verify_v03.py'
s = open(p, encoding='utf-8').read()
s = s.replace("print(", "P(")
s = s.replace("P('== SKILL.md", "P('== SKILL.md")
# 用 ## / ### 标题作为案例 ID 源
s = s.replace(r"ids = re.findall(r'\*\*(?:Test\s*0?\d+|[A-Z]{2}-\d+)\*\*', t)", r"ids = re.findall(r'^#{3,4}\s*([A-Z]{2}-\d+|Test\s*0?\d+)', t, re.M) + re.findall(r'\*\*(Test\s*0?\d+)\*\*', t)")
s += "\nopen('.gh-search/verify_out.txt','w',encoding='utf-8').write(OUT.getvalue())\nP('written')\n"
open(p,'w',encoding='utf-8').write(s)
print('patched')
