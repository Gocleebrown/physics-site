##v1  AS 9702/23 Oct/Nov 2025 (w25) -- built from the real QP + MS, every number a parameter, figures generated.
#   python3 build_w25p23.py out.json      (rows for the 6 questions, 60 marks)
import json, sys
sys.path.insert(0, '.')
from rowlib import *
from jshelpers import GSVG

LV = 'AS'; PAPER = '9702_w25_p23'
def lab(s): return '<b>' + s + '</b> '
def kwv(*alts): return '|'.join(dict.fromkeys(alts))

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

# generic small-axes sketch used for imageChoice graph options.  o: {ylab, y0lab, xlab, x0, xend, f(u)->0..1, y0level}
SKETCH = js(r"""(o)=>{const W=300,H=230,L=56,R=14,T=16,B=46,pw=W-L-R,ph=H-T-B;
let s='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 '+W+' '+H+'" width="'+W+'" height="'+H+'" font-family="Arial,sans-serif" font-size="13"><rect width="'+W+'" height="'+H+'" fill="#fff"/>';
s+='<line x1="'+L+'" y1="'+T+'" x2="'+L+'" y2="'+(T+ph)+'" stroke="#000"/><line x1="'+L+'" y1="'+(T+ph)+'" x2="'+(L+pw)+'" y2="'+(T+ph)+'" stroke="#000"/>';
s+='<text x="'+(L+8)+'" y="'+(T+10)+'" font-style="italic">'+o.ylab+'</text>';
s+='<text x="'+(L+pw/2)+'" y="'+(H-8)+'" text-anchor="middle">'+o.xlab+'</text>';
if(o.y0lab){const yy=T+ph-ph*o.y0level;s+='<line x1="'+(L-4)+'" y1="'+yy+'" x2="'+L+'" y2="'+yy+'" stroke="#000"/><text x="'+(L-8)+'" y="'+(yy+4)+'" text-anchor="end">'+o.y0lab+'</text>';}
(o.xticks||[]).forEach(t=>{const xx=L+pw*t[0];s+='<line x1="'+xx+'" y1="'+(T+ph)+'" x2="'+xx+'" y2="'+(T+ph+4)+'" stroke="#000"/><text x="'+xx+'" y="'+(T+ph+18)+'" text-anchor="middle">'+t[1]+'</text>';});
(o.yticks||[]).forEach(t=>{const yy=T+ph-ph*t[0];s+='<line x1="'+(L-4)+'" y1="'+yy+'" x2="'+L+'" y2="'+yy+'" stroke="#000"/><text x="'+(L-8)+'" y="'+(yy+4)+'" text-anchor="end">'+t[1]+'</text>';});
let p=[];for(let i=0;i<=120;i++){const u=i/120;const y=o.f(u);p.push((L+pw*u).toFixed(1)+','+(T+ph-ph*y).toFixed(1));}
s+='<polyline fill="none" stroke="#000" stroke-width="2.4" points="'+p.join(' ')+'"/></svg>';
return s;}""")
CHOICE = dict(answerType='imageChoice', imageOptions='["${o0}","${o1}","${o2}","${o3}"]', correctImageIndex='${ci}')
def choice(marks): d = dict(CHOICE); d['imageChoiceMarks'] = str(marks); return d
OPTS = "(()=>{const a=[];let j=0;for(let q=0;q<4;q++)a.push(q===@CI@?mk('ok'):mk(ks[j++]));return a})()"
def optsjs(ci): return OPTS.replace('@CI@', ci)

ALL = []
# =========================================================================== Q1  Rocket launch
GRAPH1 = ("(T,v)=>{const x1=Math.ceil(T/5)*5,y1=Math.ceil(v/100)*100;"
          "return gsvg({x0:0,x1:x1,y0:0,y1:y1,mx:1,my:20,Mx:5,My:100,xl:'time / s',yl:'velocity / m s<sup>−1</sup>',pts:[[0,0],[T,v]],cap:'Figure 1.1',W:520,H:380});}")
G1 = G_('sf', 'ex', 'us', 'sci', gsvg=GSVG, gr=GRAPH1,
  T='Math.round(Tp)', a='Math.round(ap)', v='a*T', M='+Mp.toFixed(1)', Mk='M*1e6',
  h='0.5*a*T*T', hk='+(h/1000).toPrecision(2)', Hm='hk*1000',
  EP='Mk*9.81*Hm', EK='0.5*Mk*v*v', PW='(EP+EK)/T',
  EPe='ex(EP,1)', EPd='ex(EP,2)', EKe='ex(EK,1)', EKd='ex(EK,2)', PWe='ex(PW,1)', PWd='ex(PW,2)',
  EPs='sci(EP,1)', EKs='sci(EK,1)', PWs='sci(PW,1)', Hms='sf(Hm,2)', f11='gr(T,v)',
  Eex='ex(EP+EK,2)')
P1 = {'Tp': [16, 24], 'ap': [11, 19], 'Mp': [2.2, 3.8]}
parts = []
parts.append(dict(pi=0, type='definition',
 K=lab('(a)') + 'Define acceleration.',
 B=kwv('rate of change of velocity', 'change in velocity per unit time', 'change in velocity per second', 'velocity change per unit time', 'change of velocity per unit time', 'change in velocity divided by time', 'change in velocity over time', 'change of velocity per second', 'dv/dt', 'δv/δt', 'v/t', 'velocity per unit time', 'increase in velocity per unit time', 'change in velocity/time', 'rate of increase of velocity'),
 U='Acceleration is the rate of change of velocity.',
 V='Acceleration is the change in velocity per unit time (the gradient of a velocity–time graph).'))
parts.append(dict(pi=1, type='calculation',
 K=lab('(b)(i)') + 'A rocket is launched vertically from the surface of the Earth. Figure 1.1 shows the variation of the velocity of the rocket with time for the first ${T} s after its launch.${f11}Determine the acceleration of the rocket.',
 A='${a}', tolerance='2',
 U='acceleration = gradient = ${v} / ${T} = ${a} m s⁻²',
 V='The graph is a straight line through the origin, so the acceleration is constant and equals the gradient: change in velocity ÷ time = ${v} / ${T}.'))
parts.append(dict(pi=2, type='calculation',
 K=lab('(b)(ii)') + 'Show that the height of the rocket above the surface of the Earth at a time of ${T} s after launch is ${hk} km.',
 C1=kwv('s=½(u+v)t', 's=1/2(u+v)t', 's=0.5(u+v)t', 'area under graph', 'area under the graph', 'area under', 'average velocity', 'mean velocity', 's=(u+v)t/2', '½×${T}×${v}', '1/2×${T}×${v}', '0.5×${T}×${v}', '½${T}${v}', 's=ut+½at²', 's=ut+1/2at^2', '½at²', '1/2at^2', '0.5at^2', 'triangle', 'distance=area'),
 A='${hk}|${Hm}', tolerance='3',
 U='height = area under graph = ½ × ${T} × ${v} = ${sf(h,3)} m = ${hk} km',
 V='The distance travelled equals the area under the velocity–time graph, here a triangle: ½ × base × height = ½ × ${T} × ${v}. Convert metres to kilometres by dividing by 1000.'))
