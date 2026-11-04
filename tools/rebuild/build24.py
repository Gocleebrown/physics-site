import json, sys, os
sys.path.insert(0,'.')
from rowlib import *
from jshelpers import *

LV='AS'; PAPER='9702_s26_p24'
def lab(s): return '<b>'+s+'</b> '
def kwv(*alts):
    out=[]
    for a in alts:
        out.append(a)
        if '-' in a:
            out.append(a.replace('-','−')); out.append(a.replace('-','–'))
    return '|'.join(out)
ALL=[]
SF="(x,n)=>String(+x.toPrecision(n))"
EX="(x,d)=>x.toExponential(d).replace('e+','e')"
ST="(a,b)=>'<span style=\"display:inline-flex;flex-direction:column;vertical-align:middle;line-height:1.05;font-size:0.72em;text-align:right;margin-right:1px\"><span>'+a+'</span><span>'+b+'</span></span>'"
HD="'<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 '+W+' '+H+'\" style=\"max-width:'+W+'px;width:100%;background:#fff;display:block;margin:10px 0\" font-family=\"Arial,sans-serif\" font-size=\"14\">'"
AH="'<defs><marker id=\"ah\" viewBox=\"0 0 10 10\" refX=\"9\" refY=\"5\" markerWidth=\"7\" markerHeight=\"7\" orient=\"auto-start-reverse\"><path d=\"M0,0 L10,5 L0,10 z\" fill=\"#000\"/></marker></defs>'"

# ---- Figure 3.1: stationary wave on a string (4 loops, as in the paper) ----
FIG31 = r"""(Ls)=>{const W=560,H=270,x0=130,x1=430,cy=100,A=40;
let s=""" + HD + "+" + AH + r""";
const ln=(a,b,c,d,x)=>'<line x1="'+a+'" y1="'+b+'" x2="'+c+'" y2="'+d+'" stroke="#000" stroke-width="1.4"'+(x||'')+'/>';
let p1=[],p2=[];for(let i=0;i<=300;i++){const u=i/300,x=x0+(x1-x0)*u,y=Math.sin(Math.PI*4*u)*A;p1.push(x.toFixed(1)+','+(cy-y).toFixed(1));p2.push(x.toFixed(1)+','+(cy+y).toFixed(1));}
s+='<polyline fill="none" stroke="#000" stroke-width="1.8" points="'+p1.join(' ')+'"/><polyline fill="none" stroke="#000" stroke-width="1.2" stroke-dasharray="4,3" points="'+p2.join(' ')+'"/>';
s+=ln(x0,30,x0,cy,' stroke-dasharray="3,3"')+ln(x1,30,x1,cy,' stroke-dasharray="3,3"')+ln(x0,40,x1,40,' marker-start="url(#ah)" marker-end="url(#ah)"')+'<text x="'+((x0+x1)/2)+'" y="32" text-anchor="middle">'+Ls+' m</text>';
s+='<text x="40" y="70">fixed point</text>'+ln(100,76,x0-2,cy-2,'')+'<text x="448" y="62">fixed point</text>'+ln(446,66,x1+2,cy-2,'');
s+=ln(x0,cy,x0,200)+'<rect x="100" y="200" width="60" height="42" fill="#ddd" stroke="#000" stroke-width="1.4"/>';
s+=ln(112,150,112,190,' marker-start="url(#ah)" marker-end="url(#ah)"');
s+='<text x="180" y="226">vibration generator</text><text x="300" y="150">string</text>'+ln(310,138,330,cy+14,'');
s+='</svg>';
return s+'<p style="text-align:center;margin:0 0 10px"><b>Figure 3.1</b></p>';}"""

# ---- Figure 4.1: object just below the surface of a liquid ----
FIG41 = ("'<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 520 220\" style=\"max-width:520px;width:100%;background:#fff;display:block;margin:10px 0\" font-family=\"Arial,sans-serif\" font-size=\"14\">"
 "<rect x=\"140\" y=\"30\" width=\"260\" height=\"150\" fill=\"#ddd\"/><line x1=\"140\" y1=\"30\" x2=\"400\" y2=\"30\" stroke=\"#000\" stroke-width=\"1.4\"/>"
 "<rect x=\"220\" y=\"42\" width=\"46\" height=\"36\" fill=\"#888\" stroke=\"#000\"/><text x=\"40\" y=\"104\">object</text><line x1=\"84\" y1=\"98\" x2=\"222\" y2=\"60\" stroke=\"#000\"/>"
 "<text x=\"440\" y=\"70\">liquid</text><line x1=\"436\" y1=\"66\" x2=\"380\" y2=\"90\" stroke=\"#000\"/></svg><p style=\"text-align:center;margin:0 0 10px\"><b>Figure 4.1</b></p>'")

