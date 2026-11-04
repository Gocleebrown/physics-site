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
