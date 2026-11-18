##v1
"""Fixes for the missing items in 9702_w25_p41 (Q6, Q7) and 9702_s25_p41 (Q4, Q5), 19 Nov 2026.
 - row 32  (9702-25-41-Q6 p0)  : modelAnswer filled from the table's own cell answers
 - row 37  (9702-25-41-Q7 p1)  : generated aircraft figure (two views, numbers from the question) inline in the part text; dead imageBelowMain cleared
 - row 70  (9702-25-41S-Q4 p2) : modelAnswer + explanation
 - rows 71/74 (9702-25-41S-Q5) : static E_k-labelled option files replaced by four generated E_p-vs-h sketches (correct position random)
Usage: python3 patch_41papers.py in.csv out.csv"""
import csv, json, sys
csv.field_size_limit(10**9)
FIG71 = r"""(B,L)=>{const W=520,H=250;
let s='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 '+W+' '+H+'" style="max-width:520px;width:100%;font-family:Arial,sans-serif;font-size:13px"><rect width="'+W+'" height="'+H+'" fill="#fff"/>';
s+='<defs><marker id="a71" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker></defs>';
const ln=(a,b,c,d,x)=>'<line x1="'+a+'" y1="'+b+'" x2="'+c+'" y2="'+d+'" stroke="#000" stroke-width="1.4"'+(x||'')+'/>';
s+='<text x="60" y="22" font-weight="bold">View from the side</text><text x="330" y="22" font-weight="bold">View from above</text>';
s+='<ellipse cx="110" cy="150" rx="72" ry="13" fill="#ddd" stroke="#000"/><polygon points="40,150 18,122 34,122 62,146" fill="#ddd" stroke="#000"/>';
s+='<polygon points="105,152 132,176 142,176 126,150" fill="#bbb" stroke="#000"/>';
s+=ln(110,50,110,112,' marker-end="url(#a71)"')+'<text x="118" y="68">vertical component of</text><text x="118" y="84">Earth\'s magnetic field</text><text x="118" y="100">'+B+' µT</text>';
s+=ln(40,214,110,214,' marker-end="url(#a71)"')+'<text x="40" y="236"><tspan font-style="italic">v</tspan></text>';
s+='<ellipse cx="400" cy="130" rx="11" ry="62" fill="#ddd" stroke="#000"/><polygon points="392,118 330,60 322,60 328,150 392,146" fill="#ddd" stroke="#000" transform="translate(0,0)"/><polygon points="408,118 470,60 478,60 472,150 408,146" fill="#ddd" stroke="#000"/>';
s+='<circle cx="324" cy="60" r="3"/><circle cx="476" cy="60" r="3"/><text x="305" y="55">P</text><text x="482" y="55">Q</text>';
s+=ln(327,34,473,34,' marker-start="url(#a71)" marker-end="url(#a71)"')+'<text x="400" y="52" text-anchor="middle">'+L+' m</text>';
s+=ln(400,236,400,196,' marker-end="url(#a71)"')+'<text x="408" y="226"><tspan font-style="italic">v</tspan></text>';
return s+'</svg>'}"""
EPFIG = r"""(kind,hmin,hmax,ET)=>{const W=300,H=250,x0=52,x1=270,yt=40,yb=200;
let s='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 '+W+' '+H+'" width="'+W+'" height="'+H+'" font-family="Arial,sans-serif" font-size="12"><rect width="'+W+'" height="'+H+'" fill="#fff"/>';
s+='<line x1="'+x0+'" y1="'+(yt-12)+'" x2="'+x0+'" y2="'+yb+'" stroke="#000" stroke-width="1.5"/><line x1="'+x0+'" y1="'+yb+'" x2="'+(x1+10)+'" y2="'+yb+'" stroke="#000" stroke-width="1.5"/>';
s+='<text x="6" y="'+(yt-16)+'">Eₚ / J</text><text x="'+(x1-6)+'" y="'+(yb+40)+'">h / m</text>';
s+='<text x="'+(x0-12)+'" y="'+(yb+4)+'" text-anchor="end">0</text><text x="'+(x0-6)+'" y="'+(yt+4)+'" text-anchor="end">'+ET.toFixed(1)+'</text><line x1="'+(x0-3)+'" y1="'+yt+'" x2="'+x0+'" y2="'+yt+'" stroke="#000"/>';
s+='<text x="'+x0+'" y="'+(yb+16)+'" text-anchor="middle">'+hmin.toFixed(2)+'</text><text x="'+x1+'" y="'+(yb+16)+'" text-anchor="middle">'+hmax.toFixed(2)+'</text>';
let d='';const n=40;
for(let i=0;i<=n;i++){const u=i/n,x=x0+u*(x1-x0),t=2*u-1;let f;
 if(kind==='ok')f=t*t;else if(kind==='ek')f=1-t*t;else if(kind==='offset')f=0.3+0.7*t*t;else f=u;
 d+=(i?'L':'M')+x.toFixed(1)+','+(yb-f*(yb-yt)).toFixed(1);}
return s+'<path d="'+d+'" fill="none" stroke="#000" stroke-width="2.4"/></svg>'}"""
EP_PARTS = {'epfig': EPFIG, 'ci': 'Math.floor(cip)',
  'opts': "(()=>{const a=[];const ks=['ek','offset','line'];let j=0;for(let k=0;k<4;k++)a.push(k===ci?epfig('ok',h_min,h_max,totalE):epfig(ks[j++],h_min,h_max,totalE));return a})()",
  'o0': 'opts[0]', 'o1': 'opts[1]', 'o2': 'opts[2]', 'o3': 'opts[3]'}
