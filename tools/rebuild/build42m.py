##v1  A2 9702/42 Feb/Mar 2026 (m26) -- rebuilt from the real QP + MS.  python3 build42m.py <startRow>
import json, sys, os
sys.path.insert(0,'.')
from rowlib import *
from jshelpers import *

LV='A2'; PAPER='9702_m26_p42'; ID='9702-26-42M'
def lab(s): return '<b>'+s+'</b> '
def kwv(*alts):
    out=[]
    for a in alts:
        out.append(a)
        if '-' in a:
            out.append(a.replace('-','−')); out.append(a.replace('-','–'))
    return '|'.join(dict.fromkeys(out))
def delta(*alts):  # accept both Greek delta and the increment sign
    out=[]
    for a in alts:
        out.append(a)
        if 'Δ' in a: out.append(a.replace('Δ','∆'))
    return '|'.join(dict.fromkeys(out))
ALL=[]
SF="(x,n)=>String(+x.toPrecision(n))"
EX="(x,d)=>x.toExponential(d).replace('e+','e')"
NICE="(x)=>{const e=Math.pow(10,Math.floor(Math.log10(x))),m=x/e;const c=[1,1.2,1.5,2,2.5,3,4,5,6,8,10].find(k=>k>=m-1e-9);return c*e;}"

HD="'<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 '+W+' '+H+'\" style=\"max-width:'+W+'px;width:100%;background:#fff;display:block;margin:10px 0\" font-family=\"Arial,sans-serif\" font-size=\"14\">'"
AH="'<defs><marker id=\"ah\" viewBox=\"0 0 10 10\" refX=\"9\" refY=\"5\" markerWidth=\"7\" markerHeight=\"7\" orient=\"auto-start-reverse\"><path d=\"M0,0 L10,5 L0,10 z\" fill=\"#000\"/></marker></defs>'"
LNF="const ln=(a,b,c,d,x)=>'<line x1=\"'+a+'\" y1=\"'+b+'\" x2=\"'+c+'\" y2=\"'+d+'\" stroke=\"#000\" stroke-width=\"1.4\"'+(x||'')+'/>';"
def js(s):
    return s.replace('@HD@',HD).replace('@AH@',AH).replace('@LN@',LNF)
CAPL="return s+'<p style=\"text-align:center;margin:0 0 10px\"><b>Figure '+tag+'</b></p>';"
# bare option SVG header (no style, fixed size) for generated answer sketches
OPT="'<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 '+W+' '+H+'\" width=\"'+W+'\" height=\"'+H+'\" font-family=\"Arial,sans-serif\" font-size=\"13\"><rect width=\"'+W+'\" height=\"'+H+'\" fill=\"#fff\"/>'"
def jso(s):
    return js(s).replace('@OPT@',OPT)

# ---------------------------------------------------------------- figures
# Figure 1.1: roundabout seen from above (X on the edge, Y at 2R, Z at R)
FIG11 = js(r"""(v)=>{const W=520,H=420,cx=260,cy=215,R=165,tag='1.1';
let s=@HD@+@AH@;
@LN@
const P=(deg,r)=>[cx+r*Math.cos(deg*Math.PI/180),cy+r*Math.sin(deg*Math.PI/180)];
s+='<circle cx="'+cx+'" cy="'+cy+'" r="'+R+'" fill="#fff" stroke="#000" stroke-width="1.6"/><circle cx="'+cx+'" cy="'+cy+'" r="8" fill="#fff" stroke="#000"/>';
const X=P(35,R),Y=P(-42,R*2/3),Z=P(-150,R/3);
const dx=P(35,R),ex=P(215,0);
s+=ln(cx,cy,dx[0],dx[1])+ln(cx,cy,P(-42,R)[0],P(-42,R)[1])+ln(cx,cy,P(-150,R)[0],P(-150,R)[1]);
s+='<circle cx="'+X[0]+'" cy="'+X[1]+'" r="4"/><text x="'+(X[0]-18)+'" y="'+(X[1]+6)+'">X</text>';
s+='<circle cx="'+Y[0]+'" cy="'+Y[1]+'" r="4"/><text x="'+(Y[0]+8)+'" y="'+(Y[1]+4)+'">Y</text>';
s+='<circle cx="'+Z[0]+'" cy="'+Z[1]+'" r="4"/><text x="'+(Z[0]-16)+'" y="'+(Z[1]+4)+'">Z</text>';
const tx=X[0]+Math.sin(35*Math.PI/180)*55,ty=X[1]-Math.cos(35*Math.PI/180)*55;
s+=ln(X[0],X[1],tx,ty,' marker-end="url(#ah)" stroke-width="1.8"')+'<text x="'+(tx+6)+'" y="'+(ty+14)+'">'+v+' m s<tspan font-size="10" dy="-5">−1</tspan></text>';
s+='<path d="M215,30 Q260,12 305,30" fill="none" stroke="#000" marker-start="url(#ah)"/><text x="236" y="16" font-size="13">rotation</text>';
const mY=P(-42,R/3);
s+='<text x="'+(mY[0]+4)+'" y="'+(mY[1]-6)+'" font-style="italic">2R</text>';
const mZ=P(-150,R/6);
s+='<text x="'+(mZ[0]-8)+'" y="'+(mZ[1]+18)+'" font-style="italic">R</text>';
s+=ln(cx-30,cy,cx-30,cy+R,' marker-start="url(#ah)" marker-end="url(#ah)"')+'<text x="'+(cx-24)+'" y="'+(cy+R/2)+'" font-style="italic">3R</text>';
s+='</svg>';
""" + CAPL + "}")

# Figure 6.1 (frame) and 6.2 (view from above); dimensions come from the parameters
FIGFRAME = js(r"""(hh,ww)=>{const W=420,H=330,tag='6.1';
let s=@HD@;
@LN@
s+='<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker></defs>';
s+=ln(150,28,172,52,' stroke-width="1.2"')+ln(194,28,172,52,' stroke-width="1.2"')+ln(172,52,150,52,'')+ln(172,52,194,52,'');
s+='<polyline points="150,52 150,60 150,60" fill="none" stroke="#000"/>';
s+='<rect x="150" y="60" width="100" height="190" fill="none" stroke="#000" stroke-width="2.4"/><rect x="192" y="55" width="16" height="10" fill="#fff" stroke="none"/>';
s+='<text x="193" y="80">X Y</text>'+ln(200,84,200,250,' stroke-dasharray="4,3"');
s+=ln(150,52,175,52,' stroke-width="1.2"')+ln(175,52,175,60,' stroke-width="1.2"')+ln(225,52,225,60,' stroke-width="1.2"');
s+='<text x="228" y="30">thin cotton thread</text>'+ln(226,34,196,46,'');
s+='<text x="20" y="150">wire frame</text>'+ln(70,153,150,168,'')+'<text x="10" y="236">vertical axis</text>'+ln(82,232,198,226,'');
s+=ln(265,60,285,60,' stroke-dasharray="4,3"')+ln(265,250,285,250,' stroke-dasharray="4,3"')+ln(278,60,278,250,' marker-start="url(#ah)" marker-end="url(#ah)"')+'<text x="288" y="160">'+hh+' cm</text>';
s+=ln(150,255,150,278,' stroke-dasharray="4,3"')+ln(250,255,250,278,' stroke-dasharray="4,3"')+ln(150,272,250,272,' marker-start="url(#ah)" marker-end="url(#ah)"')+'<text x="178" y="292">'+ww+' cm</text>';
s+='</svg>';
""" + CAPL + "}")
FIGTOP = js(r"""()=>{const W=420,H=140,tag='6.2';
let s=@HD@;
@LN@
s+='<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker></defs>';
s+=ln(110,70,330,70,' stroke-dasharray="4,3"')+'<line x1="140" y1="95" x2="300" y2="45" stroke="#000" stroke-width="3"/><line x1="140" y1="45" x2="300" y2="95" stroke="#000" stroke-width="2" stroke-dasharray="6,4"/>';
s+='<path d="M335,48 C348,60 348,80 335,92" fill="none" stroke="#000" marker-start="url(#ah)" marker-end="url(#ah)"/><text x="352" y="74" font-style="italic">s</text>';
s+='<text x="20" y="128">equilibrium position</text>'+ln(150,118,190,72,'');
s+='</svg>';
""" + CAPL + "}")

# 2(b)(i): four field lines between the plates; kind ok / rev / slant / uneven
PLATES = jso(r"""(up,kind)=>{const W=300,H=250;
let s=@OPT@;
const lx=70,rx=230,yt=55,yb=195;
s+='<rect x="'+lx+'" y="'+(yt-5)+'" width="'+(rx-lx)+'" height="6" fill="#444"/><rect x="'+lx+'" y="'+(yb-1)+'" width="'+(rx-lx)+'" height="6" fill="#444"/>';
s+='<line x1="150" y1="'+(yt-5)+'" x2="150" y2="20" stroke="#000"/><line x1="150" y1="'+(yb+5)+'" x2="150" y2="228" stroke="#000"/>';
s+='<text x="156" y="26">'+(up?'−':'+')+'</text><text x="156" y="232">'+(up?'+':'−')+'</text>';
const dn=!up; // field direction: from the higher potential plate to the lower one
let xs=[100,133,167,200];
let lines=[];
for(let i=0;i<4;i++){
 let x0=xs[i],x1=xs[i];
 if(kind==='slant'){x1=x0+34;}
 if(kind==='uneven'){x0=x1=[84,98,112,126][i];}
 const yS=dn?yt+1:yb-1,yE=dn?yb-1:yt+1;
 let a=up!==(kind==='rev')? [x0,yb-1,x1,yt+1] : [x0,yt+1,x1,yb-1];
 lines.push(a);
}
lines.forEach(a=>{s+='<line x1="'+a[0]+'" y1="'+a[1]+'" x2="'+a[2]+'" y2="'+a[3]+'" stroke="#000" stroke-width="1.6"/>';
 const mx=(a[0]+a[2])/2,my=(a[1]+a[3])/2,ux=a[2]-a[0],uy=a[3]-a[1],L=Math.hypot(ux,uy),nx=ux/L,ny=uy/L;
 s+='<polygon points="'+(mx+nx*7)+','+(my+ny*7)+' '+(mx-nx*4+ny*4)+','+(my-ny*4-nx*4)+' '+(mx-nx*4-ny*4)+','+(my-ny*4+nx*4)+'" fill="#000"/>';});
s+='<line x1="44" y1="'+yt+'" x2="44" y2="'+yb+'" stroke="#000"/><line x1="38" y1="'+yt+'" x2="62" y2="'+yt+'" stroke="#000" stroke-dasharray="3,2"/><line x1="38" y1="'+yb+'" x2="62" y2="'+yb+'" stroke="#000" stroke-dasharray="3,2"/><text x="30" y="'+((yt+yb)/2+4)+'" font-style="italic">x</text>';
s+='</svg>';
return s;}""")

# =========================================================================== Q1
G1={'sf':SF,'fig11':FIG11,
 'vx':'+vp.toFixed(1)','w':'+wp.toFixed(2)','r':'vx/w','rs':'sf(r,2)','rd':'r.toFixed(3)','f':'w/(2*Math.PI)','fs':'sf(f,2)','fd':'f.toFixed(4)',
 'ry':'2*r/3','a':'ry*w*w','as':'sf(a,2)','ad':'a.toFixed(3)','f11':'fig11(vx)'}
