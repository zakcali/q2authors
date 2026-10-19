# Programmed by Zafer Akçalı, MD
# merges q2authors outputs into merged-output.csv:  uv run merge.py [folder]   (default folder: merge)
#   output.csv              rows from index.html, read from the project folder (next to merge.py and
#                           index.html), where the page saves it. no need to copy it into the folder
#   resolved-addresses.csv  in the folder, hand-resolved rows, appended after output.csv. every '*' row of output.csv
#                           whose wos number is here is dropped. clean rows of output.csv are never dropped
#   missed-publications.csv in the folder, publications with no home address in wos, appended at the end
# merged-output.csv is written into the folder
# names in the two hand-made files are corrected with namedict.js (next to merge.py), as index.html does.
# all three files must have the same 42 columns. output is written the way index.html writes it:
# tab separated, every field quoted, header unquoted, UTF-8 BOM so excel reads turkish characters
import csv, re, sys
from collections import Counter
from pathlib import Path

folder = Path(sys.argv[1] if len(sys.argv) > 1 else 'merge')
project = Path(__file__).resolve().parent  # where index.html saves output.csv
NS, NAME, WOS = 0, 1, 13  # column positions

def read(path):
    name = path.name
    with open(path, encoding='utf-8-sig', newline='') as f:  # utf-8-sig drops the BOM
        rows = list(csv.reader(f, delimiter='\t'))
    rows = [r for r in rows if r]  # skip empty lines
    bad = [i+1 for i, r in enumerate(rows) if len(r) != len(rows[0])]
    if bad:
        sys.exit(f'{name}: line(s) {bad[:10]} do not have {len(rows[0])} fields, nothing written')
    print(f'{path}: {len(rows)-1} rows')
    return rows[0], rows[1:]

header, output = read(project / 'output.csv')
h1, resolved = read(folder / 'resolved-addresses.csv')
h2, missed = read(folder / 'missed-publications.csv')
if (folder / 'output.csv').exists() and (folder / 'output.csv').resolve() != (project / 'output.csv').resolve():
    print(f'note: {folder / "output.csv"} is not read any more, it can be deleted')
for name, h in (('resolved-addresses.csv', h1), ('missed-publications.csv', h2)):
    if h != header:
        sys.exit(f'{name}: header differs from output.csv, nothing written')

# hand-made rows never went through index.html, so correct their names with namedict.js the same way:
# exact match on a variation, the first pair wins. only merged-output.csv changes, the source files do not.
# excludednames.js and the department filter are not applied, these rows were chosen by hand
nameDict = {}
for correct, variation in re.findall(r'"([^"]*)",\s*"([^"]*)"',
                                     (Path(__file__).parent / 'namedict.js').read_text(encoding='utf-8')):
    nameDict.setdefault(variation, correct)
for name, rows in (('resolved-addresses.csv', resolved), ('missed-publications.csv', missed)):
    for r in rows:
        if r[NAME] in nameDict:
            print(f'corrected in {name}: {r[WOS]}  {r[NAME]} -> {nameDict[r[NAME]]}')
            r[NAME] = nameDict[r[NAME]]

byWos = {r[WOS] for r in resolved}  # resolved publications
for r in resolved:
    if r[NS] == '*':
        print(f'warning: resolved-addresses.csv still has a * row, {r[WOS]} {r[NAME]}')

merged = [r for r in output if not (r[NS] == '*' and r[WOS] in byWos)]  # drop '*' rows of resolved publications
nreplaced = len(output) - len(merged)
starWos = {r[WOS] for r in output if r[NS] == '*'}
for w in byWos:
    if w not in starWos:
        print(f'warning: {w} has no * row in output.csv, nothing was replaced for it')
merged.extend(resolved)
merged.extend(missed)

# report, never remove: an added row whose author already has a row on that publication probably
# repeats a clean row of output.csv. output.csv itself has such pairs, one author with two home
# addresses gets two rows, so only pairs that involve an added row are reported
count = Counter((r[WOS], r[NAME]) for r in merged)
for r in resolved + missed:
    if count[(r[WOS], r[NAME])] > 1:
        print(f'warning: {r[NAME]} appears more than once on {r[WOS]}, check by hand')

with open(folder / 'merged-output.csv', 'w', encoding='utf-8-sig', newline='') as f:
    f.write('\t'.join(header) + '\n')  # header left unquoted, as index.html writes it
    csv.writer(f, delimiter='\t', quoting=csv.QUOTE_ALL, lineterminator='\n').writerows(merged)

print(f'* rows replaced: {nreplaced} (in {len(byWos & starWos)} publications), resolved rows added: {len(resolved)}, '
      f'missed rows added: {len(missed)}')
print(f'merged-output.csv: {len(merged)} rows = {len(output)} - {nreplaced} + {len(resolved)} + {len(missed)}')
