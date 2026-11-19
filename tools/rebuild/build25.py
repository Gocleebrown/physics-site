##v1
"""Make the fixed-number s25 p22 / p23 questions dynamic (20 Nov 2026).
Every number that can vary becomes a parameter (ranges include the paper's own value), every figure is generated from the parameters,
and keywords / model answers / explanations use the same variables.  Paper-value check: tools/rebuild/tpaper25.js
Usage: python3 build25.py in.csv out.csv"""
import csv, json, sys
csv.field_size_limit(10**9)

HELP = {  # shared tiny helpers (JS source), merged into G of every id that needs them
 'us': "(n)=>String(n).replace(/-/g,'⁻').replace(/[0-9]/g,d=>'⁰¹²³⁴⁵⁶⁷⁸⁹'[d])",
 'sb': "(n)=>String(n).replace(/[0-9]/g,d=>'₀₁₂₃₄₅₆₇₈₉'[d])",
 'ex': "(x,d)=>x.toExponential(d).replace('e+','e')",
 'sci': "(x,d)=>{const p=x.toExponential(d).split('e');return p[0]+' × 10'+us(+p[1])}",
 'sp': "(n)=>String(Math.round(n)).replace(/\\B(?=(\\d{3})+(?!\\d))/g,' ')",
}
AX = r"""const W=440,H=270,L=58,R=18,T=16,B=48,pw=W-L-R,ph=H-T-B;"""
WAVEFIG = r"""(aX,aY,lam)=>{const W=440,H=270,L=58,R=18,T=16,B=48,pw=W-L-R,ph=H-T-B,ym=aY*1.18,xm=2*lam;
const sx=v=>L+v/xm*pw,sy=v=>T+ph/2-v/ym*ph/2;
let s='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 '+W+' '+H+'" style="max-width:440px;width:100%;font-family:Arial,sans-serif;font-size:12px"><rect width="'+W+'" height="'+H+'" fill="#fff"/>';
for(const v of [-aY,-aX,aX,aY])s+='<line x1="'+L+'" x2="'+(W-R)+'" y1="'+sy(v).toFixed(1)+'" y2="'+sy(v).toFixed(1)+'" stroke="#ddd"/>';
s+='<line x1="'+L+'" x2="'+L+'" y1="'+T+'" y2="'+(T+ph)+'" stroke="#000"/><line x1="'+L+'" x2="'+(W-R)+'" y1="'+sy(0).toFixed(1)+'" y2="'+sy(0).toFixed(1)+'" stroke="#000"/>';
for(const v of [-aY,-aX,0,aX,aY])s+='<text x="'+(L-6)+'" y="'+(sy(v)+4).toFixed(1)+'" text-anchor="end">'+v+'</text>';
for(let i=0;i<=4;i++){const v=i*lam/2;s+='<line x1="'+sx(v).toFixed(1)+'" x2="'+sx(v).toFixed(1)+'" y1="'+(sy(0)-4).toFixed(1)+'" y2="'+(sy(0)+4).toFixed(1)+'" stroke="#000"/><text x="'+sx(v).toFixed(1)+'" y="'+(T+ph+16)+'" text-anchor="middle">'+(+v.toFixed(3))+'</text>';}
s+='<text x="'+(L+pw/2)+'" y="'+(H-8)+'" text-anchor="middle">distance from A / m</text><text transform="translate(14,'+(T+ph/2)+') rotate(-90)" text-anchor="middle">displacement / cm</text>';
const pt=(k)=>{let d='';for(let i=0;i<=160;i++){const x=i/160*xm;d+=(i?'L':'M')+sx(x).toFixed(1)+','+sy(k*Math.sin(2*Math.PI*x/lam)).toFixed(1)}return d};
s+='<path d="'+pt(aX)+'" fill="none" stroke="#000" stroke-width="2"/><path d="'+pt(-aY)+'" fill="none" stroke="#000" stroke-width="2" stroke-dasharray="6 4"/>';
s+='<text x="'+(sx(lam/4)+6).toFixed(1)+'" y="'+(sy(aX)-6).toFixed(1)+'" font-weight="bold">X</text><text x="'+(sx(lam/4)+6).toFixed(1)+'" y="'+(sy(-aY)+16).toFixed(1)+'" font-weight="bold">Y</text>';
return s+'</svg>'}"""
FXFIG = r"""(k)=>{const W=420,H=300,L=64,R=18,T=14,B=48,pw=W-L-R,ph=H-T-B,xm=5,Fm=k*xm*1e-3,ym=Math.ceil(Fm/100)*100,st=ym>500?200:100;
const sx=v=>L+v/xm*pw,sy=v=>T+ph-v/ym*ph;
let s='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 '+W+' '+H+'" style="max-width:420px;width:100%;font-family:Arial,sans-serif;font-size:12px"><rect width="'+W+'" height="'+H+'" fill="#fff"/>';
for(let v=0;v<=xm;v++)s+='<line x1="'+sx(v)+'" x2="'+sx(v)+'" y1="'+T+'" y2="'+(T+ph)+'" stroke="#e3e3e3"/><text x="'+sx(v)+'" y="'+(T+ph+16)+'" text-anchor="middle">'+v+'</text>';
for(let v=0;v<=ym;v+=st)s+='<line x1="'+L+'" x2="'+(W-R)+'" y1="'+sy(v).toFixed(1)+'" y2="'+sy(v).toFixed(1)+'" stroke="#e3e3e3"/><text x="'+(L-6)+'" y="'+(sy(v)+4).toFixed(1)+'" text-anchor="end">'+v+'</text>';
s+='<line x1="'+L+'" x2="'+L+'" y1="'+T+'" y2="'+(T+ph)+'" stroke="#000"/><line x1="'+L+'" x2="'+(W-R)+'" y1="'+(T+ph)+'" y2="'+(T+ph)+'" stroke="#000"/>';
s+='<text x="'+(L+pw/2)+'" y="'+(H-8)+'" text-anchor="middle">extension / 10⁻³ m</text><text transform="translate(14,'+(T+ph/2)+') rotate(-90)" text-anchor="middle">force / N</text>';
return s+'<line x1="'+sx(0)+'" y1="'+sy(0)+'" x2="'+sx(xm)+'" y2="'+sy(Fm).toFixed(1)+'" stroke="#000" stroke-width="2"/></svg>'}"""
TRI = r"""(kind,mir,Wt,F,thd)=>{const W=300,H=250;
const th=thd*Math.PI/180,m=mir?-1:1;
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
s+='<text x="'+(B[0]+lv[0]*58-10).toFixed(1)+'" y="'+(B[1]+lv[1]*58+5).toFixed(1)+'" fill="#555">'+thd+'°</text>';
return s+'</svg>'}"""