# ---- Figures 5.2 and 5.3 ----
CK = r"""(a,tag)=>{const W=520,H=290;
let s=""" + HD + "+" + AH + r""";
const ln=(x1,y1,x2,y2)=>'<line x1="'+x1+'" y1="'+y1+'" x2="'+x2+'" y2="'+y2+'" stroke="#000" stroke-width="1.6"/>';
const box=(x,y,w,h,t)=>'<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" fill="#fff" stroke="#000" stroke-width="1.6"/><text x="'+(x+w/2)+'" y="'+(y+h+20)+'" text-anchor="middle">'+t+'</text>';
const cell=x=>ln(x,40,x,80)+ln(x+10,50,x+10,70).replace('stroke-width="1.6"','stroke-width="4"');
const amm=x=>'<circle cx="'+x+'" cy="60" r="16" fill="#fff" stroke="#000" stroke-width="1.6"/><text x="'+x+'" y="66" text-anchor="middle" font-size="16">A</text>';
if(a.par){
 s+=ln(60,60,200,60)+cell(200)+ln(210,60,314,60)+amm(330)+ln(346,60,440,60)+ln(60,60,60,230)+ln(440,60,440,230);
 s+='<text x="205" y="30" text-anchor="middle">'+a.E+' V</text>';
 s+=ln(60,140,200,140)+'<rect x="200" y="126" width="44" height="28" fill="#fff" stroke="#000" stroke-width="1.6"/><text x="222" y="145" text-anchor="middle">X</text>'+ln(244,140,440,140);
 s+=ln(60,230,250,230)+'<rect x="250" y="216" width="60" height="28" fill="#fff" stroke="#000" stroke-width="1.6"/><text x="280" y="262" text-anchor="middle">'+a.R+' Ω</text>'+ln(310,230,440,230);
 s+='<circle cx="60" cy="140" r="3.5"/><circle cx="440" cy="140" r="3.5"/>';
}else{
 s+=ln(60,60,200,60)+cell(200)+ln(210,60,314,60)+amm(330)+ln(346,60,440,60)+ln(60,60,60,200)+ln(440,60,440,200);
 s+=ln(60,200,110,200)+'<rect x="110" y="186" width="44" height="28" fill="#fff" stroke="#000" stroke-width="1.6"/><text x="132" y="205" text-anchor="middle">X</text>'+ln(154,200,320,200);
 s+='<rect x="320" y="186" width="60" height="28" fill="#fff" stroke="#000" stroke-width="1.6"/><text x="350" y="232" text-anchor="middle">'+a.R+' Ω</text>'+ln(380,200,440,200);
}
s+='</svg>';
return s+'<p style="text-align:center;margin:0 0 10px"><b>Figure '+tag+'</b></p>';}"""

# ===================================================================== Q1
V6="['displacement','velocity','acceleration','force','momentum','weight']"
S8="['distance','speed','mass','energy','time','power','work','temperature']"
G1={'sf':SF,'ex':EX,'sci':SCI,
 'm':'Math.round(mp/100)*100','u':'Math.round(up)','s':'Math.round(sp)',
 'KE':'0.5*m*u*u','KE_ans':'ex(KE,1)','KE_sci':'sci(KE,1)','KE_r':'+KE.toPrecision(2)',
 'a':'u*u/(2*s)','a_ans':'sf(a,2)','a_r':'+a.toPrecision(2)',
 'F':'m*a','F_ans':'sf(F,2)','F2_ans':'sf(m*a_r,2)','F3_ans':'sf(KE_r/s,2)',
 's4':'4*s','u2':'2*u',
 'vs':'(()=>{const a='+V6+';return [a.splice(Math.floor(r1*a.length),1)[0],a.splice(Math.floor(r2*a.length),1)[0],a.splice(Math.floor(r3*a.length),1)[0]]})()',
 'ss':'(()=>{const a='+S8+';return [a.splice(Math.floor(r4*a.length),1)[0],a.splice(Math.floor(r5*a.length),1)[0]]})()',
 'lst':'(()=>{const k=[r6,r7,r8,r9,r10];return vs.concat(ss).map((x,i)=>[x,k[i]]).sort((p,q)=>p[1]-q[1]).map(p=>p[0])})()',
 'lst_s':"lst.join(', ')",'vs_s':"vs.join(', ')",'kwV':'JSON.stringify(vs.map(x=>[x]))'}
P1={'mp':[1000,1800],'up':[12,25],'sp':[25,60],'r1':[0,0.999],'r2':[0,0.999],'r3':[0,0.999],'r4':[0,0.999],'r5':[0,0.999],'r6':[0,1],'r7':[0,1],'r8':[0,1],'r9':[0,1],'r10':[0,1]}
parts=[]
parts.append(dict(pi=0,type='definition',
 K=lab('(a)')+'Identify all the vector quantities in the following list:<br>${lst_s}.',
 B='${kwV}',
 U='The vector quantities are ${vs_s}.',
 V='A vector quantity has both magnitude and direction. Scalars (here ${ss.join(", ")}) have magnitude only. All the vector quantities must be identified and no scalar quantity should be included.'))
parts.append(dict(pi=1,type='calculation',
 K=lab('(b)(i)')+'A car of mass ${m} kg is initially travelling horizontally in a straight line at a constant speed of ${u} m s<sup>−1</sup>. The brakes are applied and the car decelerates uniformly to rest in a distance of ${s} m.<br><br>Calculate the initial kinetic energy of the car.',
 C1=kwv('ek=½mv²','ek=½mv^2','ek=0.5mv²','ek=0.5mv^2','ke=½mv²','ke=0.5mv²','e=½mv²','e=0.5mv²','½mv²','½mv^2','0.5mv²','0.5mv^2','½×${m}×${u}²','½×${m}×${u}^2','0.5×${m}×${u}²','0.5×${m}×${u}^2','1/2mv^2','1/2mv²'),
 A='${KE_ans}',tolerance='1',
 U='E<sub>K</sub> = ½mv² = ½ × ${m} × ${u}² = ${KE_sci} J',
 V='Kinetic energy = ½mv², using the initial speed of the car.'))
parts.append(dict(pi=2,type='calculation',
 K=lab('(b)(ii)')+'Calculate the acceleration of the car.',
 C1=kwv('v²=u²+2as','v^2=u^2+2as','0=${u}²+2×a×${s}','0=${u}^2+2×a×${s}','0=${u}²+(2×a×${s})','0=${u}²+2a×${s}','a=-u²/2s','a=-${u}²/(2×${s})','a=-u^2/2s','a=u²/2s','a=u^2/2s'),
 A=kwv('-${a_ans}'),tolerance='1',
 U='v² = u² + 2as: 0 = ${u}² + (2 × a × ${s}), so a = −${a_ans} m s⁻²',
 V='Use the equation of motion for uniform deceleration to rest. The acceleration is negative because the car is slowing down (the sign matters in the mark scheme).'))
