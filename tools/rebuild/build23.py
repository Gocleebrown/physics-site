import json, sys, os
sys.path.insert(0,'.')
from rowlib import *
from jshelpers import *

LV='AS'; PAPER='9702_s26_p23'
def lab(s): return '<b>'+s+'</b> '
def kwv(*alts):
    """pipe list; each alternative containing a hyphen also gets unicode-minus and en-dash forms"""
    out=[]
    for a in alts:
        out.append(a)
        if '-' in a:
            out.append(a.replace('-','−')); out.append(a.replace('-','–'))
    return '|'.join(out)
def andv(*groups):
    return andor(*[[x for a in g for x in ([a]+([a.replace('-','−'),a.replace('-','–')] if '-' in a else []))] for g in groups])
ALL=[]
SF="(x,n)=>String(+x.toPrecision(n))"
EX="(x,d)=>x.toExponential(d).replace('e+','e')"

# ---- figure 3.1 : double slit (values from the parameters) ----
FIG31 = r"""(lam,a,D)=>{const W=620,H=280;
let s='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 '+W+' '+H+'" style="max-width:'+W+'px;width:100%;background:#fff;display:block;margin:10px 0" font-family="Arial,sans-serif" font-size="14">';
s+='<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker></defs>';
const ln=(a,b,c,d,x)=>'<line x1="'+a+'" y1="'+b+'" x2="'+c+'" y2="'+d+'" stroke="#000" stroke-width="1.4"'+(x||'')+'/>';
s+='<rect x="215" y="40" width="8" height="78" fill="#999" stroke="#000"/><rect x="215" y="130" width="8" height="20" fill="#999" stroke="#000"/><rect x="215" y="162" width="8" height="78" fill="#999" stroke="#000"/>';
[70,100,140,180,210].forEach(y=>{s+=ln(40,y,190,y,' marker-end="url(#ah)"');});
s+=ln(520,25,520,255)+'<circle cx="520" cy="108" r="3.5"/><circle cx="520" cy="140" r="3.5"/>';
s+='<text x="532" y="113">Y</text><text x="532" y="145">X</text>';
s+=ln(223,140,520,140,' stroke-dasharray="5,3"');
s+=ln(236,124,236,156,' marker-start="url(#ah)" marker-end="url(#ah)"')+ln(226,124,244,124,' stroke-dasharray="2,2"')+ln(226,156,244,156,' stroke-dasharray="2,2"');
s+='<text x="248" y="116">'+a+' × 10<tspan font-size="11" dy="-6">−5</tspan><tspan dy="6"> m</tspan></text>';
s+=ln(223,200,520,200,' marker-start="url(#ah)" marker-end="url(#ah)"')+'<text x="360" y="192" text-anchor="middle">'+D+' m</text>';
s+='<text x="30" y="135">coherent light,</text><text x="30" y="153">wavelength '+lam+' nm</text>';
s+='<text x="225" y="22" text-anchor="middle">double slit</text>'+ln(225,28,219,42);
s+='<text x="570" y="22">screen</text>'+ln(566,28,522,40);
s+='<text x="600" y="250" text-anchor="end">not to scale</text></svg>';
return s+'<p style="text-align:center;margin:0 0 10px"><b>Figure 3.1</b></p>';}"""

# ===================================================================== Q1
G1={'sf':SF,'gsvg':GSVG,
 'mX':'+mxp.toPrecision(2)','mXs':'mX.toFixed(2)',
 'u':'+(Math.round(up*5)/5).toFixed(1)',
 'w':'+Math.min(Math.round(wp*5)/5,u-0.4).toFixed(1)',
 'tA':'Math.round(tAp)/100','dt':'Math.round(dtp)/100','tB':'(Math.round(tAp)+Math.round(dtp))/100',
 'tAs':'tA.toFixed(2)','tBs':'tB.toFixed(2)','dts':'dt.toFixed(2)',
 'a':'(u+w)/dt','a_ans':'sf(a,2)',
 'dp':'mX*(u+w)','dp_ans':'sf(dp,2)',
 'dist':'0.5*dt*(u*u+w*w)/(u+w)','dist_ans':'sf(dist,2)',
 'vY':'+(u-w).toFixed(1)','mY':'mX*(u+w)/vY','mY_ans':'sf(mY,2)',
 'pts':'[[0,u],[tA,u],[tB,-w],[0.2,-w]]',
 'fig11':"gsvg({x0:0,x1:0.2,y0:-2,y1:2,mx:0.01,my:0.1,Mx:0.05,My:1,xl:'time / s',yl:'velocity / m s⁻¹',pts:pts,cap:'Figure 1.1',H:440})"}
P1={'mxp':[0.10,0.30],'up':[1.15,1.85],'wp':[0.35,1.05],'tAp':[7,11],'dtp':[2,4]}
parts=[]
parts.append(dict(pi=0,type='definition',K=lab('(a)')+'Define momentum.',
 B=kwv('product of mass and velocity','mass×velocity','mass x velocity','mass*velocity','mass times velocity','mass multiplied by velocity','multiplied by velocity','mass and velocity','p=mv','momentum=mv','m×v','m*v','mass×its velocity'),
 U='Momentum is the product of mass and velocity.',V='Momentum p = mv. It is a vector, so it has the direction of the velocity (the word velocity, not speed, is needed).'))