P1={'vp':[1.8,3.6],'wp':[0.50,1.20]}
parts=[]
parts.append(dict(pi=0,type='definition',K=lab('(a)')+'Define the radian.',
 B=andor(['angle'],['arc','distance along','length'],['radius'],['equal','same','=','equals']),
 U='The radian is the angle subtended at the centre of a circle by an arc equal in length to the radius.',
 V='One radian is the angle at the centre of a circle subtended by an arc whose length equals the radius of the circle (θ = arc length / radius).'))
parts.append(dict(pi=1,type='calculation',
 K=lab('(b)(i)')+'Three children are playing on a roundabout (rotatable horizontal platform) at a playground. Child X is standing on the edge of the roundabout. This child is pushing so that the edge of the roundabout moves in a circle at a constant speed of ${vx} m s<sup>−1</sup>, as shown in the view from above in Figure 1.1.${f11}The radius of the roundabout is 3<i>R</i>.<br>Child Y is sitting on the roundabout at a distance 2<i>R</i> from the centre.<br>Child Z is sitting at a distance <i>R</i> from the centre.<br><br>Child Y is moving in a circle with an angular speed of ${w} rad s<sup>−1</sup>.<br><br>Calculate the radius of the roundabout.',
 C1=kwv('v=rω','v=ωr','r=v/ω','v=r*ω','${vx}/${w}','${vx}÷${w}'),
 A='${rs}|${rd}',tolerance='2',
 U='v = rω, so r = ${vx} / ${w} = ${rs} m',
 V='All the children on the roundabout have the same angular speed. Child X moves at speed v on a circle of radius 3R (the edge), so use v = rω with the angular speed.'))
parts.append(dict(pi=2,type='calculation',
 K=lab('(b)(ii)')+'Calculate the frequency of rotation of the roundabout.',
 C1=kwv('ω=2πf','f=ω/2π','f=ω/(2π)','ω=2π/t','f=${w}/2π','f=${w}/(2π)','${w}/2π','${w}/(2π)','${w}÷(2π)','ω=2π×f','f=1/t'),
 A='${fs}|${fd}',tolerance='2',
 U='ω = 2πf, so f = ${w} / 2π = ${fs} Hz',
 V='Angular speed and frequency are related by ω = 2πf (one revolution is 2π rad).'))
parts.append(dict(pi=3,type='calculation',
 K=lab('(b)(iii)')+'Calculate the centripetal acceleration of child Y.',
 C1=kwv('a=rω²','a=rω^2','a=ω²r','a=ω^2r','a=r×ω²','a=ω²×r','a=v²/r','a=v^2/r','rω²','ω²r','ω^2r','rω^2'),
 A='${as}|${ad}',tolerance='3',
 U='child Y is at a distance 2R = (2/3) × ${rs} m from the centre; a = rω² = (2/3 × ${rs}) × ${w}² = ${as} m s⁻²',
 V='Centripetal acceleration a = rω², where r is the distance of Y from the centre (2R, which is two thirds of the radius 3R).'))
parts.append(dict(pi=4,type='table',
 K=lab('(c)')+'For the roundabout in 1(b), compare the linear and angular velocities for child X and child Z at any instant in time. For each row complete Table 1.1. For the magnitude type <i>less</i>, <i>equal</i> or <i>greater</i> (comparing X with Z); for the direction type <i>same</i> or <i>opposite</i>.',
 answerType='table',
 tableRowLabels='["linear velocity: magnitude of X compared with Z","linear velocity: direction of X compared with Z","angular velocity: magnitude and direction of X compared with Z"]',
 tableColLabels='["Table 1.1"]',
 tableCellKeywords='[[["exact:greater","exact:greater than","exact:x greater than z","exact:larger","exact:bigger","exact:more","exact:higher","exact:x is greater","exact:x greater","exact:x is greater than z","exact:larger than z","exact:greater than z"]],[["exact:opposite","exact:opposite direction","exact:opposite directions","exact:the opposite","exact:reversed","exact:different"]],[["equal","same","identical","unchanged"]]]',
 tableCellAnswers='[["greater"],["opposite"],["equal magnitude and same direction"]]',
 U='linear velocity: X greater than Z in magnitude, opposite in direction; angular velocity: equal magnitude and same direction',
 V='Both children are on the same rigid roundabout, so they have the same angular velocity (equal magnitude, same direction). Linear velocity v = rω: X is at a greater radius so is faster. X and Z are on opposite sides of the centre, so their velocities point in opposite directions.'))
ALL+=question(LV,ID+'-Q1',PAPER,'definition','Circular motion',P1,G1,'Question 1',parts)

# =========================================================================== Q2
G2={'sf':SF,'ex':EX,'plates':PLATES,
 'upq':'Math.floor(poli)===0','hl':"upq?'higher':'lower'",'sgn':"upq?'positive':'negative'",'fdir':"upq?'upwards':'downwards'",
 'Vv':'Math.round(Vp/100)*100','xx':'+xp.toFixed(3)','nq':'Math.floor(nqp)','m':'nq*1.6e-19*Vv/(xx*9.81)','m_e':'ex(m,1)','m_f':'ex(m,2)',
 'ci':'Math.floor(cip)','ks':"['rev','slant','uneven']",
 'opts':"(()=>{const a=[];let j=0;for(let k=0;k<4;k++)a.push(k===ci?plates(upq,'ok'):plates(upq,ks[j++]));return a})()",
 'o0':'opts[0]','o1':'opts[1]','o2':'opts[2]','o3':'opts[3]',
 'kwsign':"JSON.stringify(upq?[['positive'],['up','same direction','direction of the field','with the field','along the field','parallel']]:[['negative'],['opposite','against','up','antiparallel','anti-parallel','contrary']])"}
P2={'poli':[0,1.99],'Vp':[3000,6000],'xp':[0.015,0.035],'nqp':[2,5.99],'cip':[0,3.99]}
parts=[]
parts.append(dict(pi=0,type='definition',K=lab('(a)')+'Define electric field at a point.',
 B=kwv('force per unit positive charge','force per unit charge','force on unit positive charge','force per charge','force/charge','f/q','force exerted per unit positive charge','force acting per unit positive charge','force on a unit positive charge','force per positive charge','force per coulomb','force on a positive unit charge','force that acts on a unit positive charge','force on 1 c','force per unit +ve charge','force on a positive test charge per unit charge'),
 U='The electric field at a point is the force per unit positive charge acting on a stationary positive test charge at that point.',V='Electric field strength E = F / q: the force exerted per unit positive charge placed at the point.'))
parts.append(dict(pi=1,type='imageChoice',
 K=lab('(b)(i)')+'An oil droplet has charge of magnitude <i>Q</i>. The droplet is held in equilibrium by the electric field between two horizontal parallel plates. The electric field is created by a potential difference (p.d.) <i>V</i> between the plates, with the lower plate at the ${hl} electric potential. The separation of the plates is <i>x</i>.<br><br>Which sketch shows four electric field lines that represent the electric field between the plates?',
 answerType='imageChoice',
 imageOptions=['${o0}','${o1}','${o2}','${o3}'],
 correctImageIndex='${ci}',imageChoiceMarks='3',
 U='Four straight, parallel, evenly spaced field lines perpendicular to the plates, each starting on one plate and finishing on the other, with arrows pointing ${fdir} (from the plate at the higher potential to the plate at the lower potential).',
 V='Between parallel plates the field is uniform: the lines are parallel, equally spaced and perpendicular to the plates. The direction is from the plate at the higher potential to the plate at the lower potential (the direction of the force on a positive charge).'))
parts.append(dict(pi=2,type='explain',
 K=lab('(b)(ii)')+'Explain, with reference to forces, whether the sign of <i>Q</i> is positive or negative.',
 B=kwv('electric force is upwards','electric force upwards','electric force must be upwards','electric force acts upwards','electric force acts up','electric force is up','electric force up','upward electric force','upwards electric force','force is upwards','force upwards','upward force','upwards force','must act upwards','must be upwards','balances the weight','balance the weight','balances the gravitational','balances gravitational','opposes the weight','opposes weight','electric force opposes','cancels the weight','equal and opposite to the weight','equal to the weight','weight is downwards','gravitational force is downwards','weight acts downwards','weight downwards'),
 B2='${kwsign}',
 U='The weight (gravitational force) is downwards, so the electric force on the droplet must be upwards. The field is ${fdir}, so the electric force is ${sgn=="positive"?"in the same direction as":"opposite to"} the field and Q is ${sgn}.',
 V='For equilibrium the electric force balances the weight, so it acts upwards. A positive charge experiences a force in the direction of the field; a negative charge experiences a force opposite to the field. Here the field points ${fdir}, so Q is ${sgn}.'))
parts.append(dict(pi=3,type='definition',K=lab('(c)(i)')+'For the oil droplet in 2(b), state an expression, in terms of some or all of <i>Q</i>, <i>V</i> and <i>x</i>, for the electric field strength <i>E</i>.',
 A=kwv('v/x','e=v/x','v÷x','e=v÷x','(v)/(x)','v over x'),
 U='E = V / x',V='In a uniform field the field strength is the potential difference divided by the plate separation.'))
parts.append(dict(pi=4,type='definition',K=lab('(c)(ii)')+'State an expression, in terms of some or all of <i>Q</i>, <i>V</i> and <i>x</i>, for the weight <i>W</i> of the droplet.',
 A=kwv('qv/x','vq/x','q×v/x','v×q/x','q(v/x)','(v/x)q','(qv)/x','(vq)/x','qv÷x','q×(v/x)','(v/x)×q','v/x×q','q×v÷x','w=qv/x','w=vq/x','w=q×v/x','w=(qv)/x','w=qe=qv/x'),
 U='W = QV / x',V='The droplet is in equilibrium, so the weight equals the electric force, W = QE = QV/x.'))
parts.append(dict(pi=5,type='calculation',
 K=lab('(d)')+'The plates in 2(b) have a p.d. across them of ${Vv} V and a separation of ${xx} m. The magnitude of the charge on the oil droplet is ${nq}<i>e</i>, where <i>e</i> is the elementary charge.<br><br>Calculate the mass of the oil droplet.',
 C1=kwv('w=mg','mg=qe','mg=qv/x','eq=mg','qe=mg','qe=w','m=qe/g','m=qv/xg','m=qv/(xg)','w=qe','qv/x=mg','w=qv/x','m=w/g','mg=nqe','mg=neq'),
 A='${m_e}|${m_f}',tolerance='2',
 U='W = mg = QV / x, so m = ${nq} × 1.60 × 10⁻¹⁹ × ${Vv} / (${xx} × 9.81) = ${m_e} kg',
 V='The weight of the droplet equals the electric force: mg = QE = QV/x with Q = ${nq}e.'))
parts.append(dict(pi=6,type='explain',
 K=lab('(e)')+'The polarity of the p.d. across the plates in 2(b) is reversed.<br><br>Describe and explain the subsequent motion of the oil droplet.',
 B=kwv('both forces now act downwards','both now act downwards','electric force now acts downwards','electric force is now acting downwards','both forces are acting downwards','both forces now downwards','electric force is now downwards','electric force now downwards','electric force downwards','electric force acts downwards','electric force is downwards','electric force is now down','both forces are downwards','both forces downwards','both forces act downwards','both forces are now downwards','force is now downwards','electric force reverses','electric force changes direction','field is reversed','field reverses','direction of the electric force reverses','force now acts downwards','electric force acts down'),
 B2=kwv('accelerates downwards','accelerates downward','accelerates down','accelerate downwards','acceleration downwards','downward acceleration','moves downwards','moves downward','falls','falling','accelerates towards the lower plate','accelerates to the lower plate','moves down','will fall','drops','travels downwards'),
 U='The electric force now acts downwards (the same direction as the weight), so the resultant force is downwards and the droplet accelerates downwards.',
 V='Reversing the polarity reverses the field and so the electric force. Both the electric force and the weight now act downwards, so there is a resultant downward force and the droplet accelerates downwards (F = ma).'))