parts.append(dict(pi=3, type='calculation',
 K=lab('(c)(i)') + 'The mass of the rocket in (b) is ${M} × 10<sup>6</sup> kg. Assume that this mass remains constant.<br><br>For this rocket, from launch to its height at a time of ${T} s after launch, calculate the gain in gravitational potential energy ΔE<sub>P</sub>. Use a height of ${hk} km.',
 C1=kwv('mgh', 'mgδh', 'm g h', 'gpe=mgh', 'ep=mgh', 'δep=mgδh', 'e=mgh', 'mass×g×height', 'mass x g x height', '${Mk}×9.81', '${M}×10^6×9.81', '${M}e6×9.81'),
 A='${EPe}|${EPd}', tolerance='3',
 U='ΔE_P = mgh = ${M} × 10⁶ × 9.81 × ${Hms} = ${EPs} J',
 V='Gravitational potential energy gained = mgΔh, using the height from (b)(ii) (${Hms} m) and g = 9.81 m s⁻².'))
parts.append(dict(pi=4, type='calculation',
 K=lab('(c)(ii)') + 'For the same rocket, calculate the gain in kinetic energy ΔE<sub>K</sub>.',
 C1=kwv('½mv²', '1/2mv^2', '0.5mv^2', '½mv^2', 'ek=½mv²', 'ke=½mv²', 'kinetic energy=½mv²', 'kinetic energy=1/2mv^2', 'e=½mv²', '½ × m × v²', '0.5×m×v²', '½×${M}×10^6×${v}', '0.5×${Mk}×${v}'),
 A='${EKe}|${EKd}', tolerance='3',
 U='ΔE_K = ½mv² = ½ × ${M} × 10⁶ × ${v}² = ${EKs} J',
 V='The rocket starts from rest, so the gain in kinetic energy is ½mv² with v the final velocity read from the graph, ${v} m s⁻¹.'))
parts.append(dict(pi=5, type='calculation',
 K=lab('(c)(iii)') + 'Determine the average power output of the rocket engines. Assume that resistive forces are negligible.',
 C1=kwv('work done/time', 'work done / time', 'energy/time', 'energy / time', 'power=work/time', 'power=energy/time', 'p=w/t', 'p=e/t', 'p=δe/t', 'work done divided by time', 'energy transferred/time', 'energy transferred per unit time', 'rate of work', 'rate of energy', '(${EPs}+${EKs})', '(${EPe}+${EKe})', 'total energy/time', 'total energy / time'),
 A='${PWe}|${PWd}', tolerance='3',
 U='power = (ΔE_P + ΔE_K) / t = (${EPs} + ${EKs}) / ${T} = ${PWs} W',
 V='With negligible resistive forces, the work done by the engines equals the total gain in mechanical energy, ΔE_P + ΔE_K. Average power is work done ÷ time (${T} s).'))
ALL += question(LV, '9702-25-23-Q1', PAPER, 'calculation', 'Kinematics,Energy,Dynamics', P1, G1, 'Rocket launch: velocity–time graph and energy', parts)

# =========================================================================== Q2  Pressure, upthrust and viscous drag
BALL = js(r"""(kind)=>{const W=260,H=240,cx=130,cy=120;
let s='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 '+W+' '+H+'" width="'+W+'" height="'+H+'" font-family="Arial,sans-serif" font-size="14"><rect width="'+W+'" height="'+H+'" fill="#fff"/>'+@AH@;
@LN@
@AR@
s+='<circle cx="'+cx+'" cy="'+cy+'" r="22" fill="#d9d9d9" stroke="#000" stroke-width="1.6"/>';
const lb=(x,y,t)=>(x<cx?'<text x="'+(x-6)+'" y="'+y+'" text-anchor="end">'+t+'</text>':'<text x="'+(x+6)+'" y="'+y+'">'+t+'</text>');
const up=(x,t)=>ar(x,cy-22,x,cy-82)+lb(x,cy-70,t);
const dn=(x,t)=>ar(x,cy+22,x,cy+82)+lb(x,cy+78,t);
if(kind==='ok')s+=dn(cx,'weight')+up(cx-34,'upthrust')+up(cx+34,'drag');
else if(kind==='noU')s+=dn(cx,'weight')+up(cx,'drag');
else if(kind==='dragDown')s+=dn(cx-34,'weight')+up(cx,'upthrust')+dn(cx+34,'drag');
else s+=up(cx,'weight')+dn(cx-34,'upthrust')+dn(cx+34,'drag');
return s+'</svg>';}""")
LAWS = ('[["D = 6πηrv","η","[[\\"kg\\",1],[\\"m\\",-1],[\\"s\\",-1]]","η"],'
        '["D = kv","k","[[\\"kg\\",1],[\\"s\\",-1]]","k"],'
        '["D = cv²","c","[[\\"kg\\",1],[\\"m\\",-1]]","c"],'
        '["D = bv / r","b","[[\\"kg\\",1],[\\"m\\",1],[\\"s\\",-1]]","b"]]')
G2 = G_('sf', 'ex', 'us', 'sci', uv=UNITS_VAR, ud=UDISP, brk=BALL, sk=SKETCH,
  LAWS=LAWS, li='Math.floor(lip)', law='LAWS[li]', lf='law[0]', ls='law[1]', lu='JSON.parse(law[2])',
  ukw='JSON.stringify([uv(lu)])', ud_='ud(lu)',
  mk='brk', ks="['noU','dragDown','rev']", ci='Math.floor(cip)', opts=optsjs('ci'), o0='opts[0]', o1='opts[1]', o2='opts[2]', o3='opts[3]',
  rho='Math.round(rhop/10)*10', r='+rp.toFixed(1)', rm='r*1e-3', eta='+etap.toFixed(1)', rs='Math.round(rsp/100)*100',
  V0='4/3*Math.PI*rm*rm*rm', U='rho*V0*9.81', Ue='ex(U,1)', Us='sf(U,2)', Ud='ex(U,2)',
  U2='+U.toPrecision(2)', mb='+(rs*V0).toPrecision(2)', mbe='ex(mb,1)', Wn='mb*9.81', Ws='sf(Wn,3)', Ws2='sf(Wn,2)',
  vt='(Wn-U2)/(6*Math.PI*eta*rm)', vts='sf(vt,2)', vtd='sf(vt,3)', Ue2='ex(U2,1)', Dn='Wn-U2', Dns='sf(Dn,3)', Us2='sci(U2,1)',
  rsc='us(Math.round(rs))')
P2 = {'lip': [0, 3.99], 'cip': [0, 3.99], 'rhop': [850, 980], 'rp': [3.6, 5.0], 'etap': [3.5, 6.0], 'rsp': [7600, 8000]}
parts = []
parts.append(dict(pi=0, type='definition',
 K=lab('(a)(i)') + 'Define pressure.',
 B=kwv('force per unit area', 'force per (unit) area', 'force per unit cross-sectional area', 'force/area', 'force / area', 'force divided by area', 'force over area', 'normal force per unit area', 'force acting per unit area', 'force on unit area', 'force per area', 'f/a', 'force perpendicular per unit area', 'force normal to the surface per unit area'),
 U='Pressure is force per unit area (the normal force acting per unit cross-sectional area).',
 V='Pressure = force ÷ area, where the force acts normally (at right angles) to the surface.'))
