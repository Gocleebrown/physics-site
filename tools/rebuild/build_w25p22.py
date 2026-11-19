##v1  AS 9702/22 Oct/Nov 2025 (w25) -- built from the real QP + MS, every number a parameter, figures generated.
#   python3 build_w25p22.py out.json      (rows for the 6 questions, 60 marks)
import json, sys
sys.path.insert(0, '.')
from rowlib import *
from jshelpers import GSVG

LV = 'AS'; PAPER = '9702_w25_p22'
def lab(s): return '<b>' + s + '</b> '
def kwv(*alts):
    out = []
    for a in alts:
        out.append(a)
    return '|'.join(dict.fromkeys(out))

# ---------------------------------------------------------------- shared JS helpers (each id carries its own copy)
SF = "(x,n)=>String(+x.toPrecision(n))"
EX = "(x,d)=>x.toExponential(d).replace('e+','e')"
US = "(n)=>String(n).replace(/-/g,'⁻').replace(/[0-9]/g,d=>'⁰¹²³⁴⁵⁶⁷⁸⁹'[d])"
SB = "(n)=>String(n).replace(/[0-9]/g,d=>'₀₁₂₃₄₅₆₇₈₉'[d])"
SCI = "(x,d)=>{const p=x.toExponential(d).split('e');return p[0]+' × 10'+us(+p[1])}"
BASE = {'sf': SF, 'ex': EX, 'us': US, 'sb': SB, 'sci': SCI}
def G_(*names, **more):
    g = {n: BASE[n] for n in names}
    g.update(more)
    return g

HD = "'<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 '+W+' '+H+'\" style=\"max-width:'+W+'px;width:100%;background:#fff;display:block;margin:10px 0\" font-family=\"Arial,sans-serif\" font-size=\"14\">'"
AH = "'<defs><marker id=\"ah\" viewBox=\"0 0 10 10\" refX=\"9\" refY=\"5\" markerWidth=\"7\" markerHeight=\"7\" orient=\"auto-start-reverse\"><path d=\"M0,0 L10,5 L0,10 z\" fill=\"#000\"/></marker></defs>'"
LN = "const ln=(a,b,c,d,x)=>'<line x1=\"'+a+'\" y1=\"'+b+'\" x2=\"'+c+'\" y2=\"'+d+'\" stroke=\"#000\" stroke-width=\"1.6\"'+(x||'')+'/>';"
AR = "const ar=(a,b,c,d)=>ln(a,b,c,d,' marker-end=\"url(#ah)\"');"
def js(s): return s.replace('@HD@', HD).replace('@AH@', AH).replace('@LN@', LN).replace('@AR@', AR)
def cap(tag): return "return s+'<p style=\"text-align:center;margin:0 0 10px\"><b>Figure '+" + tag + "+'</b></p>';"
UNITS_VAR = js(r"""(arr)=>{const sup=n=>String(n).replace(/-/g,'⁻').replace(/[0-9]/g,d=>'⁰¹²³⁴⁵⁶⁷⁸⁹'[d]);
const perm=(a)=>a.length<=1?[a]:a.flatMap((x,i)=>perm(a.filter((_,j)=>j!==i)).map(p=>[x,...p]));
const out=[];for(const p of perm(arr)){out.push(p.map(([s,e])=>e==1?s:s+sup(e)).join(' '));out.push(p.map(([s,e])=>e==1?s:s+e).join(' '));out.push(p.map(([s,e])=>e==1?s:s+'^'+e).join(' '));out.push(p.map(([s,e])=>e==1?s:s+'^('+e+')').join(' '));}
return out;}""")
UDISP = "(arr)=>arr.map(([s,e])=>e==1?s:s+'<sup>'+String(e).replace('-','−')+'</sup>').join(' ')"

# =========================================================================== Q1  Air pressure on a mountain
G1 = G_('sf', 'ex', uv=UNITS_VAR, ud=UDISP,
  QL='[["air temperature",[["K",1]],"scalar"],["air pressure",[["kg",1],["m",-1],["s",-2]],"scalar"],["wind velocity",[["m",1],["s",-1]],"vector"],["wind speed",[["m",1],["s",-1]],"scalar"],["air density",[["kg",1],["m",-3]],"scalar"],["upthrust on the balloon",[["kg",1],["m",1],["s",-2]],"vector"]]',
  i1='Math.floor(qa)', i2='(i1+1+Math.floor(qk))%6', q1='QL[i1]', q2='QL[i2]',
  n1='q1[0]', n2='q2[0]', u1='ud(q1[1])', u2='ud(q2[1])', t1='q1[2]', t2='q2[2]',
  ukw='JSON.stringify([uv(q1[1]),uv(q2[1])])',
  svkw="JSON.stringify(t1===t2?[[t1]]:[['scalar'],['vector']])",
  rho='+rp.toFixed(2)', r='+rr.toFixed(2)',
  V='4/3*Math.PI*r*r*r', Vs='sf(V,3)', U='rho*9.81*V', Us='sf(U,2)', Ud='sf(U,3)',
  Wb='Math.round(U*fp)', mb='Wb/9.81', mbs='sf(mb,3)', Fn='U-Wb', Fns='sf(Fn,3)', acc='Fn/mb', accs='sf(acc,2)',
  pw='Math.floor(pwi)', pk='Math.round(pkp)', pF='Math.round(pFp)', pv='Math.round(pvp)', pc='pk+pF+pw*pv',
  cv='+cvp.toFixed(1)', ab='cv*pc/100', abs1='sf(ab,1)', abs2='sf(ab,2)')
P1 = {'qa': [0, 5.99], 'qk': [0, 4.99], 'rp': [1.00, 1.30], 'rr': [0.70, 1.10], 'fp': [0.35, 0.75],
      'pwi': [2, 3.99], 'pkp': [3, 8], 'pFp': [2, 6], 'pvp': [2, 6], 'cvp': [1.2, 3.6]}
parts = []
parts.append(dict(pi=0, type='explain',
 K=lab('(a)(i)') + 'Scientists measure the physical quantities <i>${n1}</i> and <i>${n2}</i> at each location. State the SI base units of each of these quantities, in the order given.',
 B='${ukw}',
 U='${n1}: ${u1}; ${n2}: ${u2}',
 V='Base units come from the definition of each quantity. Express each quantity in terms of kg, m, s, A and K only: for example a force has base units kg m s<sup>−2</sup>, and pressure = force / area.'))
parts.append(dict(pi=1, type='explain',
 K=lab('(a)(ii)') + 'State whether each of the quantities in (a)(i) is a scalar or a vector.',
 B='${svkw}',
 U='${n1}: ${t1}; ${n2}: ${t2}',
 V='A vector has direction as well as magnitude; a scalar has magnitude only. Air pressure acts equally in all directions at a point, so it is a scalar.'))