parts.append(dict(pi=3,type='calculation',
 K=lab('(b)(iii)')+'Calculate the resultant force on the decelerating car.',
 C1=kwv('f=ma','f=m×a','f=${m}×${a_ans}','f=${m}×-${a_ans}','f=w/s','f=e/s','f=ke/s','f=${KE_ans}/${s}','f=ek/s','w=fs','w=f×s','f=w/d'),
 A='${F_ans}|${F2_ans}|${F3_ans}',tolerance='3',
 U='F = ma = ${m} × ${a_ans} = ${F_ans} N (alternatively F = W / s = ${KE_sci} / ${s})',
 V='Newton’s second law F = ma using the acceleration from (b)(ii) (follow through). Alternatively the work done by the resultant force equals the kinetic energy removed, so F = E<sub>K</sub> / s.'))
parts.append(dict(pi=4,type='explain',
 K=lab('(c)(i)')+'The initial speed of the car in 1(b) is now doubled to ${u2} m s<sup>−1</sup>. The brakes of the car are then applied and the car comes to rest. The resultant force on the car remains the same as in 1(b)(iii).<br><br>Describe and explain the effect, if any, of doubling the initial speed on the magnitude of the acceleration of the car.',
 B=andor(['same','no change','constant','unchanged','equal','does not change','doesnt change','not change','stays'],['force','mass','f=ma','f and m']),
 U='The acceleration remains the same because the force and the mass are the same (F = ma).',
 V='a = F / m. Neither the resultant force nor the mass has changed, so the magnitude of the acceleration is unchanged.'))
parts.append(dict(pi=5,type='explain',
 K=lab('(c)(ii)')+'Describe and explain the effect, if any, of doubling the initial speed on the distance travelled by the car in coming to rest.',
 B=andor(['kinetic energy','ke','k.e','ek','e_k','energy'],['four times','4 times','4×','×4','x4','quadruple','quadrupled','factor of 4','factor of four','squared','v²','v^2','proportional to speed','proportional to v','increases by 4']),
 B2=andor(['distance','s','travel','stopping','braking','further','far'],['four times','4 times','4×','×4','x4','quadruple','quadrupled','factor of 4','factor of four','${s4}','increases by 4','squared','v²','v^2']),
 U='The initial kinetic energy is four times greater, so (for the same force) the distance travelled is four times greater (${s4} m).',
 V='Kinetic energy is proportional to speed squared, so doubling the speed gives four times the kinetic energy. The work done by the same force is Fs, so the distance is four times greater. (Using v² = u² + 2as with a unchanged gives the same result.)'))
ALL+=question(LV,'9702-26-24-Q1',PAPER,'definition','Kinematics,Dynamics,Energy',P1,G1,'Question 1',parts)

# ===================================================================== Q2
TAB="<table style=\"border-collapse:collapse;margin:10px 0\"><caption style=\"caption-side:top;text-align:center\"><b>Table 2.1</b></caption><tr><td style=\"border:1px solid #000;padding:4px 10px\">original length of spring X</td><td style=\"border:1px solid #000;padding:4px 10px\">(${L0s} ± ${dls}) cm</td></tr><tr><td style=\"border:1px solid #000;padding:4px 10px\">final length of spring X</td><td style=\"border:1px solid #000;padding:4px 10px\">(${Lfs} ± ${dls}) cm</td></tr><tr><td style=\"border:1px solid #000;padding:4px 10px\">mass of suspended object</td><td style=\"border:1px solid #000;padding:4px 10px\">(${Ms} ± ${dms}) kg</td></tr></table>"
G2={'sf':SF,
 'L0':'+L0p.toFixed(1)','Lf':'+Lfp.toFixed(1)','dl':'Math.max(0.1,Math.round(dlp*10)/10)','dm':'Math.max(0.005,Math.round(dmp*1000)/1000)','M':'Math.round(Mp*20)/20',
 'L0s':'L0.toFixed(1)','Lfs':'Lf.toFixed(1)','dls':'dl.toFixed(1)','dms':'dm.toFixed(3)','Ms':'M.toFixed(3)',
 'x':'+(Lf-L0).toFixed(1)','xs':'x.toFixed(1)','dx':'+(2*dl).toFixed(1)','dxs':'dx.toFixed(1)','xm':'x/100','xms':'xm.toFixed(3)',
 'k':'M*9.81/xm','k_ans':'sf(k,3)','k2_ans':'sf(k,2)',
 'pl':'dx/x*100','pm':'dm/M*100','pl_ans':'sf(pl,3)','pm_ans':'sf(pm,3)','pct':'pl+pm','pct_ans':'sf(pct,1)','pct_d':'sf(pct,2)'}
P2={'L0p':[1.5,4.0],'Lfp':[10.0,20.0],'dlp':[0.1,0.2],'dmp':[0.005,0.010],'Mp':[0.20,0.50]}
parts=[]
parts.append(dict(pi=0,type='definition',K=lab('(a)')+'State Hooke’s law.',
 B=andor(['extension','deformation','stretch','elongation'],['proportional','∝','varies directly'],['force','load','weight','applied']),
 U='The extension of a spring (or material) is directly proportional to the applied force (load), up to the limit of proportionality.',
 V='Hooke’s law: F ∝ x (so F = kx) as long as the limit of proportionality is not exceeded.'))
parts.append(dict(pi=1,type='numeric',
 K=lab('(b)(i)')+'In an experiment to determine the spring constant of a spring X, a student measures the original length of the spring. The student then suspends an object in equilibrium from the spring and measures the final length of the spring.<br><br>The spring does not extend beyond its limit of proportionality.<br>The measurements taken by the student are shown in Table 2.1.'+TAB+'Calculate the extension, in cm, of spring X together with its absolute uncertainty.',
 A=andor(['${xs}'],['${dxs}']),
 U='extension = (${xs} ± ${dxs}) cm',
 V='Extension = final length − original length = ${Lfs} − ${L0s} = ${xs} cm. The absolute uncertainties of the two lengths add: ${dls} + ${dls} = ${dxs} cm.'))