ALL+=question(LV,ID+'-Q2',PAPER,'definition','Electric fields',P2,G2,'Question 2',parts)

# =========================================================================== Q3
G3={'sf':SF,
 'mi':'+mip.toFixed(1)','Ti':'Math.round(tip)','mw':'+mwp.toFixed(1)','Tw':'Math.round(twp)',
 'th':'(mw*4.19*Tw-mi*2.11*Ti-mi*336)/(4.19*(mw+mi))','ths':'sf(th,2)','thd':'th.toFixed(1)',
 'Lt':'mi*336','Lt3':'sf(Lt,3)','Lt3k':'sf(Lt/1000,3)','It':'mi*2.11*Ti','It3':'sf(It,3)','It3k':'sf(It/1000,3)',
 'Wt':'mw*4.19*(Tw-th)','Wt3':'sf(Wt,3)','Wt3k':'sf(Wt/1000,3)','Ht':'mi*4.19*th','Ht3':'sf(Ht,3)','Ht3k':'sf(Ht/1000,3)',
 'Wtot':'mw*4.19*Tw','mikg':'mi/1000','mwkg':'mw/1000'}
P3={'mip':[12,20],'tip':[10,25],'mwp':[110,160],'twp':[30,40]}
parts=[]
parts.append(dict(pi=0,type='definition',K=lab('(a)')+'Define specific latent heat of fusion.',
 B=kwv('energy per unit mass','thermal energy per unit mass','heat per unit mass','energy per kg','per unit mass','per kilogram','energy per mass','energy required per unit mass','energy/mass','q/m','l=q/m','energy per 1 kg','energy needed per unit mass','heat required per unit mass','thermal energy required per unit mass','thermal energy per kilogram'),
 B2=andor(['solid','melt','fusion','freez','ice'],['liquid','change of state','change state','changing state','phase','without change in temperature','constant temperature','no change in temperature','same temperature','without a change in temperature','without changing temperature','without temperature change','no temperature change']),
 U='The (thermal) energy required per unit mass to change a substance from solid to liquid (change of state) without a change in temperature.',V='Specific latent heat of fusion L = Q / m: the thermal energy per unit mass needed to melt a solid at constant temperature (the melting point).'))
parts.append(dict(pi=1,type='explain',K=lab('(b)')+'Explain why substances usually have a higher specific latent heat for vaporisation than for fusion.',
 B=kwv('change in volume is greater','volume change is greater','greater change in volume','larger change in volume','bigger change in volume','greater volume change','larger volume change','volume increases more','expands more','greater expansion','more expansion','increase in volume is greater','volume increase is greater','volume changes more','greater increase in volume','larger increase in volume','change in volume is larger','change in volume is bigger','greater increase in the volume','larger increase in the volume','bigger increase in volume','much larger volume','much greater volume'),
 B2=andor(['work'],['atmosphere','atmospheric','against','external','surroundings','pressure']),
 U='The change in volume is greater for vaporisation than for fusion, so more work is done against the atmosphere (so more thermal energy must be supplied).',
 V='When a liquid vaporises its volume increases enormously. The expanding vapour does work pushing back the atmosphere, so extra thermal energy is needed in addition to that required to separate the molecules.'))
parts.append(dict(pi=2,type='calculation',
 K=lab('(c)')+'An ice cube of mass ${mi} g at a temperature of −${Ti} °C is removed from a freezer. The ice cube is immediately placed in an insulated beaker that contains a mass of ${mw} g of water at a temperature of ${Tw} °C.<br><br>The specific heat capacity of water is 4.19 kJ kg<sup>−1</sup> °C<sup>−1</sup>.<br>The specific heat capacity of ice is 2.11 kJ kg<sup>−1</sup> °C<sup>−1</sup>.<br>The specific latent heat of fusion of water is 336 kJ kg<sup>−1</sup>.<br>The beaker has negligible specific heat capacity.<br><br>The contents of the beaker are left to reach thermal equilibrium.<br><br>Calculate the temperature, in °C, of the water in the beaker when thermal equilibrium is reached.',
 C3=kwv('${Lt3}','${Lt3k}','${It3}','${It3k}','${Wt3}','${Wt3k}','${Ht3}','${Ht3k}'),
 C2=kwv('energylost=energygained','heatlost=heatgained','thermalenergylost=thermalenergygained','lost=gained','conservationofenergy','conservationofthermalenergy','energylostbywater=energygainedbyice','heatlostbywater=heatgainedbyice','energygainedbyice=energylostbywater','heatgained=heatlost','q1=q2','energyin=energyout','energyfromwater=energytoice','energylostbythewater=energygainedbytheice'),
 C1=delta('q=mcΔθ','q=mcΔt','q=mcθ','mcΔθ','mcΔt','Δq=mcΔθ','e=mcΔθ','e=mcΔt','q=mcΔT','mcΔT','m×c×Δ','mcdt','mcθ'),
 A='${ths}|${thd}',tolerance='2',
 U='energy lost by the water = energy gained by the ice: ${mw} × 4.19 × (${Tw} − θ) = ${mi} × 2.11 × ${Ti} + ${mi} × 336 + ${mi} × 4.19 × θ, so θ = ${ths} °C',
 V='Energy lost by the cooling water = energy to warm the ice to 0 °C + energy to melt the ice + energy to warm the melted ice from 0 °C to the final temperature θ. Use Q = mcΔθ for each warming stage and Q = mL for melting. The masses may be left in grams because the same unit appears on both sides.'))
ALL+=question(LV,ID+'-Q3',PAPER,'definition','Thermal physics',P3,G3,'Question 3',parts)

# =========================================================================== Q4
KW4=json.dumps
G4={'sf':SF,
 'k':'Math.floor(kk)','p':'+pp.toFixed(1)','V2':'+v2p.toFixed(3)','V1':'+(k*V2).toFixed(3)','T1':'Math.round(t1p/10)*10',
 'U2':'+u2p.toFixed(1)','U1':'+(k*U2).toFixed(1)',
 'Wv':'Math.round(p*1e5*(V1-V2))','dU':'-Math.round((U1-U2)*1000)','Qj':'dU-Wv','Qa':'Math.abs(Qj)/1000','Qa3':'Qa.toPrecision(3)','Qjs':'String(Math.abs(Qj))',
 'Qk':'(Qj/1000).toFixed(1)','dUk':'(dU/1000).toFixed(1)','T2':'Math.round(T1/k)',
 'kwn':"['','','half','third','quarter','fifth'][k]",'kwf':"['','','halves','thirds','quarters','fifths'][k]"}
P4={'kk':[2,5.99],'pp':[1.0,3.0],'v2p':[0.008,0.016],'t1p':[500,650],'u2p':[2.0,5.0]}
parts=[]
parts.append(dict(pi=0,type='definition',
 K='The first law of thermodynamics may be written as<br><br>Δ<i>U</i> = <i>Q</i> + <i>W</i><br><br>where <i>W</i> is the work done on a system.<br><br>'+lab('(a)')+'State the meaning, in this equation, of the symbols Δ<i>U</i> and <i>Q</i>.',
 B=delta('increase in internal energy','change in internal energy','increase in the internal energy','change in the internal energy','increase of internal energy','change of internal energy','internal energy increase','internal energy change','increase in total internal energy','increase in energy of the system','increase in the internal energy of the system'),
 B2=kwv('thermal energy transferred to the system','thermal energy supplied to the system','thermal energy added to the system','heat transferred to the system','heat supplied to the system','heat added to the system','energy transferred to the system by heating','thermal energy transferred to','thermal energy supplied to','thermal energy added to','heat transferred to','heat supplied to','heat added to','heat energy supplied','heat energy added','heat energy transferred to','energy supplied by heating','heat flow into the system','heat into the system','thermal energy into the system','energy transferred to the system as heat','thermal energy gained by the system','heat gained by the system','heat given to the system','thermal energy given to the system','heat absorbed by the system','thermal energy absorbed by the system','energy transferred as heat to the system','energy transferred thermally to the system'),
 U='ΔU is the increase in internal energy of the system. Q is the thermal energy transferred to (supplied to) the system.',
 V='In ΔU = Q + W, ΔU is the increase in the internal energy of the system, Q is the thermal energy transferred to the system and W is the work done on the system.'))
parts.append(dict(pi=1,type='calculation',
 K=lab('(b)(i)')+'An ideal gas at a pressure of ${p} × 10<sup>5</sup> Pa has an initial volume of ${V1} m<sup>3</sup>, an initial thermodynamic temperature of ${T1} K, and an initial internal energy of ${U1} kJ.<br>The volume of the gas is reduced at constant pressure to a final volume of ${V2} m<sup>3</sup>.<br><br>Show that the magnitude of the work done on the gas is ${Wv} J.',
 C1=delta('w=pΔv','w=pdv','pΔv','p(v1−v2)','p(v1-v2)','p(v2−v1)','p(v2-v1)','w=p(v1−v2)','w=p(v1-v2)','w=p×Δv','w=p×(v1-v2)','w=p×(v1−v2)','Δv×p','Δvp','p*Δv','w=pΔv'),
 A='${Wv}',tolerance='1',
 U='W = pΔV = ${p} × 10⁵ × (${V1} − ${V2}) = ${Wv} J',
 V='At constant pressure the work done is W = pΔV, where ΔV is the magnitude of the change in volume.'))
parts.append(dict(pi=2,type='explain',
 K=lab('(b)(ii)')+'Explain whether the work done on the gas is positive or negative.',
 B=andor(['positive','+ve','+'],['compress','volume decreas','volume is reduced','volume reduc','reduction in volume','decrease in volume','done on','volume gets smaller','volume is smaller','volume gets less','volume of the gas decreases','smaller volume','pushed in','squash','less volume','gas is being compressed']),
 U='The work done on the gas is positive because the gas is compressed (its volume decreases).',
 V='W in ΔU = Q + W is the work done on the gas. The volume decreases, so the surroundings do work on the gas and W is positive.'))
parts.append(dict(pi=3,type='explain',
 K=lab('(b)(iii)')+'Explain why the final internal energy of the gas is ${U2} kJ.',
 B=andor(['volume','v∝','v/t','charles','v is proportional','v proportional','v directly'],['proportional','∝','directly','v/t','pv/t','charles','linear','constant pressure']),
 B2=andor(['proportional','∝','directly','depends on','depend on','function of','linked to','related to','dependent on'],['internal energy','energy','u∝','u=','u is']),
 U='At constant pressure the volume V ∝ T. The volume has been reduced to one ${kwn} of its initial value, so T has also been reduced to one ${kwn}. The internal energy U ∝ T, so U is also reduced to one ${kwn}: ${U1} / ${k} = ${U2} kJ.',
 V='For an ideal gas at constant pressure V ∝ T, so T falls by the same factor as V (from ${T1} K to ${T2} K). The internal energy of an ideal gas is the sum of the random kinetic energies of the molecules, which is proportional to T, so U falls by the same factor: ${U1} / ${k} = ${U2} kJ.'))