parts.append(dict(pi=2, type='calculation',
 K=lab('(b)(i)') + 'At one location the density of the air is ${rho} kg m<sup>−3</sup>. A spherical weather balloon is filled with a gas and released from rest. The balloon has radius ${r} m.<br><br>Calculate the upthrust acting on the balloon when it is released.',
 C1=kwv('ρgv', 'upthrust=ρvg', 'f=ρgv', 'rhogv', 'rho g v', 'weight of air displaced', 'weight of fluid displaced', '4/3πr', '4πr', '${Vs}', '${rho}×9.81', '${rho}x9.81'),
 A='${Us}|${Ud}', tolerance='2',
 U='upthrust = ρgV = ${rho} × 9.81 × (4/3 × π × ${r}³) = ${Ud} N',
 V='The upthrust equals the weight of the air displaced by the balloon, F = ρgV, where V = 4πr³/3 is the volume of the sphere.'))
parts.append(dict(pi=3, type='explain',
 K=lab('(b)(ii)') + 'Explain why an upthrust acts on the balloon.',
 B=kwv('difference in pressure', 'pressure difference', 'pressure at the bottom is greater', 'pressure at the bottom is higher', 'pressure is greater at the bottom', 'pressure increases with depth', 'pressure increases with depth', 'pressure higher at the bottom', 'pressure at bottom greater', 'pressure greater below', 'pressure at the bottom is larger', 'pressure lower at the top', 'pressure is lower at the top', 'different pressure'),
 B2=kwv('force on the bottom is greater', 'force at the bottom is greater', 'force on bottom greater', 'upward force is greater than the downward force', 'upward force greater than downward force', 'resultant force is upwards', 'resultant force upwards', 'net force is upwards', 'net force upwards', 'force on the bottom is larger', 'force on the bottom is bigger', 'force from the bottom is greater', 'upward force is larger', 'upward force bigger', 'upwards force greater', 'upwards force is greater'),
 U='The air pressure is greater at the bottom of the balloon than at the top (pressure increases with depth), so the upward force on the bottom is greater than the downward force on the top. The resultant force is upwards: the upthrust.',
 V='Pressure in a fluid increases with depth (Δp = ρgΔh). The pressure difference between the bottom and top of the balloon gives a larger upward force than downward force, and this resultant is the upthrust.'))
parts.append(dict(pi=4, type='calculation',
 K=lab('(b)(iii)') + 'The balloon has weight ${Wb} N.<br><br>Calculate the magnitude of the initial acceleration of the balloon.',
 C2=kwv('${Fns}', '${Fn}'),
 C1=kwv('${mbs}', '${Wb}/9.81', '${Wb}÷9.81', 'W=mg', 'w=mg', 'm=w/g', 'm=${Wb}/9.81', 'F=ma', 'f=ma', 'a=f/m', 'resultant force=ma'),
 A='${accs}', tolerance='3',
 U='resultant force F = ${Ud} − ${Wb} = ${Fns} N;  mass m = ${Wb} / 9.81 = ${mbs} kg;  a = F / m = ${accs} m s⁻²',
 V='The resultant force is the upthrust minus the weight. The mass comes from the weight, m = W/g. Then use Newton’s second law, a = F/m.'))
parts.append(dict(pi=5, type='calculation',
 K=lab('(c)') + 'A quantity <i>c</i> relating to the motion of the balloon is calculated from three measured quantities <i>k</i>, <i>F</i> and <i>v</i> using the formula<br><br><i>c</i> = 2<i>kF</i> / <i>v</i><sup>${pw}</sup>.<br><br>The percentage uncertainties in the measured quantities are: <i>k</i> ${pk}%, <i>F</i> ${pF}%, <i>v</i> ${pv}%. The calculated value of <i>c</i> is ${cv}.<br><br>Determine the absolute uncertainty in <i>c</i>.',
 C1='${pc}', A='${abs1}|${abs2}', tolerance='3',
 U='percentage uncertainty in c = ${pk} + ${pF} + (${pw} × ${pv}) = ${pc}%;  absolute uncertainty = ${cv} × ${pc}/100 = ±${abs1}',
 V='When quantities are multiplied or divided, their percentage uncertainties add. A power multiplies the percentage uncertainty by the power, so v<sup>${pw}</sup> contributes ${pw} × ${pv}%. The absolute uncertainty is that percentage of the calculated value.'))
ALL = question(LV, '9702-25-22-Q1', PAPER, 'explain', 'Units,Pressure,Dynamics,Measurement', P1, G1,
 'Air pressure on a mountain: units, upthrust and uncertainty', parts)

# =========================================================================== Q2  Spacecraft thrusters
FIGCRAFT = js(r"""(dA,dC)=>{const W=520,H=290,cx=270,cy=150,kx=60,ky=120;
let s=@HD@+@AH@;
@LN@
@AR@
s+='<rect x="'+(cx-170)+'" y="'+(cy-60)+'" width="340" height="120" rx="10" fill="#f2f2f2" stroke="#000" stroke-width="1.6"/>';
s+='<circle cx="'+cx+'" cy="'+cy+'" r="4"/><text x="'+(cx+8)+'" y="'+(cy+20)+'">centre of gravity</text>';
const ax=cx-dA*kx;
s+=ar(ax,cy+60,ax,cy+10)+'<text x="'+(ax-8)+'" y="'+(cy+84)+'" text-anchor="end">thruster A</text>';
s+=ar(ax+46,cy+60,ax+46,cy+10)+'<text x="'+(ax+54)+'" y="'+(cy+84)+'">thruster B</text>';
const cyy=cy-dC*ky;
s+=ar(cx+170,cyy,cx+110,cyy)+'<text x="'+(cx+176)+'" y="'+(cyy+5)+'">thruster C</text>';
s+=ln(cx,cy,ax,cy,' stroke-dasharray="4,3"')+ln(ax,cy-14,ax,cy+14,'')+'<text x="'+((cx+ax)/2)+'" y="'+(cy-8)+'" text-anchor="middle">'+dA+' m</text>';
s+=ln(cx,cy,cx,cyy,' stroke-dasharray="4,3"')+'<text x="'+(cx-8)+'" y="'+((cy+cyy)/2+4)+'" text-anchor="end">'+dC+' m</text>';
s+='<text x="'+(W-12)+'" y="24" text-anchor="end">upwards ↑   leftwards ←</text><text x="'+(W-12)+'" y="'+(H-8)+'" text-anchor="end">not to scale</text></svg>';
""" + cap("'2.1'") + "}")
SPD = js(r"""(kind)=>{const W=300,H=230,L=46,R=14,T=14,B=44,pw=W-L-R,ph=H-T-B;
let s='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 '+W+' '+H+'" width="'+W+'" height="'+H+'" font-family="Arial,sans-serif" font-size="13"><rect width="'+W+'" height="'+H+'" fill="#fff"/>';
s+='<line x1="'+L+'" y1="'+T+'" x2="'+L+'" y2="'+(T+ph)+'" stroke="#000"/><line x1="'+L+'" y1="'+(T+ph)+'" x2="'+(L+pw)+'" y2="'+(T+ph)+'" stroke="#000"/>';
s+='<text x="'+(L+pw*0.15)+'" y="'+(T+ph+17)+'" text-anchor="middle">t<tspan font-size="10" dy="4">1</tspan></text><text x="'+(L+pw*0.9)+'" y="'+(T+ph+17)+'" text-anchor="middle">t<tspan font-size="10" dy="4">2</tspan></text>';
s+='<line x1="'+(L+pw*0.15)+'" y1="'+(T+ph-4)+'" x2="'+(L+pw*0.15)+'" y2="'+(T+ph+4)+'" stroke="#000"/><line x1="'+(L+pw*0.9)+'" y1="'+(T+ph-4)+'" x2="'+(L+pw*0.9)+'" y2="'+(T+ph+4)+'" stroke="#000"/>';
s+='<text x="'+(L-6)+'" y="'+(T+ph+4)+'" text-anchor="end">0</text><text x="'+(L+pw/2)+'" y="'+(H-6)+'" text-anchor="middle">time</text><text transform="translate(14,'+(T+ph/2)+') rotate(-90)" text-anchor="middle">speed</text>';
let p=[];for(let i=0;i<=60;i++){const u=i/60;let y;
 if(kind==='ok')y=u*u;else if(kind==='lin')y=u;else if(kind==='sqrt')y=Math.sqrt(u);else y=1-u*u;
 const x=L+pw*(0.15+0.75*u);p.push(x.toFixed(1)+','+(T+ph-ph*0.9*y).toFixed(1));}
s+='<polyline fill="none" stroke="#000" stroke-width="2.4" points="'+p.join(' ')+'"/></svg>';
return s;}""")
G2 = G_('sf', 'ex', fig=FIGCRAFT, spd=SPD,
  dA='+dAp.toFixed(1)', dC='+dCp.toFixed(2)', FA='Math.round(FAp/10)*10', Mres='+Mp.toFixed(0)',
  FC='Math.round((FA*dA-Mres)/dC/10)*10', MA='FA*dA', MC='FC*dC', Mr='MA-MC', Mrs='sf(Mr,2)', MAs='sf(MA,3)', MCs='sf(MC,3)',
  f21='fig(dA,dC)',
  ci='Math.floor(cip)', ks="['lin','sqrt','dec']",
  opts="(()=>{const a=[];let j=0;for(let k=0;k<4;k++)a.push(k===ci?spd('ok'):spd(ks[j++]));return a})()",
  o0='opts[0]', o1='opts[1]', o2='opts[2]', o3='opts[3]',
  Ff='Math.round(Ffp/100)*100', tf='+tfp.toFixed(2)', dv='+dvp.toFixed(1)', Mt='Math.round(Mtp/100)*100',
  J='Ff*tf', Js='sf(J,3)', mp0='J/dv', mp='+mp0.toPrecision(2)', mc='Mt-mp', vc='J/mc', vcs='sf(vc,2)', Mts='sci(Mt,1)',
  mp_ok='mp<Mt')