parts.append(dict(pi=1, type='explain',
 K=lab('(a)(ii)') + 'Explain how hydrostatic pressure results in an upthrust force acting on a solid object immersed in a liquid.',
 B=kwv('difference in pressure', 'pressure difference', 'pressure at the bottom is greater', 'pressure at the bottom is higher', 'pressure is greater at the bottom', 'pressure increases with depth', 'pressure higher at the bottom', 'pressure at bottom greater', 'pressure greater below', 'pressure at the bottom is larger', 'pressure lower at the top', 'pressure is lower at the top', 'different pressure', 'greater pressure at the bottom', 'greater pressure on the bottom', 'greater pressure below'),
 B2=kwv('force on the bottom is greater', 'force at the bottom is greater', 'force on bottom greater', 'upward force is greater than the downward force', 'upward force greater than downward force', 'resultant force is upwards', 'resultant force upwards', 'net force is upwards', 'net force upwards', 'force on the bottom is larger', 'force on the bottom is bigger', 'force from the bottom is greater', 'upward force is larger', 'upward force bigger', 'upwards force greater', 'upwards force is greater', 'resultant upward force', 'net upward force', 'force on the bottom is higher', 'greater force on the bottom', 'larger force on the bottom'),
 U='The pressure is greater at the bottom of the object than at the top (pressure increases with depth, Δp = ρgΔh), so the force on the bottom is greater than the downward force on the top. The resultant force is upwards: the upthrust.',
 V='Hydrostatic pressure increases with depth, Δp = ρgΔh. The pressure difference between the bottom and top surfaces gives a larger upward force than downward force; that resultant is the upthrust.'))
parts.append(dict(pi=2, type='explain',
 K=lab('(b)(i)') + 'A small steel ball of radius <i>r</i> and mass <i>m</i> falls vertically at terminal speed <i>v</i> through oil. The viscous drag force <i>D</i> that acts on the ball is given by <i>D</i> = 6π<i>ηrv</i>, where <i>η</i> is a property of the oil called its viscosity.<br><br>Which diagram shows the directions of the three forces that act on the ball as it falls at terminal speed?',
 U='Three arrows from the ball: weight vertically downwards, and upthrust and drag both vertically upwards.',
 V='The weight acts downwards. The upthrust (from the pressure difference in the oil) acts upwards. The viscous drag opposes the downward motion, so it acts upwards. At terminal speed the upward forces balance the weight.',
 **choice(3)))
parts.append(dict(pi=3, type='calculation',
 K=lab('(b)(ii)') + 'A drag force <i>D</i> is described by <i>${lf}</i>, where <i>${ls}</i> is a constant. The force <i>D</i> is in newtons, the speed <i>v</i> in m s<sup>−1</sup> and the radius <i>r</i> in m.<br><br>Determine the SI base units of <i>${ls}</i>.',
 C1=kwv('kg m s-2', 'kg m s⁻²', 'kg m s^-2', 'kg m s^(-2)', 'kg m/s2', 'kg m/s^2', 'kg m/s²', 'kgms-2', 'f=ma', 'force=mass×acceleration', 'n=kg m s-2'),
 A='${ukw}',
 U='D has base units kg m s⁻²; ${ls} has base units ${ud_}',
 V='Force has base units kg m s⁻² (F = ma). Rearrange ${lf} for ${ls} and substitute the base units of D, v and (where it appears) r.'))
parts.append(dict(pi=4, type='calculation',
 K=lab('(c)(i)') + 'The oil in (b) has a density of ${rho} kg m<sup>−3</sup> and a viscosity of ${eta} in SI units. The steel ball has a mass of ${mbe} kg and a radius of ${r} × 10<sup>−3</sup> m.<br><br>Show that the upthrust force acting on the ball is ${Us2} N.',
 A='${Us}|${Ue}|${Ud}', tolerance='2',
 U='upthrust = ρgV = ${rho} × (4/3 × π × (${r} × 10⁻³)³) × 9.81 = ${Us2} N',
 V='Upthrust equals the weight of oil displaced, F = ρgV, where V is the volume of the ball, 4πr³/3, with r in metres.'))
parts.append(dict(pi=5, type='calculation',
 K=lab('(c)(ii)') + 'Determine the terminal speed <i>v</i> of the ball.',
 C2=kwv('weight=drag+upthrust', 'weight = drag + upthrust', 'w=d+u', 'mg=d+u', 'mg=u+d', 'w=u+d', 'mg=6πηrv+u', 'mg = 6πηrv + u', 'weight=upthrust+drag', 'resultant force=0', 'resultant force is zero', 'forces balance', 'forces are balanced', 'equilibrium', 'u+d=mg', 'u+d=w', 'd+u=w'),
 C1=kwv('${Ws}', '${Ws2}', '${mb}×9.81', '${mb}x9.81', '${Dns}', '6π×${eta}×${r}', '6×π×${eta}×${r}', '6π${eta}'),
 A='${vts}|${vtd}', tolerance='4',
 U='weight = ${mb} × 9.81 = ${Ws} N;  weight = drag + upthrust, so drag = ${Ws} − ${Us2} = ${Dns} N;  ${Dns} = 6π × ${eta} × (${r} × 10⁻³) × v, so v = ${vts} m s⁻¹',
 V='At terminal speed the forces balance: weight = drag + upthrust. Find the weight from mg, subtract the upthrust (use the value shown in (c)(i)), then rearrange D = 6πηrv for v.'))
ALL += question(LV, '9702-25-23-Q2', PAPER, 'calculation', 'Pressure,Forces including Density and pressure,Units,Dynamics', P2, G2, 'Pressure, upthrust and viscous drag on a falling ball', parts)

# =========================================================================== Q3  Wire: Young modulus, resistance, spring constant
MATS = ('[["copper",1.7e-8,1.3e11],["aluminium",2.8e-8,7.0e10],["silver",1.6e-8,8.3e10],["gold",2.4e-8,7.8e10],["iron",1.0e-7,2.1e11]]')
G3 = G_('sf', 'ex', 'us', 'sci', sk=SKETCH,
  MATS=MATS, mi='Math.floor(mip)', mat='MATS[mi]', mn='mat[0]', rho='mat[1]', E='mat[2]', rhos='ex(rho,1)', Es='ex(E,1)',
  d='+dp.toFixed(1)', dm='d*1e-3', A='Math.PI*dm*dm/4', Ae='ex(A,3)', Ae2='ex(A,2)',
  R='+Rp.toFixed(3)', L0='R*A/rho', Lm='+L0.toPrecision(2)', Ls='sf(Lm,2)', Ld='sf(L0,3)',
  k0='E*A/Lm', ks='ex(k0,1)', kd='ex(k0,2)', kx='E*A/L0', kxs='ex(kx,2)',
  ci1='Math.floor(cip1)', ci2='Math.floor(cip2)',
  mk1="(kind)=>sk({ylab:'R',xlab:'F',y0lab:'R<tspan font-size=\"10\" dy=\"4\">0</tspan>',y0level:0.35,f:(kind==='ok')?(u=>0.35+0.5*u):(kind==='flat')?(u=>0.35):(kind==='dec')?(u=>0.35-0.3*u):(u=>0.85*u)})",
  mk2="(kind)=>sk({ylab:'k',xlab:'F',y0lab:'k<tspan font-size=\"10\" dy=\"4\">0</tspan>',y0level:0.6,f:(kind==='ok')?(u=>0.6):(kind==='rise')?(u=>0.6+0.3*u):(kind==='dec')?(u=>0.6-0.5*u):(u=>0.9*u)})",
  ks1="['flat','dec','orig']", ks2="['rise','dec','orig']",
  opts1="(()=>{const a=[];let j=0;for(let q=0;q<4;q++)a.push(q===ci1?mk1('ok'):mk1(ks1[j++]));return a})()",
  opts2="(()=>{const a=[];let j=0;for(let q=0;q<4;q++)a.push(q===ci2?mk2('ok'):mk2(ks2[j++]));return a})()",
  p0='opts1[0]', p1='opts1[1]', p2='opts1[2]', p3='opts1[3]', q0='opts2[0]', q1='opts2[1]', q2='opts2[2]', q3='opts2[3]')