parts.append(dict(pi=1,type='calculation',
 K=lab('(b)(i)')+'A ball X of mass ${mXs} kg moves along a horizontal frictionless surface. The ball collides elastically with ball Y that is initially stationary. Balls X and Y have equal diameters but different masses.<br><br>Figure 1.1 shows the variation with time of the velocity of ball X before, during and after the collision.${fig11}Determine the magnitude of the acceleration of ball X during the collision.',
 C1=kwv('a=(v-u)/t','a=(u-v)/t','a=v/t','a=δv/δt','a=∆v/∆t','a=Δv/Δt','gradient','slope','change in velocity','(${u}+${w})/${dts}','(${w}+${u})/${dts}','(${u}-(-${w}))/${dts}','(-${w}-${u})/${dts}'),
 A=kwv('${a_ans}','-${a_ans}'),tolerance='1',
 U='a = Δv / Δt = (−${w} − ${u}) / (${tBs} − ${tAs}) = −${a_ans} m s⁻², so the magnitude is ${a_ans} m s⁻²',
 V='Acceleration is the gradient of the velocity–time graph. During the collision the velocity changes from +${u} m s⁻¹ at ${tAs} s to −${w} m s⁻¹ at ${tBs} s.'))
parts.append(dict(pi=2,type='calculation',
 K=lab('(b)(ii)')+'Determine the magnitude of the change in momentum of ball X due to the collision.',
 C1=kwv('${mXs}×${u}','${mXs}*${u}','${mXs}x${u}','${mXs}×${w}','${mXs}*${w}','${mXs}x${w}','Δp=mΔv','∆p=m∆v','δp=mδv','Δp=mv-mu','p=mv','mv-mu','mv+mu','f=ma','f=${mXs}×'),
 A=kwv('${dp_ans}','-${dp_ans}'),tolerance='1',
 U='Change in momentum = ${mXs} × (−${w} − ${u}) = −${dp_ans} kg m s⁻¹, so the magnitude is ${dp_ans} kg m s⁻¹',
 V='Change in momentum = mass × change in velocity. The velocity reverses, so the change in velocity is the SUM of the two speeds (${u} + ${w}), not their difference. (The sign is ignored in the mark scheme.)'))
parts.append(dict(pi=3,type='calculation',
 K=lab('(b)(iii)')+'Determine the total distance travelled by ball X during the collision.',
 C1=kwv('½×${u}×','0.5×${u}×','½×${w}×','0.5×${w}×','${u}²/(2×','${w}²/(2×','½at²','0.5at²','area','s=ut+½at²','s=(u+v)t/2','v²=u²+2as'),
 A='${dist_ans}',tolerance='3',
 U='The ball moves forwards until it stops, then moves backwards. Distance = ½ × ${u} × t₁ + ½ × ${w} × t₂ where t₁ = ${u}/${a_ans} and t₂ = ${w}/${a_ans}, so distance = ${dist_ans} m',
 V='The distance is the sum of the areas of the two triangles between the graph line and the time axis during the collision (one above the axis while X still moves forwards, one below as it moves backwards). Finding the displacement (the difference) instead would be wrong.'))
parts.append(dict(pi=4,type='explain',
 K=lab('(c)(i)')+'By considering relative speeds, explain why the velocity of ball Y after the collision must be +${vY} m s<sup>−1</sup>.',
 B=andor(['approach','before the collision','before collision'],['separation','separating','after the collision','after collision','move apart','moving apart'],['equal','same','=']),
 B2=kwv('vY+${w}=${u}','vY-(-${w})=${u}','vY--${w}=${u}','vY=${u}-${w}','${w}+${vY}=${u}','${vY}+${w}=${u}','${u}-${w}=${vY}','${u}-${w}','${u}−${w}','speed of separation=${u}','speed of separation is ${u}','separation=${u}','separation is ${u}','separate at ${u}','vY - (-${w})','${vY}-(-${w})','${vY}--${w}'),
 U='Relative speed of approach = relative speed of separation. Before the collision the relative speed of approach is ${u} m s⁻¹, so the speed of separation is ${u} m s⁻¹. v<sub>Y</sub> − (−${w}) = ${u}, so v<sub>Y</sub> = +${vY} m s⁻¹.',
 V='For an elastic collision the relative speed of approach equals the relative speed of separation. Ball Y was at rest, so the approach speed is the initial speed of X (${u} m s⁻¹). After the collision X moves at −${w} m s⁻¹, so v_Y − (−${w}) = ${u}.'))