P2 = {'dAp': [1.2, 2.0], 'dCp': [0.30, 0.60], 'FAp': [40, 90], 'Mp': [5, 15], 'cip': [0, 3.99],
      'Ffp': [4500, 6500], 'tfp': [0.30, 0.45], 'dvp': [7.0, 10.0], 'Mtp': [2000, 3200]}
G2['sci'] = SCI; G2['us'] = US
parts = []
parts.append(dict(pi=0, type='calculation',
 K=lab('(a)(i)') + 'A spacecraft in deep space uses jets of hot gas from its thrusters to change its velocity. Figure 2.1 shows a side view of the spacecraft and some of its thrusters.${f21}Thruster A is a distance of ${dA} m leftwards from the centre of gravity of the spacecraft. Thruster C is a distance of ${dC} m upwards from the centre of gravity. Thrusters A and B can produce forces on the spacecraft in the upwards direction only. Thruster C can produce a force on the spacecraft in the leftwards direction only. All the thrusters shown produce forces entirely in the same plane as the centre of gravity.<br><br>Thruster A is activated, producing a force of ${FA} N upwards on the spacecraft. Thruster C is also activated, producing a force of ${FC} N in the leftwards direction on the spacecraft.<br>Calculate the resultant moment due to these forces about the centre of gravity.',
 C1=kwv('${MAs}', '${MCs}', '${FA}×${dA}', '${FA}x${dA}', '${FC}×${dC}', '${FC}x${dC}', '${FA}*${dA}', '${FC}*${dC}'),
 A='${Mrs}', tolerance='3',
 U='moment of A = ${FA} × ${dA} = ${MAs} N m;  moment of C = ${FC} × ${dC} = ${MCs} N m (opposite sense);  resultant moment = ${MAs} − ${MCs} = ${Mrs} N m',
 V='The moment of a force about a point is force × perpendicular distance from the point. The force from A acts upwards a horizontal distance from the centre of gravity, and the force from C acts leftwards at a vertical distance. They turn the spacecraft in opposite senses, so subtract the two moments.'))
parts.append(dict(pi=1, type='explain',
 K=lab('(a)(ii)') + 'State and explain whether the forces from A and C are a couple.',
 B=andor(['not a couple', 'not couple', 'no', 'isnt a couple', 'arent a couple', 'is not a couple', 'are not a couple', 'cannot be a couple', 'not a pair'], ['resultant force', 'not equal', 'unequal', 'not parallel', 'not opposite', 'same point', 'not zero', 'non-zero', 'nonzero', 'different magnitude', 'different size', 'perpendicular', 'at right angles', 'not in opposite', 'different direction']),
 U='Not a couple: the resultant force of A and C is not zero (the forces are not equal in magnitude, not parallel and not in opposite directions).',
 V='A couple is a pair of forces equal in magnitude, opposite in direction and not acting along the same line, so the resultant force is zero. These two forces are perpendicular and unequal, so they are not a couple.'))
parts.append(dict(pi=2, type='explain',
 K=lab('(b)') + 'Thrusters A and C are now switched off and the spacecraft is stationary. Thruster B is activated at time <i>t</i><sub>1</sub>, producing a constant force on the spacecraft until the fuel runs out at time <i>t</i><sub>2</sub>. As the fuel is used, the total mass of the spacecraft decreases.<br><br>Which graph shows the variation of the speed of the spacecraft with time from <i>t</i><sub>1</sub> to <i>t</i><sub>2</sub>?',
 answerType='imageChoice', imageOptions='["${o0}","${o1}","${o2}","${o3}"]', correctImageIndex='${ci}', imageChoiceMarks='2',
 U='A curve starting from zero speed at t₁ with a positive and increasing gradient up to t₂.',
 V='The force is constant but the mass decreases, so the acceleration a = F/m increases. The gradient of the speed–time graph is the acceleration, so the graph starts at zero speed with a positive gradient that gets steeper.'))
parts.append(dict(pi=3, type='definition',
 K=lab('(c)(i)') + 'The spacecraft now splits apart into a carrier and a payload. State the principle of conservation of momentum.',
 B=andor(['total momentum', 'sum of the momenta', 'sum of momentum', 'momentum of a system', 'momentum of the system', 'momentum before', 'total linear momentum', 'momentum of the objects', 'momentum of the bodies', 'momentum of an isolated', 'sum of momenta'], ['constant', 'conserved', 'same', 'unchanged', 'equal', 'remains', 'does not change', 'stays', 'after', 'afterwards']),
 B2=kwv('isolated', 'closed system', 'no external force', 'no resultant external force', 'no resultant force', 'no net external force', 'no net force', 'no external forces', 'without external force', 'no outside force'),
 U='The total momentum of a system of interacting bodies is constant (momentum before = momentum after), provided no resultant external force acts on the system.',
 V='In any interaction the total linear momentum of an isolated system (no resultant external force) is conserved.'))