def hel(*names): return {n: HELP[n] for n in names}
SPEC = {}   # id -> {'params':{}, 'G':{}, 'parts':{idx:{col:val}}}

# ---------------------------------------------------------------- p22 Q2 (tree and post)
SPEC['9702_s25_p22_q2'] = dict(
 params={"cip": [0, 3.99], "mp": [0, 0.999], "mp_": [200, 350], "d1p": [1.0, 1.4], "d2p": [1.4, 1.8], "thp": [18, 32], "pkp": [110, 190]},
 G=dict(tri=TRI, ci="Math.floor(cip)", mir="mp<0.5?0:1",
  m="Math.round(mp_/5)*5", d1="Math.round(d1p*10)/10", d2="Math.round(d2p*10)/10",
  Wt="m*9.81", Mom="Wt*d1", F="Math.round(Mom*Math.cos(thp*Math.PI/180)/d2/10)*10",
  cosv="F*d2/Mom", theta="Math.round(Math.acos(cosv)*180/Math.PI)", pk="Math.round(pkp/10)*10", Area="F/(pk*1000)",
  R_="Math.hypot(Wt-F*Math.cos(theta*Math.PI/180),F*Math.sin(theta*Math.PI/180))",
  opts="(()=>{const a=[];const ks=['swap','horiz','rev'];let j=0;for(let k=0;k<4;k++)a.push(k===ci?tri('ok',mir,Wt,F,theta):tri(ks[j++],mir,Wt,F,theta));return a})()",
  o0="opts[0]", o1="opts[1]", o2="opts[2]", o3="opts[3]"),
 parts={
  1: dict(
   partText="(b) A tree of mass ${m} kg grows out of sloping ground and is supported by a post. The ground applies a total force R on the tree at point Q. The centre of gravity of the tree is a horizontal distance of ${d1.toFixed(1)} m from Q. The post applies a force F = ${F} N perpendicular to the line PQ, through point P at angle θ to the vertical. P is ${d2.toFixed(1)} m (horizontal) from Q. The tree is in equilibrium.\n\n(b)(i) By taking moments about point Q, show that θ is ${theta}°.",
   B_keywords="${m} × 9.81 × ${d1.toFixed(1)}|moment of weight|Mg × ${d1.toFixed(1)}|weight moment",
   B2_keywords="${F} × ${d2.toFixed(1)}/cosθ|${d2.toFixed(1)}/cos|moment of post force",
   B3_keywords="θ = ${theta}|${theta} degrees|cos = ${cosv.toFixed(3)}",
   modelAnswer="Moment of weight about Q = ${m} × 9.81 × ${d1.toFixed(1)} = ${Mom.toFixed(0)} N m (anticlockwise).\nPerpendicular distance from Q to line of action of F = ${d2.toFixed(1)}/cosθ.\nMoment of F = ${F} × ${d2.toFixed(1)}/cosθ (clockwise).\nEquilibrium: ${F} × ${d2.toFixed(1)}/cosθ = ${Mom.toFixed(0)} → cosθ = ${cosv.toFixed(3)} → θ = ${theta}°.",
   explanation="Take moments about Q so the unknown force R has no moment. The weight acts ${d1.toFixed(1)} m horizontally from Q, giving an anticlockwise moment. F is perpendicular to PQ, so its perpendicular distance from Q is ${d2.toFixed(1)}/cosθ. In equilibrium, clockwise moment = anticlockwise moment, so ${F} × ${d2.toFixed(1)}/cosθ = ${m} × 9.81 × ${d1.toFixed(1)}. This gives cosθ = ${cosv.toFixed(3)} and θ = ${theta}°."),
  2: dict(
   partText="<b>(b)(ii)</b> Which diagram shows the vector triangle for the three forces (weight <i>W</i>, <i>F</i> and <i>R</i>) acting on the tree? The weight is ${m} kg × 9.81 N kg⁻¹, the force <i>F</i> is ${F} N at ${theta}° to the vertical, and the diagrams are drawn to scale. The tree is in equilibrium, so the forces must form a closed triangle drawn tip to tail.",
   modelAnswer="A closed, tip-to-tail triangle drawn to scale: W = ${m} × 9.81 = ${Wt.toFixed(0)} N downwards; F = ${F} N at ${theta}° to the vertical, starting at the tip of W; R drawn from the end of F back to the start of W, closing the triangle (R ≈ ${R_.toFixed(0)} N).",
   explanation="In equilibrium the resultant force is zero, so the three forces drawn tip to tail form a closed triangle. Start with W (${Wt.toFixed(0)} N, downwards), add F (${F} N, ${theta}° from the vertical) at its tip, then R is the vector that returns to the start. Wrong options swap the lengths of W and F, measure the ${theta}° from the horizontal, or draw R pointing the wrong way round the triangle."),
  3: dict(
   partText="(b)(iii) The tree exerts a pressure of ${pk} kPa on the top of the post.\nDetermine the surface area of the tree in contact with the post.",
   A_keywords="${Area.toPrecision(2)}|${Area.toPrecision(3)}|${ex(Area,1)}|${sci(Area,1)}",
   C1_keywords="A = F/p|area = force / pressure|p = F/A",
   modelAnswer="A = F/p = ${F}/(${pk} × 10³) = ${Area.toPrecision(2)} m²",
   explanation="Pressure is force divided by area, p = F/A, so the area is A = F/p. Use the force of ${F} N and convert ${pk} kPa to ${pk} × 10³ Pa before dividing."),
 })