parts.append(dict(pi=4,type='calculation',
 K=lab('(c)')+'For the reduction of the volume of the gas in 4(b), calculate <i>Q</i>. Give a unit with your answer.',
 C1=delta('q=Δu−w','q=Δu-w','Δu=q+w','Δu−w','Δu-w','q=Δu-w','q=(u2−u1)−w','q=(u2-u1)-w','q=Δu−' )+'|${Qa3}|${Qjs}',
 A=kwv('-${Qa3}','-${Qjs}','−${Qa3}'),tolerance='1',
 U='ΔU = ${U2} − ${U1} = ${dUk} kJ = ${dU} J; Q = ΔU − W = ${dU} − ${Wv} = ${Qj} J = ${Qk} kJ',
 V='The change in internal energy is ΔU = final − initial = ${dUk} kJ. From ΔU = Q + W with W = +${Wv} J, Q = ΔU − W. The negative sign shows that thermal energy is transferred from the gas to the surroundings.'))
ALL+=question(LV,ID+'-Q4',PAPER,'definition','Thermal physics',P4,G4,'Question 4',parts)

# =========================================================================== Q5
FIG5=js(r"""(Vv,N1,mm)=>{const k=1.38e-23;const E=3*k*400/mm/1e6,Ek=1.5*N1*1e24*k*400/1e4;
const nice=@NICE@;
const y2=nice(E),y3=nice(Ek);
const o=(x0,x1,y0,y1,mx,my,Mx,My,xl,yl,pts,cap)=>gsvg({x0:x0,x1:x1,y0:y0,y1:y1,mx:mx,my:my,Mx:Mx,My:My,xl:xl,yl:yl,pts:pts,cap:cap,W:430,H:300});
return o(0,8,0,4,1,0.5,4,2,'NT / 10²⁶ K','p / 10⁴ Pa',[[0,0],[8,0.138*8/Vv]],'Figure 5.1')
+o(0,400,0,y2,20,y2/10,200,y2/2,'T / K','⟨c²⟩ / 10⁶ m² s⁻²',[[0,0],[400,E]],'Figure 5.2')
+o(0,400,0,y3,20,y3/10,200,y3/2,'T / K','E_K / 10⁴ J',[[0,0],[400,Ek]],'Figure 5.3');}""").replace('@NICE@',NICE)
G5={'sf':SF,'ex':EX,'gsvg':GSVG,'fig5':FIG5,
 'Vv':'+vp.toFixed(2)','N1':'+np.toFixed(1)','gi':'Math.floor(gip)','mm':'[6.64e-27,3.35e-26,4.65e-26,6.64e-26][gi]',
 'Mm':'[4.0,20,28,40][gi]','gname':"['helium','neon','nitrogen','argon'][gi]",
 'f5':'fig5(Vv,N1,mm)',
 'Vk':'Vv.toFixed(2)','mk':'ex(mm,1)','Mk':'ex(Mm/1000,1)','Mkg':'(Mm/1000).toPrecision(2)',
 'nmol':'N1*1e24/6.02e23','nk':'nmol.toPrecision(2)','Nk':'ex(N1*1e24,1)','gm':'N1*1e24*mm','gmk':'ex(gm,1)','rho':'gm/Vv','rhok':'ex(rho,1)',
 'idealk':"JSON.stringify([['ideal']])"}
P5={'vp':[0.35,0.90],'np':[1.2,2.0],'gip':[0,3.99]}
parts=[]
parts.append(dict(pi=0,type='definition',K=lab('(a)')+'State what is represented by the Avogadro constant.',
 B=andor(['number','atoms','particles','molecules','entities'],['per mole','in one mole','in a mole','in 1 mole','in 12 g','in 12g','in 0.012 kg','in 1 mol','in one mol','each mole','every mole','permole']),
 U='The number of particles (atoms or molecules) per mole (in one mole of a substance).',V='The Avogadro constant N_A is the number of particles (atoms or molecules) in one mole of a substance.'))
parts.append(dict(pi=1,type='explain',
 K=lab('(b)')+'A gas is in a sealed container that has a fixed volume. The thermodynamic temperature <i>T</i> of the gas is varied.<br>Figure 5.1 shows how the pressure <i>p</i> of the gas varies with <i>NT</i>, where <i>N</i> is the number of molecules of the gas.<br>Figure 5.2 shows how the mean-square speed ⟨<i>c</i><sup>2</sup>⟩ of the molecules of the gas varies with <i>T</i>.<br>Figure 5.3 shows how the total kinetic energy <i>E</i><sub>K</sub> of all the molecules of the gas varies with <i>T</i>.${f5}Determine three conclusions about the gas that can be drawn from Figure 5.1, Figure 5.2 and Figure 5.3. The conclusions may be qualitative or quantitative. Use the space below for any working.',
 A=kwv('ideal','p∝nt','p∝t','proportional to nt','proportional to t','pv=nkt','pv=nrt','obeys the ideal gas','obeys pv','follows pv','obeys the gas laws','obeys boyle','obeys charles','obeys the pressure law'),
 B='${Vk}',
 B2=kwv('${mk}','${Mk}','${Mkg}','${gname}'),
 B3=kwv('${nk}','${Nk}','${gmk}','${rhok}'),
 maxMarks='3',tolerance='5',
 U='Any three of: the gas is ideal (p ∝ NT, ⟨c²⟩ ∝ T and E_K ∝ T are straight lines through the origin); the volume of the container is ${Vk} m³ (from the gradient of Figure 5.1, V = k/gradient); the mass of one molecule is ${mk} kg (m = 3kT/⟨c²⟩ ≈ molar mass ${Mkg} kg mol⁻¹, so the gas is ${gname}); the number of molecules is ${Nk} (E_K = 3/2 NkT), which is ${nk} mol; the mass of gas is ${gmk} kg (or the density is ${rhok} kg m⁻³).',
 V='The three graphs are all straight lines through the origin, so p ∝ NT, ⟨c²⟩ ∝ T and E_K ∝ T, which is ideal-gas behaviour. Quantitative conclusions: V = k/(gradient of Fig 5.1) = ${Vk} m³; m = 3kT/⟨c²⟩ = ${mk} kg; N = 2E_K/(3kT) = ${Nk}, so n = N/N_A = ${nk} mol; mass of gas = Nm = ${gmk} kg.'))
parts.append(dict(pi=2,type='explain',
 K=lab('(c)(i)')+'One assumption of the kinetic theory of gases is that the volume of the molecules is negligible compared with the volume of the gas.<br><br>State, with a reason, whether this assumption applies to the gas in 5(b).',
 B=andor(['yes','applies','does apply','assumption is valid','is valid','true','correct'],['ideal','proportional','straight line','obeys pv','follows pv','linear']),
 U='Yes, because the gas is ideal (the graphs show ideal-gas behaviour: p ∝ NT, ⟨c²⟩ ∝ T and E_K ∝ T).',V='The graphs show the gas obeys the ideal gas equation, and an ideal gas is one for which the kinetic-theory assumptions (including negligible molecular volume) hold, so the assumption applies.'))
parts.append(dict(pi=3,type='explain',
 K=lab('(c)(ii)')+'State two other assumptions of the kinetic theory of gases.',
 A=kwv('random motion','constant motion','continuous random motion','move randomly','moving randomly','molecules move at random','constant random motion','random movement','in random motion','rapid random motion','random direction','randomly moving','move in random directions'),
 B=kwv('elastic','no energy lost in collisions','kinetic energy is conserved','kinetic energy conserved','no loss of kinetic energy','kinetic energy is not lost','no loss of energy'),
 B2=kwv('no intermolecular forces','no forces between molecules','no forces between the molecules','negligible intermolecular forces','no forces between particles','no attractive forces','no force between molecules','no interactions between molecules','no electrostatic forces','intermolecular forces are negligible','forces between molecules are negligible','no forces except during collisions','no forces of attraction','no repulsive forces','no intermolecular'),
 B3=kwv('collisions are instantaneous','time of collision is negligible','duration of collision is negligible','collision time is negligible','negligible time of collision','negligible collision time','collisions take negligible time','collisions have negligible duration','collision duration is negligible','time of collisions is negligible','time for collisions is negligible','collisions are of negligible duration','time spent in collisions is negligible','the time of a collision is negligible','negligible duration','duration of collisions is negligible','time taken for collision is negligible','time of the collisions is negligible'),
 maxMarks='2',
 U='Any two of: the molecules are in constant random motion; collisions between molecules and with the container walls are elastic; there are no intermolecular forces (except during collisions); the time of a collision is negligible compared with the time between collisions.',
 V='Other kinetic-theory assumptions: random motion, elastic collisions, no forces between molecules except during collisions, and collisions that last a negligible time.'))
ALL+=question(LV,ID+'-Q5',PAPER,'definition','Thermal physics',P5,G5,'Question 5',parts)

# ------------------------------------------------------------ generic answer-sketch plot (axes with ticks, curves in data coords)
SKP = jso(r"""(o)=>{const W=o.W||300,H=o.H||230,L=54,R=14,T=14,B=46,pw=W-L-R,ph=H-T-B;
let s=@OPT@;
const sx=v=>L+(v-o.x0)/(o.x1-o.x0)*pw,sy=v=>T+ph-(v-o.y0)/(o.y1-o.y0)*ph;
s+='<line x1="'+L+'" y1="'+T+'" x2="'+L+'" y2="'+(T+ph)+'" stroke="#000"/>';
const yb=o.zero?sy(0):T+ph;
s+='<line x1="'+L+'" y1="'+yb+'" x2="'+(L+pw)+'" y2="'+yb+'" stroke="#000"/>';
(o.xt||[]).forEach(t=>{s+='<line x1="'+sx(t[0])+'" y1="'+yb+'" x2="'+sx(t[0])+'" y2="'+(yb+4)+'" stroke="#000"/><text x="'+sx(t[0])+'" y="'+(T+ph+17)+'" text-anchor="middle">'+t[1]+'</text>';});
(o.yt||[]).forEach(t=>{s+='<line x1="'+(L-4)+'" y1="'+sy(t[0])+'" x2="'+L+'" y2="'+sy(t[0])+'" stroke="#000"/><text x="'+(L-7)+'" y="'+(sy(t[0])+4)+'" text-anchor="end">'+t[1]+'</text>';});
s+='<text x="'+(L+pw/2)+'" y="'+(H-6)+'" text-anchor="middle">'+o.xl+'</text><text transform="translate(13,'+(T+ph/2)+') rotate(-90)" text-anchor="middle">'+o.yl+'</text>';
(o.c||[]).forEach(c=>{s+='<polyline fill="none" stroke="#000" stroke-width="2.2" points="'+c.map(p=>sx(p[0]).toFixed(1)+','+sy(p[1]).toFixed(1)).join(' ')+'"/>';});
return s+'</svg>';}""")