parts.append(dict(pi=4, type='calculation',
 K=lab('(c)(ii)') + 'During the split, an average force of ${Ff} N acts on the payload for a time of ${tf} s. The velocity of the payload increases by ${dv} m s<sup>−1</sup> in the upwards direction. The combined mass of the carrier and payload is ${Mts} kg.<br><br>Show that the mass of the payload is ${mp} kg. Give your answer to 2 significant figures.',
 C1=kwv('Δp=fΔt', 'impulse', 'ft=mΔv', 'ft=mv', 'fΔt=mΔv', 'f=ma', 'f=mΔv/Δt', 'a=Δv/Δt', 'm=ft/Δv', 'm=ft/v', '${Ff}×${tf}', '${Ff}x${tf}', '${Ff}*${tf}', '${Js}'),
 A='${mp}', tolerance='2',
 U='impulse = FΔt = Δp, so m = FΔt / Δv = ${Ff} × ${tf} / ${dv} = ${mp0.toFixed(1)} ≈ ${mp} kg',
 V='The force acting for a time gives an impulse equal to the change of momentum of the payload: FΔt = mΔv. Rearrange for m and substitute.'))
G2['mp0f'] = '+mp0.toFixed(1)'
parts[-1]['U'] = 'impulse = FΔt = Δp, so m = FΔt / Δv = ${Ff} × ${tf} / ${dv} = ${mp0f} ≈ ${mp} kg'
parts.append(dict(pi=5, type='calculation',
 K=lab('(c)(iii)') + 'Calculate the magnitude of the change in velocity of the carrier.',
 C2=kwv('${Js}', '${Ff}×${tf}', '${Ff}x${tf}'),
 C1=kwv('${mc}', '(${Mt}−${mp})', '(${Mt}-${mp})', '${Mt}−${mp}', '${Mt}-${mp}', 'conservation of momentum', 'momentum is conserved', 'f=ma', 'a=f/m', 'a=${Ff}/${mc}'),
 A='${vcs}', tolerance='3',
 U='momentum gained by payload = FΔt = ${Js} N s, so the carrier gains the same momentum in the opposite direction: ${Js} = (${Mts} − ${mp}) × v, so v = ${vcs} m s⁻¹',
 V='Momentum is conserved, so the carrier has the same magnitude of momentum change as the payload, in the opposite direction. The mass of the carrier is the combined mass minus the payload mass. (Using the payload mass 2 s.f. value is fine.)'))
ALL += question(LV, '9702-25-22-Q2', PAPER, 'calculation', 'Forces including Density and pressure,Dynamics', P2, G2,
 'Spacecraft thrusters: moments and momentum', parts)

# =========================================================================== Q3  Spring and pulley
FIGSPRING = js(r"""(n,showF)=>{const W=560,H=150+Math.max(0,n-1)*52,cy=H/2,px=380;
let s=@HD@+@AH@;
@LN@
@AR@
s+='<rect x="30" y="'+(cy-26-(n-1)*26)+'" width="12" height="'+(52+(n-1)*52)+'" fill="#bbb" stroke="#000"/><text x="36" y="'+(H-6)+'" text-anchor="middle" font-size="12">fixed end</text>';
for(let k=0;k<n;k++){const y=cy+(k-(n-1)/2)*52;let d='M42,'+y;
 for(let i=0;i<7;i++){d+=' L'+(80+i*34)+','+(y+(i%2?-14:14));}
 d+=' L'+(80+7*34)+','+y+' L'+px+','+y;s+='<path d="'+d+'" fill="none" stroke="#000" stroke-width="1.6"/>';}
s+='<rect x="'+px+'" y="'+(cy-30-(n-1)*26)+'" width="56" height="'+(60+(n-1)*52)+'" fill="#f2f2f2" stroke="#000" stroke-width="1.6"/><circle cx="'+(px+28)+'" cy="'+cy+'" r="22" fill="#fff" stroke="#000" stroke-width="1.6"/><circle cx="'+(px+28)+'" cy="'+cy+'" r="3"/>';
s+='<text x="'+(px+28)+'" y="'+(cy-(n-1)*26-36)+'" text-anchor="middle">pulley frame</text>';
s+='<path d="M'+(px+120)+','+(cy-22)+' L'+(px+28)+','+(cy-22)+' A22,22 0 0 0 '+(px+28)+','+(cy+22)+' L'+(px+120)+','+(cy+22)+'" fill="none" stroke="#000" stroke-width="1.6"/>';
s+='<text x="'+(px+126)+'" y="'+(cy+4)+'">cable</text>';
s+='<text x="'+(W-12)+'" y="'+(H-8)+'" text-anchor="end">view from above, not to scale</text></svg>';
""" + cap("showF") + "}")
PUL = js(r"""(kind)=>{const W=320,H=200,cx=130,cy=100;
let s='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 '+W+' '+H+'" width="'+W+'" height="'+H+'" font-family="Arial,sans-serif" font-size="15"><rect width="'+W+'" height="'+H+'" fill="#fff"/>'+@AH@;
@LN@
@AR@
s+='<rect x="'+(cx-52)+'" y="'+(cy-52)+'" width="104" height="104" fill="#f2f2f2" stroke="#000" stroke-width="1.6"/><circle cx="'+cx+'" cy="'+cy+'" r="30" fill="#fff" stroke="#000" stroke-width="1.6"/><circle cx="'+cx+'" cy="'+cy+'" r="3"/>';
if(kind==='ok'||kind==='oneT'||kind==='noF'){s+='';}
const F=(dir)=>{ if(dir==='L')return ar(cx-52,cy,cx-120,cy)+'<text x="'+(cx-98)+'" y="'+(cy-8)+'" font-style="italic">F</text>'; return ar(cx+52,cy,cx+120,cy)+'<text x="'+(cx+86)+'" y="'+(cy-8)+'" font-style="italic">F</text>';};
const T=(y,dir)=>{ if(dir==='R')return ar(cx+30,y,cx+110,y)+'<text x="'+(cx+86)+'" y="'+(y-6)+'" font-style="italic">T</text>'; return ar(cx-30,y,cx-110,y)+'<text x="'+(cx-86)+'" y="'+(y-6)+'" font-style="italic">T</text>';};
if(kind==='ok'){s+=F('L')+T(cy-30,'R')+T(cy+30,'R');}
else if(kind==='oneT'){s+=F('L')+T(cy-30,'R');}
else if(kind==='swap'){s+=F('R')+T(cy-30,'L')+T(cy+30,'L');}
else {s+=T(cy-30,'R')+T(cy+30,'R');}
return s+'</svg>';}""")
G3 = G_('sf', 'ex', fig=FIGSPRING, pul=PUL,
  k='Math.round(kp/10)*10', F='Math.round(Fp/10)*10', n='Math.floor(np_)', T='F/2', x1='F/k', x1s='sf(x1,3)', x2='T/k', x2s='sf(x2,3)',
  E1='0.5*F*x1', E2='n*0.5*(F/n)*(F/n/k)', ratio='E1/E2', ratios='sf(ratio,2)', Fn='F/n', xn='Fn/k', xns='sf(xn,3)',
  f31="fig(1,'3.1')", f33="fig(n,'3.2')", ci='Math.floor(cip)', ks="['oneT','swap','noF']",
  opts="(()=>{const a=[];let j=0;for(let q=0;q<4;q++)a.push(q===ci?pul('ok'):pul(ks[j++]));return a})()",
  o0='opts[0]', o1='opts[1]', o2='opts[2]', o3='opts[3]', nw="['','','two','three','four'][n]")