P3 = {'mip': [0, 4.99], 'dp': [1.0, 2.4], 'Rp': [0.020, 0.060], 'cip1': [0, 3.99], 'cip2': [0, 3.99]}
parts = []
parts.append(dict(pi=0, type='definition',
 K=lab('(a)') + 'A wire has length <i>L</i> and cross-sectional area <i>A</i>. The wire is made from a metal that has Young modulus <i>E</i> and resistivity <i>ρ</i>.<br><br>Define the Young modulus of a material.',
 B=kwv('stress/strain', 'stress / strain', 'stress divided by strain', 'stress over strain', 'ratio of stress to strain', 'stress÷strain', 'stress per strain', 'stress to strain', '(force/area)/(extension/length)', 'force per unit area divided by extension per unit length', 'tensile stress divided by tensile strain', 'tensile stress/tensile strain', 'stress ÷ strain', 'stress:strain', 'stress per unit strain', 'stress/ strain', 'stress /strain'),
 U='The Young modulus is the ratio of stress to strain (E = stress ÷ strain, below the limit of proportionality).',
 V='Young modulus = tensile stress ÷ tensile strain = (F/A) ÷ (x/L).'))
parts.append(dict(pi=1, type='definition',
 K=lab('(b)(i)') + 'State an expression, in terms of some or all of <i>L</i>, <i>A</i>, <i>E</i> and <i>ρ</i>, for the resistance <i>R</i><sub>0</sub> of the wire.',
 A=kwv('ρl/a', 'ρ l/a', 'ρ×l/a', 'ρxl/a', 'ρ*l/a', 'lρ/a', 'l×ρ/a', 'lxρ/a', 'l*ρ/a', '(ρl)/a', 'ρ(l/a)', 'ρla⁻¹', 'rho l/a', 'rho×l/a', 'rho*l/a', 'rho x l/a', 'rl/a', 'ρl÷a', 'ρl / a', 'ρ l / a', 'ρ × l / a', 'l ρ / a', 'ρ l a^-1', 'ρl/a', 'r0=ρl/a', 'ρ(l/a)', 'ρ × (l/a)', 'ρ x (l/a)', 'ρ*(l/a)'),
 U='R₀ = ρL / A',
 V='Resistivity is defined by R = ρL/A, so the resistance of the wire is ρL / A.'))
parts.append(dict(pi=2, type='explain',
 K=lab('(b)(ii)') + 'Show that the spring constant <i>k</i><sub>0</sub> of the wire is given by <i>k</i><sub>0</sub> = <i>EA</i> / <i>L</i>.',
 C1=kwv('k=f/x', 'k = f/x', 'f=kx', 'f = kx', 'k=f/e', 'k=f/δx', 'f=ke', 'hooke', 'spring constant=force/extension', 'spring constant = force / extension', 'k=force/extension', 'force/extension'),
 A=kwv('k0=ea/l', 'k=ea/l', 'ea/l', 'e×a/l', 'exa/l', 'e*a/l', 'e a / l', 'k0 = ea / l', 'k0=e×a/l', 'ea÷l', '(f/x)(l/a)', '(f/x)×(l/a)', 'k=(ea)/l', 'k0=(ea)/l', 'k = e a / l', 'ea / l', 'e × a / l'),
 U='E = stress/strain = (F/A) / (x/L) = FL / (Ax). Since k = F/x, E = kL/A, so k₀ = EA / L.',
 V='Start from the definition of the Young modulus, E = (F/A)/(x/L) = FL/(Ax). The spring constant is k = F/x, so E = kL/A. Rearranging gives k = EA/L.'))
parts.append(dict(pi=3, type='explain',
 K=lab('(c)(i)') + 'The wire is stretched, within the limit of proportionality, by a tensile force <i>F</i>. Assume that any changes in the cross-sectional area of the wire are negligible.<br><br>Which graph shows the variation with <i>F</i> of the resistance <i>R</i> of the wire?',
 U='A straight line with positive gradient starting at (0, R₀).',
 V='Within the limit of proportionality the extension is proportional to F, so the length L increases linearly with F. With A constant, R = ρL/A increases linearly: a straight line with positive gradient from R₀ at F = 0.',
 answerType='imageChoice', imageOptions='["${p0}","${p1}","${p2}","${p3}"]', correctImageIndex='${ci1}', imageChoiceMarks='1'))
parts.append(dict(pi=4, type='explain',
 K=lab('(c)(ii)') + 'Which graph shows the variation with <i>F</i> of the spring constant <i>k</i> of the wire?',
 U='A straight horizontal line starting at (0, k₀).',
 V='The wire obeys Hooke’s law within the limit of proportionality, so F is proportional to the extension and k = F/x is constant, equal to k₀.',
 answerType='imageChoice', imageOptions='["${q0}","${q1}","${q2}","${q3}"]', correctImageIndex='${ci2}', imageChoiceMarks='1'))
parts.append(dict(pi=5, type='calculation',
 K=lab('(d)(i)') + '${mn} has a resistivity of ${rhos} Ω m and a Young modulus of ${Es} Pa. A ${mn} wire of diameter ${d} mm has a resistance of ${R} Ω.<br><br>Show that the length of the wire is ${Ls} m.',
 A='${Ls}|${Ld}', tolerance='2',
 U='A = π(d/2)² = π × (${d} × 10⁻³ / 2)² = ${Ae2} m²;  L = RA/ρ = ${R} × ${Ae2} / ${rhos} = ${Ld} m = ${Ls} m',
 V='Use R = ρL/A and rearrange for L = RA/ρ. The cross-sectional area of a circular wire is A = πd²/4, with d converted to metres.'))
parts.append(dict(pi=6, type='calculation',
 K=lab('(d)(ii)') + 'Use the equation in (b)(ii) to determine the spring constant of the wire. Use a length of ${Ls} m.',
 C1=kwv('k=ea/l', 'k=e×a/l', 'ea/l', 'k0=ea/l', 'k=exa/l', 'k=e*a/l', 'e/r', 'k=e/r', '${Ae}', '${Ae2}', 'a=πd²/4', 'a=πr²', 'πr²', 'πd²/4', 'π(d/2)²', 'cross-sectional area=π'),
 A='${ks}|${kd}|${kxs}', tolerance='5',
 U='k₀ = EA / L = ${Es} × ${Ae2} / ${Ls} = ${ks} N m⁻¹',
 V='Substitute into k₀ = EA/L using the area from (d)(i) (${Ae2} m²), the Young modulus ${Es} Pa and the length ${Ls} m.'))
