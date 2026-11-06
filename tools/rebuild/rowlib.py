"""Helpers to build sheet rows for a whole question (Rule 8). Used by build21.py etc."""
import json, csv
HDR = ['level','id','paper','type','tags','params','computedValues','tableRequest','mainText','partIndex','partText','imageBelowMain','imageAfterPart','A_keywords','C3_keywords','C2_keywords','C1_keywords','M_keywords','B_keywords','B2_keywords','modelAnswer','explanation','graphSpec','graph_straight_line_spec','will not work alone','make image','answerType','imageOptions','correctImageIndex','imageChoiceMarks','B3_keywords','tableRowLabels','tableColLabels','tableCellKeywords','tableCellAnswers','tolerance','maxMarks']
KW = {'A':'A_keywords','C3':'C3_keywords','C2':'C2_keywords','C1':'C1_keywords','M':'M_keywords','B':'B_keywords','B2':'B2_keywords','B3':'B3_keywords'}

def kw(*alts):
    """pipe-separated OR list"""
    return '|'.join(alts)
def andor(*groups):
    """AND of ORs as JSON (no apostrophes allowed)"""
    for g in groups:
        for e in g: assert "'" not in e, e
    return json.dumps([list(g) for g in groups], ensure_ascii=False)

def question(level, qid, paper, qtype, tags, params, G, mainText, parts):
    """parts: list of dicts with keys pi,type,K,U,V,tol, A/C3/C2/C1/M/B/B2/B3, plus image/table keys"""
    rows = []
    for n, p in enumerate(parts):
        r = {h: '' for h in HDR}
        r.update(level=level, id=qid, paper=paper, type=p.get('type', qtype), partIndex=str(p['pi']),
                 partText=p['K'], modelAnswer=p.get('U',''), explanation=p.get('V',''))
        if n == 0:
            r['tags'] = tags
            r['params'] = json.dumps(params) if params else ''
            r['computedValues'] = json.dumps(G, ensure_ascii=False) if G else ''
            r['mainText'] = mainText
            r['type'] = qtype if p.get('type') is None else p['type']
        for k, col in KW.items():
            if k in p: r[col] = p[k]
        for k in ('tolerance','graphSpec','answerType','imageOptions','correctImageIndex','imageChoiceMarks',
                  'tableRowLabels','tableColLabels','tableCellKeywords','tableCellAnswers','imageAfterPart','imageBelowMain','maxMarks'):
            if k in p: r[k] = p[k] if isinstance(p[k], str) else json.dumps(p[k], ensure_ascii=False)
        rows.append(r)
    return rows

def write_json(rows, path, start=2):
    for i, r in enumerate(rows, start=start): r['_r'] = i
    json.dump(rows, open(path, 'w', encoding='utf-8'), ensure_ascii=False)

def to_values(rows):
    return [[r[h] for h in HDR] for r in rows]