parts.append(dict(pi=2,type='calculation',
 K=lab('(b)(ii)')+'Calculate the spring constant of spring X.',
 C2=kwv('k=f/x','f=kx','k=f/e','k=f/l','f=ke','k=w/x','k=mg/x'),
 C1=kwv('${Ms}×9.81/${xms}','${Ms}×9.81/${xs}','${Ms}*9.81/${xms}','${Ms}x9.81/${xms}','${Ms}g/${xms}','(${Ms}×9.81)/${xms}','(${Ms}×9.81)/${xs}'),
 A='${k_ans}|${k2_ans}',tolerance='0.5',
 U='k = F / x = (${Ms} × 9.81) / ${xms} = ${k_ans} N m⁻¹',
 V='The force is the weight of the object, F = mg (use g = 9.81 m s⁻²). The extension must be in metres: ${xs} cm = ${xms} m. (Follow through from (b)(i) for the extension.)'))
parts.append(dict(pi=3,type='calculation',
 K=lab('(b)(iii)')+'Calculate the percentage uncertainty in the value of the spring constant calculated in 2(b)(ii) due to the uncertainties in the measurements.',
 C1=kwv('${dxs}/${xs}','${dms}/${Ms}','${pl_ans}','${pm_ans}','${pl_ans}%','${pm_ans}%'),
 A='${pct_ans}|${pct_d}',tolerance='0',
 U='percentage uncertainty = (${dxs} / ${xs} + ${dms} / ${Ms}) × 100 = ${pl_ans}% + ${pm_ans}% = ${pct_ans}%',
 V='The percentage uncertainties are added for a quotient: % uncertainty in x (${pl_ans}%) plus % uncertainty in the mass (${pm_ans}%). The answer is given to 1 significant figure in the mark scheme.'))
parts.append(dict(pi=4,type='explain',
 K=lab('(c)(i)')+'An identical object to the one in 2(b) is suspended in equilibrium from a spring Y that has a greater spring constant than spring X.<br><br>Spring Y does not extend beyond its limit of proportionality.<br><br>Describe and explain any difference in the extension of the springs.',
 B=andor(['less','smaller','shorter','not as much','not as large','reduced','lower extension'],['spring constant is greater','spring constant is larger','spring constant is higher','spring constant is bigger','greater spring constant','larger spring constant','higher spring constant','bigger spring constant','stiffer','more stiff','k is greater','k is larger','k is higher','k is bigger','greater k','larger k','higher k','inversely proportional','spring constant of y is greater','y has a greater','y has a larger','y has a higher']),
 U='The extension will be less for spring Y because the spring constant is greater (and the applied force is the same).',
 V='Extension x = F / k. The object (so the force) is the same, so the spring with the greater spring constant has the smaller extension.'))
parts.append(dict(pi=5,type='explain',
 K=lab('(c)(ii)')+'Describe and explain any difference in the elastic potential energy of the springs.',
 B=andor(['less','smaller','lower','reduced','not as much','not as great'],['energy','epe','potential','ep']),
 B2=kwv('½fx','1/2fx','0.5fx','½mgx','1/2mgx','0.5mgx','f²/k','f^2/k','(mg)²/2k','(mg)^2/2k','½(mg)²/k','½f²/k','extension is less','smaller extension','less extension','extension is smaller','extension is shorter','x is less','x is smaller','spring constant is greater','spring constant is larger','spring constant is higher','greater spring constant','larger spring constant','higher spring constant','k is greater','k is larger','k is higher','inversely proportional'),
 U='The elastic potential energy will be less for spring Y. The extension is less (for the same force) and E = ½Fx (or: the spring constant is greater and E = ½F² / k).',
 V='Elastic potential energy E = ½Fx = ½F²/k. The force F = mg is the same for both springs; spring Y has the smaller extension (larger k), so it stores less energy.'))
ALL+=question(LV,'9702-26-24-Q2',PAPER,'definition','Materials,Measurement',P2,G2,'Question 2',parts)

# ===================================================================== Q3
G3={'sf':SF,'fig31':FIG31,
 'L':'+Lp.toPrecision(2)','Ls':'L.toFixed(1)','f':'Math.round(fp)','lam':'L/2','lam_s':'lam.toFixed(2)','lam_t':'sf(lam,2)','v':'f*lam','v_ans':'sf(v,2)',
 'f31':'fig31(Ls)'}
P3={'Lp':[1.2,2.8],'fp':[20,40]}
parts=[]
parts.append(dict(pi=0,type='explain',
 K=lab('(a)')+'A stretched string is attached to two fixed points and a vibration generator as shown in Figure 3.1.${f31}The vibration generator oscillates vertically and a stationary wave is formed on the string.<br><br>Explain how the stationary wave is formed on the string.',
 B=kwv('reflect','reflection','reflected','bounces back off the fixed','rebounds'),
 B2=andor(['incident','reflected','two waves','two progressive','two travelling','two traveling','opposite direction','from the generator','original wave','initial wave','wave from the vibrator','waves travelling in opposite'],['superpose','superimpose','overlap','interfere','combine','interference','superposition','add','sum']),
 U='The wave from the vibration generator (incident wave) is reflected at the fixed point. The incident and reflected waves (travelling in opposite directions) superpose.',
 V='A stationary wave is formed by the superposition of two progressive waves of the same frequency travelling in opposite directions: the incident wave and the wave reflected at the fixed end.'))