ALL += question(LV, '9702-25-23-Q3', PAPER, 'calculation', 'Materials,Electricity', P3, G3, 'A metal wire: Young modulus, resistivity and spring constant', parts)

# =========================================================================== Q4  Diffraction grating
INT = js(r"""(o)=>{const W=520,H=260,L=60,R=16,T=18,B=46,pw=W-L-R,ph=H-T-B;
const X=v=>L+(v+o.lim)/(2*o.lim)*pw,Y=y=>T+ph-ph*y*0.5;
let s='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 '+W+' '+H+'" width="'+W+'" height="'+H+'" font-family="Arial,sans-serif" font-size="13"><rect width="'+W+'" height="'+H+'" fill="#fff"/>';
s+='<rect x="'+L+'" y="'+T+'" width="'+pw+'" height="'+ph+'" fill="none" stroke="#000"/>';
for(let t=-Math.floor(o.lim/5)*5;t<=o.lim;t+=5){s+='<line x1="'+X(t)+'" y1="'+(T+ph)+'" x2="'+X(t)+'" y2="'+(T+ph+5)+'" stroke="#000"/><text x="'+X(t)+'" y="'+(T+ph+19)+'" text-anchor="middle">'+t+'</text>';}
s+='<text x="'+(L+pw/2)+'" y="'+(H-6)+'" text-anchor="middle">θ / °</text><text x="'+(L-8)+'" y="'+(Y(1)+4)+'" text-anchor="end">I<tspan font-size="10" dy="4">0</tspan></text><text x="'+(L-8)+'" y="'+(Y(2)+4)+'" text-anchor="end">2I<tspan font-size="10" dy="4">0</tspan></text><text x="'+(L-8)+'" y="'+(Y(0)+4)+'" text-anchor="end">0</text><text x="14" y="'+(T+ph/2)+'" font-style="italic" transform="rotate(-90 14,'+(T+ph/2)+')" text-anchor="middle">I</text>';
const w=o.lim*0.022;let p=[];
for(let i=0;i<=500;i++){const v=-o.lim+2*o.lim*i/500;let y=o.base;
 for(const pk of o.peaks){y+=(pk[1]-o.base)*Math.exp(-Math.pow((v-pk[0])/w,2));}
 p.push(X(v).toFixed(1)+','+Y(Math.min(y,1.98)).toFixed(1));}
s+='<polyline fill="none" stroke="#000" stroke-width="2" points="'+p.join(' ')+'"/></svg>';
return s;}""")
G4 = G_('sf', 'ex', 'us', 'sci', itn=INT,
  lam='Math.round(lamp/10)*10', dd='+dp.toFixed(1)', d='dd*1e-6', ln='lam*1e-9',
  t1='Math.asin(ln/d)*180/Math.PI', t2='Math.asin(2*ln/d)*180/Math.PI', t3='Math.asin(3*ln/d)*180/Math.PI',
  t1s='sf(t1,2)', t1d='sf(t1,3)', t2s='sf(t2,2)', t2d='sf(t2,3)', lim='Math.floor((t2+t3)/2)',
  ks="['shift','flat','tall']", ci='Math.floor(cip)',
  mk="(kind)=>{const P=(pos,h)=>pos.map(v=>[v,h(Math.abs(v))]);const hh=(a)=>a===0?1:(Math.abs(a-t1)<0.01?0.85:0.7);"
     "if(kind==='ok')return itn({lim:lim,base:0,peaks:[[0,1],[t1,0.85],[-t1,0.85],[t2,0.7],[-t2,0.7]]});"
     "if(kind==='shift'){const pk=[[0,1]];for(let n=1;n*t1/2<lim;n++){pk.push([n*t1/2,0.85]);pk.push([-n*t1/2,0.85]);}return itn({lim:lim,base:0,peaks:pk});}"
     "if(kind==='flat')return itn({lim:lim,base:0.35,peaks:[[0,1],[t1,0.85],[-t1,0.85],[t2,0.7],[-t2,0.7]]});"
     "return itn({lim:lim,base:0,peaks:[[0,1],[t1,1.6],[-t1,1.6],[t2,1.5],[-t2,1.5]]});}",
  opts=optsjs('ci'), o0='opts[0]', o1='opts[1]', o2='opts[2]', o3='opts[3]',
  ph='Math.round(php/5)*5', fac='+(Math.cos(ph*Math.PI/180)**2).toFixed(2)', pct='Math.round(fac*100)',
  fkw="JSON.stringify([['intensity','intensities','brightness','amplitude','peak','peaks','maxima','maximum','fringe'],"
      "[String(fac),String(pct)+'%',String(pct)+' %',(fac===0.5?'half':'zzzz'),(fac===0.5?'1/2':'zzzz'),(fac===0.5?'½':'zzzz'),'cos²','cos^2','cos2','malus',(fac===0.25?'quarter':'zzzz'),(fac===0.25?'1/4':'zzzz'),(fac===0.75?'3/4':'zzzz'),(fac===0.75?'three quarters':'zzzz'),(fac===0.75?'three-quarters':'zzzz')]])")
P4 = {'lamp': [480, 680], 'dp': [4.0, 7.0], 'cip': [0, 3.99], 'php': [30, 60]}
parts = []
parts.append(dict(pi=0, type='definition',
 K=lab('(a)') + 'State what is meant by diffraction of a wave.',
 B=kwv('through a gap', 'through a slit', 'through an aperture', 'passes through', 'passing through', 'passes a gap', 'passing an edge', 'passes an edge', 'at an edge', 'around an obstacle', 'past an obstacle', 'around an edge', 'at a gap', 'at a slit', 'at an aperture', 'through an opening', 'through a hole', 'encounters an obstacle', 'meets an obstacle', 'goes through a gap', 'goes through an aperture', 'obstacle', 'aperture', 'slit', 'gap', 'edge'),
 B2=kwv('spreads', 'spread out', 'spreads out', 'spreading', 'bends', 'diverge', 'spread', 'spreads into', 'bending', 'fan out', 'fans out', 'expands', 'widens', 'wavefront spreads', 'spreading out'),
 U='Diffraction is the spreading of a wave (into the region behind a gap or obstacle) as it passes through a gap / aperture or past an edge.',
 V='Waves spread out as they pass through a gap or around an obstacle. The effect is greatest when the gap width is comparable to the wavelength.'))
