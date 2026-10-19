# Programmed by Zafer Akçalı, MD
# lists initials-only author names (Haberal, M. / Ozdemir, B. H. / Akova, YA) that sit next to a full name with the
# same surname and fitting initials, for manual review before adding them to namedict.js
#   uv run name-review.py [input] [output]     default: merge/merged-output.csv -> name-review.csv
# a one letter short form fits any given name, first or middle: Haberal, M. fits Mehmet and Kemal Murat.
# correct names in namedict.js are candidates too, under the surname of each of their variations
# "unambiguous" only means unambiguous among the names in this output and namedict.js. someone who never
# published here under a full name cannot show up as a candidate
# Status
#   unambiguous  exactly one candidate fits (or, with two or more initials, exactly one fits them all), filled in
#   likely       several fit, but all except the first have at most 2 publications and are not in namedict.js,
#                typos most of the time.
#                it is filled in, check it: Onal, Candan has 1 publication and is a different person
#   ambiguous    several fit, Correct name is left empty for you
# Shared WOS counts publications where the short form and the candidate are both listed: two different people,
# or wos listing one person twice. a candidate with many shared WOS is probably NOT the same person
# full names that differ only by case or by wos writing ü/ö as ue/oe (Kirnap, MahIr / Ozin, Buelent) count as one
# person, shown under the most used spelling with "also spelled ...". those spellings need namedict entries too
# '*' rows are skipped, their name cell holds a whole author list
import csv, re, sys, unicodedata
from collections import Counter, defaultdict
from pathlib import Path

src = Path(sys.argv[1] if len(sys.argv) > 1 else 'merge/merged-output.csv')
dst = Path(sys.argv[2] if len(sys.argv) > 2 else 'name-review.csv')

with open(src, encoding='utf-8-sig', newline='') as f:
    rows = list(csv.reader(f, delimiter='\t'))
header, rows = rows[0], [r for r in rows[1:] if r]
NS, NAME, ADDR, WOS, YEAR = (header.index(c) for c in ('NS', 'Author name', 'Author address', 'Wos number', 'Year'))

pairs = re.findall(r'"([^"]*)","([^"]*)"', Path('namedict.js').read_text(encoding='utf-8'))  # "Correct","Variation"
known = {correct for correct, _ in pairs}  # correct names in namedict.js, real people, never treated as a typo
nameDict = {}
for correct, variation in pairs:
    nameDict.setdefault(variation, correct)  # the first pair wins, as in index.html

# names are corrected with the current namedict.js, as the next conversion will do, so a new entry
# takes effect here without converting and merging again
pubs, addrs, years = defaultdict(set), defaultdict(Counter), defaultdict(list)
for r in rows:
    if r[NS] == '*' or ', ' not in r[NAME]:
        continue
    name = nameDict.get(r[NAME], r[NAME])
    pubs[name].add(r[WOS])
    addrs[name][r[ADDR]] += 1
    if r[YEAR].isdigit():
        years[name].append(int(r[YEAR]))

def plain(s):  # Göksel -> goksel, for comparing surnames
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower().strip()

INITIALS = re.compile(r'^(?:[A-Z]\.?[\s-]*)+$')  # M. / M / B. H. / YA / M.A.
def split(name):
    surname, given = name.split(', ', 1)
    return plain(surname), given.strip()
def initials(given):  # 'B. Handan' -> 'BH', 'YA' -> 'YA', 'Mehmet' -> 'M'
    return ''.join(t[0] for t in re.split(r'[\s.\-]+', given) if t) if not INITIALS.match(given) else re.sub(r'[^A-Z]', '', given)

def person(given):  # 'MahIr' = 'Mahir', 'Buelent' = 'Bulent': wos writes ü as ue and ö as oe
    return plain(given).replace('ue', 'u').replace('oe', 'o')

candIni = defaultdict(lambda: defaultdict(set))  # surname -> candidate (correct) name -> initials it is known by
spellings = defaultdict(list)    # candidate -> its other spellings in the output
groups = defaultdict(list)
for n in pubs:
    s, g = split(n)
    if not INITIALS.match(g):
        groups[(s, person(g))].append(n)
def words(given):
    return [w for w in re.split(r'[\s.\-]+', person(given)) if w]
def abbreviates(short, full):  # 'E. Sebnem' abbreviates 'Ebru Sebnem', 'Ali F.' abbreviates 'Ali Fuat'
    a, b = words(short), words(full)
    return len(a) == len(b) and a != b and all(x == y or (len(x) == 1 and y.startswith(x)) for x, y in zip(a, b))