# (p0 of Q2 is unchanged: definition of moment)

# ---------------------------------------------------------------- p22 Q3 (two water waves)
SPEC['9702_s25_p22_q3'] = dict(
 params={"aXp": [8, 12], "aYp": [15, 25], "lamp": [0.30, 0.60], "fp": [12, 20]},
 G=dict(wavefig=WAVEFIG, aX="Math.round(aXp)", aY="Math.round(aYp)", lam="Math.round(lamp*100)/100", f="Math.round(fp)",
  v="f*lam", vS3="+(v).toPrecision(3)", vS2="+(v).toPrecision(2)", res="aY-aX", ratio="(aX/aY)*(aX/aY)", fig="wavefig(aX,aY,lam)"),
 parts={
  0: dict(
   mainText="Two progressive water waves X and Y travel from point A to point B. Wave X has amplitude ${aX} cm and wavelength ${lam.toFixed(2)} m. Wave Y has amplitude ${aY} cm and the same wavelength, but is 180° out of phase with X. Fig. 3.1 shows the displacement of both waves against distance from A.<div style=\"margin-top:.8em\">${fig}<p style=\"margin:0;text-align:center\"><b>Fig. 3.1</b> &nbsp; X solid line, Y dashed line</p></div>",
   imageBelowMain="",
   A_keywords="${aX}|${aX}.0", modelAnswer="${aX} cm",
   explanation="Amplitude is the maximum displacement from the equilibrium (zero) position. Read the peak height of wave X from the graph."),
  1: dict(
   partText="(b)(i) Both waves have frequency ${f} Hz. Determine the speed of wave X.",
   A_keywords="${vS3}|${vS2}", C1_keywords="v = fλ|v = f × λ|speed = frequency × wavelength",
   modelAnswer="Wavelength λ = ${lam.toFixed(2)} m (from graph). v = fλ = ${f} × ${lam.toFixed(2)} = ${vS3} m s⁻¹",
   explanation="Wave speed is v = fλ. Read one full wavelength of wave X from the horizontal axis of the graph (${lam.toFixed(2)} m), then multiply by the frequency of ${f} Hz."),
  2: dict(
   partText="(b)(ii) State and explain whether X and Y are coherent.",
   modelAnswer="Yes, X and Y are coherent. They have a constant phase difference (of 180°/π), so they are coherent."),
  3: dict(
   partText="(c) Wave X and wave Y superpose to form a resultant wave. Describe the shape of the resultant wave displacement against distance.",
   B_keywords="amplitude ${res}|${res} cm|amplitude of ${res}",
   modelAnswer="The resultant wave has amplitude ${res} cm (= ${aY} − ${aX} cm, since the waves are antiphase) and wavelength ${lam.toFixed(2)} m. The resultant is a negative sine wave: where wave X has positive displacement, the resultant has negative displacement.",
   explanation="Superposition: add the displacements of X and Y at each point. The waves are in antiphase, so the displacements have opposite signs and the resultant amplitude is the difference, ${aY} − ${aX} = ${res} cm. The wavelength is unchanged. Wave Y is larger, so the resultant follows the shape of Y (opposite in sign to X)."),
  4: dict(
   partText="(d) The intensity of wave X is I_X. The intensity of wave Y is I_Y.\nUse Fig. 3.1 to determine the ratio I_X / I_Y.",
   A_keywords="${+ratio.toPrecision(2)}|${+ratio.toPrecision(3)}|${aX*aX}/${aY*aY}|${aX}/${aY} squared",
   modelAnswer="I ∝ A². I_X/I_Y = A_X²/A_Y² = ${aX}²/${aY}² = ${aX*aX}/${aY*aY} = ${+ratio.toPrecision(2)}",
   explanation="Intensity is proportional to the amplitude squared, I ∝ A². So I_X/I_Y = (A_X/A_Y)² = (${aX}/${aY})² = ${+ratio.toPrecision(2)}. Read both amplitudes from Fig. 3.1."),
 })

