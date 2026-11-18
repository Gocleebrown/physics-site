##v1
"""s25 p22 Q2(b)(ii): replace the 'draw on Fig. 2.2' part (no figure existed) with a pick-the-vector-triangle imageChoice.
Options are generated from the question's own numbers (weight 270 kg, F 1800 N, 25 deg), drawn to scale, correct option at a random
position, and the whole set is randomly mirrored. Not a copy of the CIE figure.
Usage: python3 patch_s25p22q2.py in.csv out.csv   (in.csv = sheet export; edits rows with id 9702_s25_p22_q2)"""
import csv, json, sys
csv.field_size_limit(10**9)
TRI = r"""(kind,mir)=>{const W=300,H=250;
const Wt=270*9.81,F=1800,th=25*Math.PI/180,m=mir?-1:1;
let w=[0,-Wt],f=[-m*F*Math.sin(th),F*Math.cos(th)];
if(kind==='swap'){w=[0,-F];f=[-m*Wt*Math.sin(th),Wt*Math.cos(th)];}
if(kind==='horiz')f=[-m*F*Math.cos(th),F*Math.sin(th)];
const pts=[[0,0],[w[0],w[1]],[w[0]+f[0],w[1]+f[1]]];
const xs=pts.map(p=>p[0]),ys=pts.map(p=>p[1]);
const k=Math.min(150/(Math.max(...xs)-Math.min(...xs)||1),140/(Math.max(...ys)-Math.min(...ys)||1),0.06);
const ox=150-k*(Math.max(...xs)+Math.min(...xs))/2,oy=125+k*(Math.max(...ys)+Math.min(...ys))/2;
const P=pts.map(p=>[ox+k*p[0],oy-k*p[1]]);
let s='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 '+W+' '+H+'" width="'+W+'" height="'+H+'" font-family="Arial,sans-serif" font-size="14"><rect width="'+W+'" height="'+H+'" fill="#fff"/>';
s+='<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker></defs>';
const ar=(a,b)=>'<line x1="'+a[0].toFixed(1)+'" y1="'+a[1].toFixed(1)+'" x2="'+b[0].toFixed(1)+'" y2="'+b[1].toFixed(1)+'" stroke="#000" stroke-width="1.6" marker-end="url(#ah)"/>';
const A=P[0],B=P[1],C=P[2];
s+=ar(A,B)+ar(B,C);
s+=kind==='rev'?ar(A,C):ar(C,A);
const mid=(a,b)=>[(a[0]+b[0])/2,(a[1]+b[1])/2];
const cen=[(A[0]+B[0]+C[0])/3,(A[1]+B[1]+C[1])/3];
const lab=(a,b,t)=>{const q=mid(a,b);let dx=q[0]-cen[0],dy=q[1]-cen[1];const d=Math.hypot(dx,dy)||1;return '<text x="'+(q[0]+dx/d*20-5).toFixed(1)+'" y="'+(q[1]+dy/d*20+5).toFixed(1)+'" font-style="italic">'+t+'</text>'};
s+=lab(A,B,'W')+lab(B,C,'F')+lab(C,A,'R');
const nrm=v=>{const d=Math.hypot(v[0],v[1])||1;return [v[0]/d,v[1]/d]};
const fv=nrm([C[0]-B[0],C[1]-B[1]]);
const u=kind==='horiz'?[fv[0]<0?-1:1,0]:[0,fv[1]<0?-1:1];
s+='<line x1="'+B[0].toFixed(1)+'" y1="'+B[1].toFixed(1)+'" x2="'+(B[0]+u[0]*44).toFixed(1)+'" y2="'+(B[1]+u[1]*44).toFixed(1)+'" stroke="#888" stroke-dasharray="4 3"/>';
const lv=nrm([u[0]+fv[0],u[1]+fv[1]]);
s+='<text x="'+(B[0]+lv[0]*58-10).toFixed(1)+'" y="'+(B[1]+lv[1]*58+5).toFixed(1)+'" fill="#555">25°</text>';
return s+'</svg>'}"""
G = {'tri': TRI, 'ci': 'Math.floor(cip)', 'mir': 'mp<0.5?0:1',
     'opts': "(()=>{const a=[];const ks=['swap','horiz','rev'];let j=0;for(let k=0;k<4;k++)a.push(k===ci?tri('ok',mir):tri(ks[j++],mir));return a})()",
     'o0': 'opts[0]', 'o1': 'opts[1]', 'o2': 'opts[2]', 'o3': 'opts[3]'}