parts.append(dict(pi=1,type='imageChoice',
 K=lab('(b)')+'On the string in Figure 3.1, a cross (×) is drawn at the position of a node. Which sketch shows the cross at the position of a node?',
 answerType='imageChoice',
 imageOptions=['as2624_q3b_c.svg','as2624_q3b_d.svg','as2624_q3b_a.svg','as2624_q3b_b.svg'],
 correctImageIndex='2',imageChoiceMarks='1',
 U='The cross is on the string at a point where the displacement is always zero (a node, vertically aligned with a node of the stationary wave).',
 V='Nodes are points of zero amplitude, where the string always passes through its equilibrium position. Antinodes are the points of maximum amplitude.'))
parts.append(dict(pi=2,type='calculation',
 K=lab('(c)')+'The distance between the fixed points is ${Ls} m. The vibration generator oscillates at a frequency of ${f} Hz.<br><br>Calculate the speed of progressive waves on the string.',
 C2=kwv('λ=${Ls}/2','λ=l/2','2λ=${Ls}','λ=${lam_s}','λ=${lam_t}','wavelength=${Ls}/2','${Ls}/2'),
 C1=kwv('v=fλ','v=f×λ','v=λf','v=λ×f','v=λ/t','v=λ/T','v=fl','c=fλ','v=f*λ','v=${f}×${lam_s}','v=${f}×${lam_t}','${f}×${lam_s}','${f}×${lam_t}'),
 A='${v_ans}',tolerance='2',
 U='The string has two wavelengths between the fixed points: λ = ${Ls} / 2 = ${lam_s} m. v = fλ = ${f} × ${lam_s} = ${v_ans} m s⁻¹',
 V='Figure 3.1 shows four loops, i.e. two complete wavelengths between the fixed points, so λ = ${Ls} / 2. Then use v = fλ.'))
parts.append(dict(pi=3,type='imageChoice',
 K=lab('(d)')+'The frequency of the vibration generator is now halved and a new stationary wave is formed on the string. The speed of progressive waves on the string is unchanged.<br><br>Which sketch shows the string at an instant when it has maximum displacement?',
 answerType='imageChoice',
 imageOptions=['as2624_q3d_d.svg','as2624_q3d_b.svg','as2624_q3d_c.svg','as2624_q3d_a.svg'],
 correctImageIndex='3',imageChoiceMarks='2',
 U='A sinusoidal line from fixed point to fixed point that crosses the equilibrium line once, in the middle: one complete wavelength between the fixed points (two loops).',
 V='v = fλ with v unchanged: halving f doubles λ. The wavelength was ${Ls}/2 = ${lam_s} m, so it becomes ${Ls} m: one complete wavelength between the fixed points (two loops), with a node at the centre.'))
ALL+=question(LV,'9702-26-24-Q3',PAPER,'definition','Superposition,Waves',P3,G3,'Question 3',parts)

# ===================================================================== Q4
G4={'sf':SF,
 'mo':'+mop.toPrecision(2)','Vo5':'+Vop.toPrecision(2)','Vos':'Vo5.toFixed(1)','Vo':'Vo5*1e-5','rl':'Math.round(rlp/50)*50',
 'W':'mo*9.81','U':'rl*Vo*9.81','D':'W-U','Wd':'W.toFixed(2)','Ud':'U.toFixed(2)','D_ans':'sf(D,2)','mos':'mo.toFixed(3)'}
P4={'mop':[0.050,0.090],'Vop':[0.8,1.4],'rlp':[1000,1300]}
parts=[]
parts.append(dict(pi=0,type='table',
 K=lab('(a)')+'An object is held at rest just below the surface of a liquid of uniform density as shown in Figure 4.1.'+FIG41.replace("'<svg","<svg").replace("</p>'","</p>")+'The object is released and accelerates downwards until it reaches terminal velocity.<br><br>The magnitude of the weight of the object is <i>W</i>.<br>The magnitude of the upthrust acting on the object is <i>U</i>.<br>The magnitude of the drag force acting on the object is <i>D</i>.<br><br>Complete Table 4.1 to show what happens to the magnitude of the three forces acting on the object as it accelerates. Type <i>increases</i>, <i>stays the same</i> or <i>decreases</i> in each box.',
 answerType='table',
 tableRowLabels='["W","D","U"]',
 tableColLabels='["Table 4.1: change as the object accelerates"]',
 tableCellKeywords='[[["exact:stays the same","exact:stay the same","exact:stays same","exact:the same","exact:same","exact:constant","exact:unchanged","exact:no change","exact:stays constant"]],[["exact:increases","exact:increase","exact:gets bigger","exact:gets larger","exact:increasing"]],[["exact:stays the same","exact:stay the same","exact:stays same","exact:the same","exact:same","exact:constant","exact:unchanged","exact:no change","exact:stays constant"]]]',
 tableCellAnswers='[["stays the same"],["increases"],["stays the same"]]',
 U='W: stays the same; D: increases; U: stays the same',
 V='The weight and (for a fully submerged object in a liquid of uniform density) the upthrust do not change. The drag force increases as the speed increases, until the resultant force is zero at terminal velocity.'))
parts.append(dict(pi=1,type='definition',
 K=lab('(b)')+'State an expression, in terms of <i>W</i>, <i>D</i> and <i>U</i>, that shows the relationship between the forces acting on the object when the object is at its terminal velocity.',
 A=kwv('w=d+u','w=u+d','d+u=w','u+d=w','w-d=u','w-u=d','d=w-u','u=w-d','w-u-d=0','w=(d+u)','w=(u+d)','d+u-w=0','u+d-w=0'),
 U='W = D + U',V='At terminal velocity the acceleration is zero, so the resultant force is zero: the downward force (the weight W) equals the sum of the upward forces (drag D and upthrust U).'))