P3 = {'kp': [180, 330], 'Fp': [80, 150], 'np_': [2, 3.99], 'cip': [0, 3.99]}
parts = []
parts.append(dict(pi=0, type='explain',
 K=lab('(a)') + 'A spring is fixed at one end and attached to the frame of a pulley at the other end. A cable is passed around the wheel of the pulley. The spring is stretched to a fixed length using the cable and pulley. Figure 3.1 shows the view from above of the spring, cable and pulley.${f31}The spring obeys Hooke’s law and has a spring constant <i>k</i> of ${k} N m<sup>−1</sup>. A force <i>F</i> acts on the spring. The tension in the cable is <i>T</i>. The pulley is in equilibrium.<br><br>Which diagram shows the directions of the forces acting on the pulley?',
 answerType='imageChoice', imageOptions='["${o0}","${o1}","${o2}","${o3}"]', correctImageIndex='${ci}', imageChoiceMarks='2',
 U='One arrow to the left labelled F (the force from the spring), and two arrows to the right, each labelled T (the two sections of cable).',
 V='The spring pulls the pulley frame with force F (towards the fixed end). The cable passes round the wheel, so the pulley is pulled by two sections of cable, each with tension T, in the opposite direction. For equilibrium F = 2T.'))
parts.append(dict(pi=1, type='calculation',
 K=lab('(b)(i)') + 'The force <i>F</i> is ${F} N.<br><br>Determine <i>T</i>.',
 A='${T}', tolerance='1',
 U='T = F / 2 = ${F} / 2 = ${T} N',
 V='Two sections of cable pull on the pulley, each with tension T. The pulley is in equilibrium, so the force from the spring equals the total pull of the cable: F = 2T.'))
parts.append(dict(pi=2, type='calculation',
 K=lab('(b)(ii)') + 'Calculate the extension of the spring.',
 C1=kwv('x=f/k', 'f=kx', 'extension=force/spring constant', 'e=f/k', 'f=ke', 'hooke', '${F}/${k}'),
 A='${x1s}', tolerance='2',
 U='F = kx, so x = F / k = ${F} / ${k} = ${x1s} m',
 V='The spring obeys Hooke’s law, F = kx. The force on the spring is F (not T).'))
parts.append(dict(pi=3, type='calculation',
 K=lab('(c)(i)') + '${nw|cap} identical springs, each with the same spring constant of ${k} N m<sup>−1</sup>, are now connected to the pulley, as shown in Figure 3.2.${f33}The tension in the cable is kept the same. The pulley is again in equilibrium.<br><br>Determine the extension of each spring.',
 C1=kwv('${T}/${k}', 'f=kx', 'x=f/k', '${F}/(${n}×${k})', '${F}/(${n}x${k})', '${F}/${n}', 'force on each spring', 'extension=${T}/${k}'),
 A='${xns}', tolerance='2',
 U='The tension is unchanged, so the total force from the springs is still F = ${F} N, shared equally: ${F} / ${n} = ${Fn} N each. x = ${Fn} / ${k} = ${xns} m',
 V='The cable tension is unchanged, so the total force on the pulley frame is still F. The springs are identical and in parallel, so each carries F/n. Then apply F = kx to one spring.'))
G3['nw'] = "['','','Two','Three','Four'][n]"
parts[-1]['K'] = parts[-1]['K'].replace('${nw|cap}', '${nw}')
parts.append(dict(pi=4, type='calculation',
 K=lab('(c)(ii)') + 'The elastic potential energy stored in the spring in Figure 3.1 is <i>E</i><sub>1</sub>. The total elastic potential energy stored in the ${n} springs in Figure 3.2 is <i>E</i><sub>2</sub>.<br><br>Calculate the ratio <i>E</i><sub>1</sub> / <i>E</i><sub>2</sub>.',
 C1=kwv('½fx', '1/2fx', '0.5fx', '½kx²', '1/2kx^2', '0.5kx^2', 'f^2/2k', 'f²/2k', 'e=½fx', 'elastic potential energy=½', 'ep=½'),
 A='${ratios}', tolerance='2',
 U='E = ½kx² = ½Fx.  E₁ = ½ × ${F} × ${x1s} (single spring);  E₂ = ${n} × ½ × ${Fn} × ${xns}.  E₁ / E₂ = ${ratios}',
 V='Elastic potential energy stored is E = ½Fx = ½kx². Add the energy stored in all the springs and divide. Because the force is shared between the springs the energy stored in the group is smaller, so the ratio is exactly the number of springs.'))
ALL += question(LV, '9702-25-22-Q3', PAPER, 'calculation', 'Materials,Forces including Density and pressure', P3, G3,
 'Springs and a pulley: equilibrium and elastic energy', parts)

# =========================================================================== Q4  Double slit
FIGDS = js(r"""(a,D,x)=>{const W=600,H=300;
let s=@HD@+@AH@;
@LN@
s+=ln(20,150,120,150,' stroke-dasharray="5,3"')+'<text x="22" y="140">laser light</text>';
s+='<rect x="120" y="50" width="12" height="200" fill="#ccc" stroke="#000"/><rect x="118" y="135" width="16" height="10" fill="#fff"/><rect x="118" y="155" width="16" height="10" fill="#fff"/>';
s+=ln(134,150,420,150,' stroke-dasharray="3,4" stroke-opacity="0.5"');
s+='<text x="126" y="40" text-anchor="middle">double slit</text><text x="126" y="272" text-anchor="middle" font-size="13">separation '+a+' × 10⁻³ m</text>';
s+='<rect x="420" y="30" width="10" height="240" fill="#e8e8e8" stroke="#000"/><text x="425" y="22" text-anchor="middle">screen</text>';
s+=ln(134,150,420,150,'');
s+='<line x1="140" y1="288" x2="420" y2="288" stroke="#000" marker-start="url(#ah)" marker-end="url(#ah)" stroke-width="1.4"/><text x="280" y="283" text-anchor="middle">'+D+' m</text>';
for(let k=-4;k<=4;k++){const y=150+k*28,b=(k%2===0);
 s+='<rect x="470" y="'+(y-14)+'" width="40" height="28" fill="'+(b?'#e8d36a':'#555')+'" stroke="none"/>';}
s+='<text x="520" y="124" font-size="13">dark fringe</text><text x="520" y="152" font-size="13">bright fringe</text>';
s+='<line x1="536" y1="108" x2="536" y2="68" stroke="#000" stroke-width="0"/>';
s+='<line x1="462" y1="122" x2="462" y2="66" stroke="#000" marker-start="url(#ah)" marker-end="url(#ah)" stroke-width="1.4"/><text x="456" y="98" text-anchor="end">'+x+' mm</text>';
s+='<text x="'+(W-12)+'" y="'+(H-8)+'" text-anchor="end" font-size="12">not to scale</text></svg>';
""" + cap("'4.1'") + "}")
G4 = G_('sf', 'ex', fig=FIGDS,
  a='+ap.toFixed(2)', Dd='+Dp.toFixed(1)', lt='lamp*1e-7', xm='+(lt*Dd/(a*1e-3)*1e3).toFixed(1)', lam='a*1e-3*xm*1e-3/Dd', lamn='sf(lam*1e9,3)', lame='ex(lam,2)',
  f='3.00e8/lam', fs='ex(f,1)', fs3='ex(f,2)', f41='fig(a,Dd,xm)')