# =========================================================================== Q6
SK6=js(r"""(kind)=>{const c=[];for(let i=0;i<=160;i++){const u=i/80;let v;
 if(kind==='ok')v=Math.cos(2*Math.PI*u);else if(kind==='sin')v=Math.sin(2*Math.PI*u);else if(kind==='one')v=Math.cos(Math.PI*u);else v=Math.abs(Math.cos(2*Math.PI*u));
 c.push([u,v]);}
return skp({x0:0,x1:2,y0:-1.3,y1:1.3,zero:true,xt:[[0,'0'],[1,'T'],[2,'2T']],yt:[[1,'E₀'],[-1,'−E₀']],xl:'t',yl:'E',c:[c],W:300,H:230});}""")
G6={'sf':SF,'ex':EX,'fframe':FIGFRAME,'ftop':FIGTOP,'skp':SKP,'sk6':SK6,
 'A':'+ap.toFixed(1)','w':'+wp.toFixed(1)','B':'+bp.toFixed(3)','H':'+hp.toFixed(1)','Wd':'+dp.toFixed(1)',
 'T':'2*Math.PI/w','Ts':'sf(T,2)','Td':'T.toFixed(3)','v0':'A*w','v02':'sf(v0,2)','v03':'v0.toPrecision(3)',
 'Hm':'(H/100).toFixed(3)','H2m':'(2*H/100).toFixed(3)','E0':'B*2*(H/100)*(v0/1000)','E02':'ex(E0,1)','E03':'ex(E0,2)',
 'v0m':'(v0/1000).toPrecision(3)','ci':'Math.floor(cip)','ks':"['sin','one','abs']",
 'opts':"(()=>{const a=[];let j=0;for(let k=0;k<4;k++)a.push(k===ci?sk6('ok'):sk6(ks[j++]));return a})()",
 'o0':'opts[0]','o1':'opts[1]','o2':'opts[2]','o3':'opts[3]','f61':'fframe(H.toFixed(1),Wd.toFixed(1))','f62':'ftop()'}
P6={'ap':[2.0,4.5],'wp':[5.0,9.5],'bp':[0.030,0.070],'hp':[4.0,8.0],'dp':[3.0,6.0],'cip':[0,3.99]}
parts=[]
parts.append(dict(pi=0,type='definition',K=lab('(a)')+'State what is meant by simple harmonic motion.',
 B=andor(['acceleration','a∝','force'],['proportional','∝','directly'],['displacement','distance','x','equilibrium','fixed point']),
 B2=kwv('opposite direction','opposite in direction','directed towards','towards a fixed point','towards the equilibrium','towards equilibrium','towards the centre','towards the mean position','towards the central point','opposite to displacement','opposite to the displacement','negative','a=-','a=−','−ω²x','-ω²x','-ω^2','directed to a fixed point','directed towards a fixed point','directed towards the equilibrium','always towards the equilibrium','always towards a fixed point','acts towards','always opposite','oppositeto'),
 U='The acceleration of the oscillating object is proportional to its displacement from a fixed (equilibrium) point and is always directed towards that point (opposite in direction to the displacement).',
 V='Simple harmonic motion: a ∝ −x, i.e. the acceleration is directly proportional to the displacement from the equilibrium position and is in the opposite direction to the displacement (towards a fixed point).'))
parts.append(dict(pi=1,type='calculation',
 K=lab('(b)(i)')+'A length of thick copper wire is formed into a rectangular frame, as shown in Figure 6.1.${f61}The frame has side lengths of ${H} cm and ${Wd} cm.<br>There is a small gap XY at the ends of the wire at the top of the frame.<br>The frame is suspended so that it hangs vertically using thin cotton thread attached to the two ends of the wire. The frame oscillates about its vertical axis, as shown in the view from above in Figure 6.2.${f62}The oscillations are simple harmonic. The displacement <i>s</i> of the edge of the frame from its equilibrium position varies with time <i>t</i> according to<br><br><i>s</i> = ${A} sin ${w}<i>t</i><br><br>where <i>s</i> is in mm and <i>t</i> is in s.<br><br>Calculate the period <i>T</i> of the oscillations.',
 C1=kwv('t=2π/ω','t=2π/${w}','ω=2π/t','${w}=2π/t','2π/${w}','2π÷${w}','ω=2πf','f=ω/2π','t=1/f','ω=2π/t','t=2π/ω','t=2*π/ω','t=2π÷ω'),
 A='${Ts}|${Td}',tolerance='2',
 U='ω = 2π / T, so T = 2π / ${w} = ${Ts} s',
 V='Compare s = A sin ωt with s = ${A} sin ${w}t: the angular frequency ω = ${w} rad s⁻¹. The period is T = 2π/ω.'))
parts.append(dict(pi=2,type='calculation',
 K=lab('(b)(ii)')+'Show that the maximum speed of the edges of the frame is ${v02} mm s<sup>−1</sup>.',
 C1=kwv('v0=ωx0','v=ωx0','v0=ωa','v=ωa','v=aω','v0=aω','v=x0ω','v0=x0ω','v=ω×a','v=ω×x0','v0=ω×x0','v=ωa','ωx0','ωa','x0ω','aω','v0=ωa','v=ω×${A}','v=${w}×${A}','v=${A}×${w}','${A}×${w}','${w}×${A}','v=ωa0','v=ωs0','v0=ωs0','v=ωs','v=ωa=','v=ds/dt','ω×${A}','${A}*${w}','${w}*${A}'),
 A='${v02}|${v03}',tolerance='1',
 U='v₀ = ωx₀ = ${w} × ${A} = ${v03} ≈ ${v02} mm s⁻¹',
 V='In simple harmonic motion the maximum speed is v₀ = ωx₀, where x₀ = ${A} mm is the amplitude and ω = ${w} rad s⁻¹. (Differentiating s = ${A} sin ${w}t gives v = ${A} × ${w} cos ${w}t.)'))
parts.append(dict(pi=3,type='calculation',
 K=lab('(c)(i)')+'The frame in 6(b) is in a uniform horizontal magnetic field that is parallel to the equilibrium position of the frame.<br>The flux density of the magnetic field is ${B} T.<br><br>Calculate the electromotive force (e.m.f.) <i>E</i><sub>0</sub> induced across XY when the frame is moving at its maximum speed.',
 C2=kwv('${H2m}','2×${Hm}','2*${Hm}','2×${H}','2*${H}','${E03}','${E02}','${v0m}','2×bl×v','2blv','2bvl','2lbv','n=2','2 edges','two edges','two sides','2 sides'),
 C1=delta('e=blv','e=bvl','e=b×l×v','e=bl*v','blv','bvl','e=bΔa/Δt','e=Δφ/Δt','Δφ/Δt','bΔa/Δt','e=ΔΦ/Δt','ΔΦ/Δt','rate of change of flux','rate of cutting','e=nΔφ/Δt','nΔφ/Δt','emf=blv','e=Δ(bl)','blΔx/Δt','e=blΔx/Δt','blv','e0=blv','e0=2blv','ε=blv','e=bav','blv','ε=ΔΦ/Δt'),
 A='${E02}|${E03}',tolerance='3',
 U='E = BLv for each vertical edge; there are two edges moving across the field, so E₀ = B × 2L × v₀ = ${B} × ${H2m} × (${v02} × 10⁻³) = ${E02} V',
 V='The e.m.f. is the rate of change of flux linkage: E = BLv for each moving vertical edge (length L = ${Hm} m). Both vertical edges cut flux in the same sense, so the e.m.f. across XY is E₀ = B(2L)v₀ with v₀ = ${v02} × 10⁻³ m s⁻¹. The width of the frame is not needed.'))
parts.append(dict(pi=4,type='imageChoice',
 K=lab('(c)(ii)')+'Which sketch shows the variation of the induced e.m.f. <i>E</i> across XY with <i>t</i> between <i>t</i> = 0 and <i>t</i> = 2<i>T</i>?',
 answerType='imageChoice',imageOptions=['${o0}','${o1}','${o2}','${o3}'],correctImageIndex='${ci}',imageChoiceMarks='2',
 U='A cosine curve of amplitude E₀ that starts at E₀ at t = 0, crosses zero at T/4, 3T/4, 5T/4 and 7T/4 and completes two full cycles by t = 2T.',
 V='The displacement is s = A sin ωt, so the velocity v = Aω cos ωt. The e.m.f. is proportional to the speed of the edges, so E = E₀ cos ωt: it is a maximum at t = 0, T, 2T and zero at T/4, 3T/4, 5T/4 and 7T/4.'))
ALL+=question(LV,ID+'-Q6',PAPER,'definition','Oscillations,Electromagnetic induction',P6,G6,'Question 6',parts)

# =========================================================================== Q7
SK7=js(r"""(P,T0,kind)=>{const c=[];const n=200;
for(let i=0;i<=n;i++){const u=i/n;const t=u*T0;const cs=Math.cos(2*Math.PI*u);const on=(u<=0.25||u>=0.75);let v;
 if(kind==='ok')v=on?P*cs*cs:0;else if(kind==='unrect')v=P*cs*cs;else if(kind==='half')v=on?P/2*cs*cs:0;else v=on?P:0;
 c.push([t,v]);}
const xt=[];for(let k=0;k*0.01<=T0+1e-9;k++)xt.push([+(k*0.01).toFixed(2),k===0?'0':String(+(k*0.01).toFixed(2))]);
return skp({x0:0,x1:T0,y0:0,y1:8,xt:xt,yt:[[0,'0'],[4,'4'],[8,'8']],xl:'t / s',yl:'P / W',c:[c],W:320,H:240});}""")
FIG71=js(r"""(P,T0)=>{const pts=[];for(let i=0;i<=200;i++){const u=i/200;pts.push([u*T0,P*Math.pow(Math.cos(2*Math.PI*u),2)]);}
return gsvg({x0:0,x1:T0,y0:0,y1:8,mx:0.005,my:1,Mx:0.01,My:4,xl:'t / s',yl:'P / W',pts:pts,cap:'Figure 7.1',W:480,H:300});}""")
G7={'sf':SF,'gsvg':GSVG,'skp':SKP,'sk7':SK7,'fig71':FIG71,
 'R':'Math.round(rp)','Pm0':'Math.round(pp/0.4)*0.4','Pmax':'+Pm0.toFixed(1)','T0':'[0.04,0.05,0.06][Math.floor(tp)]','T0s':'T0.toFixed(3)',
 'Pm':'+(Pmax/2).toFixed(2)','Pms':'Pm.toFixed(1)','Pm2':'Pm.toFixed(2)','Ir':'Math.sqrt(Pm/R)','Is':'sf(Ir,2)','Id':'Ir.toFixed(3)',
 'Pm3':'Pm/2','Pm3s':'Pm3.toFixed(2)','Ir2':'Math.sqrt(Pm3/R)','Is2':'sf(Ir2,2)','Id2':'Ir2.toFixed(3)',
 'ci':'Math.floor(cip)','ks':"['unrect','half','rect']",
 'opts':"(()=>{const a=[];let j=0;for(let k=0;k<4;k++)a.push(k===ci?sk7(Pmax,T0,'ok'):sk7(Pmax,T0,ks[j++]));return a})()",
 'o0':'opts[0]','o1':'opts[1]','o2':'opts[2]','o3':'opts[3]','f71':'fig71(Pmax,T0)'}
P7={'rp':[15,45],'pp':[4.0,7.2],'tp':[0,2.99],'cip':[0,3.99]}
parts=[]
parts.append(dict(pi=0,type='definition',K=lab('(a)')+'State what is meant by the root-mean-square (r.m.s.) value of an alternating current.',
 M=kwv('direct current','steady current','constant current','d.c.','dc current','d.c. current','steady d.c.','constant d.c.','direct','steady','constant','square root of the mean','square root of the average','root of the mean of the square','square root of mean'),
 A=kwv('same power','same mean power','same average power','same heating','same heating effect','same energy','same rate of energy','same thermal energy','same rate of heating','same power dissipation','same power dissipated','same mean rate','same rate of dissipation','equal power','equal heating','equal mean power','same effect','same average rate','mean of the squares','mean square','average of the square','mean of the square','mean of square','mean value of the square','average value of the square','mean of squares'),
 U='The r.m.s. current is the value of the direct (steady) current that dissipates the same mean power in a resistor as the alternating current.',
 V='r.m.s. current: the steady (direct) current that would dissipate the same mean power in a given resistor as the alternating current does.'))
