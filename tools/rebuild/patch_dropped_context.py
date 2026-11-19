##v1
"""Rule 8: mainText/imageBelowMain are read from the partIndex-0 row only, so context typed on a later part's row was never shown.
This moves every such cell into the partText of the row that holds it (as a lead-in paragraph); the 41-Q3 context image goes to imageAfterPart.
Usage: python3 patch_dropped_context.py in.csv out.csv  (fails loudly if the sheet no longer matches)"""
import csv, json, sys
csv.field_size_limit(10**9)
def main(i, o):
    rows = list(csv.reader(open(i, encoding='utf-8', newline='')))
    h = rows[0]; c = {n: k for k, n in enumerate(h) if n}
    edits = {}
    for n, r in enumerate(rows):
        if n == 0 or len(r) <= c['partIndex'] or not r[c['id']] or r[c['partIndex']] in ('', '0'): continue
        r += [''] * (len(h) - len(r))
        mt = r[c['mainText']].strip()
        if mt:
            r[c['partText']] = '<div style="margin-bottom:.5em">' + mt + '</div>' + r[c['partText']]
            r[c['mainText']] = ''
            edits.setdefault(n + 1, {}).update(partText=r[c['partText']], mainText='')
        if r[c['imageBelowMain']].strip():
            assert not r[c['imageAfterPart']].strip(), n + 1
            r[c['imageAfterPart']] = r[c['imageBelowMain']]; r[c['imageBelowMain']] = ''
            edits.setdefault(n + 1, {}).update(imageAfterPart=r[c['imageAfterPart']], imageBelowMain='')
    assert sorted(edits) == [17, 152, 709, 711, 714, 721, 723, 729, 736, 740], sorted(edits)
    csv.writer(open(o, 'w', encoding='utf-8', newline='')).writerows(rows)
    json.dump(edits, open(o + '.edits.json', 'w', encoding='utf-8'), ensure_ascii=False)
if __name__ == '__main__': main(sys.argv[1], sys.argv[2])
