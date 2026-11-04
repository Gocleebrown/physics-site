"""Convert the sheet CSV export into the JSON the test scripts read.
Usage: python3 csv_to_json.py sheet.csv sheet.json
Each row gets _r = its row number in the Google Sheet (header is row 1)."""
import csv, json, sys
csv.field_size_limit(10**9)
rows = list(csv.reader(open(sys.argv[1], newline='', encoding='utf-8')))
hdr = rows[0]
out = []
for i, r in enumerate(rows[1:], start=2):
    d = {h: (r[j] if j < len(r) else '') for j, h in enumerate(hdr) if h}
    d['_r'] = i
    out.append(d)
json.dump(out, open(sys.argv[2], 'w', encoding='utf-8'))
print(len(out), 'rows')
