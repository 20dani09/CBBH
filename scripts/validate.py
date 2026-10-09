#!/usr/bin/env python3
"""Validate documentation locally; never execute examples or contact targets."""
from pathlib import Path
from collections import Counter
import argparse, ast, csv, hashlib, json, re, sys, urllib.parse

ROOT=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='scripts' else Path(__file__).resolve().parent/'consolidated'
parser=argparse.ArgumentParser()
parser.add_argument('--migration',action='store_true',help='Also check immutable migration evidence.')
parser.add_argument('--json',dest='json_path',help='Write a machine-readable validation report.')
args=parser.parse_args()
errors=[];warnings=[];links=0;images=0;fences=0;examples=0;inline_examples=0
docs={str(p.relative_to(ROOT)):p.read_text(encoding='utf-8') for p in ROOT.rglob('*.md') if '.git' not in p.parts}

def outside_code(text):
    return re.sub(r'(?ms)^```[^\n]*\n.*?^```[^\n]*$', '', text)

def anchors(text):
    result=set();counts=Counter()
    for line in outside_code(text).splitlines():
        m=re.match(r'^#{1,6}\s+(.*)',line)
        if not m:continue
        value=re.sub(r'[^\w\s-]','',m.group(1).strip().lower()).replace(' ','-')
        n=counts[value];counts[value]+=1
        result.add(value+(('-'+str(n)) if n else ''))
    return result

HIGH_CONFIDENCE=[r'-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----',r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b',r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b',r'\bxox[baprs]-[A-Za-z0-9-]{15,}\b',r'\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b',r'--api-token\s+[A-Za-z0-9_-]{16,}',r'PHPSESSID=[A-Za-z0-9_-]{12,}',r'Cookie:\s*session=[A-Za-z0-9_-]{16,}']

for path,text in docs.items():
    docpath=ROOT/path
    raw_fences=re.findall(r'(?m)^```([^\n]*)$',text)
    if len(raw_fences)%2:errors.append({'file':path,'type':'unbalanced-fence'})
    for i,tag in enumerate(raw_fences):
        if i%2==0 and not tag.strip():errors.append({'file':path,'type':'missing-code-language'})
    fences+=len(raw_fences)//2
    plain=outside_code(text)
    if len(re.findall(r'(?m)^#\s',plain))!=1:errors.append({'file':path,'type':'title-count'})
    if re.search(r'!?\[\[[^\]]+\]\]',plain):errors.append({'file':path,'type':'unconverted-wikilink'})
    for match in re.finditer(r'(!?)\[[^\]]*\]\(([^\n]+?)\)',plain):
        bang,url=match.group(1),match.group(2).strip()
        # Optional quoted link title is not part of the destination.
        url=re.split(r'\s+[\x22\x27]',url,1)[0].strip('<>')
        if re.match(r'^(?:https?://|mailto:|data:|app:)',url):continue
        if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:',url):
            warnings.append({'file':path,'type':'nonportable-uri','reference':url});continue
        links+=1
        if bang:images+=1
        split=urllib.parse.urlsplit(url)
        target=(docpath.parent/urllib.parse.unquote(split.path)).resolve() if split.path else docpath.resolve()
        if not target.is_relative_to(ROOT.resolve()):errors.append({'file':path,'type':'path-outside-repository','reference':url});continue
        if not target.exists():errors.append({'file':path,'type':'missing-target','reference':url});continue
        if split.fragment and target.suffix=='.md':
            ref=urllib.parse.unquote(split.fragment)
            if ref not in anchors(target.read_text()):errors.append({'file':path,'type':'missing-anchor','reference':url})
    for pattern in HIGH_CONFIDENCE:
        if re.search(pattern,text):errors.append({'file':path,'type':'possible-sensitive-literal'})
    # Newly corrected Python reference must parse; source exploit snippets are
    # treated as immutable text, not imported or executed by the validator.
    if path=='Tools/burpsuite-python-proxy.md':
        for code in re.findall(r'(?ms)^```python\n(.*?)^```\s*$',text):
            try:ast.parse(code)
            except SyntaxError:errors.append({'file':path,'type':'invalid-proxy-example-syntax'})

if args.migration:
    audit=ROOT/'Resources/Audit'
    snapshot=json.loads((audit/'integrity.json').read_text())
    migration=list(csv.DictReader((audit/'migration.csv').open(newline='')))
    if len(migration)!=snapshot['original_files']:errors.append({'type':'source-count-mismatch'})
    if len({(r['source_repo'],r['source_path']) for r in migration})!=len(migration):errors.append({'type':'duplicate-source-row'})
    for row in migration:
        for dest in json.loads(row['destinations']):
            if not (ROOT/dest).exists():errors.append({'file':dest,'type':'migration-destination-missing'})
    for check in snapshot['expected_code']:
        text=docs.get(check['destination'],'')
        hashes={hashlib.sha256(b.encode()).hexdigest() for b in re.findall(r'(?ms)^```[^\n]*\n(.*?)^```\s*$',text)}
        examples+=len(check['blocks'])
        for sha in set(check['blocks']):
            if sha not in hashes:errors.append({'file':check['destination'],'type':'original-example-changed','source':check['source'],'hash':sha})
        # An inline example may legitimately appear once in a fenced block of
        # the canonical document. Search both contexts for its unchanged hash.
        inline_hashes={hashlib.sha256(s.encode()).hexdigest() for s in re.findall(r'`([^`\n]+)`',outside_code(text))}
        block_lines=[line.strip() for b in re.findall(r'(?ms)^```[^\n]*\n(.*?)^```\s*$',text) for line in b.splitlines()]
        inline_hashes.update(hashlib.sha256(s.encode()).hexdigest() for s in block_lines)
        inline_examples+=len(check.get('inline',[]))
        for sha in set(check.get('inline',[])):
            if sha not in inline_hashes:errors.append({'file':check['destination'],'type':'original-inline-example-changed','source':check['source'],'hash':sha})
    for check in snapshot['images']:
        path=ROOT/check['destination']
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest()!=check['sha256']:
            errors.append({'file':check['destination'],'type':'binary-integrity-failure'})

report={'markdown_documents':len(docs),'local_links_checked':links,'image_links_checked':images,'fenced_blocks':fences,'source_example_occurrences_checked':examples,'inline_example_occurrences_checked':inline_examples,'errors':errors,'warnings':warnings,'result':'pass' if not errors else 'fail'}
if args.json_path:Path(args.json_path).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(bool(errors))