P4 = {'ap': [0.80, 1.40], 'Dp': [3.0, 5.5], 'lamp': [4.2, 6.8]}
parts = []
parts.append(dict(pi=0, type='explain',
 K=lab('(a)') + 'A laser emits visible light of a single frequency in a vacuum. The light is incident normally on a double slit and then forms a pattern of bright and dark fringes on a screen, as shown in Figure 4.1.${f41}The separation of the slits is ${a} × 10<sup>−3</sup> m. The distance from the slits to the screen is ${Dd} m. The distance between the centres of adjacent dark fringes on the screen is ${xm} mm.<br><br>Explain how the pattern of bright and dark fringes is formed.',
 B=kwv('diffract', 'diffraction', 'spreads', 'spread out', 'spreads out', 'diffracted'),
 B2=kwv('superpose', 'superposition', 'interfere', 'interference', 'overlap', 'overlaps', 'meet', 'combine', 'superimpose'),
 B3=andor(['path difference', 'phase difference', 'in phase', 'out of phase', 'antiphase', 'anti-phase', 'nλ', 'nλ', 'λ/2', 'half a wavelength', 'whole number of wavelengths', 'integer number of wavelengths', 'integer multiple', '180', 'phase of 0', 'zero phase difference'], ['bright', 'constructive', 'maximum', 'maxima', 'dark', 'destructive', 'minimum', 'minima', 'fringe']),
 U='Light diffracts (spreads out) at each slit. The light from the two slits superposes (interferes) on the screen. Where the path difference is a whole number of wavelengths (phase difference 0) there is constructive interference and a bright fringe; where the path difference is an odd number of half wavelengths (phase difference 180°) there is destructive interference and a dark fringe.',
 V='Each slit acts as a source of diffracted, coherent waves. The waves overlap and superpose. Constructive interference gives bright fringes (path difference nλ); destructive interference gives dark fringes (path difference (n + ½)λ).'))
parts.append(dict(pi=1, type='calculation',
 K=lab('(b)') + 'Calculate the frequency of the light emitted by the laser.',
 C3=kwv('λ=ax/d', 'ax/d', 'lambda=ax/d', 'λ=ax/d', 'x=λd/a', 'x=λ×d/a', 'x=λd/a', 'double slit equation', 'λ=a×x/d'),
 C2=kwv('${lame}', '${lamn}', '${a}×10^-3×${xm}', '${a}x10^-3x${xm}'),
 C1=kwv('f=c/λ', 'f=v/λ', 'c=fλ', 'v=fλ', 'f=3.00×10^8', 'f=3×10^8', 'f=3x10^8', 'c/λ'),
 A='${fs}|${fs3}', tolerance='2',
 U='λ = ax / D = ${a} × 10⁻³ × ${xm} × 10⁻³ / ${Dd} = ${lame} m;  f = c / λ = 3.00 × 10⁸ / ${lame} = ${fs} Hz',
 V='The double-slit equation λ = ax/D uses the fringe separation x (centre to centre of adjacent dark fringes), the slit separation a and the slit-to-screen distance D. Convert mm to m. Then use c = fλ for light in a vacuum.'))
parts.append(dict(pi=2, type='explain',
 K=lab('(c)') + 'The double slit is removed. A second laser is placed beside the first laser. The second laser produces visible light of a different frequency from that of the first laser. The beams of light from the two lasers overlap on the screen.<br><br>Explain why a steady pattern of bright and dark fringes is not formed on the screen.',
 B=andor(['different frequencies', 'different frequency', 'frequencies are different', 'not coherent', 'incoherent', 'not the same frequency', 'different wavelength', 'phase difference is not constant', 'phase difference changes', 'phase difference varies', 'constant phase', 'not constant'], ['not coherent', 'incoherent', 'phase difference', 'constant', 'coherent', 'phase']),
 U='The light from the two lasers has different frequencies, so it is not coherent: the phase difference between the two beams is not constant, so no steady interference pattern forms.',
 V='A steady interference pattern requires coherent sources: the same frequency and a constant phase difference. Lasers of different frequencies have a continually changing phase difference.'))
ALL += question(LV, '9702-25-22-Q4', PAPER, 'explain', 'Superposition,Waves', P4, G4, 'Double-slit interference with a laser', parts)

# =========================================================================== Q5  LDR circuit
FIGCKT = js(r"""(E,r,RX)=>{const W=520,H=330;
let s=@HD@+@AH@;
@LN@
@AR@
s+='<rect x="120" y="26" width="290" height="76" fill="none" stroke="#000" stroke-dasharray="6,4"/>';
s+=ln(30,64,200,64)+ln(200,46,200,82)+ln(212,54,212,74)+ln(238,54,238,74)+ln(252,46,252,82)+ln(212,64,238,64,' stroke-dasharray="0"');
s+=ln(200,64,150,64,'')+ln(252,64,282,64)+'<rect x="282" y="52" width="60" height="24" fill="#fff" stroke="#000" stroke-width="1.6"/>'+ln(342,64,420,64);
s+='<text x="225" y="22" text-anchor="middle">'+E+' V</text><text x="312" y="22" text-anchor="middle">'+r+' Ω</text>';
s+=ln(30,64,30,270)+ln(420,64,420,270);
s+=ln(30,160,120,160)+'<rect x="120" y="148" width="84" height="24" fill="#fff" stroke="#000" stroke-width="1.6"/>'+ln(204,160,250,160)+'<rect x="250" y="148" width="84" height="24" fill="#fff" stroke="#000" stroke-width="1.6"/>'+ln(334,160,420,160);
s+='<text x="162" y="144" text-anchor="middle">'+RX+' Ω</text><text x="162" y="194" text-anchor="middle">X</text><text x="292" y="194" text-anchor="middle">Z</text>';
s+=ln(266,120,282,142,' marker-end="url(#ah)"')+ln(282,116,298,138,' marker-end="url(#ah)"');
s+=ln(30,250,150,250)+'<rect x="150" y="238" width="84" height="24" fill="#fff" stroke="#000" stroke-width="1.6"/>'+ln(234,250,420,250)+'<text x="192" y="284" text-anchor="middle">Y</text>';
s+=ln(60,150,100,150,' marker-end="url(#ah)"')+'<text x="68" y="140" font-style="italic">I<tspan font-size="11" dy="4">1</tspan></text>';
s+=ln(60,240,100,240,' marker-end="url(#ah)"')+'<text x="68" y="230" font-style="italic">I<tspan font-size="11" dy="4">2</tspan></text>';
s+='<circle cx="30" cy="160" r="3.5"/><circle cx="420" cy="160" r="3.5"/>';
s+='<text x="'+(W-12)+'" y="'+(H-8)+'" text-anchor="end" font-size="12">not to scale</text></svg>';
""" + cap("'5.1'") + "}")
LDRG = ("(A,IL,RZ)=>{const pts=[];for(let I=26;I<=250;I+=2){const R=A*Math.pow(I/50,-1.2);if(R<=500)pts.push([I,+R.toFixed(1)]);}"
        "return gsvg({x0:0,x1:250,y0:0,y1:500,mx:10,my:20,Mx:50,My:100,xl:'intensity / W m<sup>−2</sup>',yl:'resistance / Ω',pts:pts,cap:'Figure 5.2',W:520,H:380});}")
