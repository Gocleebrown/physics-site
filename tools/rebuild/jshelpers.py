# JS helper functions stored in computedValues (G). Single quotes only inside the JS.
SCI = "(x,d)=>{const p=x.toExponential(d).split('e');return p[0]+' × 10<sup>'+(+p[1])+'</sup>'}"

GSVG = r"""(o)=>{const W=o.W||520,H=o.H||380,L=64,B=50,T=14,R=18,pw=W-L-R,ph=H-T-B;
const sx=v=>L+(v-o.x0)/(o.x1-o.x0)*pw,sy=v=>T+ph-(v-o.y0)/(o.y1-o.y0)*ph;
const f=v=>String(+v.toPrecision(6));
let s='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 '+W+' '+H+'" style="max-width:'+W+'px;width:100%;background:#fff;display:block;margin:10px 0;border:1px solid #ccc" font-family="Arial,sans-serif" font-size="13">';
for(let i=0;i*o.mx<=o.x1-o.x0+1e-9;i++){const x=sx(o.x0+i*o.mx);s+='<line x1="'+x+'" y1="'+T+'" x2="'+x+'" y2="'+(T+ph)+'" stroke="#e8b4b4" stroke-width="0.6"/>';}
for(let i=0;i*o.my<=o.y1-o.y0+1e-9;i++){const y=sy(o.y0+i*o.my);s+='<line x1="'+L+'" y1="'+y+'" x2="'+(L+pw)+'" y2="'+y+'" stroke="#e8b4b4" stroke-width="0.6"/>';}
for(let i=0;i*o.Mx<=o.x1-o.x0+1e-9;i++){const v=o.x0+i*o.Mx,x=sx(v);s+='<line x1="'+x+'" y1="'+T+'" x2="'+x+'" y2="'+(T+ph)+'" stroke="#c97878" stroke-width="1.2"/><text x="'+x+'" y="'+(T+ph+18)+'" text-anchor="middle">'+f(v)+'</text>';}
for(let i=0;i*o.My<=o.y1-o.y0+1e-9;i++){const v=o.y0+i*o.My,y=sy(v);s+='<line x1="'+L+'" y1="'+y+'" x2="'+(L+pw)+'" y2="'+y+'" stroke="#c97878" stroke-width="1.2"/><text x="'+(L-8)+'" y="'+(y+4)+'" text-anchor="end">'+f(v)+'</text>';}
s+='<rect x="'+L+'" y="'+T+'" width="'+pw+'" height="'+ph+'" fill="none" stroke="#000" stroke-width="1.2"/>';
s+='<polyline fill="none" stroke="#000" stroke-width="1.8" points="'+o.pts.map(p=>sx(p[0]).toFixed(1)+','+sy(p[1]).toFixed(1)).join(' ')+'"/>';
s+='<text x="'+(L+pw/2)+'" y="'+(H-8)+'" text-anchor="middle">'+o.xl+'</text>';
s+='<text transform="translate(14,'+(T+ph/2)+') rotate(-90)" text-anchor="middle">'+o.yl+'</text></svg>';
return s+'<p style="text-align:center;margin:0 0 10px"><b>'+o.cap+'</b></p>';}"""