parts.append(dict(pi=1,type='calculation',
 K=lab('(b)(i)')+'There is a sinusoidal alternating current in a resistor of resistance ${R} Ω. The power <i>P</i> dissipated in the resistor varies with time <i>t</i> as shown in Figure 7.1.${f71}Determine the mean power dissipated in the resistor.',
 A='${Pms}|${Pm2}',tolerance='1',
 U='The graph oscillates between 0 and ${Pmax} W, so the mean power = ${Pmax} / 2 = ${Pms} W',
 V='Over a whole number of cycles the power varies symmetrically between 0 and its peak value ${Pmax} W, so the mean power is half the peak power.'))
parts.append(dict(pi=2,type='calculation',
 K=lab('(b)(ii)')+'Calculate the r.m.s. current in the resistor.',
 C1=kwv('p=i²r','p=i^2r','i²r','i^2r','p=i2r','i=√(p/r)','i=sqrt(p/r)','i=√p/r','p=ri²','p=ri^2','i²=p/r','i^2=p/r','√(p/r)','sqrt(p/r)','${Pms}/${R}','${Pm2}/${R}','p=vi','p=v²/r','p=v^2/r'),
 A='${Is}|${Id}',tolerance='2',
 U='P = I²R, so I = √(${Pms} / ${R}) = ${Is} A',
 V='The mean power is P = I_rms²R, so I_rms = √(P/R) using the mean power from (b)(i).'))
parts.append(dict(pi=3,type='definition',K=lab('(c)(i)')+'The current in the resistor in 7(b) is now half-wave rectified.<br><br>State the name of the electric circuit component that is used to achieve this rectification.',
 B=kwv('diode','semiconductor diode','rectifier diode','p-n junction','pn junction','p-n diode','rectifying diode'),
 U='A diode.',V='A diode conducts in one direction only, so it removes one half of each cycle of the alternating current.'))
parts.append(dict(pi=4,type='imageChoice',
 K=lab('(c)(ii)')+'Which sketch shows the variation of the power <i>P</i> dissipated in the resistor between <i>t</i> = 0 and <i>t</i> = ${T0s} s?',
 answerType='imageChoice',imageOptions=['${o0}','${o1}','${o2}','${o3}'],correctImageIndex='${ci}',imageChoiceMarks='2',
 U='The power follows the same cos² shape as in Figure 7.1, with a maximum of ${Pmax} W, but it is zero for the middle half of the time (from ${T0s}/4 to 3×${T0s}/4) while the diode blocks the current.',
 V='With half-wave rectification the current is zero for half of each cycle, so the power is zero for that half. During the conducting half the power is unchanged: P = I²R follows the same cos² curve with the same maximum ${Pmax} W.'))
parts.append(dict(pi=5,type='calculation',
 K=lab('(c)(iii)')+'Determine the r.m.s. current in the resistor. Explain your reasoning.',
 B=andor(['power','p','energy','heating'],['half','halved','halves','1/2','0.5','50%','half the time','half of the time','half the cycle','half of the cycle','zero for half','reduced by a factor of 2','factor of 2','factor 2','divided by 2','÷2']),
 A='${Is2}|${Id2}',tolerance='2',
 U='The mean power is halved (the current is zero for half of the time), so the mean power = ${Pm3s} W and I_rms = √(${Pm3s} / ${R}) = ${Is2} A',
 V='The power is zero for half of each cycle and unchanged for the other half, so the mean power halves to ${Pm3s} W. Then I_rms = √(P/R) = √(${Pm3s} / ${R}) = ${Is2} A.'))
ALL+=question(LV,ID+'-Q7',PAPER,'definition','Alternating currents',P7,G7,'Question 7',parts)

# =========================================================================== Q8
LAM=[410,434,486,656]
SK8=js(r"""(sh,kind)=>{const W=470,H=120,L=20,R=20,pw=W-L-R,lam=[410,434,486,656];
const X=l=>L+(l-380)/(760-380)*pw;
let s='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 '+W+' '+H+'" width="'+W+'" height="'+H+'" font-family="Arial,sans-serif" font-size="17"><rect width="'+W+'" height="'+H+'" fill="#fff"/>';
s+='<rect x="'+L+'" y="30" width="'+pw+'" height="50" fill="#eee" stroke="#000"/>';
lam.forEach(l=>{s+='<line x1="'+X(l)+'" y1="30" x2="'+X(l)+'" y2="80" stroke="#888" stroke-dasharray="3,3" stroke-width="1.5"/>';});
let nl;
if(kind==='ok')nl=lam.map(l=>l*(1+sh/656));
else if(kind==='left')nl=lam.map(l=>l*(1-sh/656));
else if(kind==='irr')nl=[lam[0]+sh*0.2,lam[1]-sh*0.9,lam[2]+sh*1.7,lam[3]+sh*0.1];
else nl=lam.slice(1).map(l=>l*(1+sh/656));
nl.forEach(l=>{s+='<line x1="'+X(l)+'" y1="30" x2="'+X(l)+'" y2="80" stroke="#000" stroke-width="3"/>';});
s+='<text x="'+L+'" y="104">violet</text><text x="'+(L+pw)+'" y="104" text-anchor="end">red</text><text x="'+(L+pw/2)+'" y="104" text-anchor="middle">wavelength increases →</text>';
s+='<text x="'+(L+pw/2)+'" y="20" text-anchor="middle" fill="#555">dashed lines: positions in the original spectrum</text>';
return s+'</svg>';}""")
G8={'sf':SF,'ex':EX,'sk8':SK8,
 'd':'+(dp*1).toPrecision(2)','H0':'+(hp*1).toPrecision(2)','dS':'d.toFixed(1)','H0S':'H0.toFixed(1)',
 'v':'H0*1e-18*d*1e24','vk':'ex(v,1)','vk2':'ex(v,2)','vc':'v/3.0e8','dl':'656*vc','dl2':'sf(dl,2)','dl3':'dl.toPrecision(3)',
 'obs':'656+dl','obs3':'obs.toPrecision(3)','obsi':'String(Math.round(obs))',
 'ci':'Math.floor(cip)','ks':"['left','irr','three']",
 'opts':"(()=>{const a=[];let j=0;for(let k=0;k<4;k++)a.push(k===ci?sk8(dl,'ok'):sk8(dl,ks[j++]));return a})()",
 'o0':'opts[0]','o1':'opts[1]','o2':'opts[2]','o3':'opts[3]'}
P8={'dp':[3.0,9.0],'hp':[1.8,2.6],'cip':[0,3.99]}
parts=[]
parts.append(dict(pi=0,type='explain',
 K='A star in a distant galaxy consists mostly of hydrogen. Visible light emitted by the star consists of discrete spectral absorption lines at wavelengths of 410 nm, 434 nm, 486 nm and 656 nm.<br><br>'+lab('(a)')+'Explain, with reference to photons, how the existence of these spectral lines provides evidence for discrete electron energy levels in the hydrogen atom.',
 A=andor(['photon'],['discrete','specific','fixed','quantised','quantized','particular','certain']),
 B=andor(['difference','change','transition','jump','drop','falls','moves between','moving between','moves from','e=hf','hf=','e2−e1','e2-e1','Δe','between energy levels','between levels'],['energy level','energy levels','levels','electron','state','states']),
 B2=andor(['wavelength','wavelengths','frequency','frequencies','lines'],['energy difference','energy change','energy transition','energy gap','energy of photon','energy of the photon','energies of photons','energies of the photons','photon energy','photon energies','energy of each photon','energies','energy']),
 B3=andor(['electron','electrons','energy level','energy levels','levels','atom'],['discrete','fixed','quantised','quantized','specific energies','specific energy','only certain','only particular']),
 maxMarks='3',
 U='Any three of: photons have discrete (specific) energies; the photon energy is equal to the difference between two electron energy levels; discrete wavelengths mean discrete photon energies, so only certain energy differences are possible; therefore the electron energy levels are discrete.',
 V='A photon carries energy E = hf = hc/λ. Each spectral line is one wavelength, so one photon energy. A photon is absorbed when an electron makes a transition between two energy levels, so the photon energy equals the difference between the levels. Only a few discrete wavelengths are seen, so only certain energy differences exist, which shows that the energy levels are discrete.'))
parts.append(dict(pi=1,type='explain',
 K=lab('(b)(i)')+'The galaxy is at a distance of ${dS} × 10<sup>24</sup> m from the Earth.<br><br>Explain why the spectral lines observed on the Earth are at different wavelengths from those given above.',
 B=kwv('galaxy is receding','galaxy is moving away','galaxy moves away','galaxy recedes','receding','moving away','moves away','recedes','recession','moving apart','expansion of the universe','expansion of space','expanding universe','expanding space','universe is expanding','moves away from the earth','moving away from the earth','moving away from us','moves away from us','galaxy is moving','galaxies are moving away','galaxies move away'),
 B2=kwv('redshift','red shift','red-shift','red shifted','red-shifted','redshifted','wavelength increases','wavelengths increase','longer wavelength','longer wavelengths','greater wavelength','greater wavelengths','larger wavelength','larger wavelengths','increase in wavelength','increased wavelength','wavelength is longer','wavelength is greater','wavelength is larger','wavelengths are longer','wavelengths are greater','wavelengths are larger','shifted to longer','shifted to greater','shifted to larger','shifted towards the red','shift towards the red','towards red','wavelength is stretched','wavelengths are stretched','wavelength gets longer','wavelengths get longer','doppler'),
 U='The galaxy is moving away from the Earth (receding), so there is a redshift: the observed wavelengths are greater than the emitted wavelengths.',
 V='Galaxies are receding because the universe is expanding. By the Doppler effect the light from a receding source is red-shifted, so the observed wavelengths are longer than the emitted wavelengths.'))
parts.append(dict(pi=2,type='imageChoice',
 K=lab('(b)(ii)')+'Which sketch shows possible positions for the four spectral lines observed on the Earth?',
 answerType='imageChoice',imageOptions=['${o0}','${o1}','${o2}','${o3}'],correctImageIndex='${ci}',imageChoiceMarks='2',
 U='All four lines are present, and each is shifted to a longer wavelength (towards the red end), by a similar amount.',
 V='Redshift moves every line to a longer wavelength. All four lines are still seen; Δλ/λ = v/c is the same for each line, so every line moves to the right by a similar amount (slightly more for the longer wavelengths).'))
parts.append(dict(pi=3,type='calculation',
 K=lab('(b)(iii)')+'The Hubble constant may be taken as ${H0S} × 10<sup>−18</sup> s<sup>−1</sup>.<br><br>Determine the observed wavelength, in nm, of the lowest frequency spectral line of visible light from the star.',
 C2=delta('${dl2}','${dl3}','Δλ/λ=v/c','Δλ/λ=v/c','Δλ=λv/c','Δλ=λ×v/c','Δf/f=v/c','z=v/c','v/c=Δλ/λ','Δλ/λ≈v/c','Δλ/λ','Δλλ=','Δλ=','z=Δλ/λ'),
 C1=kwv('v=h0d','v=h0×d','v=hd','v=h0*d','h0d','h0×d','v=h0 d','${vk}','${vk2}','v=${H0S}','v=h×d'),
 A='${obs3}|${obsi}',tolerance='0.3',
 U='v = H₀d = ${H0S} × 10⁻¹⁸ × ${dS} × 10²⁴ = ${vk} m s⁻¹; Δλ = 656 × v/c = ${dl2} nm; observed wavelength = 656 + ${dl2} = ${obs3} nm',
 V='The lowest frequency line has the longest wavelength, 656 nm. The recession speed is v = H₀d. The Doppler shift gives Δλ/λ ≈ v/c, so Δλ = 656 × v/c, and the observed wavelength is 656 nm + Δλ.'))