heads = defaultdict(list)  # surname -> the spellings of each full name, one list per person
for (s, _), names in groups.items():
    names.sort(key=lambda x: -len(pubs[x]))
    heads[s].append(names)
for s, lst in heads.items():
    # a partly abbreviated full name (E. Sebnem) is a spelling of the full name it abbreviates (Ebru Sebnem),
    # not another person. it is folded in only when exactly one full name fits
    for names in sorted(lst, key=lambda x: len(words(split(x[0])[1]))):
        if not names:
            continue
        targets = [t for t in lst if t and t is not names and abbreviates(split(names[0])[1], split(t[0])[1])]
        if len(targets) == 1:
            targets[0].extend(names)
            names.clear()
    for names in lst:
        if names:
            # a correct name from namedict.js wins, otherwise the most complete spelling
            head = max(names, key=lambda x: (x in known, len(''.join(words(split(x)[1]))), len(pubs[x])))
            candIni[s][head].add(initials(split(head)[1]))
            spellings[head] = [x for x in sorted(names, key=lambda x: -len(pubs[x])) if x != head]
            for x in spellings[head]:
                pubs[head] = pubs[head] | pubs[x]  # the person's publications under every spelling
# names already decided in namedict.js are candidates under the surname of every variation, with that variation's
# initials: "Haberal, Murat" -> Haberal, Kemal Murat is also known as M, "Haberal, Asuman Nihan" -> Reyhan, ... as AN
for correct, variation in pairs:
    if ', ' in variation and ', ' in correct and not INITIALS.match(split(variation)[1]):
        candIni[split(variation)[0]][correct].add(initials(split(variation)[1]))

def fits(ini, known):
    # M. fits Mehmet and Kemal Murat (many go by their middle name), B.H. fits B. Handan and Beril
    return any(ini in k or ini.startswith(k) for k in known)

def npubs(c):
    return len(pubs.get(c, ()))

def info(n):
    if n not in pubs:
        return f'{n} (namedict.js only, not in this output)'
    y = years[n]
    top = addrs[n].most_common(1)[0][0]
    top = re.sub(r'^(Baskent Univ|Univ Baskent),?\s*', '', top)
    also = f', also spelled {" / ".join(spellings[n])}' if spellings[n] else ''
    return f'{n} ({npubs(n)} pubs, {min(y) if y else "?"}-{max(y) if y else "?"}, {top[:60]}{also})'

out = []
for n in pubs:
    s, g = split(n)
    if not INITIALS.match(g):
        continue
    ini = initials(g)
    fit = [c for c, known in candIni[s].items() if fits(ini, known)]
    if not fit:
        continue
    # with two or more initials an exact match decides: B.H. -> B. Handan, not Beril. one initial never decides,
    # Haberal, M. may be Mehmet or Kemal Murat
    exact = [c for c in fit if ini in candIni[s][c]] if len(ini) > 1 else []
    ranked = sorted(fit, key=lambda c: (c not in exact, -npubs(c)))
    if len(exact) == 1 or len(fit) == 1:
        status, suggest = 'unambiguous', ranked[0]
    elif all(npubs(c) <= 2 and c not in known for c in ranked[1:]):  # the others look like typos, check anyway
        status, suggest = 'likely', ranked[0]
    else:
        status, suggest = 'ambiguous', ''
    shared = [len(pubs[n] & pubs.get(c, set())) for c in ranked]
    out.append([status, n, suggest, len(pubs[n]),
                f'{min(years[n]) if years[n] else "?"}-{max(years[n]) if years[n] else "?"}',
                addrs[n].most_common(1)[0][0][:90],
                ' | '.join(f'{info(c)}{" shared WOS: " + str(k) if k else ""}' for c, k in zip(ranked, shared))])

order = {'unambiguous': 0, 'likely': 1, 'ambiguous': 2}
out.sort(key=lambda r: (order[r[0]], -r[3], r[1]))
with open(dst, 'w', encoding='utf-8-sig', newline='') as f:
    f.write('\t'.join(['Status', 'Short form', 'Correct name', 'Short form pubs', 'Short form years',
                       'Short form main address', 'Candidates (pubs, years, main address)']) + '\n')
    csv.writer(f, delimiter='\t', quoting=csv.QUOTE_ALL, lineterminator='\n').writerows(out)

print(f'{dst}: {len(out)} short forms, ' + ', '.join(
    f'{sum(1 for r in out if r[0] == s)} {s} ({sum(r[3] for r in out if r[0] == s)} pubs)' for s in order))