# Figure 3.1: transverse wave on a string PQ, with 2 dimension arrows. labels: twoLam (peak to peak 3rd), pp (peak-to-trough)
WAVE31 = r"""(a,b)=>{const W=520,H=230,cy=130,A=55,lam=150,x0=118;
const X=u=>x0+(u+0.25)*lam,Y=u=>cy-A*Math.cos(2*Math.PI*u);
let pts=[];for(let u=-0.25;u<=2.2501;u+=0.02)pts.push(X(u).toFixed(1)+','+Y(u).toFixed(1));
let s='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 '+W+' '+H+'" style="max-width:'+W+'px;width:100%;background:#fff;display:block;margin:10px 0" font-family="Arial,sans-serif" font-size="14">';
s+='<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker></defs>';
s+='<polyline fill="none" stroke="#000" stroke-width="2" points="'+pts.join(' ')+'"/>';
s+='<line x1="'+X(0)+'" y1="'+(cy-A)+'" x2="'+X(0)+'" y2="34" stroke="#000" stroke-dasharray="4,3"/><line x1="'+X(2)+'" y1="'+(cy-A)+'" x2="'+X(2)+'" y2="34" stroke="#000" stroke-dasharray="4,3"/>';
s+='<line x1="'+X(0)+'" y1="40" x2="'+X(2)+'" y2="40" stroke="#000" marker-start="url(#ar)" marker-end="url(#ar)"/><text x="'+((X(0)+X(2))/2)+'" y="30" text-anchor="middle">'+a+' cm</text>';
s+='<line x1="'+(X(0)-85)+'" y1="'+(cy-A)+'" x2="'+X(0)+'" y2="'+(cy-A)+'" stroke="#000" stroke-dasharray="4,3"/><line x1="'+(X(0)-85)+'" y1="'+(cy+A)+'" x2="'+X(0.5)+'" y2="'+(cy+A)+'" stroke="#000" stroke-dasharray="4,3"/>';
s+='<line x1="'+(X(0)-70)+'" y1="'+(cy-A)+'" x2="'+(X(0)-70)+'" y2="'+(cy+A)+'" stroke="#000" marker-start="url(#ar)" marker-end="url(#ar)"/><text x="'+(X(0)-77)+'" y="'+(cy+4)+'" text-anchor="end">'+b+' cm</text>';
s+='<text x="'+(X(-0.25)-10)+'" y="'+(cy+22)+'" text-anchor="end">P</text><text x="'+(X(2.25)+8)+'" y="'+(cy+22)+'">Q</text>';
s+='<circle cx="'+X(0.75)+'" cy="'+cy+'" r="4.5" fill="#000"/><text x="'+(X(0.75)+9)+'" y="'+(cy-8)+'">X</text>';
s+='<text x="'+(W-14)+'" y="'+(H-16)+'" text-anchor="end">not to scale</text></svg>';
return s+'<p style="text-align:center;margin:0 0 10px"><b>Figure 3.1</b></p>';}"""

# ======================= AS 26-22 figure helpers =======================
HDR_SVG = "'<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 '+W+' '+H+'\" style=\"max-width:'+W+'px;width:100%;background:#fff;display:block;margin:10px 0\" font-family=\"Arial,sans-serif\" font-size=\"14\">'"
ARROWDEF = "'<defs><marker id=\"ah\" viewBox=\"0 0 10 10\" refX=\"9\" refY=\"5\" markerWidth=\"7\" markerHeight=\"7\" orient=\"auto-start-reverse\"><path d=\"M0,0 L10,5 L0,10 z\" fill=\"#000\"/></marker></defs>'"

# Figure 2.1 (plank, ropes, block) with the two masses as labels
FIG21 = r"""(mb,mp)=>{const W=520,H=330;
let s=""" + HDR_SVG + "+" + ARROWDEF + r""";
const ln=(a,b,c,d,x)=>'<line x1="'+a+'" y1="'+b+'" x2="'+c+'" y2="'+d+'" stroke="#000" stroke-width="'+(x||1.6)+'"/>';
const dl=(a,b,c,d)=>'<line x1="'+a+'" y1="'+b+'" x2="'+c+'" y2="'+d+'" stroke="#000" stroke-dasharray="4,3"/>';
s+=ln(90,270,430,270,3);
s+='<rect x="238" y="228" width="44" height="42" rx="4" fill="#bbb" stroke="#000"/>';
s+='<circle cx="205" cy="70" r="14" fill="#bbb" stroke="#000"/><circle cx="315" cy="70" r="14" fill="#bbb" stroke="#000"/>';
s+=ln(260,228,212,83)+ln(260,228,308,83)+ln(90,270,192,66)+ln(430,270,328,66);
s+=dl(90,270,90,215)+dl(430,270,430,215)+dl(260,228,260,150);
s+='<text x="102" y="244">&#952;</text><text x="408" y="244">&#952;</text><text x="244" y="180">&#952;</text><text x="266" y="180">&#952;</text>';
s+='<text x="260" y="26" text-anchor="middle">pulleys</text>'+ln(260,31,212,56,1)+ln(260,31,308,56,1);
s+='<text x="118" y="120" text-anchor="end">rope</text>'+ln(122,118,153,142,1);
s+='<text x="90" y="300">plank, mass '+mb2+' kg</text>';
s+='<text x="290" y="300">block, mass '+mb+' kg</text>'+ln(270,268,280,284,1);
s+='<text x="'+(W-14)+'" y="60" text-anchor="end">not to scale</text></svg>';
return s+'<p style="text-align:center;margin:0 0 10px"><b>Figure 2.1</b></p>';}"""
FIG21 = FIG21.replace('mb2','mp')

