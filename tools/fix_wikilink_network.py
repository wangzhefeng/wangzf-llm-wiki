#!/usr/bin/env python3
from pathlib import Path
import re
import unicodedata
from collections import defaultdict

ROOT=Path('wiki')
FILES=[p for p in ROOT.rglob('*.md')]
LINK_RE=re.compile(r'\[\[([^\]|#]+)(?:#[^\]]*)?(?:\|[^\]]*)?\]\]')


def normalize(s:str)->str:
    s=unicodedata.normalize('NFKC', s).lower().strip()
    s=re.sub(r'\s+','',s)
    s=re.sub(r'[\-—_·•,，。:：;；!！?？"“”‘’()（）\[\]【】{}<>《》`~]','',s)
    return s


def is_path_like(t:str)->bool:
    if '/' in t or '\\' in t:
        return True
    if re.search(r'\.(png|jpg|jpeg|gif|svg|pdf|ipynb|py|json|yaml|yml|txt|csv|tsv|md)$', t, re.I):
        return True
    if t.startswith('http://') or t.startswith('https://'):
        return True
    return False


def split_frontmatter(text:str):
    if not text.startswith('---\n'):
        return {},text
    end=text.find('\n---\n',4)
    if end==-1:
        return {},text
    fm_raw=text[4:end]
    body=text[end+5:]
    fm={}
    key=None
    for line in fm_raw.splitlines():
        m=re.match(r'^([A-Za-z0-9_]+):\s*(.*)$', line)
        if m:
            key=m.group(1);v=m.group(2).strip()
            fm[key]=[] if v=='' else v
        elif line.strip().startswith('- ') and key and isinstance(fm.get(key), list):
            fm[key].append(line.strip()[2:].strip())
    return fm, body


def write_md(path:Path, fm:dict, body:str):
    lines=['---']
    lines.append(f"created_at: {fm.get('created_at','2026-04-09')}")
    lines.append('topics:')
    topics=fm.get('topics') or ['自动补链','断链修复']
    if isinstance(topics,str): topics=[topics]
    for t in topics[:3]:
        lines.append(f'  - {t}')
    lines.append('related_concepts:')
    rc=fm.get('related_concepts') or []
    if isinstance(rc,str): rc=[rc]
    for t in rc[:5]:
        lines.append(f'  - {t}')
    lines.append(f"status: {fm.get('status','inbox')}")
    lines.append('---\n')
    path.write_text('\n'.join(lines)+body.strip()+"\n", encoding='utf-8')


existing={p.stem for p in FILES}
norm_to_stems=defaultdict(list)
for s in existing:
    norm_to_stems[normalize(s)].append(s)

# pass1/2: rewrite files
all_targets=[]
for p in FILES:
    txt=p.read_text(encoding='utf-8')
    for t in LINK_RE.findall(txt):
        all_targets.append((p,t.strip()))

counters={'replacements':0,'plain_text_fixes':0}
for p in FILES:
    txt=p.read_text(encoding='utf-8')

    def repl(m):
        target=m.group(1).strip()
        if not target:
            return m.group(0)
        if target in existing:
            return m.group(0)
        n=normalize(target)
        cands=norm_to_stems.get(n,[])
        if len(cands)==1:
            counters['replacements']+=1
            return f'[[{cands[0]}]]'
        if is_path_like(target):
            counters['plain_text_fixes']+=1
            return f'`{target}`'
        return m.group(0)

    new=LINK_RE.sub(repl, txt)
    if new!=txt:
        p.write_text(new, encoding='utf-8')

# recompute broken
FILES=[p for p in ROOT.rglob('*.md')]
existing={p.stem for p in FILES}
broken_targets=set()
for p in FILES:
    txt=p.read_text(encoding='utf-8')
    for t in LINK_RE.findall(txt):
        t=t.strip()
        if t and t not in existing:
            broken_targets.add(t)

# pass3: create stubs for unresolved non-path targets
stub_dir=ROOT/'concepts'/'autofix'
stub_dir.mkdir(parents=True, exist_ok=True)
created=0
for t in sorted(broken_targets):
    if is_path_like(t):
        continue
    stub=stub_dir/f'{t}.md'
    if stub.exists():
        continue
    fm={'created_at':'2026-04-09','topics':['自动补链','待完善'],'related_concepts':[],'status':'inbox'}
    body=f'# {t}\n\n> 自动创建的占位页，用于修复断链。后续请补充正式内容与来源。\n'
    write_md(stub,fm,body)
    created+=1

# final stats
FILES=[p for p in ROOT.rglob('*.md')]
existing={p.stem for p in FILES}
broken=0
for p in FILES:
    txt=p.read_text(encoding='utf-8')
    for t in LINK_RE.findall(txt):
        t=t.strip()
        if t and t not in existing:
            broken+=1

print('rewired_alias_links', counters['replacements'])
print('converted_pathlike_to_plain', counters['plain_text_fixes'])
print('created_stub_pages', created)
print('final_broken_links', broken)