parts.append(dict(pi=2,type='calculation',
 K=lab('(c)')+'The object has a mass of ${mos} kg and a volume of ${Vos} × 10<sup>−5</sup> m<sup>3</sup>.<br>The density of the liquid is ${rl} kg m<sup>−3</sup>.<br><br>Calculate <i>D</i> when the object is at terminal velocity.',
 C2=kwv('w=${mos}×9.81','w=mg','${mos}×9.81','${Wd}'),
 C1=kwv('u=${rl}×9.81×${Vos}','u=ρvg','u=ρgv','u=${rl}×${Vos}','${rl}×9.81×${Vos}','${Ud}','u=weight of liquid displaced','u=rhogv','u=rhovg','u=rho*g*v','u=rho×g×v','u=ρ*g*v','u=ρ×g×v','u=ρvg'),
 A='${D_ans}',tolerance='2',
 U='W = ${mos} × 9.81 = ${Wd} N. U = ρVg = ${rl} × 9.81 × ${Vos} × 10⁻⁵ = ${Ud} N. D = W − U = ${Wd} − ${Ud} = ${D_ans} N',
 V='At terminal velocity W = D + U. The upthrust equals the weight of liquid displaced: U = ρVg (the object is completely submerged, so the displaced volume equals the volume of the object).'))
ALL+=question(LV,'9702-26-24-Q4',PAPER,'definition','Pressure,Dynamics',P4,G4,'Question 4',parts)

# ===================================================================== Q5
G5={'sf':SF,'ex':EX,'gsvg':GSVG,'ck':CK,
 'V1':'[0.66,0.68,0.70,0.72,0.74][Math.floor(v1i)]','I1':'[4,5][Math.floor(i1i)]','dV':'0.80-V1','R':'Math.round(dV*1000/I1)',
 'I2':'[25,30,35,40][Math.floor(i2i)]','Vt':'dV/Math.log(I2/I1)',
 'V1s':'V1.toFixed(2)','V1t':'String(+V1.toFixed(2))','I1s':'I1.toFixed(1)','I1A':'I1/1000','dVs':'dV.toFixed(2)','dVt':'String(+dV.toFixed(2))',
 'IR':'0.80/R','IRs':'(0.80/R).toFixed(3)','IRt':'String(+(0.80/R).toFixed(3))','I2A':'I2/1000','I2As':'(I2/1000).toFixed(3)','Itot':'IR+I2/1000','Itot_ans':'sf(Itot,2)','Itot_s':'Itot.toFixed(3)',
 'pts':'(()=>{const a=[];for(let v=0;v<=0.8001;v+=0.005)a.push([+v.toFixed(3),I1*Math.exp((v-V1)/Vt)]);return a})()',
 'fig51':"gsvg({x0:0,x1:0.8,y0:0,y1:40,mx:0.02,my:1,Mx:0.2,My:10,xl:'V / V',yl:'I / mA',pts:pts,cap:'Figure 5.1',H:440})",
 'f52':"ck({R:R},'5.2')",'f53':"ck({R:R,par:1,E:'0.80'},'5.3')"}
P5={'v1i':[0,4.99],'i1i':[0,1.99],'i2i':[0,3.99]}
parts=[]
parts.append(dict(pi=0,type='definition',
 K=lab('(a)')+'The I–V characteristic of an electrical component X is shown in Figure 5.1.${fig51}State the name of electrical component X.',
 B=kwv('diode','exact:led','exact:an led','exact:the led','light emitting diode','light-emitting diode'),
 U='(Semiconductor) diode',V='The current is almost zero until the p.d. reaches the threshold value (about 0.6–0.7 V) and then increases rapidly; there would be almost no current if the p.d. were reversed. This is the characteristic of a diode.'))
parts.append(dict(pi=1,type='imageChoice',
 K=lab('(b)')+'A metallic conductor has a constant resistance of 40 Ω. Which sketch shows the <i>I</i>–<i>V</i> characteristic of this conductor between <i>V</i> = 0 and <i>V</i> = 0.80 V? All the sketches use the axes of Figure 5.1.',
 answerType='imageChoice',
 imageOptions=['as2624_q5b_b.svg','as2624_q5b_d.svg','as2624_q5b_a.svg','as2624_q5b_c.svg'],
 correctImageIndex='2',imageChoiceMarks='2',
 U='A straight line through the origin passing through (0.80 V, 20 mA).',
 V='For a constant resistance the I–V graph is a straight line through the origin. At V = 0.80 V, I = V / R = 0.80 / 40 = 0.020 A = 20 mA.'))
parts.append(dict(pi=2,type='calculation',
 K=lab('(c)')+'Component X is connected in a circuit with a resistor of resistance ${R} Ω as shown in Figure 5.2.${f52}The current in the ammeter is ${I1s} mA and the cell has negligible internal resistance.<br><br>Show that the electromotive force (e.m.f.) of the cell is 0.80 V.',
 C2=kwv('${V1s}','${V1t}','${V1s} v','${V1t} v'),
 C1=kwv('${dVs}','${dVt}','${I1A}×${R}','${I1A}*${R}','${I1A}x${R}','${I1}e-3×${R}'),
 A=andor(['${V1s}','${V1t}'],['${I1A}','${I1}e-3','${I1}×10^-3','${I1}×10-3','${I1}x10^-3'],['${R}'],['0.80','0.8']),
 tolerance='3',
 U='From Figure 5.1, the p.d. across X when the current is ${I1s} mA is ${V1s} V. The p.d. across the resistor = ${I1A} × ${R} = ${dVs} V. e.m.f. = ${V1s} + ${I1A} × ${R} = 0.80 V',
 V='The e.m.f. is shared between X and the resistor (they are in series, with negligible internal resistance). Read the p.d. across X from the graph at the stated current; the p.d. across the resistor is IR (current in amperes). Add them.'))