# Figure 2.2 (force diagrams) - symbols only
FIG22 = r"""()=>{const W=520,H=290;
let s=""" + HDR_SVG + "+" + ARROWDEF + r""";
const ar=(a,b,c,d)=>'<line x1="'+a+'" y1="'+b+'" x2="'+c+'" y2="'+d+'" stroke="#000" stroke-width="1.6" marker-end="url(#ah)"/>';
const dl=(a,b,c,d)=>'<line x1="'+a+'" y1="'+b+'" x2="'+c+'" y2="'+d+'" stroke="#000" stroke-dasharray="4,3"/>';
s+='<line x1="40" y1="190" x2="200" y2="190" stroke="#000" stroke-width="3"/>';
s+=ar(40,190,62,140)+ar(200,190,178,140)+dl(40,190,40,138)+dl(200,190,200,138);
s+='<text x="26" y="136">T</text><text x="206" y="136">T</text><text x="46" y="162">&#952;</text><text x="186" y="162">&#952;</text>';
s+=ar(120,138,120,186)+'<text x="128" y="152">R</text>'+ar(120,190,120,262)+'<text x="128" y="262">W<tspan font-size="11" dy="4">P</tspan></text>';
s+='<text x="60" y="226">plank</text>';
s+='<rect x="330" y="170" width="46" height="44" rx="4" fill="#bbb" stroke="#000"/>';
s+=ar(353,170,327,112)+ar(353,170,379,112)+ar(353,170,353,106)+dl(353,170,353,118);
s+='<text x="312" y="108">T</text><text x="384" y="108">T</text><text x="358" y="98">R</text><text x="336" y="140">&#952;</text><text x="362" y="140">&#952;</text>';
s+=ar(353,214,353,262)+'<text x="360" y="262">W<tspan font-size="11" dy="4">B</tspan></text>';
s+='<text x="400" y="200">block</text>';
s+='<text x="'+(W-14)+'" y="60" text-anchor="end">not to scale</text></svg>';
return s+'<p style="text-align:center;margin:0 0 10px"><b>Figure 2.2</b></p>';}"""

# Figure 3.1: two sets of semicircular wavefronts from dippers A and B; P at a crest/crest point
FIG31 = r"""()=>{const W=620,H=290,cy=205,ax=230,bx=420,lam=48;
let s=""" + HDR_SVG + r""";
const arc=(cx,r,d)=>'<path d="M'+(cx-r)+','+cy+' A'+r+','+r+' 0 0 1 '+(cx+r)+','+cy+'" fill="none" stroke="#000" stroke-width="1.4"'+(d?' stroke-dasharray="6,5"':'')+'/>';
for(let m=1;m<=7;m++){const r=m*lam/2,d=(m%2===1);s+=arc(ax,r,d)+arc(bx,r,d);}
s+='<line x1="30" y1="'+cy+'" x2="600" y2="'+cy+'" stroke="#000" stroke-width="1.6"/>';
[ax,bx].forEach(x=>{s+='<circle cx="'+x+'" cy="'+(cy+2)+'" r="9" fill="#888"/><rect x="'+(x-4)+'" y="'+(cy+2)+'" width="8" height="26" fill="#888"/><circle cx="'+x+'" cy="'+(cy-1)+'" r="2.2" fill="#000"/>';});
const hl='stroke="#fff" stroke-width="4" paint-order="stroke"';s+='<text x="'+(ax-18)+'" y="'+(cy+22)+'" text-anchor="end" '+hl+'>A</text><text x="'+(bx+18)+'" y="'+(cy+22)+'" '+hl+'>B</text>';
const d=bx-ax,dA=3*lam,dB=2*lam,px=ax+(dA*dA-dB*dB+d*d)/(2*d),py=cy-Math.sqrt(dA*dA-Math.pow((dA*dA-dB*dB+d*d)/(2*d),2));
s+='<circle cx="'+px+'" cy="'+py+'" r="3"/><text x="'+(px-7)+'" y="'+(py-7)+'" text-anchor="end" '+hl+'>P</text>';
s+='<text x="325" y="272" text-anchor="middle">dippers</text><line x1="300" y1="258" x2="'+(ax+4)+'" y2="'+(cy+26)+'" stroke="#000"/><line x1="350" y1="258" x2="'+(bx-4)+'" y2="'+(cy+26)+'" stroke="#000"/>';
s+='<line x1="470" y1="24" x2="520" y2="24" stroke="#000" stroke-width="1.4"/><text x="528" y="28">crest</text><line x1="470" y1="46" x2="520" y2="46" stroke="#000" stroke-dasharray="6,5"/><text x="528" y="50">trough</text>';
s+='<text x="'+(W-14)+'" y="'+(H-8)+'" text-anchor="end">not to scale</text></svg>';
return s+'<p style="text-align:center;margin:0 0 10px"><b>Figure 3.1</b></p>';}"""