M32 = 'Series: Q_S = Q_1 = Q_2 (the same charge on each capacitor) and V_S = V_1 + V_2 (the p.d.s add). Parallel: Q_S = Q_1 + Q_2 (the charges add) and V_S = V_1 = V_2 (the same p.d. across each capacitor).'
M70 = 'Compression: work done on gas +W, increase in internal energy +2U. Cooling at constant volume: work done on gas 0, increase in internal energy −U.'
V70 = 'For an ideal gas the internal energy is proportional to the thermodynamic temperature, so U ∝ T. Compression takes T to 3T, so the internal energy rises from U to 3U, an increase of 2U. Cooling at constant volume does no work (the volume does not change), so the work done on the gas is 0. Cooling from 3T to 2T takes the internal energy from 3U to 2U, an increase of −U (it decreases by U).'
M74 = 'A U-shaped (parabolic) curve: E_p is zero at the equilibrium position (where all the energy is kinetic) and rises to the total energy at both ends of the oscillation. It is the mirror image of the E_k graph.'
V74 = 'The total energy is constant, so E_p = E_total − E_k. E_k is a maximum at equilibrium and zero at the ends, so E_p is zero at equilibrium and E_total at both extremes: a U-shaped curve whose minimum touches zero. The inverted curve is E_k, the curve with a non-zero minimum would mean energy is lost or gained, and a straight line does not match a simple harmonic oscillation.'
def main(i, o):
    rows = list(csv.reader(open(i, encoding='utf-8', newline='')))
    h = rows[0]; c = {n: k for k, n in enumerate(h) if n}
    pad = lambda r: r + [''] * (len(h) - len(r))
    def get(n, qid, pi):
        r = pad(rows[n - 1]); assert r[c['id']] == qid and r[c['partIndex']] == str(pi), (n, r[c['id']], r[c['partIndex']]); rows[n - 1] = r; return r
    r = get(32, '9702-25-41-Q6', 0); assert not r[c['modelAnswer']]; r[c['modelAnswer']] = M32
    r = get(37, '9702-25-41-Q7', 1)
    g = json.loads(r[c['computedValues']]); assert list(g) == ['flux_Wb']
    g['fig71'] = FIG71; g['f71'] = 'fig71(B_uT,wingspan_m)'
    r[c['computedValues']] = json.dumps(g, ensure_ascii=False)
    assert r[c['partText']].rstrip().endswith('with your answer.')
    r[c['partText']] = r[c['partText']].rstrip() + '<div style="margin-top:.8em">${f71}<p style="text-align:center;margin:0"><b>Figure 7.1</b> (not to scale)</p></div>'
    assert r[c['imageBelowMain']] == 'fig7_1_context.svg'; r[c['imageBelowMain']] = ''
    r = get(70, '9702-25-41S-Q4', 2); assert not r[c['modelAnswer']] and not r[c['explanation']]
    r[c['modelAnswer']] = M70; r[c['explanation']] = V70
    r = get(71, '9702-25-41S-Q5', 0)
    g = json.loads(r[c['computedValues']]); assert 'epfig' not in g; g.update(EP_PARTS)
    r[c['computedValues']] = json.dumps(g, ensure_ascii=False)
    p = json.loads(r[c['params']]); assert 'cip' not in p; p['cip'] = [0, 3.99]; r[c['params']] = json.dumps(p)
    r = get(74, '9702-25-41S-Q5', 3); assert r[c['imageOptions']].startswith('["p2fig5_4_choice_0.svg"')
    r[c['imageOptions']] = '["${o0}","${o1}","${o2}","${o3}"]'; r[c['correctImageIndex']] = '${ci}'
    r[c['modelAnswer']] = M74; r[c['explanation']] = V74
    csv.writer(open(o, 'w', encoding='utf-8', newline='')).writerows(rows)
if __name__ == '__main__': main(sys.argv[1], sys.argv[2])