# ---------------------------------------------------------------- p22 Q5 (wire, force-extension graph)
SPEC['9702_s25_p22_q5'] = dict(
 params={"Lp": [0.60, 1.00], "Ep": [80, 120], "kp": [1.0, 1.6], "x1p": [1.5, 2.4], "x2p": [2.6, 3.5]},
 G=dict(fxfig=FXFIG, L="Math.round(Lp*100)/100", E="Math.round(Ep/5)*5", kk="Math.round(kp*100)/100", k="kk*1e5",
  x1="Math.round(x1p*10)/10", x2="Math.round(x2p*10)/10", Fr="Math.round(k*4e-3)",
  Area="k*L/(E*1e9)", W="0.5*k*((x2*1e-3)*(x2*1e-3)-(x1*1e-3)*(x1*1e-3))", fig="fxfig(k)"),
 parts={
  0: dict(
   mainText="A wire of unstretched length ${L.toFixed(2)} m is made of a metal with Young modulus ${E} GPa. The wire obeys Hooke's law and has a constant cross-sectional area. Fig. 5.1 shows the force–extension graph for the wire.<div style=\"margin-top:.8em\">${fig}<p style=\"margin:0;text-align:center\"><b>Fig. 5.1</b></p></div>",
   imageBelowMain=""),
  1: dict(
   A_keywords="${ex(Area,1)}|${ex(Area,2)}|${sci(Area,1)}",
   C1_keywords="k = F/x (gradient from graph)|gradient = ${kk} × 10⁵ N/m|A = kL/E",
   modelAnswer="From graph: at F = ${Fr} N, x = 4.0 × 10⁻³ m → k = ${Fr}/(4.0 × 10⁻³) = ${kk} × 10⁵ N m⁻¹.\nA = kL/E = (${kk} × 10⁵ × ${L.toFixed(2)})/(${E} × 10⁹) = ${sci(Area,1)} m²",
   explanation="The graph is a straight line, so the force constant is k = F/x, read from a point on the line (for example ${Fr} N at 4.0 × 10⁻³ m). Young modulus E = stress/strain = (F/A)/(x/L) = kL/A. Rearranging gives A = kL/E. Use L = ${L.toFixed(2)} m and E = ${E} GPa = ${E} × 10⁹ Pa."),
  2: dict(
   partText="(b)(ii) The extension of the wire is initially ${x1.toFixed(1)} × 10⁻³ m. Determine the work done to increase the extension of the wire to ${x2.toFixed(1)} × 10⁻³ m.",
   A_keywords="${W.toFixed(2)}|${W.toPrecision(4)}|${W.toPrecision(3)}",
   modelAnswer="ΔW = ½k(x₂² − x₁²) = ½ × ${kk} × 10⁵ × ((${x2.toFixed(1)} × 10⁻³)² − (${x1.toFixed(1)} × 10⁻³)²)\n= ½ × ${kk} × 10⁵ × ${sci((x2*x2-x1*x1)*1e-6,1)} = ${W.toFixed(2)} J",
   explanation="The work done stretching a wire equals the area under the force–extension graph, W = ½Fx = ½kx² for a wire obeying Hooke's law. The extra work between the two extensions is ½k(x₂² − x₁²) = ${W.toFixed(2)} J. Use the same k found from the graph in part (b)(i)."),
 })