parts.append(dict(pi=3,type='numeric',
 K=lab('(d)')+'The terminals of the cell in 5(c) are now reversed without making any other changes to the circuit.<br><br>State the reading on the ammeter.',
 A=kwv('exact:0','exact:0a','exact:0amps','exact:0amp','exact:0 a','exact:zero','exact:zero a','exact:zero amps','approximately zero','approximately 0','about zero','almost zero','nearly zero','zero current','no current'),
 U='0 A (approximately zero)',V='The diode does not conduct when it is reverse biased (the p.d. is in the reverse direction), so the current is approximately zero.'))
parts.append(dict(pi=4,type='calculation',
 K=lab('(e)')+'The resistor of resistance ${R} Ω and component X are now connected in parallel to the cell in 5(c) in the circuit shown in Figure 5.3.${f53}The current in component X is not negligible.<br><br>Use Figure 5.1 to determine the current in the ammeter.',
 C2=kwv('0.80/${R}','0.8/${R}','${IRt}','${IRs}','i=v/r'),
 C1=kwv('${I2} ma','${I2}ma','${I2A}','${I2As}','${I2}×10^-3','${I2}×10-3','${I2}e-3'),
 A='${Itot_ans}|${Itot_s}',tolerance='5',
 U='Current in the resistor = 0.80 / ${R} = ${IRs} A. From Figure 5.1, the current in X at 0.80 V is ${I2} mA = ${I2As} A. The current in the ammeter = ${IRs} + ${I2As} = ${Itot_s} A',
 V='In a parallel circuit the p.d. across each branch is the e.m.f. (0.80 V). Find each branch current (resistor: I = V/R; X: read from the graph at 0.80 V) and add them, because the ammeter carries the total current.'))
ALL+=question(LV,'9702-26-24-Q5',PAPER,'definition','Electricity',P5,G5,'Question 5',parts)

# ===================================================================== Q6
G6={'sf':SF,'ex':EX,'sci':SCI,
 'An':'+Anp.toPrecision(2)','Ans':'An.toFixed(1)','A':'An*1e-8','Vq':'Math.round(Vqp/10)*10','Pk':'+Pkp.toPrecision(2)','Pks':'Pk.toFixed(1)','Pw':'Pk*1000',
 'R':'Vq*Vq/Pw','Rs':'sf(R,2)','Rr':'+R.toPrecision(2)','rn':'+rnp.toPrecision(2)','rns':'rn.toFixed(1)','rho':'rn*1e-6',
 'L':'Rr*A/rho','L_ans':'sf(L,2)','vd':'+vdp.toPrecision(2)','vds':'vd.toFixed(1)',
 'I':'Pw/Vq','I_ans':'sf(I,3)','I_2':'sf(I,2)','n':'I/(1.6e-19*A*vd*1e-3)','n_ans':'ex(n,1)','n_sci':'sci(n,1)'}
G6['n']='I/(1.6e-19*A*vd*1e-3)'
P6={'Anp':[4.0,9.0],'Vqp':[200,240],'Pkp':[0.5,1.5],'rnp':[1.0,1.5],'vdp':[4.0,8.0]}
parts=[]
parts.append(dict(pi=0,type='calculation',
 K=lab('(a)')+'A nichrome wire of cross-sectional area ${Ans} × 10<sup>−8</sup> m<sup>2</sup> is connected to a power supply. The potential difference (p.d.) across the wire is ${Vq} V. The power dissipated in the wire is ${Pks} kW.<br><br>Show that the resistance of the wire is ${Rs} Ω.',
 C1=kwv('p=v²/r','p=v^2/r','p=vi','p=iv','p=i²r','p=i^2r','r=v²/p','r=v^2/p','v²/p','v^2/p','p=v×i'),
 A=andor(['${Vq}'],['${Pw}','${Pw}w','${Pks}e3','${Pks}×10^3','${Pks}×10³','${Pks}x10^3'],['${Rs}']),
 U='P = V² / R, so R = V² / P = ${Vq}² / ${Pw} = ${Rs} Ω',
 V='Use P = V²/R. The power must be in watts (${Pks} kW = ${Pw} W) – a full substitution is needed in a “show that” question.'))
parts.append(dict(pi=1,type='calculation',
 K=lab('(b)')+'The resistivity of nichrome is ${rns} × 10<sup>−6</sup> Ω m.<br><br>Calculate the length of the wire.',
 C1=kwv('r=ρl/a','ρ=ra/l','l=ra/ρ','r=ρ×l/a','l=r×a/ρ','l=${Rs}×${Ans}','ρl/a','rho=ra/l','r=rhol/a','l=ra/rho','r=rho×l/a','r=rho*l/a'),
 A='${L_ans}',tolerance='2',
 U='R = ρL / A, so L = RA / ρ = (${Rs} × ${Ans} × 10⁻⁸) / (${rns} × 10⁻⁶) = ${L_ans} m',
 V='Resistivity ρ = RA / L, rearranged for the length. Use the resistance found in (a) and the cross-sectional area given in the stem.'))
parts.append(dict(pi=2,type='calculation',
 K=lab('(c)')+'The average drift speed of the charge carriers (free electrons) in the nichrome wire is ${vds} × 10<sup>−3</sup> m s<sup>−1</sup>.<br><br>Calculate the number density of charge carriers of nichrome.',
 C2=kwv('i=anvq','i=nqav','n=i/(qav)','n=i/qav','n=i/(anv)','n=i/(eav)','n=i/anve','i=nave','i=navq','n=i/aqv','i=a×n×v×q'),
 C1=kwv('${I_ans}','${I_2}','i=p/v','i=v/r','i=${Pw}/${Vq}','${Pw}/${Vq}','${Vq}/${Rs}'),
 A='${n_ans}',tolerance='2',
 U='I = P / V = ${Pw} / ${Vq} = ${I_ans} A. I = Anvq, so n = I / (Avq) = ${I_ans} / (1.6 × 10⁻¹⁹ × ${Ans} × 10⁻⁸ × ${vds} × 10⁻³) = ${n_sci} m⁻³',
 V='The current is found from P = IV. Then use I = Anvq (q is the elementary charge 1.6 × 10⁻¹⁹ C). Check the powers of ten in the cross-sectional area and drift speed.'))