parts.append(dict(pi=5,type='imageChoice',
 K=lab('(c)(ii)')+'Which sketch correctly shows the variation of the velocity of ball Y with time from time = 0 to time = 0.20 s? In each sketch the collision begins at time <i>t</i><sub>1</sub> = ${tAs} s and ends at time <i>t</i><sub>2</sub> = ${tBs} s, and <i>v</i> = ${vY} m s<sup>−1</sup>.',
 answerType='imageChoice',
 imageOptions=['as2623_q1cii_b.svg','as2623_q1cii_c.svg','as2623_q1cii_a.svg','as2623_q1cii_d.svg'],
 correctImageIndex='2',imageChoiceMarks='2',
 U='A horizontal line at zero velocity from 0 to t₁, a straight diagonal line from (t₁, 0) to (t₂, v), then a horizontal line at v to 0.20 s.',
 V='Y is at rest until the collision begins at t₁. During the collision its velocity increases uniformly (the force is constant, as for X) from 0 to ${vY} m s⁻¹ at t₂, and then stays constant because no further force acts on it.'))
parts.append(dict(pi=6,type='calculation',
 K=lab('(c)(iii)')+'Calculate the mass of ball Y.',
 C1=kwv('${mXs}×${u}=${mXs}×(-${w})','${mXs}×${u}=-${mXs}×${w}','${mXs}×${u}','${mXs}*${u}','${mXs}x${u}','pbefore=pafter','momentum before=momentum after','total momentum','conservation of momentum','m1u1=m1v1','${mXs}×${u}+0','½×${mXs}×','0.5×${mXs}×','${mXs}×${w}×'),
 A='${mY_ans}',tolerance='2',
 U='Conservation of momentum: ${mXs} × ${u} = ${mXs} × (−${w}) + ${vY}m, so m = ${mXs} × (${u} + ${w}) / ${vY} = ${mY_ans} kg',
 V='Total momentum before = total momentum after. Take the initial direction of X as positive: X has +${u} m s⁻¹ before and −${w} m s⁻¹ after; Y has ${vY} m s⁻¹ after. (Follow through from (b) for the velocities read from the graph.)'))
ALL+=question(LV,'9702-26-23-Q1',PAPER,'definition','Dynamics,Kinematics',P1,G1,'Question 1',parts)

# ===================================================================== Q2
G2={'sf':SF,'sci':SCI,'ex':EX,'gsvg':GSVG,
 'm':'+mp.toPrecision(2)','ms':'m.toFixed(3)','An':'+Anp.toPrecision(2)','Ans':'An.toFixed(1)','A':'An*1e-6','Aex':'An.toFixed(1)+\'e-6\'',
 'rho':'Math.round(rhop)','En':'+Enp.toPrecision(2)','Ens':'En.toFixed(1)','E':'En*1e8',
 'g':'9.81','L':'m/(rho*A)','Ls':'sf(L,2)','Lr':'+L.toPrecision(2)',
 'sig':'m*g/A','sig_ex':'ex(sig,1)','sigr':'+sig.toPrecision(2)','sigs':'sci(sig,1)',
 'x':'Lr*sigr/E','x_ans':'ex(x,1)','x_sci':'sci(x,1)','x_dec':'x.toFixed(6)',
 'Ep':'0.5*sigr*A*x','Ep_ans':'ex(Ep,1)','Ep_sci':'sci(Ep,1)',
 'xmax':'Math.ceil(L/4)*4','ymax':'Math.ceil(sig/1e4/4)*4',
 'pts':'[[0,sig/1e4],[L,0]]',
 'fig21':"gsvg({x0:0,x1:xmax,y0:0,y1:ymax,mx:xmax/20,my:ymax/20,Mx:xmax/4,My:ymax/4,xl:'distance / m',yl:'stress / 10⁴ Pa',pts:pts,cap:'Figure 2.1',H:420})"}
P2={'mp':[0.012,0.030],'Anp':[2.0,4.0],'rhop':[930,980],'Enp':[6.0,9.5]}
parts=[]
parts.append(dict(pi=0,type='definition',K=lab('(a)')+'Define the Young modulus of a material.',
 B=andor(['stress'],['strain'],['per','divided by','over','/','ratio','÷']),
 U='The Young modulus is the stress per unit strain (stress divided by strain).',
 V='E = stress / strain, where stress = force / cross-sectional area and strain = extension / original length. It is the gradient of a stress–strain graph in the region where Hooke’s law is obeyed.'))
parts.append(dict(pi=1,type='calculation',
 K=lab('(b)(i)')+'A long, thin thread of high-density polythene has a uniform cross-section. The thread is suspended from one end so that it hangs vertically.<br><br>The thread has a mass of ${ms} kg and a cross-sectional area of ${Ans} × 10<sup>−6</sup> m<sup>2</sup>.<br>High-density polythene has a density of ${rho} kg m<sup>−3</sup> and a Young modulus of ${Ens} × 10<sup>8</sup> Pa.<br><br>Show that the length of the thread is ${Ls} m.',
 C1=kwv('ρ=m/v','d=m/v','density=mass/volume','v=m/ρ','v=m/d','v=${ms}/${rho}','m=ρal','m=ρ×a×l','l=m/(ρa)','l=m/ρa'),
 A=andor(['${ms}'],['${rho}'],['${Ans}e-6','${Ans}×10^-6','${Ans}×10-6','${Ans}x10^-6','${Ans}x10-6'],['${Ls}']),
 U='V = m / ρ = ${ms} / ${rho}, and V = AL, so L = ${ms} / (${rho} × ${Ans} × 10⁻⁶) = ${Ls} m',
 V='Density = mass / volume, so the volume is m/ρ. The thread has a uniform cross-section, so volume = A × L and L = m / (ρA). A full substitution is needed in a “show that” question.'))