PARAMS = {'cip': [0, 3.99], 'mp': [0, 0.999]}
TEXT = ('<b>(b)(ii)</b> Which diagram shows the vector triangle for the three forces (weight <i>W</i>, <i>F</i> and <i>R</i>) acting on the tree? '
        'The weight is 270 kg × 9.81 N kg⁻¹, the force <i>F</i> is 1800 N at 25° to the vertical, and the diagrams are drawn to scale. '
        'The tree is in equilibrium, so the forces must form a closed triangle drawn tip to tail.')
MODEL = ('A closed, tip-to-tail triangle drawn to scale: W = 270 × 9.81 = 2648 N downwards; F = 1800 N at 25° to the vertical, starting at the tip of W; '
         'R drawn from the end of F back to the start of W, closing the triangle (R ≈ 1270 N).')
EXPL = ('In equilibrium the resultant force is zero, so the three forces drawn tip to tail form a closed triangle. Start with W (2648 N, downwards), add F (1800 N, '
        '25° from the vertical) at its tip, then R is the vector that returns to the start. Wrong options swap the lengths of W and F, measure the 25° from the horizontal, '
        'or draw R pointing the wrong way round the triangle.')
def main(i, o):
    rows = list(csv.reader(open(i, encoding='utf-8', newline='')))
    h = rows[0]; c = {n: k for k, n in enumerate(h) if n}
    idx = [n for n, r in enumerate(rows) if len(r) > 1 and r[c['id']] == '9702_s25_p22_q2']
    assert len(idx) == 4, idx
    r0, r2 = rows[idx[0]], rows[idx[2]]
    assert r0[c['partIndex']] == '0' and r2[c['partIndex']] == '2' and r2[c['partText']].startswith('(b)(ii)'), (r0[c['partIndex']], r2[c['partText']][:10])
    pad = lambda r: r + [''] * (len(h) - len(r))
    r0 = pad(r0); r2 = pad(r2)
    assert not r0[c['params']] and not r0[c['computedValues']]
    r0[c['params']] = json.dumps(PARAMS); r0[c['computedValues']] = json.dumps(G, ensure_ascii=False)
    r2[c['partText']] = TEXT; r2[c['modelAnswer']] = MODEL; r2[c['explanation']] = EXPL; r2[c['type']] = 'imageChoice'
    for k in ('A_keywords', 'M_keywords'): r2[c[k]] = ''
    r2[c['answerType']] = 'imageChoice'; r2[c['imageOptions']] = '["${o0}","${o1}","${o2}","${o3}"]'
    r2[c['correctImageIndex']] = '${ci}'; r2[c['imageChoiceMarks']] = '2'
    rows[idx[0]] = r0; rows[idx[2]] = r2
    csv.writer(open(o, 'w', encoding='utf-8', newline='')).writerows(rows)
    json.dump({'row_p0': idx[0] + 1, 'row_p2': idx[2] + 1, 'p0': {'params': r0[c['params']], 'computedValues': r0[c['computedValues']]},
               'p2': {k: r2[c[k]] for k in ('type', 'partText', 'modelAnswer', 'explanation', 'A_keywords', 'M_keywords', 'answerType', 'imageOptions', 'correctImageIndex', 'imageChoiceMarks')}},
              open(o + '.edits.json', 'w', encoding='utf-8'), ensure_ascii=False)
if __name__ == '__main__': main(sys.argv[1], sys.argv[2])