# ---------------------------------------------------------------- p22 Q7 (beta-minus emitters)
EL = "[[14,6,'carbon','nitrogen','N'],[3,1,'hydrogen','helium','He'],[32,15,'phosphorus','sulfur','S'],[35,16,'sulfur','chlorine','Cl'],[60,27,'cobalt','nickel','Ni'],[90,38,'strontium','yttrium','Y']]"
SPEC['9702_s25_p22_q7'] = dict(
 params={"ip": [0, 5.99]},
 G=dict(EL=EL, ii="Math.floor(ip)", A="EL[ii][0]", Z="EL[ii][1]", nm0="EL[ii][2]", nm1="EL[ii][3]", sy="EL[ii][4]",
  ratio="+(Z*1.60e-19/(A*1.66e-27)).toPrecision(2)", rS="sci(ratio,1)", pcalc="ratio*A*1.66e-27/1.60e-19", pS="pcalc.toFixed(2)"),
 parts={
  1: dict(
   partText="<div style=\"margin-bottom:.5em\">A nucleus X has ${A} nucleons and p protons. The ratio of charge to mass for nucleus X is ${rS} C kg⁻¹.</div>(b)(i) Determine p, the number of protons in nucleus X.",
   A_keywords="${Z}",
   C2_keywords="charge/mass = pe/(${A}u)|charge = pe|mass = ${A}u",
   C1_keywords="p = (${rS} \u00d7 ${A} \u00d7 1.66 \u00d7 10\u207b\u00b2\u2077)/(1.60 \u00d7 10\u207b\u00b9\u2079)",
   modelAnswer="charge/mass = pe/(${A}u). p = (${rS} × ${A} × 1.66 × 10⁻²⁷)/(1.60 × 10⁻¹⁹) = ${pS} ≈ ${Z}.",
   explanation="The specific charge of the nucleus is charge/mass = pe/(${A}u), where p is the number of protons and u is the atomic mass unit. Rearrange to find p = (specific charge × ${A}u)/e = ${pS}. The answer must be a whole number, so round to the nearest integer, ${Z}."),
  2: dict(
   partText="(b)(ii) Nucleus X undergoes β⁻ decay to form nucleus Z. Complete the nuclear equation: ${us(A)}${sb(Z)}X → Z + ... + ...",
   B_keywords="${nm1}|${us(A)}${sb(Z+1)}Z|${Z+1}|atomic number ${Z+1}|proton number ${Z+1}",
   modelAnswer="${us(A)}${sb(Z)}X → ${us(A)}${sb(Z+1)}Z + ⁰₋₁e + v̄ₑ.  Z is ${nm1}-${A} (${sy}, proton number ${Z+1}, nucleon number ${A}).",
   explanation="In β⁻ decay a neutron changes into a proton, so the proton number increases by 1 (${Z} → ${Z+1}) and the nucleon number stays ${A}. An electron and an electron antineutrino are emitted. Check that charge and nucleon number balance on both sides of the equation."),
 })

# ---------------------------------------------------------------- p23 Q1 (two falling objects)
SPEC['9702_s25_p23_q1'] = dict(
 params={"Hp": [8, 12], "up": [2.0, 4.0]},
 G=dict(H="Math.round(Hp*2)/2", u="Math.round(up*2)/2", v2="2*u", t="Math.sqrt(2*H/9.81)", h="H-u*t", hS="h.toFixed(1)", hS2="h.toFixed(2)"),
 parts={
  0: dict(mainText="Object A: released from rest at height ${H.toFixed(1)} m. Object B: released from height h with initial upward velocity ${u.toFixed(1)} m s⁻¹. Both reach the ground at the same time. Air resistance is negligible."),
  1: dict(
   A_keywords="${hS}|${hS2}|${(h-0.1).toFixed(1)}|${(h+0.01).toFixed(2)}",
   C2_keywords="s = ut + ½at²|kinematics for A|t for A from s = ½at²|t = √(2×${H.toFixed(1)}/9.81)|t = ${t.toFixed(2)} s",
   C1_keywords="h = −${u.toFixed(1)}×t + ½×9.81×t²|s = ut + ½at² for B|h = ${H.toFixed(1)} − ${u.toFixed(1)}t",
   modelAnswer="For A: ${H.toFixed(1)} = ½ × 9.81 × t² → t = √(2×${H.toFixed(1)}/9.81) = ${t.toFixed(2)} s.\nFor B: h = −(${u.toFixed(1)} × ${t.toFixed(2)}) + ½ × 9.81 × ${t.toFixed(2)}² = −${(u*t).toFixed(2)} + ${(0.5*9.81*t*t).toFixed(1)} = ${hS} m",
   explanation="Both objects accelerate downwards at g, so they share the same time of flight. Find the time for A from s = ½gt² (it starts from rest): t = ${t.toFixed(2)} s. Then use the same time for B, taking upwards as positive: its displacement is ut − ½gt², which must equal minus its starting height. Rearranging gives a start height of ${hS} m. Watch the signs: the initial velocity is upwards but the displacement to the ground is downwards."),
  2: dict(
   partText="<div style=\"margin-bottom:.5em\">In a second experiment, object B is released from the same height h (from part b) but with speed ${v2.toFixed(1)} m s⁻¹ at 60° to the vertical.</div>(c)(i) State and explain whether the time taken for object B to reach the ground is less than, the same as, or greater than in the first experiment.",
   B2_keywords="vertical component of velocity is the same|vertical component is ${u.toFixed(1)} m s⁻¹|${v2.toFixed(1)} × cos 60° = ${u.toFixed(1)}|initial vertical velocity unchanged|vertical component same",
   modelAnswer="Same. The vertical component of the initial velocity = ${v2.toFixed(1)} × cos 60° = ${u.toFixed(1)} m s⁻¹ (upward), which is the same as in part (b). Since vertical motion determines the time of flight and air resistance is negligible, the time taken is the same."),
  3: dict(
   B2_keywords="total initial energy greater|more initial kinetic energy|KE is greater|initial KE greater|change in gravitational PE is same|${v2.toFixed(1)} > ${u.toFixed(1)}",
   modelAnswer="Greater. The total initial energy (KE + GPE) is greater in this experiment since ½m(${v2.toFixed(1)})² > ½m(${u.toFixed(1)})². The change in gravitational PE is the same (same height). By conservation of energy, the final KE (and speed) must be greater."),
 })

