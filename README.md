# q2authors

Turns a Web of Science (WOS) export into **one row per home-institution author per publication**, with the
journal quartile (Q1–Q4) and index (SCIE, SSCI, ESCI, …) of each publication. The result is used to count
each author's publications at Başkent University.

Programmed by Dr. Zafer Akçalı, MD.

- **Input:** the tab-separated file made by the **wos2q** tool, with *Include addresses* ticked
  (it needs the `Addresses` and `Correspondence` columns).
- **Main program:** `index.html`, runs in the browser, no installation.
- **Helper scripts:** Python, run with [uv](https://docs.astral.sh/uv/) (`uv run script.py`).

---

## The workflow, step by step

| # | Do this | Produces |
|---|---|---|
| 1 | Open `index.html` in the browser. After editing any `.js` data file, press **Ctrl+F5** first, otherwise the browser keeps the old copy. | |
| 2 | Select the wos2q file, press **Read**, then **Convert**. | the result in the text area and a status line with the counts |
| 3 | Press **Save csv**, **Save dropped departments**, **Save dropped names**, **Save dropped addresses**. Save into the project folder. | `output.csv`, `dropped-*.csv` |
| 4 | `uv run .\merge.py` | `merge\merged-output.csv` |
| 5 | `uv run .\count-authors.py` | `merge\author-counts.csv` |
| 6 | Optional, when cleaning names: `uv run .\name-review.py` | `name-review.csv` |

Each step reads the output of the step before it, so after any change run **all the steps from that point on**.
If the browser saves `output (1).csv`, an older `output.csv` was still in the folder: delete it and save again.

---

## What `index.html` does with each publication

1. **Finds the home-institution addresses.** An address counts when it contains one of the strings in
   `addresslist.js` (case-insensitive). If no `Addresses` entry matches, the `Correspondence` address is tried.
2. **Splits the address groups into authors.** `[Author A; Author B] Address` gives one row per author.
3. **Corrects the name** with `namedict.js` (exact match on a variation → its correct name). Then, for a short
   name that fits several people (`Haberal, M.`), `namedict-addresses.js` picks the person by a word in the
   row's address (`Gen Surg` → Mehmet, `Radiol` → Kemal Murat). Only when exactly one person fits, and never on
   a `*` row; otherwise the short name stays.
4. **Drops exact repeats** (same corrected name + same address in one record; WOS sometimes repeats them).
5. **Drops excluded names** (`excludednames.js`) → `dropped-names.csv`.
6. **Drops excluded departments** (`excludeddepts.js`), unless the author is in `protectedNames`
   → `dropped-departments.csv`.
7. **Keeps one row per author per publication.** WOS lists some authors with two or three home addresses
   (e.g. Fac Med + Burn Ctr, Ankara + Adana). The first row is kept, the others are dropped, the address is not
   compared → `dropped-addresses.csv`. Only rows that reached the output count, so an author whose first address
   was excluded in step 6 still keeps the valid one.

### Rows marked `*` in the `NS` column

A `*` row came from a record whose addresses could not be read cleanly: empty `Addresses`, no `[author]`
brackets, or an address rebuilt from the correspondence. Its name cell may hold **a whole author list**
(`Akova, YA - Yilmaz, G - ...`) or a misparsed name.

**`*` rows are never filtered automatically** (steps 5–7 skip them), because a wrong name could drop someone
else's publication. Resolve them by hand (see `resolved-addresses.csv` below). `count-authors.py` skips them.

---

## Files in the project folder

### Program

| File | What it is |
|---|---|
| `index.html` | The converter. The comments at the top list the changes of every version. |
| `merge.py` | Builds `merge\merged-output.csv`, see the merge folder below. |
| `count-authors.py` | Counts **distinct WOS numbers** per author, also split by quartile. |
| `name-review.py` | Lists initials-only names (`Moray, G.`) that probably belong to a full name, for review before adding them to `namedict.js`. |

### Data files (edit these by hand)

All five are JavaScript, so **every line needs its comma** and every name its quotes. A missing comma stops the
whole page. Check after editing with `node --check namedict.js` (or the other file name).

| File | Contains | Format |
|---|---|---|
| `addresslist.js` | Strings that mark a home-institution address, including WOS misspellings (`baflkent univ`, `bapkent univ`, …). | `"baskent univ",` |
| `namedict.js` | Name corrections: spelling variants and short forms → one correct name. The first matching line wins. | `"Correct name","Variation",` |
| `namedict-addresses.js` | Short names shared by several people, resolved by a word in the address. Applied after `namedict.js`. | `{name: "Haberal, Mehmet", shortnames: ["Haberal, M."], addresses: ["Gen Surg"]},` |
| `excludednames.js` | Authors who are not counted (not medical faculty). Applies after correction. | `"Surname, Name",` |
| `excludeddepts.js` | `excludedDepartments`: matched anywhere in a home address. `protectedNames`: authors never dropped by department. | `"Comp Engn",` |

Rules learned the hard way:

- **`namedict.js`: the correct name comes first.** `"Savas, N. A.","Savas, Nurten Akyurek",` is reversed and
  turns the full name into the short form.
- **Do not map a single initial to the most common author.** Many authors use their middle name:
  `Haberal, M.` could be *Mehmet* or *Kemal Murat*, so it stays out of `namedict.js` on purpose and is
  resolved by address in `namedict-addresses.js` instead.
- **`namedict-addresses.js`: a wrong address match is fixed with `wos`.** An entry's optional
  `wos: ["WOS:…"]` list holds publications checked by hand; on those the entry wins whatever the address
  (e.g. two 2008 `Dept Radiol` papers that are Mehmet Haberal's, not Kemal Murat's).
- **`namedict-addresses.js`: lists use square brackets.** `addresses: ["Gen Surg", "Radiol"]`, not curly ones,
  and every entry ends with `},`.
- **Departments, not faculties, in `excludeddepts.js`.** WOS prints `Fac Dent` or `Fac Engn` on some medical
  records (`Fac Engn, Dept Pathol`), so match the department (`Periodontol`, `Comp Engn`). When a faculty-level
  entry such as `Fac Eng` is used anyway, put the medical authors it catches into `protectedNames`.
- Turkish-language addresses need their own entries (`Bilgisayar Muhendisligi` next to `Comp Engn`).

### Input and outputs

| File | Made by | Contains |
|---|---|---|
| `wos_….csv` | wos2q | The input. |
| `output.csv` | Save csv | The result: one row per author per publication, 42 columns. |
| `dropped-names.csv` | Save dropped names | Rows dropped by `excludednames.js`. |
| `dropped-departments.csv` | Save dropped departments | Rows dropped by `excludeddepts.js`. |
| `dropped-addresses.csv` | Save dropped addresses | Every author with several rows on one publication: **all** rows, sorted by name and WOS number, with `Group` and `Action` (`kept` / `removed`) in front. |
| `name-review.csv` | name-review.py | See *Cleaning names* below. |

Every output is **tab-separated, every field in quotes, UTF-8 with BOM**, so Excel shows Turkish characters
correctly. If Excel saves a file back, it usually writes `;` instead of tabs: convert it back before a script
reads it.

---

## The merge folder

`merge.py` combines the converter's result with the rows fixed by hand:

```
merged-output.csv = output.csv
                    − the * rows of every publication listed in resolved-addresses.csv
                    + resolved-addresses.csv
                    + missed-publications.csv
```

| File | Where | Contains |
|---|---|---|
| `output.csv` | **project folder** (read from there, no copy needed) | from `index.html` |
| `resolved-addresses.csv` | `merge` | `*` rows resolved by hand: one clean row per real author, with the real address. Every `*` row of those publications is replaced. |
| `missed-publications.csv` | `merge` | Publications with no home address in WOS that still belong to the institution, added by hand. |
| `merged-output.csv` | `merge` | The final list. |
| `author-counts.csv` | `merge` | Made by `count-authors.py` from the final list. |

- Names in the two hand-made files are corrected with `namedict.js` too; `merge.py` prints each correction.
- Both hand-made files must have **the same 42 columns** as `output.csv`. `merge.py` stops without writing
  anything if a row or the header does not match.
- Copies of the two hand-made files in the project folder are **not** read. Edit the ones in `merge`.

---

## Counting

`count-authors.py` writes `author-counts.csv`: `Author name`, `Publications` (distinct WOS numbers), then one
column per quartile value. An author with several rows on one publication is counted once. `*` rows are skipped
until resolved.

---

## Cleaning names

1. `uv run .\name-review.py` writes `name-review.csv`, one row per short form (`Pirat, A.`), with the candidate
   full names, their publication counts, years and main address.
   - `unambiguous`: only one full name fits. *Only* among the names in this data, so still check.
   - `likely`: one main candidate; the others have at most 2 publications (typos most of the time).
   - `ambiguous`: decide yourself.
2. Fill the **Correct name** column for the rows you approve, leave the others empty.
3. Add the approved rows to `namedict.js` as `"Correct name","Short form",`.
4. Rerun the workflow from step 1 (Ctrl+F5).

`name-review.py` already applies the current `namedict.js`, so a new entry shows up in the next review without
converting again.

---

## Checking that nothing is lost

Every publication of the input should end up in exactly one of these places:

- `merge\merged-output.csv`,
- `dropped-names.csv` or `dropped-departments.csv` (all its home authors were excluded),
- or nowhere, because no address or correspondence contains a home-institution string. Those are found by
  comparing the WOS numbers of the input with the outputs; they go into `missed-publications.csv` when they
  belong to the institution, or into the `NOT UT=(...)` part of the WOS query when they do not.

---

## License

MIT License

Copyright (c) 2026 Zafer Akçalı

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of
the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