G5 = G_('sf', 'ex', fig=FIGCKT, gsvg=GSVG, ldr=LDRG,
  E='+Ep.toFixed(1)', r='+rp.toFixed(1)', RX='Math.round(RXp/10)*10', IL='Math.round(ILp/10)*10', RZ='Math.round(RZp/5)*5', Ry='Math.round(Ryp/10)*10',
  Rtop='RX+RZ', Rext='Rtop*Ry/(Rtop+Ry)', Iex='E/(r+Rext)', Ib='+(Iex*1000).toPrecision(2)', Iba='Ib/1000',
  Vt='E-Iba*r', Vts='sf(Vt,2)', Vtd='sf(Vt,3)', Ir='sf(Iba*r,2)',
  I1='Vt/Rtop', I1s='sf(I1,3)', I2='Iba-I1', I2s='sf(I2,2)', I2d='sf(I2,3)', P='I2*Vt', Ps='sf(P,2)', Pd='sf(P,3)',
  RZlo='+(RZ*0.92).toFixed(1)', RZhi='+(RZ*1.08).toFixed(1)', A_='RZ*Math.pow(IL/50,1.2)',
  f51='fig(E,r,RX)', f52='ldr(A_,IL,RZ)')
P5 = {'Ep': [4.5, 6.0], 'rp': [3.0, 6.0], 'RXp': [80, 140], 'ILp': [90, 170], 'RZp': [90, 200], 'Ryp': [200, 450]}
parts = []
parts.append(dict(pi=0, type='definition', K=lab('(a)') + 'State Kirchhoff’s first law.',
 B=andor(['sum of current', 'sum of the current', 'total current', 'sum of the currents', 'algebraic sum', 'current into', 'currents into', 'current entering', 'currents entering', 'current flowing into', 'sum of the current'], ['junction', 'point', 'node', 'in a circuit']),
 B2=None,
 U='The sum of the currents into a junction is equal to the sum of the currents out of the junction (the algebraic sum of the currents at a junction is zero).',
 V='Kirchhoff’s first law is conservation of charge: charge cannot build up at a junction, so the current arriving equals the current leaving.'))
del parts[-1]['B2']
parts.append(dict(pi=1, type='calculation',
 K=lab('(b)(i)') + 'Figure 5.1 shows a circuit containing a battery, two fixed resistors X and Y, and a light-dependent resistor (LDR) Z.${f51}The battery has electromotive force (e.m.f.) ${E} V and internal resistance ${r} Ω. The current in X is <i>I</i><sub>1</sub> and the current in Y is <i>I</i><sub>2</sub>. The resistance of X is ${RX} Ω. The resistance of Z varies with the intensity of light incident on it as shown in Figure 5.2.${f52}The intensity of light incident on Z is ${IL} W m<sup>−2</sup>. The current in the battery is ${Ib} mA.<br><br>Show that the terminal potential difference of the battery is ${Vts} V.',
 C1=kwv('v=e−ir', 'v=e-ir', 'e-ir', 'e−ir', 'emf-ir', 'emf−ir', 'terminal p.d.=e', 'terminal pd=e', 'lost volts', 'v=ε-ir', 'v=ε−ir', 'p.d. across internal resistance'),
 A='${Vts}|${Vtd}', tolerance='1',
 U='V = E − Ir = ${E} − (${Ib} × 10⁻³ × ${r}) = ${Vtd} V = ${Vts} V (2 s.f.)',
 V='The terminal p.d. is the e.m.f. minus the “lost volts” across the internal resistance, V = E − Ir. Convert the current from mA to A.'))
parts.append(dict(pi=2, type='calculation',
 K=lab('(b)(ii)') + 'Calculate the current <i>I</i><sub>2</sub> in Y.',
 C2='${RZlo} to ${RZhi}',
 C1=kwv('${I1s}', '${Vts}/(${RX}+${RZ})', '${Vtd}/(${RX}+${RZ})', 'i=v/r', 'v/r', 'i1=', 'current in x'),
 A='${I2s}|${I2d}', tolerance='5',
 U='From Figure 5.2, R(Z) = ${RZ} Ω.  I₁ = V / (Rₓ + Rᶻ) = ${Vts} / (${RX} + ${RZ}) = ${I1s} A;  I₂ = ${Ib} × 10⁻³ − ${I1s} = ${I2s} A',
 V='Read the resistance of Z from the graph at the stated intensity. X and Z are in series, so the current in that branch is I₁ = V/(Rₓ + R_Z), using the terminal p.d. The battery current splits between the two branches, so I₂ = I − I₁.'))
parts.append(dict(pi=3, type='calculation',
 K=lab('(b)(iii)') + 'Calculate the power dissipated in Y.',
 C1=kwv('p=iv', 'p=i2r', 'p=i²r', 'p=v2/r', 'p=v²/r', 'p=vi', 'p=${I2s}×${Vts}', 'p=${I2s}x${Vts}', 'p=${I2s}*${Vts}'),
 A='${Ps}|${Pd}', tolerance='5',
 U='P = I₂V = ${I2s} × ${Vts} = ${Ps} W',
 V='Y is connected across the terminals of the battery, so the p.d. across Y is the terminal p.d. The power dissipated is P = IV.'))
parts.append(dict(pi=4, type='explain',
 K=lab('(b)(iv)') + 'The intensity of the light incident on Z decreases.<br><br>State and explain the effect on the terminal potential difference of the battery.',
 B=andor(['resistance of z', 'resistance of the ldr', 'ldr resistance', 'z resistance', 'resistance of ldr', 'resistance of the z', 'resistance of the light dependent', 'resistance of the light-dependent'], ['increases', 'increase', 'greater', 'larger', 'higher', 'rises', 'goes up', 'more']),
 M=kwv('total resistance increases', 'total resistance of the circuit increases', 'total resistance of circuit increases', 'external resistance increases', 'current in the battery decreases', 'current in the battery is smaller', 'current in the battery is less', 'current decreases', 'current from the battery decreases', 'current in the cell decreases', 'total current decreases', 'current in battery decreases', 'total resistance is greater', 'total resistance greater', 'total resistance is larger', 'total resistance goes up', 'total resistance rises', 'overall resistance increases'),
 A=andor(['terminal', 'p.d.', 'pd', 'voltage', 'potential difference'], ['increases', 'increase', 'greater', 'larger', 'higher', 'rises', 'goes up']),
 U='The resistance of Z increases, so the total resistance of the circuit increases and the current in the battery decreases. The p.d. across the internal resistance (lost volts, Ir) decreases, so the terminal p.d. (E − Ir) increases.',
 V='A lower intensity means a higher LDR resistance, so the total resistance is higher and the battery current falls. The lost volts Ir across the internal resistance get smaller, so the terminal p.d. = E − Ir gets larger.'))
