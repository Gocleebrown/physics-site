##v1
"""9702-25-41S-Q4 row 70: restore the third table column 'thermal energy supplied to gas' (real Table 4.1 has it). python3 patch_s25p41q4_table.py in.csv out.csv"""
import csv, json, sys
csv.field_size_limit(10**9)
TEXT_OLD = 'the work done on the gas and the increase in internal energy of the gas, for each of the two processes.'
TEXT_NEW = 'the work done on the gas, the thermal energy supplied to the gas and the increase in internal energy of the gas, for each of the two processes.'
COLS = ["work done on gas", "thermal energy supplied to gas", "increase in internal energy"]
KW = [[["+w"], ["2u-w", "2u−w", "2u–w", "-w+2u", "−w+2u", "2u minus w", "(2u-w)", "(2u−w)"], ["2u", "+2u"]],
      [["0"], ["-u", "−u", "–u", "minus u"], ["-u", "−u", "–u", "minus u"]]]
ANS = [["+W", "2U − W", "+2U"], ["0", "−U", "−U"]]
M70 = 'Compression: work done on gas +W, thermal energy supplied 2U − W, increase in internal energy +2U. Cooling at constant volume: work done on gas 0, thermal energy supplied −U, increase in internal energy −U.'
V70 = ('For an ideal gas the internal energy is proportional to the thermodynamic temperature, so U ∝ T. Compression takes T to 3T, so the internal energy rises from U to 3U, an increase of 2U. '
       'The first law, increase in internal energy = thermal energy supplied + work done on the gas, gives thermal energy supplied = 2U − W. '
       'Cooling at constant volume does no work (the volume does not change), so the work done on the gas is 0. Cooling from 3T to 2T takes the internal energy from 3U to 2U, an increase of −U, '
       'and with no work done the thermal energy supplied is also −U (thermal energy leaves the gas).')
def main(i, o):
    rows = list(csv.reader(open(i, encoding='utf-8', newline='')))
    h = rows[0]; c = {n: k for k, n in enumerate(h) if n}
    r = rows[69] + [''] * (len(h) - len(rows[69]))
    assert r[c['id']] == '9702-25-41S-Q4' and r[c['partIndex']] == '2'
    assert TEXT_OLD in r[c['partText']] and json.loads(r[c['tableColLabels']]) == ["work done on gas", "increase in internal energy"]
    r[c['partText']] = r[c['partText']].replace(TEXT_OLD, TEXT_NEW)
    r[c['tableColLabels']] = json.dumps(COLS); r[c['tableCellKeywords']] = json.dumps(KW, ensure_ascii=False)
    r[c['tableCellAnswers']] = json.dumps(ANS, ensure_ascii=False); r[c['modelAnswer']] = M70; r[c['explanation']] = V70
    rows[69] = r
    csv.writer(open(o, 'w', encoding='utf-8', newline='')).writerows(rows)
    json.dump({k: r[c[k]] for k in ('partText', 'tableColLabels', 'tableCellKeywords', 'tableCellAnswers', 'modelAnswer', 'explanation')}, open(o + '.edits.json', 'w', encoding='utf-8'), ensure_ascii=False)
if __name__ == '__main__': main(sys.argv[1], sys.argv[2])