# Figure 5.1: three resistors in parallel
FIG51 = r"""()=>{const W=440,H=250;
let s=""" + HDR_SVG + "+" + ARROWDEF + r""";
const ln=(a,b,c,d)=>'<line x1="'+a+'" y1="'+b+'" x2="'+c+'" y2="'+d+'" stroke="#000" stroke-width="1.6"/>';
const ys=[70,130,190];
s+='<line x1="130" y1="22" x2="340" y2="22" stroke="#000" marker-start="url(#ah)" marker-end="url(#ah)"/><text x="235" y="16" text-anchor="middle" font-style="italic">V</text>';
s+=ln(130,70,130,190)+ln(340,70,340,190)+ln(340,130,420,130)+ln(50,130,130,130);
const sub=['1','2','3'];
ys.forEach((y,i)=>{s+=ln(130,y,195,y)+ln(275,y,340,y)+'<rect x="195" y="'+(y-12)+'" width="80" height="24" fill="#fff" stroke="#000" stroke-width="1.6"/>';
 s+='<text x="235" y="'+(y+38)+'" text-anchor="middle" font-style="italic">R<tspan font-size="11" dy="4">'+sub[i]+'</tspan></text>';
 s+='<text x="150" y="'+(y-10)+'" font-style="italic">I<tspan font-size="11" dy="4">'+sub[i]+'</tspan></text><polyline points="166,'+(y-6)+' 178,'+y+' 166,'+(y+6)+'" fill="none" stroke="#000" stroke-width="1.4"/>';});
s+='<circle cx="130" cy="130" r="3.5"/><circle cx="340" cy="130" r="3.5"/>';
s+='<text x="62" y="120" font-style="italic">I<tspan font-size="11" dy="4">T</tspan></text><polyline points="94,124 106,130 94,136" fill="none" stroke="#000" stroke-width="1.4"/>';
s+='</svg>';
return s+'<p style="text-align:center;margin:0 0 10px"><b>Figure 5.1</b></p>';}"""

# Figures 5.2 / 5.3: battery with two parallel resistance wires; X (a light sensitive component) in one branch when withX
CKT = r"""(E,I,withX)=>{const W=480,H=290;
let s=""" + HDR_SVG + "+" + ARROWDEF + r""";
const ln=(a,b,c,d,w)=>'<line x1="'+a+'" y1="'+b+'" x2="'+c+'" y2="'+d+'" stroke="#000" stroke-width="'+(w||1.6)+'"/>';
s+=ln(60,60,222,60)+ln(268,60,420,60)+ln(60,60,60,230)+ln(420,60,420,230);
s+=ln(222,42,222,78)+ln(232,50,232,70)+ln(246,50,246,70)+ln(256,42,256,78)+ln(268,60,256,60)+ln(222,60,232,60);
s+='<line x1="236" y1="60" x2="244" y2="60" stroke="#000" stroke-dasharray="3,3"/><text x="240" y="30" text-anchor="middle">'+E+' V</text>';
if(I){s+='<line x1="130" y1="60" x2="80" y2="60" stroke="#000" stroke-width="1.6" marker-end="url(#ah)"/><text x="84" y="84">'+I+' A</text>';}
s+=ln(60,140,420,140)+ln(60,230,420,230);
s+=ln(110,140,240,140,5)+ln(110,230,240,230,5);
s+='<circle cx="60" cy="140" r="3.5"/><circle cx="110" cy="140" r="3.5"/><circle cx="240" cy="140" r="3.5"/><circle cx="110" cy="230" r="3.5"/><circle cx="240" cy="230" r="3.5"/><circle cx="420" cy="140" r="3.5"/>';
s+='<text x="262" y="190">resistance wires</text>'+ln(260,182,200,146,1)+ln(260,196,200,226,1);
if(withX){s+='<rect x="320" y="127" width="62" height="26" fill="#fff" stroke="#000" stroke-width="1.6"/><text x="351" y="176" text-anchor="middle">X</text>';
 s+='<line x1="316" y1="102" x2="330" y2="118" stroke="#000" stroke-width="1.4" marker-end="url(#ah)"/><line x1="332" y1="98" x2="346" y2="114" stroke="#000" stroke-width="1.4" marker-end="url(#ah)"/>';}
s+='</svg>';
return s+'<p style="text-align:center;margin:0 0 10px"><b>Figure '+(withX?'5.3':'5.2')+'</b></p>';}"""