ALL += question(LV, '9702-25-22-Q5', PAPER, 'calculation', 'Electricity,D.C. circuits', P5, G5, 'Battery, resistors and a light-dependent resistor', parts)

# =========================================================================== Q6  Particle physics and decay
MESON = js(r"""(fam)=>{const U=['up','charm','top'],D=['down','strange','bottom'];
const out=[];for(const a of (fam==='U'?U:D)){for(const an of ['anti'+a,'anti-'+a,'anti '+a,a+' antiquark',a+'bar',a+' bar','anti'+a+' quark','anti-'+a+' quark','anti '+a+' quark'])out.push(an);}
return out.join('|');}""")
G6 = G_('sf', 'ex', 'us', 'sb', 'sci', mesonkw=MESON,
  gi='Math.floor(chp)', fi='Math.floor(fp_)', gf="['U','D','U','D'][gi]", of_="['U','D','D','U'][gi]", qtxt="['0','0','+1','−1'][gi]",
  gq="(gf==='U'?['up','charm','top']:['down','strange','bottom'])[fi]", oq="(of_==='U'?['up','charm','top']:['down','strange','bottom'])[fi]",
  mk='mesonkw(of_)', mu='+mup.toFixed(2)', KE='+KEp.toFixed(1)', mkg='mu*1.66e-27', mkgs='ex(mkg,2)', v='Math.sqrt(2*KE*1e-16/mkg)', vs='ex(v,1)', vs2='ex(v,2)',
  RAD="[['radium',228,88,'Ra'],['thorium',232,90,'Th'],['uranium',238,92,'U'],['radium',226,88,'Ra'],['thorium',230,90,'Th'],['radon',222,86,'Rn']]",
  ri='Math.floor(rip)', rn='RAD[ri][0]', rA='RAD[ri][1]', rZ='RAD[ri][2]', rS='RAD[ri][3]', na='Math.floor(nap)', nb='Math.floor(nbp)',
  Ap='rA-4*na', Zp='rZ-2*na+nb', Np='Ap-Zp', nucl='us(rA)+sb(rZ)+rS', nuclX='us(Ap)+sb(Zp)+"X"')
P6 = {'chp': [0, 3.99], 'fp_': [0, 2.99], 'mup': [0.40, 1.20], 'KEp': [1.0, 4.0], 'rip': [0, 5.99], 'nap': [3, 6.99], 'nbp': [2, 4.99]}
parts = []
parts.append(dict(pi=0, type='definition', K=lab('(a)') + 'State what is meant by a fundamental particle.',
 B=kwv('cannot be divided', 'cannot be subdivided', 'can not be divided', 'cannot be split', 'not made up of smaller', 'not made of smaller', 'no smaller particles', 'cannot be broken down', 'cannot be broken', 'no internal structure', 'indivisible', 'no constituents', 'not composed of', 'cannot be sub-divided', 'cannot be divided into smaller', 'not made up of anything smaller', 'has no smaller'),
 U='A fundamental particle is a particle that cannot be divided (subdivided) into smaller particles.',
 V='Fundamental particles (for example quarks, electrons and neutrinos) have no internal structure and are not made of smaller particles.'))
parts.append(dict(pi=1, type='explain',
 K=lab('(b)(i)') + 'Particle Q is a meson with a charge of ${qtxt} (in units of <i>e</i>). One of the constituents of Q is a ${gq} quark.<br><br>Determine a possible identity for the other constituent of Q.',
 C1=kwv('antiquark', 'anti-quark', 'anti quark', 'quark and an antiquark', 'quark and antiquark'),
 A='${mk}',
 U='A meson contains one quark and one antiquark, so the other constituent is an antiquark: an anti-${oq} quark. (Charge: up-type quarks +⅔ e, down-type −⅓ e; antiquarks have opposite charge.)',
 V='Mesons are made of one quark and one antiquark. Up, charm and top quarks have charge +2/3; down, strange and bottom quarks have charge −1/3. Each antiquark has the opposite charge. Choose a combination whose charges add up to the charge of Q.'))
parts.append(dict(pi=2, type='calculation',
 K=lab('(b)(ii)') + 'Particle Q has a mass of ${mu} u and a kinetic energy of ${KE} × 10<sup>−16</sup> J.<br><br>Calculate the speed of particle Q.',
 C2=kwv('e=½mv²', 'ek=½mv²', 'ke=½mv²', '½mv²', '1/2mv^2', '0.5mv^2', 'v=√(2e/m)', '√(2e/m)'),
 C1=kwv('${mkgs}', '${mu}×1.66×10^-27', '${mu}x1.66x10^-27', '${mu}*1.66e-27', 'mass in kg', '${mu}×1.66e-27'),
 A='${vs}|${vs2}', tolerance='2',
 U='Eₖ = ½mv² with m = ${mu} × 1.66 × 10⁻²⁷ = ${mkgs} kg;  v = √(2 × ${KE} × 10⁻¹⁶ / ${mkgs}) = ${vs} m s⁻¹',
 V='Convert the mass from unified atomic mass units to kilograms (1 u = 1.66 × 10⁻²⁷ kg), then rearrange Eₖ = ½mv² for v.'))
parts.append(dict(pi=3, type='calculation',
 K=lab('(c)(i)') + '${rn|c} -${rA} (<sup>${rA}</sup><sub>${rZ}</sub>${rS}) is a radioactive nuclide. State the number of electrons in a neutral atom of ${rn}-${rA}.',
 A='${rZ}',
 U='number of electrons = ${rZ} (equal to the proton number)',
 V='A neutral atom has the same number of electrons as protons, which is the proton number ${rZ}.'))
G6['rnc'] = "RAD[ri][0].charAt(0).toUpperCase()+RAD[ri][0].slice(1)"
parts[-1]['K'] = parts[-1]['K'].replace('${rn|c}', '${rnc}')
parts.append(dict(pi=4, type='calculation',
 K=lab('(c)(ii)') + 'A nucleus of ${rn}-${rA} undergoes a series of decays to form nucleus X. During the process, ${na} α-particles and ${nb} β<sup>−</sup> particles are emitted.<br><br>Determine the number of protons and the number of neutrons in nucleus X. Give your answer in the form “protons = …, neutrons = …”.',
 B='${Zp}', B2='${Np}',
 U='nucleon number = ${rA} − ${na} × 4 = ${Ap};  protons = ${rZ} − (${na} × 2) + ${nb} = ${Zp};  neutrons = ${Ap} − ${Zp} = ${Np}',
 V='Each α-particle removes 2 protons and 2 neutrons (nucleon number −4, proton number −2). Each β⁻ decay changes a neutron into a proton (proton number +1, nucleon number unchanged). Neutron number = nucleon number − proton number.'))
ALL += question(LV, '9702-25-22-Q6', PAPER, 'explain', 'Particle physics', P6, G6, 'Fundamental particles and radioactive decay', parts)

json.dump(ALL, open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False)
write_json(ALL, sys.argv[1] + '.rows.json') if False else None
print(len(ALL), 'rows')