parts.append(dict(pi=1, type='calculation',
 K=lab('(b)(i)') + 'A beam of vertically polarised light of wavelength ${lam} nm is incident normally on a diffraction grating. The diffraction grating has a line spacing of ${dd} × 10<sup>−6</sup> m. The light transmitted by the grating illuminates a circular screen with the grating at the centre. The central bright fringe is formed at O and has intensity <i>I</i><sub>0</sub>. The intensity <i>I</i> of the light on the screen varies with the angle <i>θ</i> to the line from the grating to O.<br><br>Show that the angle <i>θ</i> at which the first-order bright fringe is formed is ${t1s}°.',
 C1=kwv('nλ=dsinθ', 'nλ = dsinθ', 'n λ = d sin θ', 'dsinθ=nλ', 'd sinθ=nλ', 'd sin θ = n λ', 'dsinθ=λ', 'd sin θ = λ', 'sinθ=λ/d', 'sin θ = λ/d', 'θ=sin-1(λ/d)', 'θ=sin^-1', 'sin-1', 'arcsin', 'asin', 'dsinθ=1λ', 'nλ=dsinθ', 'n*λ=d*sinθ', 'λ=dsinθ', 'λ = d sin θ'),
 A='${t1s}|${t1d}', tolerance='2',
 U='nλ = d sinθ with n = 1: θ = sin⁻¹(λ/d) = sin⁻¹(${lam} × 10⁻⁹ / (${dd} × 10⁻⁶)) = ${t1d}° = ${t1s}°',
 V='For a diffraction grating, d sinθ = nλ. For the first order n = 1, so sinθ = λ/d. Convert both lengths to metres and take the inverse sine.'))
parts.append(dict(pi=2, type='calculation',
 K=lab('(b)(ii)') + 'Determine the value of <i>θ</i> at which the second-order bright fringe is formed.',
 A='${t2s}|${t2d}', tolerance='3',
 U='n = 2: sinθ = 2λ/d, so θ = sin⁻¹(2 × ${lam} × 10⁻⁹ / (${dd} × 10⁻⁶)) = ${t2d}° ≈ ${t2s}°',
 V='Use d sinθ = nλ with n = 2. (The angle is not simply double the first-order angle, because sinθ, not θ, is proportional to n.)'))
parts.append(dict(pi=3, type='explain',
 K=lab('(b)(iii)') + 'Which graph shows the variation of the intensity <i>I</i> with <i>θ</i> for values of <i>θ</i> from −${lim}° to +${lim}°?',
 U='Narrow peaks at θ = 0 and at ±${t1s}° and ±${t2s}°, with zero intensity between them; the central peak has intensity I₀ and the other peaks are no taller than I₀.',
 V='Bright fringes (peaks) occur where d sinθ = nλ: θ = 0, ±${t1s}° and ±${t2s}° in this range (the third order, at ±${sf(t3,3)}°, is beyond the range shown). Between the orders the waves cancel, so the intensity is zero. The central peak is I₀ and the others are no larger.',
 **choice(3)))
parts.append(dict(pi=4, type='explain',
 K=lab('(c)') + 'A polarising filter is placed in the path of the light beam that is incident on the diffraction grating. The transmission axis of the filter is at ${ph}° to the vertical.<br><br>Suggest how the variation of intensity with <i>θ</i> for the light on the screen compares with the answer in (b)(iii).',
 B=kwv('same angle', 'same angles', 'same positions', 'same position', 'peaks at the same', 'same places', 'angles unchanged', 'angle unchanged', 'positions unchanged', 'position unchanged', 'same θ', 'same theta', 'same location', 'same pattern', 'no change in position', 'no change in angle', 'same place', 'maxima at the same', 'peaks in the same', 'peaks are in the same', 'fringes at the same', 'same fringe positions', 'same fringe spacing', 'same spacing', 'unchanged position', 'peak positions are the same', 'peaks remain at', 'remain at the same'),
 B2='${fkw}',
 U='The peaks occur at the same angles as in (b)(iii), but the intensity of every peak is reduced to cos²${ph}° = ${fac} (${pct}%) of its previous value.',
 V='The grating equation does not involve the polarisation, so the peak positions do not change. The filter only transmits the component of the (vertical) polarisation along its axis, ${ph}° from the vertical, so the amplitude is multiplied by cos ${ph}° and the intensity by cos² ${ph}° = ${fac}.'))
ALL += question(LV, '9702-25-23-Q4', PAPER, 'calculation', 'Waves,Superposition', P4, G4, 'Diffraction and a diffraction grating', parts)

# =========================================================================== Q5  Thermistor circuit
FIGCKT = js(r"""(E,r,R,dirw)=>{const W=520,H=300;
let s=@HD@+@AH@;
@LN@
@AR@
const box=(x,y,w,h)=>'<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" fill="#fff" stroke="#000" stroke-width="1.6"/>';
s+=ln(40,50,100,50)+ln(100,32,100,68)+ln(112,40,112,60)+ln(138,40,138,60)+ln(150,32,150,68)+ln(112,50,138,50,' stroke-dasharray="0"')+ln(150,50,170,50)+box(170,38,64,24)+ln(234,50,420,50);
s+='<text x="125" y="26" text-anchor="middle" font-style="italic">E = '+E+' V</text><text x="202" y="30" text-anchor="middle" font-style="italic">r = '+r+' Ω</text>';
s+=ln(40,50,40,250)+ln(420,50,420,250)+ln(40,250,420,250);
s+=ln(290,50,290,100)+box(278,100,24,70)+ln(290,170,290,250)+'<text x="272" y="140" text-anchor="end" font-style="italic">R = '+R+' Ω</text>';
s+=ln(370,50,370,100)+box(358,100,24,70)+ln(370,170,370,250)+'<line x1="348" y1="176" x2="392" y2="94" stroke="#000" stroke-width="1.6"/><text x="396" y="150" font-style="italic">T</text>';
s+='<circle cx="290" cy="50" r="3.5"/><circle cx="370" cy="50" r="3.5"/><circle cx="290" cy="250" r="3.5"/><circle cx="370" cy="250" r="3.5"/>';
s+='<text x="'+(W-12)+'" y="'+(H-8)+'" text-anchor="end" font-size="12">not to scale</text></svg>';
""" + cap("'5.1'") + "}")
G5 = G_('sf', 'ex',
  fig=FIGCKT, sk=SKETCH,
  E='+Ep.toFixed(2)', r='+rp.toFixed(2)', R='+Rp.toFixed(1)', frac='0.55+0.35*frp',
  IR='+(frac*E/R).toFixed(3)', VR='IR*R', Vr='E-VR', Ic0='Vr/r', Ic='+Ic0.toPrecision(2)', Ics='sf(Ic,2)', Icd='sf(Ic0,3)',
  IT='Ic-IR', IT0='Ic0-IR', RTa='VR/IT', RTb='VR/IT0', RTs='sf(RTa,2)', RTd='sf(RTa,3)', RTbs='sf(RTb,2)', RTbd='sf(RTb,3)',
  Vrs='sf(Vr,2)', VRs='sf(VR,3)', ITs='sf(IT,2)',
  dr='Math.floor(drp)', up='dr===0', w1='up?"increases":"decreases"', w2='up?"decreases":"increases"',
  q0t="up?'decreases with increasing temperature':'increases with decreasing temperature'",
  WI="['increases','rises','goes up','is greater','is larger','is higher','increased','gets bigger','gets larger','is bigger','increase']",
  WD="['decreases','falls','goes down','is smaller','is lower','is less','decreased','drops','gets smaller','reduces','is reduced','decrease','reduced']",
  gen="(subs,ws)=>subs.flatMap(x=>ws.map(w=>x+' '+w)).join('|')",
  rk="['resistance of the circuit','total resistance','circuit resistance','overall resistance','resistance of the whole circuit','resistance of the thermistor','thermistor resistance','resistance of t','resistance']",
  ck="['current in the cell','cell current','current in the battery','total current','current from the cell','current through the cell','current in cell','current from cell','current from the battery','current through the battery','current in the circuit','current']",
  tk="['terminal p.d.','terminal pd','terminal potential difference','terminal voltage','p.d. across the cell','p.d. across the resistor','p.d. across r','pd across r','voltage across r','p.d. across the terminals','potential difference across r','voltage across the resistor','p.d. across the internal resistance','pd across the internal resistance','voltage across the internal resistance','p.d. across internal resistance','pd across internal resistance','potential difference across the internal resistance','lost volts','p.d. across the thermistor','pd across the thermistor','voltage across the thermistor']",
  b1="gen(rk,up?WD:WI)", b2="gen(ck,up?WI:WD)",
  b3="gen(tk.filter(x=>/internal|lost volts| r$/.test(x)),up?WI:WD)+'|'+gen(tk.filter(x=>!/internal|lost volts| r$/.test(x)),up?WD:WI)",
  mk="(kind)=>{const f=(kind==='ok')?(u=>0.8*(0.05+0.95*Math.exp(-3.2*u))):(kind==='up')?(u=>0.8+0.18*Math.pow(u,2)):(kind==='zero')?(u=>0.8*(1-u)):(u=>0.8);"
     "return sk({ylab:'resistance',xlab:'temperature / °C',y0lab:'R<tspan font-size=\"10\" dy=\"4\">0</tspan>',y0level:0.8,xticks:[[0,'0'],[1,'100']],f:f});}",
  ks="['up','zero','flat']", ci='Math.floor(cip)', opts=optsjs('ci'), o0='opts[0]', o1='opts[1]', o2='opts[2]', o3='opts[3]', f51='fig(E,r,R,0)')