# ---------------------------------------------------------------- p23 Q2 (beam, pivot, wire)
SPEC['9702_s25_p23_q2'] = dict(
 params={"Lbp": [8, 10], "mAp": [70, 110], "mCp": [130, 170], "xBp": [2.0, 3.0], "dp": [1.4, 2.2], "ep": [0.9, 1.5]},
 G=dict(Lb="Math.round(Lbp*2)/2", hf="Lb/2", mA="Math.round(mAp/5)*5", mC="Math.round(mCp/5)*5", xB="Math.round(xBp*2)/2",
  mB="(mC-mA)*hf/xB", mBr="Math.round(mB)", Tw="mA*9.81", dd="Math.round(dp*10)/10", eps="Math.round(ep*10)/10",
  Aw="Math.PI*(dd*1e-3/2)*(dd*1e-3/2)", Ew="Tw/(Aw*eps*1e-3)", mom1="mC*9.81*hf", mom2="mA*9.81*hf"),
 parts={
  0: dict(mainText="A beam of length ${Lb.toFixed(1)} m is in equilibrium on a pivot at its midpoint. Object A (${mA} kg) at one end, B (mass m) ${xB.toFixed(1)} m from pivot, C (${mC} kg) at the other end."),
  1: dict(
   A_keywords="${mB.toPrecision(2)}|${mB.toPrecision(3)}|${mBr}",
   C2_keywords="taking moments about pivot|moments equation|clockwise = anticlockwise|${mC}×9.81×${hf} or ${mA}×9.81×${hf}",
   C1_keywords="${mC}×9.81×${hf} = ${mA}×9.81×${hf} + m×9.81×${xB.toFixed(1)}|moment equation set up",
   modelAnswer="Pivot at midpoint, so A and C are each ${hf} m from pivot; B is ${xB.toFixed(1)} m from pivot.\nTaking moments about pivot (A and B on same side):\n${mC} × 9.81 × ${hf} = ${mA} × 9.81 × ${hf} + m × 9.81 × ${xB.toFixed(1)}\n${(mC*hf).toFixed(1)} = ${(mA*hf).toFixed(1)} + ${xB.toFixed(1)}m → m = ${mB.toPrecision(3)} kg",
   explanation="The beam is in equilibrium, so the clockwise moments equal the anticlockwise moments about the pivot. The pivot is at the midpoint, so the end masses are each ${hf} m away. Write the moments for each object (the g values cancel): ${mC} × ${hf} = ${mA} × ${hf} + m × ${xB.toFixed(1)}. Rearranging gives m = ${mB.toPrecision(3)} kg."),
  2: dict(
   partText="(b)(ii) Object A is removed and replaced by a wire fixed to the end of the beam and to the ground. The beam is again horizontal and in equilibrium (B and C positions unchanged). The wire has diameter ${sci(dd*1e-3,1)} m and strain ${sci(eps*1e-3,1)}. The wire is not extended beyond its limit of proportionality.\nCalculate the Young modulus of the wire.",
   A_keywords="${ex(Ew,1)}|${sci(Ew,1).replace(' ','')}",
   C1_keywords="A = π(d/2)²|A = π × (${(dd/2).toFixed(2)} × 10⁻³)²|cross-sectional area of wire|A = ${sci(Aw,1)} m²",
   modelAnswer="From moments: wire tension T = ${mA} × 9.81 = ${Tw.toFixed(0)} N (same as weight of A).\nA = π(d/2)² = π × (${(dd/2).toFixed(2)} × 10⁻³)² = ${sci(Aw,3)} m².\nE = F/(Aε) = ${Tw.toFixed(0)} / (${sci(Aw,3)} × ${sci(eps*1e-3,1)}) = ${sci(Ew,1)} Pa",
   explanation="Young modulus E = stress/strain, where stress = force/area. The wire takes the place of object A, so the tension equals the force that A's weight exerted, ${mA} × 9.81 = ${Tw.toFixed(0)} N. The cross-sectional area is a circle, A = π(d/2)², using the radius (half the diameter), which gives ${sci(Aw,3)} m². Then E = F/(A × strain) = ${sci(Ew,1)} Pa. A common error is to use the diameter instead of the radius."),
 })