parts.append(dict(pi=2,type='calculation',
 K=lab('(b)(ii)')+'Show that the stress at the top of the thread due to its own weight is ${sigs} Pa.',
 C1=kwv('σ=f/a','stress=f/a','stress=force/area','stress=force/cross','σ=w/a','σ=mg/a','stress=w/a','stress=mg/a','f/a'),
 A=andor(['${ms}'],['9.81','9.8'],['${Ans}e-6','${Ans}×10^-6','${Ans}×10-6','${Ans}x10^-6','${Ans}x10-6'],['${sig_ex}']),
 U='σ = F / A = mg / A = (${ms} × 9.81) / (${Ans} × 10⁻⁶) = ${sigs} Pa',
 V='The force at the top of the thread is the whole weight of the thread, W = mg. Stress = force / cross-sectional area. Use g = 9.81 m s⁻².'))
parts.append(dict(pi=3,type='explain',
 K=lab('(b)(iii)')+'Figure 2.1 shows the variation with distance from the top of the thread of the stress in the thread due to its own weight.${fig21}Suggest an explanation for the fact that the variation shown in Figure 2.1 is linear.',
 B=andor(['weight','force','mass','load'],['decreases','decrease','less','reduces','smaller','lower','falls','varies','changes','depends'],['distance','length','down','lower','further','increases']),
 B2=andor(['stress'],['proportional','directly proportional','∝'],['weight','force','mass','load']),
 U='The weight of the thread supported below a point decreases (linearly) as the distance from the top increases. The cross-section is uniform, so the stress at a point is proportional to the weight of the thread below that point.',
 V='At a distance d from the top, the thread below supports only the weight of the remaining length (L − d). Because the cross-sectional area is uniform, stress = weight below ÷ A, which is proportional to (L − d): a straight line that falls to zero at the bottom.'))
parts.append(dict(pi=4,type='calculation',
 K=lab('(c)(i)')+'The thread in 2(b) is now laid horizontally on a frictionless bench. A tensile force is applied to the ends of the thread so that there is a uniform stress throughout the thread of ${sigs} Pa.<br><br>Calculate the extension of the thread.',
 C1=kwv('e=σ/ε','e=stress/strain','e=σl/x','e=σ/(x/l)','x=σl/e','x=σ×l/e','ε=x/l','strain=x/l','strain=extension/length','strain=σ/e','σ/e','e=σ×l/x'),
 A='${x_ans}|${x_dec}',tolerance='2',
 U='E = σ / ε = σL / x, so x = σL / E = ${Ls} × ${sigs} / (${Ens} × 10⁸) = ${x_sci} m',
 V='Young modulus E = stress / strain with strain = x / L. Rearrange to x = σL / E. Use the length found in (b)(i) and the stress given here.'))
parts.append(dict(pi=5,type='calculation',
 K=lab('(c)(ii)')+'Calculate the elastic potential energy of the thread.',
 C1=kwv('e=½fx','e=½kx²','e=½f²/k','e=0.5fx','e=0.5kx²','w=½fx','½fx','0.5fx','½kx²','0.5kx^2','½kx^2','½σ×a×x','½×σ×a×x','½σax','½×f×x','0.5×f×x','area under','½f×x','½×${sigr}','0.5×${sigr}'),
 A='${Ep_ans}',tolerance='3',
 U='E = ½Fx = ½ × σA × x = ½ × ${sigs} × ${Ans} × 10⁻⁶ × ${x_sci} = ${Ep_sci} J',
 V='The energy stored equals the area under a force–extension graph: E = ½Fx. The force in the thread is F = σA. (Follow through from (c)(i) for the extension.)'))
parts.append(dict(pi=6,type='explain',
 K=lab('(d)')+'Suggest, with a reason, whether the total extension of the vertically suspended thread in 2(b) is less than, equal to or greater than the answer in 2(c)(i).',
 B=andor(['less','smaller','lower','shorter','not as much','not as big','not as large'],['stress','force','tension','weight','load','mass']),
 U='Less, because the stress in the vertically suspended thread is less than ${sigs} Pa everywhere except at the top (it decreases to zero at the bottom).',
 V='Extension depends on the stress in each part of the thread. In the horizontal thread the stress is uniform and equal to the maximum value in the vertical thread, so the vertical thread extends by less.'))
ALL+=question(LV,'9702-26-23-Q2',PAPER,'definition','Materials',P2,G2,'Question 2',parts)