P5 = {'Ep': [1.2, 1.8], 'rp': [0.08, 0.20], 'Rp': [4.0, 9.0], 'frp': [0, 1], 'drp': [0, 1.99], 'cip': [0, 3.99]}
parts = []
parts.append(dict(pi=0, type='definition',
 K=lab('(a)') + 'State Kirchhoff’s first law.',
 B=andor(['sum of current', 'sum of the current', 'total current', 'sum of the currents', 'algebraic sum', 'current into', 'currents into', 'current entering', 'currents entering', 'current flowing into', 'current in', 'currents in'], ['junction', 'point', 'node', 'in a circuit']),
 U='The sum of the currents into a junction is equal to the sum of the currents out of the junction (the algebraic sum of the currents at a junction is zero).',
 V='Kirchhoff’s first law is conservation of charge: charge cannot build up at a junction, so the current arriving equals the current leaving.'))
parts.append(dict(pi=1, type='explain',
 K=lab('(b)(i)') + 'Figure 5.1 shows a circuit containing a thermistor T that has a negative temperature coefficient.${f51}The thermistor has resistance <i>R</i><sub>0</sub> at a temperature of 0 °C.<br><br>Which graph shows a possible variation of the resistance of the thermistor with temperature between 0 °C and 100 °C?',
 U='A line starting at R₀ with negative gradient throughout, falling from 0 °C to 100 °C and never reaching zero resistance.',
 V='For a negative temperature coefficient (NTC) thermistor the resistance falls as the temperature rises. The curve starts at R₀ at 0 °C and decreases, flattening out, but the resistance never reaches zero.',
 **choice(2)))
parts.append(dict(pi=2, type='explain',
 K=lab('(b)(ii)') + 'With reference to the current in the cell, explain why the current in resistor R ${q0t}.',
 B='${b1}', B2='${b2}', B3='${b3}',
 U='The resistance of the thermistor ${w2}, so the total resistance of the circuit ${w2} and the current in the cell ${w1}. The p.d. across the internal resistance (Ir) ${w1}, so the terminal p.d. ${w2}; R is constant, so the current in R ${w2}.',
 V='The thermistor resistance ${w2} as the temperature changes, so the total resistance ${w2}. The cell current therefore ${w1} (I = E/(R_total + r)), and the lost volts Ir ${w1} with it. The terminal p.d. is E − Ir, and it is the p.d. across R, so the current in R ${w2}.'))
parts.append(dict(pi=3, type='calculation',
 K=lab('(c)(i)') + 'The electromotive force (e.m.f.) <i>E</i> of the cell in Figure 5.1 is ${E} V. The internal resistance <i>r</i> of the cell is ${r} Ω. Resistor R has a resistance of ${R} Ω. At a particular temperature of the thermistor, the current in R is ${IR} A.<br><br>For this temperature of the thermistor, determine the current in the cell.',
 C1=kwv('v=ir', 'e-ir', 'e−ir', 'terminal p.d.=e', '${VRs}', '${IR}×${R}', '${IR}x${R}', '${IR}*${R}', 'p.d. across r', 'v=e-ir', 'lost volts', 'e=v+ir', '${Vrs}', 'i=v/r'),
 A='${Ics}|${Icd}', tolerance='3',
 U='terminal p.d. = p.d. across R = ${IR} × ${R} = ${VRs} V;  p.d. across r = ${E} − ${VRs} = ${sf(Vr,2)} V;  current in cell = ${sf(Vr,2)} / ${r} = ${Ics} A',
 V='R is connected across the terminals, so its p.d. is the terminal p.d. The e.m.f. minus the terminal p.d. is the p.d. across the internal resistance. Divide by r to get the cell current, I = (E − V) / r.'))
parts.append(dict(pi=4, type='calculation',
 K=lab('(c)(ii)') + 'Determine the resistance of the thermistor. (Use the current in the cell from (c)(i), to 2 significant figures.)',
 C1=kwv('${ITs}', 'i=i1+i2', 'i=ir+it', 'current in thermistor', 'current in the thermistor', '${Ics}−${IR}', '${Ics}-${IR}', '${Ic}−${IR}', '${Ic}-${IR}', 'kirchhoff', 'junction'),
 A='${RTs}|${RTd}|${RTbs}|${RTbd}', tolerance='3',
 U='current in thermistor = ${Ics} − ${IR} = ${ITs} A;  resistance of T = ${VRs} / ${ITs} = ${RTs} Ω',
 V='The cell current splits at the junction (Kirchhoff’s first law): I_T = I − I_R. The thermistor is in parallel with R, so it has the same p.d., ${VRs} V. Then R_T = V / I_T.'))
ALL += question(LV, '9702-25-23-Q5', PAPER, 'calculation', 'Electricity,D.C. circuits', P5, G5, 'A thermistor circuit: current, resistance and e.m.f.', parts)