# ---------------------------------------------------------------- p23 Q3 (car on a slope)
SPEC['9702_s25_p23_q3'] = dict(
 params={"mp": [1200, 1800], "vp": [20, 35], "thp": [4, 8], "Fp": [1200, 2000]},
 G=dict(m="Math.round(mp/50)*50", v="Math.round(vp)", th="Math.round(thp*2)/2", Fr="Math.round(Fp/100)*100",
  dh="v*Math.sin(th*Math.PI/180)", dE="m*9.81*dh", dEs="Math.round(+dE.toPrecision(2))", Pr="Fr*v", Pt="Pr+dEs", PtS="+Pt.toPrecision(2)"),
 parts={
  0: dict(mainText="A car of mass ${m} kg travelling at constant velocity v on a horizontal road. Total resistive force F."),
  1: dict(
   partText="<div style=\"margin-bottom:.5em\">The car moves up a slope at constant speed ${v} m s⁻¹. Slope at angle ${th.toFixed(1)}° to horizontal. Total resistive force is ${Fr} N.</div>(b)(i) Show that the increase in gravitational potential energy of the car in a time of 1.0 s is ${sp(dEs)} J.",
   B_keywords="ΔEP = mgΔh|mgΔh|${sp(dEs)}",
   B2_keywords="${m} × 9.81 × ${dh.toFixed(3)}|${sp(dEs)} J|sin ${th.toFixed(1)}°",
   modelAnswer="Distance travelled in 1.0 s = ${v} m.\nIncrease in height Δh = ${v} × sin ${th.toFixed(1)}° = ${dh.toFixed(3)} m.\nΔEP = mgΔh = ${m} × 9.81 × ${dh.toFixed(3)} = ${sp(dEs)} J (2 s.f.)",
   explanation="In 1.0 s the car travels a distance equal to its speed, ${v} m. On a slope of angle θ the height gained is distance × sinθ = ${dh.toFixed(3)} m, not distance × cosθ. Then the gain in gravitational potential energy is mgΔh = ${sp(dEs)} J. Because this is the energy gained in 1.0 s, it is also the power needed to lift the car, in watts."),
  2: dict(
   A_keywords="${ex(PtS,1)}|${Pt}|${sci(PtS,1).replace(' ','')}",
   C1_keywords="P_resist = Fv = ${Fr} × ${v}|power against resistive forces|P = Fv",
   modelAnswer="Power to overcome resistive forces = Fv = ${Fr} × ${v} = ${sp(Pr)} W.\nPower to increase GPE = ${sp(dEs)} J/s = ${sp(dEs)} W.\nTotal power = ${sp(Pr)} + ${sp(dEs)} = ${sp(Pt)} W = ${sci(PtS,1)} W",
   explanation="The engine has two jobs when climbing at constant speed. It must overcome the resistive forces (power = Fv = ${sp(Pr)} W) and it must increase the car's gravitational potential energy each second (${sp(dEs)} W). These two powers add to give ${sp(Pt)} W. The kinetic energy is constant, so no power goes into speeding up."),
  3: dict(partText="<div style=\"margin-bottom:.5em\">The car picks up a passenger and continues up the slope at the same speed.</div>(c)(i) State and explain the effect, if any, that the passenger has on the air resistance acting on the car."),
 })

# ---------------------------------------------------------------- p23 Q5 (polarisation)
SPEC['9702_s25_p23_q5'] = dict(
 params={"alp": [10, 40]},
 G=dict(al="Math.round(alp)", ang="90-al", cf="Math.cos(ang*Math.PI/180)", c2="cf*cf"),
 parts={
  2: dict(
   partText="(b)(ii) The amplitude of the incident wave is A₀ when intensity is I₀. Use Malus's law to determine, in terms of A₀, the amplitude of the transmitted wave when α = ${al}°.",
   A_keywords="${cf.toFixed(2)}|${cf.toFixed(2)} A₀|${cf.toFixed(3)}",
   C1_keywords="θ = ${ang}°|angle between filter and plane of polarisation is ${ang}°|90° − ${al}° = ${ang}°",
   modelAnswer="At α = ${al}°, the angle between the filter axis and the plane of polarisation = 90° − ${al}° = ${ang}°.\nBy Malus's law: I = I₀ cos²(${ang}°) = I₀ × ${c2.toFixed(3)}.\nSince I ∝ A²: amplitude = A₀ × √(${c2.toFixed(3)}) = A₀ × cos(${ang}°) = ${cf.toFixed(2)} A₀",
   explanation="Malus's law, I = I₀cos²θ, uses the angle θ between the plane of polarisation and the filter's axis. The filter starts perpendicular to the wave's polarisation, so at a rotation of ${al}° this angle is 90° − ${al}° = ${ang}°. Intensity is proportional to amplitude squared, so the amplitude is A₀ cos${ang}° = ${cf.toFixed(2)} A₀. Take the square root of the intensity factor to get the amplitude factor."),
 })