# ===================================================================== Q3
G3={'sf':SF,'sci':SCI,'ex':EX,'fig':FIG31,
 'lam_n':'Math.round(lamp/10)*10','lam':'lam_n*1e-9','a5':'+a5p.toPrecision(2)','a5s':'a5.toFixed(1)','a':'a5*1e-5',
 'D':'+Dp.toPrecision(2)','Ds':'D.toFixed(2)',
 'x':'lam*D/a','x_ans':'sf(x,2)','XY':'x/2','XY_ans':'sf(XY,2)',
 'f':'3.00e8/lam','f_ans':'ex(f,1)','f_sci':'sci(f,1)',
 'f31':'fig(lam_n,a5s,Ds)'}
P3={'lamp':[450,700],'a5p':[1.0,2.0],'Dp':[0.30,0.80]}
parts=[]
parts.append(dict(pi=0,type='definition',K=lab('(a)')+'State the principle of superposition.',
 B=kwv('waves meet','waves overlap','two waves meet','two or more waves meet','when two waves','when waves','waves intersect','waves merge','waves cross','waves travelling in opposite directions','waves travelling in opposite'),
 B2=andor(['displacement'],['sum','added','adding','add together','total','resultant','combined'],['individual','each wave','separate','the waves','two waves']),
 U='When two (or more) waves meet (at a point), the resultant displacement is the sum of the individual displacements of the waves.',
 V='Superposition: the displacements of the waves add vectorially (as signed quantities) at every point where they meet. Constructive and destructive interference are special cases.'))
parts.append(dict(pi=1,type='definition',
 K=lab('(b)(i)')+'Parallel rays of coherent light of wavelength ${lam_n} nm are incident normally in free space on two narrow slits as shown in Figure 3.1.${f31}Light passing through the double slit reaches a screen that is parallel to the plane of the slits.<br>The distance between the centres of the slits is ${a5s} × 10<sup>−5</sup> m.<br>The distance between the slits and the screen is ${Ds} m.<br><br>State what is meant by coherent.',
 B=kwv('constant phase difference','fixed phase difference','phase difference is constant','phase difference is fixed','phase difference that is constant','phase difference that is fixed','phase difference constant','phase difference fixed','phase difference remains constant','phase difference stays constant','phase difference does not change','phase difference doesnt change','unchanging phase difference','constant phase diff','fixed phase diff'),
 U='Coherent waves have a constant phase difference.',V='Coherent sources emit waves with a constant (fixed) phase difference between them. This also means they have the same frequency.'))
parts.append(dict(pi=2,type='definition',K=lab('(b)(ii)')+'State what happens to the light at the point where it passes through the slits.',
 B=kwv('diffract'),U='The light diffracts.',V='Light spreads out (diffracts) as it passes through a narrow slit. The diffracted waves from the two slits overlap and superpose on the screen.'))
parts.append(dict(pi=3,type='explain',K=lab('(b)(iii)')+'At point X on the screen, there is a central bright fringe.<br><br>Explain how this bright fringe is formed.',
 B=kwv('waves from each slit meet','waves from both slits meet','waves meet at x','waves overlap','waves superpose','waves superimpose','waves interfere','waves combine','waves from the slits meet','waves from the two slits meet','light from each slit meet','light from both slits meet','meet at the screen','meet at x','overlap at','superpose at','superimpose at','interfere at','combine at'),
 B2=kwv('zero path difference','0 path difference','no path difference','path difference of zero','path difference is zero','path difference=0','zero phase difference','0 phase difference','no phase difference','phase difference of zero','phase difference is zero','phase difference=0','in phase','same distance','equal distance','equal path','same path','path difference of 0','path lengths are equal','path lengths equal','phase difference of 0'),
 B3=kwv('constructive','maximum amplitude','max amplitude','largest amplitude','greatest amplitude','amplitude is a maximum','amplitude is maximum','amplitude is largest','amplitudes add','double the amplitude','resultant amplitude is max'),
 U='Waves from each slit meet (superpose) at X. They have travelled the same distance, so the path difference is zero (they are in phase). Constructive interference occurs, so the resultant wave has maximum amplitude.',
 V='Three marks: (1) the waves from the two slits meet/superpose at the screen; (2) X is equidistant from the two slits so the path difference (and phase difference) is zero; (3) constructive interference gives a bright fringe (maximum amplitude).'))
parts.append(dict(pi=4,type='calculation',K=lab('(b)(iv)')+'At point Y on the screen, the dark fringe closest to point X is formed.<br><br>Calculate the distance XY.',
 C2=kwv('λ=ax/d','λ=ax/D','x=λd/a','x=λD/a','x=λ×d/a','x=λ×D/a','x=λd/a','xd/a','λd/a','λd/(2a)','λd/2a'),
 C1='${x_ans}',
 A='${XY_ans}',tolerance='3',
 U='λ = ax / D, so the fringe separation x = λD / a = (${lam_n} × 10⁻⁹ × ${Ds}) / (${a5s} × 10⁻⁵) = ${x_ans} m. The dark fringe closest to X is half a fringe separation from X: XY = x / 2 = ${XY_ans} m',
 V='The fringe separation is x = λD/a (the distance between adjacent bright fringes). The nearest dark fringe is half a fringe separation from the central bright fringe at X, so XY = x/2.'))