ALL+=question(LV,ID+'-Q8',PAPER,'definition','Cosmology,Quantum physics',P8,G8,'Question 8',parts)

# =========================================================================== Q9
SK9=js(r"""(A0,th,ymax,kind)=>{const c=[];const t1=20;
const lam=Math.LN2/th;
for(let i=0;i<=100;i++){const t=t1*i/100;let v;
 if(kind==='ok')v=A0*Math.exp(-lam*t);
 else if(kind==='lin')v=A0+(A0*Math.exp(-lam*t1)-A0)*t/t1;
 else if(kind==='slow')v=A0*Math.exp(-lam*t/2);
 else v=A0*0.55*Math.exp(-lam*t);
 c.push([t,v]);}
const yt=[];for(let y=0;y<=ymax+1e-9;y+=2)yt.push([y,String(y)]);
return skp({x0:0,x1:20,y0:0,y1:ymax,xt:[[0,'0'],[5,'5'],[10,'10'],[15,'15'],[20,'20']],yt:yt,xl:'t / min',yl:'A / 10¹⁴ Bq',c:[c],W:310,H:240});}""")
G9={'sf':SF,'ex':EX,'skp':SKP,'sk9':SK9,
 'th':'+thp.toFixed(1)','A0':'+ap.toFixed(2)','t':'+tp.toFixed(1)','lam':'Math.LN2/(th*60)','lams':'sf(lam,3)','lame':'ex(lam,2)','lamm':'(lam*60).toPrecision(3)',
 'At':'A0*Math.exp(-Math.LN2*t/th)','At3':'At.toPrecision(3)','At2':'At.toPrecision(2)','Ate':'ex(At*1e14,2)','Ate1':'ex(At*1e14,1)',
 'A0e':'ex(A0*1e14,2)','ymax':'Math.ceil((A0+0.2)/2)*2','nh':'t/th','nhs':'nh.toFixed(2)',
 'ci':'Math.floor(cip)','ks':"['lin','slow','low']",
 'opts':"(()=>{const a=[];let j=0;for(let k=0;k<4;k++)a.push(k===ci?sk9(A0,th,ymax,'ok'):sk9(A0,th,ymax,ks[j++]));return a})()",
 'o0':'opts[0]','o1':'opts[1]','o2':'opts[2]','o3':'opts[3]'}
P9={'thp':[8.0,25.0],'ap':[3.0,9.0],'tp':[15.0,30.0],'cip':[0,3.99]}
parts=[]
parts.append(dict(pi=0,type='definition',K=lab('(a)')+'State what is meant by radioactive decay.',
 B=kwv('spontaneous','spontaneously','random and spontaneous','spontaneous and random'),
 B2=andor(['emi','releas','decay','giving out','gives out','radiat','particle','alpha','beta','gamma','ejects','ejected','emits','emitted','disintegrat','breaks down','breaks up','change'],['unstable','nucleus','nuclei','nuclide','isotope','atom']),
 U='Radioactive decay is the spontaneous emission of radiation (alpha, beta or gamma) from an unstable nucleus.',
 V='Radioactive decay is a spontaneous and random process in which an unstable nucleus emits an alpha particle, a beta particle or gamma radiation and becomes more stable.'))
parts.append(dict(pi=1,type='calculation',
 K=lab('(b)(i)')+'An isotope X is radioactive and decays to a stable product with a half-life of ${th} minutes.<br>A sample of X has an activity of ${A0} × 10<sup>14</sup> Bq at time <i>t</i> = 0.<br><br>Calculate the decay constant of X. Give a unit with your answer.',
 C1=kwv('λ=ln2/t½','λ=ln2/t1/2','λ=0.693/t½','λ=0.693/t1/2','t½=ln2/λ','t1/2=ln2/λ','t½=0.693/λ','t1/2=0.693/λ','λ=ln2/t','ln2/${th}','0.693/${th}','ln2/(${th}','0.693/(${th}','ln2÷','0.693÷','λt½=ln2','λt1/2=ln2','λ=ln2÷t½','ln(2)/','ln 2/','ln2/(${th}×60)','0.693/(${th}×60)','ln2/${th}×60'),
 A='${lams}|${lame}|${lamm}',tolerance='2',
 U='λ = ln 2 / t½ = 0.693 / (${th} × 60) = ${lams} s⁻¹',
 V='The decay constant is λ = ln 2 / t½. The unit s⁻¹ requires the half-life to be converted to seconds (${th} min = ${th} × 60 s). (A value in min⁻¹ is equally valid: λ = 0.693 / ${th} min.)'))
parts.append(dict(pi=2,type='calculation',
 K=lab('(b)(ii)')+'Calculate the activity of the sample at <i>t</i> = ${t} minutes.',
 C1=kwv('a=a0e^(-λt)','a=a0e^-λt','a=a0exp(-λt)','a=a0e⁻λt','a=a0e^(−λt)','a=a0e^−λt','a=a0e-λt','a=a0(1/2)^','a=a0(0.5)^','a=a0×0.5^','a=a0/2^','a/a0=','a0e','x=x0e','a=a0×e','a=a0×exp','a=a0 e','exp(-λt)','e^(-λt)','e^-λt','(1/2)^','(0.5)^','0.5^','number of half-lives','half-lives','a=a0 × e'),
 A='${Ate}|${Ate1}',tolerance='2',
 U='A = A₀ e^(−λt) = ${A0e} × e^(−${lams} × ${t} × 60) = ${Ate} Bq',
 V='Activity decays exponentially: A = A₀e^(−λt). With t = ${t} min = ${t} × 60 s (or equivalently t/t½ = ${nhs} half-lives): A = ${A0e} × e^(−λt) = ${Ate} Bq.'))
parts.append(dict(pi=3,type='imageChoice',
 K=lab('(b)(iii)')+'Which sketch shows the variation of the activity <i>A</i> of the sample with <i>t</i> between <i>t</i> = 0 and <i>t</i> = 20.0 minutes?',
 answerType='imageChoice',imageOptions=['${o0}','${o1}','${o2}','${o3}'],correctImageIndex='${ci}',imageChoiceMarks='3',
 U='A curve starting at ${A0} × 10¹⁴ Bq at t = 0 and decreasing exponentially (decreasing gradient, not a straight line) to ${Ate1} Bq at t = 20.0 min.',
 V='Activity falls exponentially from ${A0} × 10¹⁴ Bq. The curve must start at the initial activity, have a gradient that becomes less steep, and be at ${Ate1} Bq when t = 20.0 min (using the value of A at t = 20.0 min from (b)(ii) as a check on the half-life).'))
parts.append(dict(pi=4,type='explain',
 K=lab('(c)')+'A scientist uses a radiation detector to determine the measured count rate of radiation emitted by the sample in 9(b).<br><br>Explain why the measured count rate at any given time is less than the activity of the sample.',
 A=kwv('all directions','every direction','in all directions','emitted in all directions','emitted in different directions','emitted in random directions','emitted randomly in all directions','radiation spreads out','spreads out in all directions','spread out in all directions','not all radiation reaches the detector','not all of the radiation reaches the detector','not all radiation enters the detector','not all of the radiation enters the detector','only some radiation reaches','only a fraction of the radiation','some radiation does not reach the detector','only some of the radiation','spreads over a large area','radiation is emitted in all directions','sphere','spherically','in random directions','randomly in all directions','emitted randomly'),
 B=kwv('absorbed by the sample','absorbed within the sample','absorbed in the sample','self-absorption','self absorption','absorption in the sample','absorbed by the source','absorbed within the source','absorbed inside the source','absorbed in the source','absorbed by the source itself','absorbed inside the sample','absorbed by the material of the sample','absorbed by the sample itself','absorbed by sample','absorbed by source','absorbed within the material'),
 B2=kwv('absorbed by the air','absorbed in the air','absorbed by air','air absorbs','absorption in air','absorption by air','absorbed by the surrounding air','absorbed by the atmosphere','absorbed in air','absorbed by gas in the air','scattered by the air','absorbed by air molecules','absorbed by the air between','absorbed by the air molecules','absorbed by the gas','air between the sample and the detector','absorbed by the air in','absorbed in the atmosphere','absorbed as it travels through the air','absorbed as it passes through the air','absorbed travelling through air'),
 B3=kwv('absorbed by the detector window','absorbed by the window','absorbed in the window','absorbed by the casing','absorbed by the detector casing','absorbed by the detector','detector window absorbs','window absorbs','casing absorbs','not all radiation entering the detector is counted','detector does not detect all','not all radiation entering the detector','detector is not 100% efficient','detector not 100% efficient','detector efficiency','dead time','not all the radiation is detected','not all radiation is detected','not all of the radiation is detected','detector does not count all','some radiation passes through the detector','passes through the detector without being detected','passes through the detector','some passes through without being detected','some passes straight through the detector','some radiation passes straight through','not all of the radiation that enters the detector is detected','not all radiation that enters is detected','not every particle is detected','not all particles are detected','not all particles entering are detected','detector does not detect every','detector cannot detect all','detector cannot count every'),
 maxMarks='3',
 U='Any three of: radiation is emitted in all directions so not all of it enters the detector; some radiation is absorbed in the sample itself; some radiation is absorbed by the air between the sample and the detector; some radiation is absorbed by the detector window / not all radiation entering the detector is detected.',
 V='The activity is the number of nuclei decaying per second in the whole sample. The detector measures only the radiation that actually reaches it and is counted: radiation goes out in all directions, some is absorbed in the sample itself, some is absorbed in the air, and some is absorbed in the detector window or passes through the detector without being counted.'))
ALL+=question(LV,ID+'-Q9',PAPER,'definition','Nuclear physics',P9,G9,'Question 9',parts)

# =========================================================================== Q10
TAB10=('<table style="border-collapse:collapse;margin:8px 0"><caption style="caption-side:top;text-align:center"><b>Table 10.1</b></caption>'
 '<tr><th style="border:1px solid #000;padding:4px 14px">medium</th><th style="border:1px solid #000;padding:4px 14px"><i>Z</i> / kg m<sup>−2</sup> s<sup>−1</sup></th></tr>'
 '<tr><td style="border:1px solid #000;padding:4px 14px">air</td><td style="border:1px solid #000;padding:4px 14px">${za} × 10<sup>2</sup></td></tr>'
 '<tr><td style="border:1px solid #000;padding:4px 14px">water</td><td style="border:1px solid #000;padding:4px 14px">${zw} × 10<sup>6</sup></td></tr>'
 '<tr><td style="border:1px solid #000;padding:4px 14px">glass</td><td style="border:1px solid #000;padding:4px 14px">${zg} × 10<sup>6</sup></td></tr></table>')