ALL+=question(LV,'9702-26-24-Q6',PAPER,'definition','Electricity',P6,G6,'Question 6',parts)

# ===================================================================== Q7
EL="[['thorium','Th',90,226,234],['uranium','U',92,230,238],['radium','Ra',88,222,228],['polonium','Po',84,208,216]]"
G7={'st':ST,
 'e':EL+'[Math.floor(ei)]','en':'e[0]','sy':'e[1]','Z':'e[2]','A0':'e[3]+Math.round(ap*(e[4]-e[3]))','k':'Math.floor(kp)','Af':'A0-4*k','nb':'2*k',
 'nuc':"st(A0,Z)+sy",'nucf':"st(Af,Z)+sy"}
P7={'ei':[0,3.99],'ap':[0,1],'kp':[1,3.99]}
parts=[]
parts.append(dict(pi=0,type='definition',K=lab('(a)(i)')+'State what is meant by isotopes.',
 B=kwv('same proton number','same number of protons','same atomic number','equal number of protons','same number of proton','same proton no','same atomic no','identical number of protons','same number protons','same protons'),
 B2=kwv('different nucleon number','different number of neutrons','different mass number','different neutron number','different number of nucleons','different nucleon no','different neutron no','different numbers of neutrons','different amount of neutrons','different neutrons','different mass'),
 U='Isotopes are (different forms of the same) element / nuclei with the same proton number (atomic number) and different nucleon number (number of neutrons).',
 V='Isotopes of an element have the same number of protons (so the same chemical properties) but different numbers of neutrons, hence different nucleon numbers.'))
parts.append(dict(pi=1,type='numeric',
 K=lab('(a)(ii)')+'A ${en}-${A0} nucleus (${nuc}) undergoes radioactive decay to form another nucleus. A sequence of further decays occurs until a nucleus is formed that is another isotope of ${en}. In each decay, either a single α-particle or a single β<sup>−</sup> particle is emitted.<br><br>Determine the minimum numbers of α-particles and β<sup>−</sup> particles that could be emitted during the sequence of decays to form the other isotope of ${en} from ${en}-${A0}.',
 B=kwv('alpha=${k}','alpha:${k}','alpha${k}','${k}alpha','α=${k}','α:${k}','α${k}','${k}α','alphaparticles=${k}','alphaparticle=${k}','α-particles=${k}','α-particle=${k}','alphas=${k}'),
 B2=kwv('beta=${nb}','beta:${nb}','beta${nb}','${nb}beta','β=${nb}','β:${nb}','β${nb}','${nb}β','betaparticles=${nb}','beta-=${nb}','β-=${nb}','β⁻=${nb}','betas=${nb}','beta-particles=${nb}','β-particles=${nb}','β⁻particles=${nb}','β⁻particle=${nb}','β⁻-particles=${nb}','β⁻=${nb}','β−=${nb}','β−particles=${nb}','β+=${nb}'.replace('+','-')),
 U='minimum number of α-particles = ${k}; minimum number of β⁻ particles = ${nb}',
 V='Each α decay reduces the nucleon number by 4 and the proton number by 2. The isotope formed has the same proton number but a different nucleon number. Each β⁻ decay increases the proton number by 1. To return to proton number ${Z} after ${k} α decay(s) (proton number falls by ${nb}) needs ${nb} β⁻ decays.'))
parts.append(dict(pi=2,type='numeric',
 K=lab('(a)(iii)')+'State the nucleon number and the proton number of the ${en} isotope formed by the sequence of decays in (a)(ii).',
 B='${Af}',B2='${Z}',
 U='nucleon number = ${Af}; proton number = ${Z}  (${nucf})',
 V='The nucleon number falls by 4 for each α-particle emitted: ${A0} − 4 × ${k} = ${Af}. The proton number is the same as before, ${Z}, because it is another isotope of ${en}.'))
parts.append(dict(pi=3,type='definition',K=lab('(b)(i)')+'State the quark composition of a proton.',
 B=kwv('uud','udu','duu','up up down','up, up, down','up up and down','two up and one down','two up and a down','2 up and 1 down','2 up 1 down','u u d','u,u,d','up up anti','2 up quarks and 1 down','two up quarks and one down','two up quarks and a down','u, u, d'),
 U='up, up, down (uud)',V='A proton is a baryon made of two up quarks (+⅔e each) and one down quark (−⅓e): total charge +1e.'))
parts.append(dict(pi=4,type='definition',K=lab('(b)(ii)')+'Describe the change to the quark composition of the proton when it undergoes β<sup>+</sup> decay.',
 B=kwv('up to down','u to d','up quark to down','up quark changes to a down','up becomes down','up changes to down','one up becomes one down','u→d','u->d','u−>d','u–>d','u → d','one up quark changes to one down','uud to udd','uud→udd','uud -> udd','uud −> udd','uud –> udd','uud → udd','up to a down','changes to udd','becomes udd','up quark turns into a down','up quark turns to a down','up quark is changed to a down','an up quark changes to a down quark'),
 U='An up quark changes to a down quark (uud → udd).',V='In β⁺ decay a proton changes into a neutron: an up quark changes into a down quark, with emission of a positron and an electron neutrino.'))
ALL+=question(LV,'9702-26-24-Q7',PAPER,'definition','Particle physics',P7,G7,'Question 7',parts)

if __name__=='__main__':
    start=int(sys.argv[1]) if len(sys.argv)>1 else 288
    write_json(ALL,'new24.json',start=start)
    from collections import Counter
    print(len(ALL),'rows',Counter(r['id'] for r in ALL))