parts.append(dict(pi=5,type='imageChoice',
 K=lab('(c)(i)')+'On the screen in Figure 3.1, a cross (×) labelled with the letter B is drawn at the position of another bright fringe. Which sketch correctly shows the position of B? In each sketch, X is the central bright fringe and Y is the dark fringe closest to X.',
 answerType='imageChoice',
 imageOptions=['as2623_q3ci_c.svg','as2623_q3ci_a.svg','as2623_q3ci_d.svg','as2623_q3ci_b.svg'],
 correctImageIndex='1',imageChoiceMarks='1',
 U='B is above Y at the same distance above Y as XY (that is, a distance 2XY from X). It could also be 2XY below X.',
 V='Bright fringes are a whole fringe separation apart. The next bright fringe from X is at a distance x = 2XY from X, so it is as far above Y as Y is above X.'))
parts.append(dict(pi=6,type='imageChoice',
 K=lab('(c)(ii)')+'On the screen in Figure 3.1, a cross (×) labelled with the letter D is drawn at the position of another dark fringe. Which sketch correctly shows the position of D?',
 answerType='imageChoice',
 imageOptions=['as2623_q3cii_b.svg','as2623_q3cii_c.svg','as2623_q3cii_d.svg','as2623_q3cii_a.svg'],
 correctImageIndex='3',imageChoiceMarks='1',
 U='D is below X at a distance below X equal to XY.',
 V='Dark fringes lie midway between bright fringes. The dark fringe on the other side of X from Y is also a distance XY from X.'))
parts.append(dict(pi=7,type='calculation',K=lab('(d)')+'Calculate the frequency of the light in 3(b).',
 C1=kwv('c=fλ','v=fλ','c=f×λ','v=f×λ','f=c/λ','c=λf','v=λf','f=v/λ'),
 A='${f_ans}',tolerance='1',
 U='c = fλ, so f = c / λ = (3.00 × 10⁸) / (${lam_n} × 10⁻⁹) = ${f_sci} Hz',
 V='The speed of light in free space is c = 3.00 × 10⁸ m s⁻¹. Use c = fλ with the wavelength converted to metres.'))
ALL+=question(LV,'9702-26-23-Q3',PAPER,'definition','Waves',P3,G3,'Question 3',parts)

# ===================================================================== Q4
G4={'sf':SF,'ex':EX,
 'E':'+Ep.toPrecision(3)','R':'Math.round(Rp/10)*10','r0':'+rp.toPrecision(2)','V':'+(E*R/(R+r0)).toPrecision(3)',
 'P_ans':'sf(V*V/R,2)','r_ans':'sf((E-V)*R/V,2)','r_raw':'((E-V)*R/V).toFixed(2)'}
P4={'Ep':[4.50,6.00],'Rp':[150,300],'rp':[5.0,10.0]}
parts=[]
parts.append(dict(pi=0,type='imageChoice',
 K=lab('(a)')+'A light-dependent resistor (LDR) is connected across the terminals of a cell that has internal resistance. A voltmeter is connected across the LDR.<br><br>Which circuit diagram shows this arrangement?',
 answerType='imageChoice',
 imageOptions=['as2623_q4a_d.svg','as2623_q4a_a.svg','as2623_q4a_b.svg','as2623_q4a_c.svg'],
 correctImageIndex='1',imageChoiceMarks='3',
 U='A cell with its internal resistance (cell symbol in series with a resistor, in a dotted box) connected to an LDR (resistor symbol with two arrows pointing at it), with a voltmeter connected in parallel with the LDR.',
 V='Three marks: the correct symbol for a cell with internal resistance (a cell, not a battery); the LDR connected to the terminals of the cell; a voltmeter symbol connected in parallel with the LDR.'))
parts.append(dict(pi=1,type='explain',
 K=lab('(b)(i)')+'The cell has an electromotive force (e.m.f.) of ${E} V.<br>At a particular light intensity, the LDR has a resistance of ${R} Ω and a potential difference (p.d.) across it of ${V} V.<br><br>Identify one possible source of systematic error in measuring the p.d. across the LDR using a digital voltmeter.',
 B=kwv('zero error','calibration','calibrated','contact resistance','resistance of connecting wires','resistance of the connecting wires','resistance of the wires','resistance of wires','resistance in the connections','resistance of the connections','resistance of the leads','resistance of leads','offset error','wire resistance'),
 U='Zero error (or calibration error) of the voltmeter.',V='A systematic error shifts all readings by the same amount, e.g. a zero error or a calibration error in the voltmeter, or contact resistance in the connections.'))
parts.append(dict(pi=2,type='calculation',K=lab('(b)(ii)')+'Calculate the power dissipated in the LDR.',
 C1=kwv('p=v²/r','p=v^2/r','p=vi','p=i²r','p=i^2r','v²/r','v^2/r','p=v×i','p=iv','p=v×v/r','p=${V}²/${R}','p=${V}^2/${R}','${V}²/${R}','${V}^2/${R}','${V}×(${V}/${R})','${V}x(${V}/${R})'),
 A='${P_ans}',tolerance='1',
 U='P = V² / R = ${V}² / ${R} = ${P_ans} W',
 V='Use P = V²/R with the p.d. across the LDR and its resistance (or find I = V/R first and then P = VI).'))