G10={'sf':SF,'ex':EX,
 'za':'+zap.toFixed(2)','zw':'+zwp.toFixed(2)','zg':'+zgp.toFixed(2)','rho':'Math.round(rp)',
 'c':'zw*1e6/rho','c3':'c.toPrecision(3)','c4':'c.toPrecision(4)','c2':'ex(c,2)',
 'dZ':'(zg-zw)*1e6','sZ':'(zg+zw)*1e6','R':'Math.pow((zg-zw)/(zg+zw),2)','R3':'R.toPrecision(3)','R4':'R.toFixed(4)','Rt':'(1-R).toPrecision(3)',
 'dZe':'ex(dZ,2)','dZe3':'ex(dZ,3)','sZe':'ex(sZ,2)','sZe3':'ex(sZ,3)','Rair':'Math.pow((zg*1e6-za*1e2)/(zg*1e6+za*1e2),2)','Rair5':'Rair.toFixed(5)','Rair6':'Rair.toPrecision(6)'}
P10={'zap':[4.0,4.8],'zwp':[1.40,1.60],'zgp':[8.5,11.0],'rp':[990,1000]}
parts=[]
parts.append(dict(pi=0,type='explain',K=lab('(a)(i)')+'Explain how ultrasound waves are detected by a piezoelectric transducer.',
 B=kwv('crystal vibrates','crystal oscillates','crystal is made to vibrate','crystal is made to oscillate','causes the crystal to vibrate','causes the crystal to oscillate','crystal to vibrate','crystal to oscillate','vibrates the crystal','oscillates the crystal','crystal is compressed','crystal is deformed','crystal changes shape','crystal is stressed','crystal is compressed and expanded','crystal is compressed and decompressed','crystal vibrations','vibration of the crystal','oscillation of the crystal','compresses the crystal','compresses and expands the crystal','crystal is vibrated','crystal resonates','crystal vibrate','pressure variations','pressure changes on the crystal','changes in pressure on the crystal','sound waves hit the crystal and cause it to vibrate','ultrasound causes vibration','causes it to vibrate','cause it to vibrate','makes it vibrate','make it vibrate','vibrations in the crystal','vibrations of the crystal','vibrations in crystal','oscillations in the crystal','oscillations of the crystal','alternating pressure','varying pressure','changing pressure'),
 B2=kwv('emf is induced','e.m.f. is induced','emf induced','e.m.f. induced','induced emf','induced e.m.f.','potential difference is induced','potential difference across','p.d. across','p.d. is induced','voltage is induced','voltage across the crystal','alternating voltage','alternating e.m.f.','alternating p.d.','alternating emf','varying voltage','varying e.m.f.','varying p.d.','varying emf','voltage is produced','voltage produced','voltage generated','e.m.f. produced','emf produced','e.m.f. generated','emf generated','potential difference is produced','potential difference produced','potential difference generated','p.d. is produced','p.d. produced','p.d. generated','electrical signal','electric signal','alternating potential difference','potential difference of the same frequency','voltage of the same frequency','voltage is created','voltage created','p.d. is generated','e.m.f. across','emf across','voltage across','potential difference between','voltage between','p.d. between','e.m.f. between','emf between','charge is produced','charge produced','charge is generated','charge generated','current produced','current is produced','electrical current','alternating current','voltage output','p.d. output','e.m.f. output'),
 U='The ultrasound wave causes the crystal to vibrate (oscillate), and this produces an alternating e.m.f. (p.d.) across the crystal.',
 V='In a piezoelectric transducer the pressure variations in the ultrasound wave make the crystal vibrate. The changing deformation of the crystal induces an alternating e.m.f. (potential difference) across it, which has the same frequency as the ultrasound.'))
parts.append(dict(pi=1,type='definition',K=lab('(a)(ii)')+'Define the specific acoustic impedance of a medium.',
 M=kwv('density × speed','density x speed','density×speed','density times speed','density multiplied by speed','product of density and speed','density*speed','density × velocity','density x velocity','density times velocity','density multiplied by velocity','product of density and velocity','density and speed','density and velocity','ρc','ρv','ρ×c','ρ×v','z=ρc','z=ρv','z=ρ×c','z=ρ×v','density × the speed','density x the speed','density × sound','density x sound','density times the speed','density multiplied by the speed','product of the density and the speed','product of density and the speed','product of the density and speed','ρ × c','ρ × v','z=ρ × c','z=ρ × v','z = ρc','z = ρv','cρ','vρ','c×ρ','v×ρ','c x ρ','v x ρ','speed×density','speed x density','velocity×density','velocity x density'),
 A=kwv('speed of sound','speed of ultrasound','velocity of sound','velocity of ultrasound','speed of the sound','speed of the ultrasound','speed of waves','speed of the waves','speed of sound in the medium','speed of ultrasound in the medium','speed of sound in that medium','speed of sound in the material','speed of sound in the substance','speed of sound in the medium','speed of sound through','sound speed','ultrasound speed','speed of ultrasound waves','speed of the ultrasound waves','velocity of the sound','velocity of the ultrasound','velocity of waves','velocity of the waves','sound velocity','ρc','ρv','z=ρc','z=ρv','cρ','vρ','ρ×c','ρ×v','z=ρ×c','z=ρ×v','ρ × c','ρ × v','c×ρ','v×ρ'),
 U='The specific acoustic impedance of a medium is the product of the density of the medium and the speed of sound (ultrasound) in the medium: Z = ρc.',
 V='Specific acoustic impedance Z = ρc, where ρ is the density of the medium and c is the speed of sound in that medium.'))
parts.append(dict(pi=2,type='calculation',
 K=lab('(b)(i)')+'Table 10.1 lists the specific acoustic impedances <i>Z</i> of air, water and glass.'+TAB10+'The density of water is ${rho} kg m<sup>−3</sup>.<br><br>Determine the speed of sound in water.',
 C1=kwv('z=ρc','z=ρv','c=z/ρ','v=z/ρ','z=ρ×c','z=ρ×v','c=z÷ρ','v=z÷ρ','z=cρ','z=vρ','ρ=z/c','ρ=z/v','z/ρ','${zw}×10⁶/${rho}','${zw}×10^6/${rho}','${zw}e6/${rho}','${zw}x10^6/${rho}','${zw}×10⁶÷${rho}','z/${rho}','${zw}×10⁶/','${zw}×10^6/'),
 A='${c3}|${c4}',tolerance='1',
 U='Z = ρc, so c = Z / ρ = ${zw} × 10⁶ / ${rho} = ${c3} m s⁻¹',
 V='Use Z = ρc with the impedance of water from Table 10.1 and the density of water.'))
parts.append(dict(pi=3,type='calculation',
 K=lab('(b)(ii)')+'Calculate, to three significant figures, the intensity reflection coefficient for sound incident on a water-glass boundary.',
 C1=kwv('(z2−z1)²/(z2+z1)²','(z2-z1)^2/(z2+z1)^2','(z2−z1)^2/(z2+z1)^2','((z2−z1)/(z2+z1))²','((z2-z1)/(z2+z1))^2','(z2-z1)²','(z2−z1)²','z2−z1','z2-z1','z1-z2','z1−z2','(zg-zw)','(zg−zw)','(zw-zg)','(zw−zg)','(zglass','(zwater','${dZe}','${dZe3}','${sZe}','${sZe3}','i_r/i_0=','ir/i0=','ir/io=','(z₂−z₁)','(z₂-z₁)','(z1+z2)','(z1−z2)','(z1-z2)','(z2+z1)','(z₁−z₂)','z₁-z₂','(z2-z1)','(z2 − z1)','(z2 - z1)','(zglass-zwater)','(zglass−zwater)'),
 A='${R3}|${R4}',tolerance='1',
 U='I_R / I₀ = ((Z₂ − Z₁) / (Z₂ + Z₁))² = ((${zg} − ${zw}) × 10⁶ / ((${zg} + ${zw}) × 10⁶))² = ${R3}',
 V='Use the intensity reflection coefficient α = (Z₂ − Z₁)²/(Z₂ + Z₁)² with the impedances of water and glass from Table 10.1. The coefficient has no unit.'))
parts.append(dict(pi=4,type='explain',
 K=lab('(b)(iii)')+'Explain, without calculation, what happens when sound is incident on an air-glass boundary.',
 A=kwv('very different','big difference','large difference','greater difference','great difference','mismatch','mismatched','not matched','differ greatly','differ a lot','differ significantly','large change in impedance','impedances are very different','huge difference','very large difference','different impedance','large impedance difference','difference in impedance is large','difference in z is large','difference between impedances is large','large difference in impedance','big difference in impedance','large difference in z','big difference in z','impedance of air is much smaller','impedance of air is much less','impedance of glass is much larger','impedance of glass is much greater','z of air is much smaller','z of glass is much larger','z of air is much less','z of glass is much greater','impedance of air is very small','air has a much lower impedance','glass has a much higher impedance','glass has much greater impedance','air has much smaller impedance','air has much lower impedance','glass has much larger impedance','impedance of glass is much higher','impedance of air is much lower'),
 B=kwv('close to 1','near to 1','approximately 1','almost 1','nearly 1','about 1','≈1','close to one','reflection coefficient is large','reflection coefficient is high','reflection coefficient is almost','coefficient is nearly','intensity reflection coefficient is close','large reflection coefficient','high reflection coefficient','approaches 1','tends to 1','very high reflection coefficient','reflection coefficient is very high','reflection coefficient is very large','reflection coefficient is approximately','reflection coefficient is nearly','reflection coefficient is near','coefficient is close','coefficient is approximately','coefficient is almost','coefficient is near','coefficient close to','coefficient approximately','coefficient nearly','coefficient almost','coefficient near'),
 B2=andor(['almost all','nearly all','most','majority','large proportion','large fraction','high proportion','mostly','much of','almost completely','large amount','large percentage','high percentage','nearly entire','almost entire','nearly total','almost total','total','all'],['reflect']),
 B3=kwv('almost no','hardly any','negligible','nearly no','tiny','very small','small proportion','small fraction','small amount','minimal','almost none','not much','barely','virtually no','almost zero','nothing is transmitted','nothing transmitted','no ultrasound is transmitted','no sound is transmitted','none is transmitted','none transmitted','no transmission','not transmitted','little is transmitted','little transmitted','very little','little ultrasound','little sound','little energy','little intensity','small transmission','little transmission','hardly any transmitted','hardly any is transmitted','barely any transmitted','very little transmitted','very little is transmitted','very little sound is transmitted','very little ultrasound is transmitted','almost no sound is transmitted','almost no ultrasound is transmitted','almost nothing is transmitted','almost nothing transmitted','little penetration','little passes into','very little passes into','hardly any passes into','almost none passes into','almost none enters','almost none transmitted','almost none is transmitted','almost no energy is transmitted','almost no intensity is transmitted'),
 maxMarks='3',
 U='Any three of: the impedances of air and glass are very different (large mismatch); the intensity reflection coefficient is close to 1; almost all of the sound is reflected; almost none (very little) is transmitted into the glass.',
 V='Z for air (${za} × 10²) is vastly smaller than Z for glass (${zg} × 10⁶). There is a very large impedance mismatch, so the intensity reflection coefficient is almost 1: nearly all of the incident intensity is reflected and almost none is transmitted.'))
ALL+=question(LV,ID+'-Q10',PAPER,'definition','Medical physics',P10,G10,'Question 10',parts)

if __name__=='__main__':
    start=int(sys.argv[1]) if len(sys.argv)>1 else 547
    write_json(ALL,'new42m.json',start=start)
    from collections import Counter
    print(len(ALL),'rows',dict(Counter(r['id'] for r in ALL)))