# ---------------------------------------------------------------- p23 Q6 (diffraction grating)
SPEC['9702_s25_p23_q6'] = dict(
 params={"lp": [600, 750], "angp": [40, 60]},
 G=dict(lam="Math.round(lp/30)*30", ang="Math.round(angp)", th="ang/2", f="3.00e8/(lam*1e-9)", d="2*lam*1e-9/Math.sin(th*Math.PI/180)", lines="1/d", lam3="2*lam/3"),
 parts={
  0: dict(mainText="Diffraction grating. Light of wavelength ${lam} nm in vacuum. Angle between second-order maxima = ${ang}°."),
  1: dict(
   A_keywords="${ex(f,1)}|${ex(f,2)}",
   C1_keywords="v = fλ|f = c/λ|f = 3.00×10⁸/λ",
   modelAnswer="f = c/λ = 3.00×10⁸ / (${lam}×10⁻⁹) = ${sci(f,1)} Hz",
   explanation="The wave equation c = fλ applies to light in a vacuum. Convert the wavelength from nm to m (×10⁻⁹) and divide the speed of light by it: f = ${sci(f,2)} Hz."),
  2: dict(
   A_keywords="${ex(lines,1)}|${ex(lines,2)}",
   C1_keywords="θ = ${th}°|half of ${ang}°|d = 2×${lam}×10⁻⁹/sin${th}°",
   modelAnswer="Second-order maxima at θ = ${ang}°/2 = ${th}° from centre.\nd sin θ = nλ: d = 2 × ${lam}×10⁻⁹ / sin ${th}° = ${2*lam}×10⁻⁹ / ${Math.sin(th*Math.PI/180).toFixed(3)} = ${sci(d,2)} m.\nLines per m = 1/d = 1/(${sci(d,2)}) = ${sci(lines,1)} m⁻¹",
   explanation="The ${ang}° is the angle between the two second-order maxima on opposite sides of the centre, so the angle of each from the central axis is half of that, ${th}°. The grating equation is d sinθ = nλ with n = 2. The number of lines per metre is the reciprocal of the slit spacing d. A common error is to use ${ang}° directly in the grating equation."),
  3: dict(
   partText="(b)(iii) The light is now replaced with light of wavelength λ. The third-order maxima of this light coincide with the second-order maxima of the original ${lam} nm light. Calculate λ in nm.",
   A_keywords="${Math.round(lam3)}",
   C1_keywords="3λ = 2×${lam}|nλ = same|third-order at same angle as second-order|dsinθ = 3λ = 2×${lam}",
   modelAnswer="d sin θ = 3λ = 2×${lam} → 3λ = ${2*lam} → λ = ${Math.round(lam3)} nm",
   explanation="The two maxima coincide at the same angle, so d sinθ is the same for both. For the original light d sinθ = 2 × ${lam} nm and for the new light d sinθ = 3λ. Equating these gives 3λ = ${2*lam} nm, so λ = ${Math.round(lam3)} nm. Neither d nor the angle is needed, because they cancel."),
 })

# ---------------------------------------------------------------- apply
def main(i, o):
    rows = list(csv.reader(open(i, encoding='utf-8', newline='')))
    h = rows[0]; c = {n: k for k, n in enumerate(h) if n}
    log = {}
    for n, r in enumerate(rows):
        if n == 0 or len(r) <= c['partIndex'] or r[c['id']] not in SPEC: continue
        r += [''] * (len(h) - len(r)); rows[n] = r
        sp = SPEC[r[c['id']]]; pi = int(r[c['partIndex']])
        if pi == 0:
            old = json.loads(r[c['params']] or '{}'); oldg = json.loads(r[c['computedValues']] or '{}')
            assert r[c['id']] == '9702_s25_p22_q2' or (not old and not oldg), r[c['id']]
            r[c['params']] = json.dumps(sp['params'], ensure_ascii=False)
            G = {}; G.update(hel('us', 'sb', 'ex', 'sci', 'sp')); G.update(sp['G'])
            r[c['computedValues']] = json.dumps(G, ensure_ascii=False)
        for col, val in sp['parts'].get(pi, {}).items():
            r[c[col]] = val
        log.setdefault(r[c['id']], []).append(n + 1)
    assert set(log) == set(SPEC), set(SPEC) - set(log)
    csv.writer(open(o, 'w', encoding='utf-8', newline='')).writerows(rows)
    json.dump(log, open(o + '.rows.json', 'w'))
if __name__ == '__main__': main(sys.argv[1], sys.argv[2])