parts.append(dict(pi=3,type='calculation',K=lab('(b)(iii)')+'Determine the internal resistance of the cell.',
 C1=kwv('e=v+ir','e=i(r+r)','e=i(r+r)','e=ir+v','e=i(r+r)','lost volts','${E}-${V}','${E}−${V}','${E}-${V}=','(${E}-${V})×${R}/${V}','(${E}-${V})*${R}/${V}','${V}/${E}=${R}/(${R}+r)','${V}/${E}','i=${V}/${R}','i=v/r'),
 A='${r_ans}|${r_raw}',tolerance='2',
 U='E = V + Ir with I = V / R, so r = (E − V)R / V = (${E} − ${V}) × ${R} / ${V} = ${r_ans} Ω',
 V='The e.m.f. is shared between the internal resistance (lost volts Ir) and the LDR: E = V + Ir. The current is I = V/R for the LDR, then r = (E − V)/I.'))
parts.append(dict(pi=4,type='table',
 K=lab('(b)(iv)')+'The intensity of the light illuminating the LDR is gradually decreased.<br><br>Complete Table 4.1 to show what happens to the quantities indicated as the light intensity decreases. Type <i>decreases</i>, <i>unchanged</i> or <i>increases</i> in each box.',
 answerType='table',
 tableRowLabels='["resistance of LDR","current in cell","p.d. across LDR"]',
 tableColLabels='["Table 4.1: change as the light intensity decreases"]',
 tableCellKeywords='[[["exact:increases"]],[["exact:decreases"]],[["exact:increases"]]]',
 tableCellAnswers='[["increases"],["decreases"],["increases"]]',
 U='resistance of LDR: increases; current in cell: decreases; p.d. across LDR: increases',
 V='In less light the resistance of the LDR increases. The total resistance of the circuit rises so the current in the cell falls. The lost volts (Ir) fall, so the terminal p.d. – which is the p.d. across the LDR – increases.'))
ALL+=question(LV,'9702-26-23-Q4',PAPER,'definition','Electricity',P4,G4,'Question 4',parts)

# ===================================================================== Q5
st="(a,b)=>'<span style=\"display:inline-flex;flex-direction:column;vertical-align:middle;line-height:1.05;font-size:0.72em;text-align:right;margin-right:1px\"><span>'+a+'</span><span>'+b+'</span></span>'"
G5={'st':st,'A_n':'Math.round(A_p)','Z_n':'Math.floor(Math.round(A_p)/2)','Q_n':'Math.floor(Math.round(A_p)/2)-1',
 'nucX':"st(Math.round(A_p),Math.floor(Math.round(A_p)/2))+'X'",
 'eqn':"st(Math.round(A_p),Math.floor(Math.round(A_p)/2))+'X &rarr; '+st('P','Q')+'Y + '+st('R','S')+'&beta;<sup>+</sup> + '+st(0,0)+'Z'",
 'pi':'Math.min(5,Math.floor(pair_p))','c1':'[-1,-1,-1,0,0,1][pi]','c2':'[0,1,2,1,2,2][pi]',
 'c1_d':"c1===0?'0':(c1>0?'+':'−')+Math.abs(c1)+'e'",'c2_d':"c2===0?'0':(c2>0?'+':'−')+Math.abs(c2)+'e'",
 'kwTbl':"['ddd|three down|3 down|−⅓ −⅓ −⅓|-1/3 -1/3 -1/3|-⅓ -⅓ -⅓|−1/3 −1/3 −1/3','udd|ddu|dud|one up and two down|one up quark and two down|1 up quark and 2 down|1 up and 2 down|1 up 2 down|one up two down|up and two down|up quark and two down|+⅔ −⅓ −⅓|+2/3 -1/3 -1/3|⅔ −⅓ −⅓','uud|udu|duu|two up and one down|two up quarks and one down|2 up quarks and 1 down|2 up and 1 down|2 up 1 down|two up one down|up and two down|up quark and two down|+⅔ +⅔ −⅓|+2/3 +2/3 -1/3|⅔ ⅔ −⅓','uuu|three up|3 up|+⅔ +⅔ +⅔|+2/3 +2/3 +2/3|⅔ ⅔ ⅔']",
 'dscTbl':"['three down quarks: (−⅓e) + (−⅓e) + (−⅓e) = −1e','one up quark and two down quarks: (+⅔e) + (−⅓e) + (−⅓e) = 0','two up quarks and one down quark: (+⅔e) + (+⅔e) + (−⅓e) = +1e','three up quarks: (+⅔e) + (+⅔e) + (+⅔e) = +2e']",
 'kw1':'kwTbl[c1+1]','kw2':'kwTbl[c2+1]','d1':'dscTbl[c1+1]','d2':'dscTbl[c2+1]'}
