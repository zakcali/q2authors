# Programmed by Zafer Akçalı, MD
# counts distinct wos numbers per author:  uv run count-authors.py [input] [output]
#   default input:  merge/merged-output.csv
#   default output: author-counts.csv next to the input
# an author with two home addresses on one paper has two rows, a publication is still counted once.
# '*' rows are skipped, their name cell holds a whole author list (Akova, YA - Yilmaz, G - ...), not one author.
# columns: Author name, Publications (distinct wos), then distinct wos per Q value (Q1, Q2, Q3, Q4, ...)
# written the way index.html writes: tab separated, every field quoted, header unquoted, UTF-8 BOM
import csv, sys
from collections import defaultdict
from pathlib import Path

src = Path(sys.argv[1] if len(sys.argv) > 1 else 'merge/merged-output.csv')
dst = Path(sys.argv[2] if len(sys.argv) > 2 else src.parent / 'author-counts.csv')

with open(src, encoding='utf-8-sig', newline='') as f:
    rows = list(csv.reader(f, delimiter='\t'))
header, rows = rows[0], [r for r in rows[1:] if r]
NS, NAME, Q, WOS = (header.index(c) for c in ('NS', 'Author name', 'Q', 'Wos number'))

pubs = defaultdict(set)                       # author -> distinct wos numbers
byQ = defaultdict(lambda: defaultdict(set))   # author -> Q value -> distinct wos numbers
qvalues, nweird = set(), 0
for r in rows:
    if r[NS] == '*':
        nweird += 1
        continue
    q = r[Q] or '(none)'
    pubs[r[NAME]].add(r[WOS])
    byQ[r[NAME]][q].add(r[WOS])
    qvalues.add(q)
qcols = sorted(qvalues)  # Q1, Q2, Q3, Q4, then the rest (Q?, (none), ...)

with open(dst, 'w', encoding='utf-8-sig', newline='') as f:
    f.write('\t'.join(['Author name', 'Publications'] + qcols) + '\n')
    w = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_ALL, lineterminator='\n')
    for name in sorted(pubs, key=lambda n: (-len(pubs[n]), n)):  # most publications first
        w.writerow([name, len(pubs[name])] + [len(byQ[name][q]) for q in qcols])

print(f'{src}: {len(rows)} rows, {nweird} * rows skipped (author list, not one author)')
print(f'{dst}: {len(pubs)} authors, {len(set().union(*pubs.values()))} distinct publications')