# =========================================================================== Q6  Isotope, beta decay, quarks
ATOM = js(r"""(kind,Z,N)=>{const W=280,H=260,cx=140,cy=130;
let s='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 '+W+' '+H+'" width="'+W+'" height="'+H+'" font-family="Arial,sans-serif" font-size="11"><rect width="'+W+'" height="'+H+'" fill="#fff"/>';
const np=(kind==='noN')?Z:Z, nn=(kind==='noN')?0:(kind==='wrongN')?(N+2):N, ne=Z;
const items=[];for(let i=0;i<np;i++)items.push('p');for(let i=0;i<nn;i++)items.push('n');
if(kind==='eIn'){for(let i=0;i<ne;i++)items.push('e');}
for(let i=items.length-1;i>0;i--){const j=(i*7+3)%(i+1);const t=items[i];items[i]=items[j];items[j]=t;}
const c=7.5;
if(kind!=='eIn'){s+='<circle cx="'+cx+'" cy="'+cy+'" r="95" fill="none" stroke="#999" stroke-dasharray="3,3"/>';
 for(let i=0;i<ne;i++){const a=2*Math.PI*i/ne-Math.PI/2;const x=cx+95*Math.cos(a),y=cy+95*Math.sin(a);s+='<circle cx="'+x.toFixed(1)+'" cy="'+y.toFixed(1)+'" r="6" fill="#1f5fbf"/><text x="'+x.toFixed(1)+'" y="'+(y+3.5).toFixed(1)+'" text-anchor="middle" fill="#fff" font-size="9">e</text>';}}
items.forEach((t,i)=>{const r=c*Math.sqrt(i+0.5),a=i*2.39996;const x=cx+r*Math.cos(a),y=cy+r*Math.sin(a);const col=t==='p'?'#d9534f':(t==='n'?'#8c8c8c':'#1f5fbf');s+='<circle cx="'+x.toFixed(1)+'" cy="'+y.toFixed(1)+'" r="6.5" fill="'+col+'" stroke="#000" stroke-width="0.6"/><text x="'+x.toFixed(1)+'" y="'+(y+3.5).toFixed(1)+'" text-anchor="middle" fill="#fff" font-size="9">'+t+'</text>';});
s+='<text x="8" y="16" font-size="12">p proton, n neutron, e electron</text></svg>';
return s;}""")
ISO = ('[["H",1,3,"hydrogen","He",2,"helium","tritium"],["Li",3,8,"lithium","Be",4,"beryllium",""],["Be",4,10,"beryllium","B",5,"boron",""],'
       '["B",5,12,"boron","C",6,"carbon",""],["C",6,14,"carbon","N",7,"nitrogen",""]]')
G6 = G_('us', 'sb', 'sf', atom=ATOM, ISO=ISO,
  ii='Math.floor(iip)', iso='ISO[ii]', S='iso[0]', Z='iso[1]', A='iso[2]', nm='iso[3]', dS='iso[4]', Z2='iso[5]', dnm='iso[6]', tri='iso[7]',
  N='A-Z', ntxt="tri?(' that is called '+tri):''", nuc='us(A)+sb(Z)+S', dnuc='us(A)+sb(Z2)+dS',
  uu='2*Z+N', dd='Z+2*N',
  mk="(kind)=>atom(kind,Z,N)", ks="['eIn','noN','wrongN']", ci='Math.floor(cip)', opts=optsjs('ci'), o0='opts[0]', o1='opts[1]', o2='opts[2]', o3='opts[3]')
P6 = {'iip': [0, 4.99], 'cip': [0, 3.99]}
parts = []
parts.append(dict(pi=0, type='calculation',
 K=lab('(a)(i)') + 'The nuclide <sup>${A}</sup><sub>${Z}</sub>${S} is an isotope of ${nm}${ntxt}.<br><br>Determine the numbers of protons, neutrons and electrons in a neutral atom of this nuclide. Give your answer in the form “protons = …, neutrons = …, electrons = …”.',
 B='${Z}', B2='${N}',
 U='protons = ${Z}, neutrons = ${A} − ${Z} = ${N}, electrons = ${Z}',
 V='The proton number is ${Z}, so the atom has ${Z} protons. The number of neutrons is the nucleon number minus the proton number, ${A} − ${Z} = ${N}. A neutral atom has as many electrons as protons, ${Z}.'))
parts.append(dict(pi=1, type='explain',
 K=lab('(a)(ii)') + 'Which diagram shows a simple model of the arrangement of the protons, neutrons and electrons in an atom of the nuclide in (a)(i)?',
 U='A nucleus containing ${Z} protons and ${N} neutrons, with ${Z} electrons outside the nucleus, separated from it.',
 V='Protons and neutrons are together in the small central nucleus. The electrons are outside the nucleus, orbiting at a distance. There must be ${Z} protons, ${N} neutrons and ${Z} electrons.',
 **choice(2)))
parts.append(dict(pi=2, type='calculation',
 K=lab('(b)(i)') + 'The nuclide <sup>${A}</sup><sub>${Z}</sub>${S} is radioactive and undergoes β<sup>−</sup> decay to form an isotope of ${dnm} (${dS}). Gamma radiation is not emitted during this decay.<br><br>The decay is <sup>${A}</sup><sub>${Z}</sub>${S} → <sup>…</sup><sub>…</sub>${dS} + <sup>…</sup><sub>…</sub>β + <sup>0</sup><sub>0</sub>X.<br>Give the nucleon number and proton number of the ${dnm} nucleus and of the β<sup>−</sup> particle, in the form “${dS}: nucleon number = …, proton number = …; β: nucleon number = …, proton number = …”.',
 A=andor(['${A}'], ['${Z2}']), B='[["0"],["-1"]]',
 U='${dnuc}  (nucleon number ${A}, proton number ${Z2});  β⁻ particle: nucleon number 0, proton number −1',
 V='Nucleon number and charge are conserved. A neutron changes into a proton, so the proton number increases by 1 (${Z} → ${Z2}) and the nucleon number is unchanged (${A}). The β⁻ particle is an electron: nucleon number 0 and charge −1 (proton number −1). Check: ${Z} = ${Z2} + (−1) + 0.'))
parts.append(dict(pi=3, type='definition',
 K=lab('(b)(ii)') + 'State the name of particle X.',
 B=kwv('antineutrino', 'anti-neutrino', 'anti neutrino', 'electron antineutrino', 'electron anti-neutrino', 'electron anti neutrino', 'antielectron neutrino', 'anti electron neutrino', 'ν̄', 'v bar', 'neutrino bar', 'antineutrinos'),
 U='(electron) antineutrino',
 V='In β⁻ decay a neutron changes into a proton, an electron and an electron antineutrino. Lepton number is conserved: the electron (+1) is balanced by the antineutrino (−1).'))
parts.append(dict(pi=4, type='calculation',
 K=lab('(c)') + 'Determine the quark composition of a nucleus of <sup>${A}</sup><sub>${Z}</sub>${S}. Give your answer as the total numbers of up and down quarks.',
 C1=kwv('uud', 'udd', 'up up down', 'up down down', '2 up 1 down', '1 up 2 down', '2 up and 1 down', '1 up and 2 down', 'two up and one down', 'one up and two down', 'proton=uud', 'neutron=udd', 'proton: uud', 'neutron: udd', 'proton is uud', 'neutron is udd', 'proton = uud', 'neutron = udd', 'proton up up down', 'neutron up down down'),
 A=andor(['${uu}'], ['${dd}']),
 U='proton = uud, neutron = udd.  up quarks = 2 × ${Z} + ${N} = ${uu};  down quarks = ${Z} + 2 × ${N} = ${dd}',
 V='A proton contains two up quarks and one down quark (uud); a neutron contains one up and two down (udd). The nucleus has ${Z} protons and ${N} neutrons: up = 2(${Z}) + ${N} = ${uu}, down = ${Z} + 2(${N}) = ${dd}.'))
ALL += question(LV, '9702-25-23-Q6', PAPER, 'calculation', 'Particle physics', P6, G6, 'Isotopes, beta decay and quark composition', parts)

json.dump(ALL, open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False)
print(len(ALL), 'rows')