P5={'A_p':[14,60],'pair_p':[0,5.99]}
parts=[]
parts.append(dict(pi=0,type='definition',K=lab('(a)')+'State what is meant by a meson.',
 B=kwv('one quark and one antiquark','quark and antiquark','quark and an antiquark','quark-antiquark','quark–antiquark','1 quark and 1 antiquark','quark and anti-quark','quark and anti quark','quark+antiquark','antiquark and a quark','antiquark and quark','q q-bar','qq̄','q̅','quark anti-quark'),
 U='A meson is a hadron consisting of one quark and one antiquark.',V='A meson is a hadron made of one quark and one antiquark (e.g. the pion π⁺ = u d̄). Baryons contain three quarks.'))
parts.append(dict(pi=1,type='explain',
 K=lab('(b)')+'The elementary charge is e. Explain, in terms of quark composition, how two baryons may have overall charges of ${c1_d} and ${c2_d}.',
 C1=kwv('⅔','2/3','⅓','1/3','magnitudes of','magnitude of charge','either ⅔ or ⅓'),
 B='${kw1}',B2='${kw2}',
 U='A baryon is made of three quarks. Quark charges are +⅔e (up) and −⅓e (down). For ${c1_d}: ${d1}. For ${c2_d}: ${d2}.',
 V='Up (u) = +⅔e, down (d) = −⅓e. Add the three quark charges: uuu = +2e, uud = +1e, udd = 0, ddd = −1e.'))
parts.append(dict(pi=2,type='calculation',
 K=lab('(c)(i)')+'The nuclide ${nucX} undergoes β<sup>+</sup> decay to produce nuclide Y and one other particle Z, as shown in the equation<br><br>${eqn}<br><br>State the values of P, Q, R and S.',
 B=andor(['p=${A_n}','p:${A_n}'],['q=${Q_n}','q:${Q_n}']),B2=andor(['r=0','r:0'],['s=+1','s=1','s:+1','s:1']),
 U='P = ${A_n}, Q = ${Q_n}, R = 0, S = +1',
 V='In β⁺ decay a proton changes into a neutron. The nucleon number is unchanged (P = ${A_n}) and the proton number falls by 1 (Q = ${Z_n} − 1 = ${Q_n}). The β⁺ particle is a positron: R = 0, S = +1.'))
parts.append(dict(pi=3,type='definition',K=lab('(c)(ii)')+'State the name of particle Z.',
 B=kwv('electron neutrino','electron-neutrino','exact:neutrino','exact:a neutrino','exact:the neutrino','exact:neutrino particle','exact:νe','exact:ν_e','exact:νₑ','exact:ν'),
 U='Electron neutrino (νe)',V='In β⁺ decay an electron neutrino is emitted with the positron. It carries away part of the decay energy, which is why the β⁺ particles have a continuous range of kinetic energies.'))
parts.append(dict(pi=4,type='definition',K=lab('(c)(iii)')+'State the net change in quark composition as nuclide ${nucX} turns into nuclide Y.',
 B=kwv('up to down','u to d','up quark to down','up quark changes to a down','up becomes down','up changes to down','one up becomes one down','u→d','u->d','u → d','one up quark changes to one down','uud to udd','uud→udd','uud -> udd','uud → udd','up to a down'),
 U='One up quark changes to one down quark (u → d).',V='In β⁺ decay an up quark changes to a down quark: u → d + e⁺ + νₑ. This converts a proton (uud) into a neutron (udd).'))
parts.append(dict(pi=5,type='explain',
 K=lab('(c)(iv)')+'Explain why the emission of particle Z results in the β<sup>+</sup> particles from the decays of different nuclei of ${nucX} having a continuous range of kinetic energies.',
 B=kwv('in each decay is constant','in each decay is the same','total energy constant','total energy emitted is constant','total energy is constant','total energy is the same','energy is constant','energy released is constant','same energy released','the same total energy','fixed amount of energy','fixed energy','energy emitted is constant','energy is the same in each'),
 B2=kwv('takes some of','Z takes some','takes some of the energy','takes some energy','shared between','shared with','shared among','energy is shared','shared by','different amounts','different for each decay','distributed differently','distributed in a different','neutrino takes','neutrino carries','neutrino shares','neutrino has some','z carries','z has some'),
 U='The total energy emitted in each decay is constant. Particle Z takes some of this energy, so the energy is shared between Z and the β⁺ particle. The way the energy is distributed is different for each decay, giving the β⁺ a continuous range of kinetic energies.',
 V='If only the β⁺ were emitted, every β⁺ would carry the same energy. The neutrino Z takes a variable share of the (constant) decay energy, so the β⁺ kinetic energy varies from decay to decay up to a maximum.'))
ALL+=question(LV,'9702-26-23-Q5',PAPER,'definition','Particle physics',P5,G5,'Question 5',parts)

if __name__=='__main__':
    start=int(sys.argv[1]) if len(sys.argv)>1 else 255
    write_json(ALL,'new23.json',start=start)
    from collections import Counter
    print(len(ALL),'rows',Counter(r['id'] for r in ALL))
