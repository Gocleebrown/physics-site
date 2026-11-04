import json, sys
sys.path.insert(0,'.')
from rowlib import *
from jshelpers import *

LV='AS'; PAPER='9702_s26_p21'
GRAV='9.81'
def lab(s): return '<b>'+s+'</b> '

ALL=[]
# =====================================================================  Q1
G1={
 'sci':SCI,'gsvg':GSVG,
 'M':'M6*1e6','r':'r4*1e4','tb':'Math.round(tbp)','g':GRAV,
 'T':'M*(a0+g)','ue':'T/r','mf':'M-r*tb',
 'vf':'(t)=>ue*Math.log(M/(M-r*t))-g*t',
 'v_tb':'vf(tb)','KE':'0.5*mf*v_tb*v_tb',
 'hgt':'(()=>{let s=0;const n=600,h=tb/n;for(let i=0;i<n;i++){const t=(i+0.5)*h;s+=vf(t)}return s*h})()',
 'xmax':'Math.ceil(tb/10)*10',
 'ymax':'v_tb>200?Math.ceil(v_tb/100)*100:Math.ceil(v_tb/50)*50',
 'Mj':'ymax<=200?50:100','mn':'ymax<=400?10:20',
 'pts1':'Array.from({length:tb+1},(_,i)=>[i,+vf(i).toFixed(2)])',
 'fig11':"gsvg({x0:0,x1:xmax,y0:0,y1:ymax,mx:1,my:mn,Mx:10,My:Mj,xl:'time / s',yl:'speed / m s⁻¹',pts:pts1,cap:'Figure 1.1'})",
 'T_ans':'T.toExponential(2)','Fma_ans':'(M*a0).toExponential(2)',
 'v_ans':'String(Math.round(v_tb))','mf_ans':'mf.toExponential(3)','KE_ans':'KE.toExponential(2)',
 'h_ans':'String(Math.round(hgt))','ue_ans':'ue.toExponential(3)',
 'M6s':'M6.toFixed(2)','r4s':'r4.toFixed(2)','a0s':'a0.toFixed(2)','h_disp':'String(Math.round(hgt/100)*100)',
}
P1={'M6':[2.4,3.2],'r4':[1.6,2.2],'a0':[2.0,3.0],'tbp':[40,60]}
parts=[]
parts.append(dict(pi=0,type='definition',K=lab('(a)')+'Define force.',
  B=kw('rate of change of momentum','change in momentum / time','change in momentum per unit time','change in momentum per time','change in momentum over time','change in momentum divided by time','change in momentum divided by the time','ratio of change in momentum and time','ratio of change in momentum to time','change in momentum per second','dp/dt','Δp/Δt','∆p/∆t','change in momentum/time taken','change in momentum / time taken','change in momentum per time taken'),
  U='Force is the rate of change of momentum.',
  V='Newton’s second law: force = (change in momentum) / (time taken). For constant mass this gives F = ma.'))
parts.append(dict(pi=1,type='explain',
  K=lab('(b)(i)')+'A rocket is launched vertically upwards from a launch pad. The initial mass of the rocket, with all of its fuel, is ${M6} × 10<sup>6</sup> kg. For the first ${tb} s after lift‑off, the rocket engine burns fuel at a rate of ${r4} × 10<sup>4</sup> kg s<sup>−1</sup> to produce a constant thrust force.<br><br>Figure 1.1 shows the variation of the speed of the rocket with time for the first ${tb} s after lift‑off.${fig11}Assume that the drag force acting on the rocket is negligible over this time.<br><br>By considering the mass of unburnt fuel in the rocket, explain why the speed of the rocket does <b>not</b> increase linearly with time, despite the thrust force from the engine being constant.',
  B=andor(['mass','weight','fuel'],['decreas','reduc','less','lower','lighter','loses','lost','burn','consumed','used up','falls','smaller','↓']),
  B2=andor(['acceleration','a increases','gradient','accelerates','speed increases at an increasing rate','faster and faster','a gets bigger','a gets larger'],['increas','greater','larger','bigger','more','rises','steeper','↑']),
  tolerance='0',
  U='The mass of the rocket decreases as fuel is burnt. The thrust force is constant, so the acceleration (a = F/m) increases, i.e. the gradient of the speed–time graph increases. The graph is therefore a curve, not a straight line.',
  V='Two marks: (1) mass decreases as fuel is consumed; (2) with constant thrust, acceleration increases (gradient of the speed–time graph increases).'))
parts.append(dict(pi=2,type='explain',
  K=lab('(b)(ii)')+'Describe how Figure 1.1 may be used to determine the acceleration of the rocket at lift‑off. No calculations are required.',
  B=kw('gradient','slope','steepness'),
  B2=kw('tangent','at t=0','at t = 0','at t=0s','at the start','at lift-off','at lift off','at lift‑off','at time zero','at zero','initial gradient','initially','at 0 s','at the origin','when t is 0','when t = 0','at the beginning','start of the graph','at time 0'),
  U='Find the gradient of the graph at t = 0, i.e. draw a tangent to the curve at t = 0 and find its gradient.',
  V='Acceleration is the gradient of a speed–time graph. At lift‑off use the gradient of the tangent drawn at t = 0.'))
parts.append(dict(pi=3,type='calculation',
  K=lab('(b)(iii)')+'The acceleration of the rocket at lift‑off is ${a0} m s<sup>−2</sup>.<br><br>Determine a value for the thrust force <i>T</i> produced by the rocket engine.',
  C1=kw('f=ma','t-mg=ma','t−mg=ma','t - mg = ma','t=m(a+g)','t=mg+ma','${Fma_ans}','resultant force=ma','f=m×a','f=m*a'),
  A='${T_ans}', tolerance='2',
  U='T − mg = ma, so T = m(a + g) = ${M6} × 10<sup>6</sup> × (${a0} + 9.81) = ${sci(T,2)} N',
  V='The resultant force on the rocket is T − mg (weight acts downwards), so T = m(a + g). Using only F = ma gives the resultant force, not the thrust. Method mark for F = ma (or any calculated force); accuracy mark for the thrust.'))
parts.append(dict(pi=4,type='calculation',
  K=lab('(b)(iv)')+'Determine the kinetic energy of the rocket at time ${tb} s after lift‑off.',
  C2=kw('ek=½mv²','ek=1/2mv²','ek=0.5mv²','½mv²','1/2mv²','0.5mv²','½mv^2','0.5mv^2','1/2mv^2','e=½mv²','ke=½mv²','½×m×v²','0.5x','0.5×','½x','½×','1/2x','1/2×','0.5*','½*'),
  C1='${v_ans}|${mf_ans}',
  A='${KE_ans}', tolerance='5',
  U='From Figure 1.1, v = ${v_ans} m s<sup>−1</sup> at t = ${tb} s. Mass of rocket = ${M6} × 10<sup>6</sup> − ${r4} × 10<sup>4</sup> × ${tb} = ${sci(mf,3)} kg. E<sub>K</sub> = ½mv² = ½ × ${sci(mf,3)} × ${v_ans}² = ${sci(KE,2)} J',
  V='Read the speed at the end of the burn from the graph, find the remaining mass (initial mass − burn rate × time), then use E_K = ½mv². Reading the graph accurately matters: a 1% error in v gives a 2% error in E_K.'))
parts.append(dict(pi=5,type='explain',
  K=lab('(b)(v)')+'Use Figure 1.1 to estimate the height of the rocket above the launch pad at time ${tb} s after lift‑off. Explain your reasoning.',
  B=kw('area','under the graph','under graph','under the curve','under the line','integral','integrate','counting squares'),
  A='${h_ans}', tolerance='10',
  U='Height = area under the speed–time graph (e.g. by counting squares) ≈ ${h_ans} m',
  V='Distance travelled (here height) is the area under a speed–time graph; the statement that an area is being found earns the B mark. Counting squares gives an answer within about 10% of the true value.'))
parts.append(dict(pi=6,type='calculation',
  K=lab('(c)')+'The mass of the emitted exhaust gases is the same as the mass of fuel burnt by the engine.<br><br>Use your answer in 1(b)(iii) to calculate the speed at which the exhaust gases are emitted from the rocket in 1(b).',
  C1=kw('f=δp/δt','f=∆p/∆t','f=Δp/Δt','f=dp/dt','f=p/t','f=(m/t)v','t=(m/t)v','t=m/t×v','rate of change of momentum','f=mv/t','f=∆(mv)/∆t','f=Δ(mv)/Δt','t=v×m/t','t=v×(m/t)'),
  A='${ue_ans}', tolerance='4',
  U='Thrust = rate of change of momentum of the exhaust gases = (m/t) × v, so v = ${sci(T,2)} / (${r4} × 10<sup>4</sup>) = ${ue_ans} m s<sup>−1</sup>',
  V='F = Δp/Δt = (Δm/Δt) × v. The thrust equals the burn rate multiplied by the exhaust speed. Error carried forward: using your own answer to (b)(iii) gains full marks if the working is correct.'))
parts.append(dict(pi=7,type='table',
  K=lab('(d)')+'In practice, the drag force on the rocket in 1(b) is not negligible.<br><br>Complete the table to show the effect of the drag force on the acceleration at lift‑off and on the kinetic energy at time ${tb} s, compared with the values in 1(b) that assumed negligible drag force. Type <i>less</i>, <i>same</i> or <i>greater</i> in each box.',
  answerType='table',
  tableRowLabels='["acceleration at lift‑off","kinetic energy at time ${tb} s"]',
  tableColLabels='["less / same / greater"]',
  tableCellKeywords='[[["exact:same"]],[["exact:less"]]]',
  tableCellAnswers='[["same"],["less"]]',
  U='acceleration at lift‑off: same; kinetic energy at ${tb} s: less',
  V='At lift‑off the speed is zero, so there is no drag and the acceleration is unchanged. Later drag opposes the motion, so the speed (and kinetic energy) at ${tb} s is less.'))
ALL+=question(LV,'9702-26-21-Q1',PAPER,'definition','Dynamics,Kinematics,Energy',P1,G1,'Question 1',parts)

# =====================================================================  Q2
G2={
 'm':'+mp.toPrecision(2)','x':'+xp.toPrecision(2)','d':'+dp.toPrecision(2)','g':GRAV,
 'W':'m*g','k':'W/x','E1':'0.5*W*x','E2':'0.5*k*(x+d)*(x+d)','Eadd':'E2-E1','dG':'m*g*d','KE':'Eadd-dG',
 'k_ans':'k.toPrecision(3)','Wt2':'W.toPrecision(2)','E1s':'E1.toPrecision(2)','E2_ans':'E2.toPrecision(3)',
 'Eadd_ans':'Eadd.toPrecision(3)','dG_ans':'dG.toPrecision(3)','KE_ans':'KE.toPrecision(2)',
 'k2':'k.toPrecision(2)',
 'ms':'m.toPrecision(2)','xs':'x.toPrecision(2)','ds':'d.toPrecision(2)',
}
P2={'mp':[0.080,0.150],'xp':[0.020,0.035],'dp':[0.012,0.020]}
parts=[]
parts.append(dict(pi=0,type='definition',K=lab('(a)')+'State what is meant by the spring constant of a spring.',
  B=kw('force per unit extension','force per extension','ratio of force to extension','ratio of force and extension','ratio between force and extension','force ÷ extension','force/extension','force / extension','force over extension','force divided by extension','force per unit change in length','force per unit compression','change in force per unit extension','change in force per extension','force per unit length'),
  U='The spring constant is the force per unit extension.',V='k = F/x: the force needed per unit extension of the spring (for a spring obeying Hooke’s law).'))
parts.append(dict(pi=1,type='explain',
  K=lab('(b)(i)')+'A block of mass ${m} kg is suspended in equilibrium from a spring that obeys Hooke’s law. In this position, the extension of the spring is ${x} m.<br><br>The block is pulled vertically down a distance of ${d} m from the equilibrium position and then released from rest so that it starts moving upwards. Air resistance is negligible.<br><br>Identify one possible source of random error in determining experimentally the extension of the spring using a ruler.',
  B=kw('parallax','eye level','not at eye level','line of sight','spring moves','spring is moving','spring oscillat','spring bounces','spring swings','spring vibrat','reading the ruler','reading of the ruler','reading the scale','reading the length','spring wobbl','spring is not still','spring not still','movement of the spring','spring moving'),
  U='Parallax error: the ruler is not read at eye level. (Or: the spring moves slightly so the reading fluctuates.)',
  V='A random error varies unpredictably from reading to reading, for example parallax error or a spring that is slightly moving while the position is read.'))
parts.append(dict(pi=2,type='calculation',K=lab('(b)(ii)')+'Calculate the spring constant <i>k</i> of the spring.',
  C1=kw('mg=kx','f=kx','k=mg/x','k=f/x','k=w/x','mg/x','f/x','w/x','${Wt2}','mg=ke','k=mg/e','${ms}x9.81','${ms}×9.81','${ms}*9.81','${ms}x9.8','${ms}×9.8'),
  A='${k_ans}',tolerance='3',
  U='At equilibrium kx = mg, so k = mg/x = (${m} × 9.81) / ${x} = ${k_ans} N m<sup>−1</sup>',
  V='In equilibrium the spring force equals the weight: kx = mg. Using g = 10 N kg⁻¹ gives an answer within 3%, which is accepted.'))
parts.append(dict(pi=3,type='calculation',K=lab('(b)(iii)')+'Show that, in the equilibrium position, the elastic potential energy of the spring is ${E1s} J.',
  C1=kw('½fx','1/2fx','0.5fx','½kx²','1/2kx²','0.5kx²','½kx^2','0.5kx^2','1/2kx^2','½mgx','0.5mgx','1/2mgx','½f²/k','0.5f²/k','½×f×x','½×k×x','0.5×k×x','0.5×f×x','½ f x','${Wt2}','${ms}x9.81','${ms}×9.81','${ms}*9.81','${ms}x9.8','${ms}×9.8'),
  A='${E1s}',tolerance='3',
  U='E = ½Fx = ½ × ${m} × 9.81 × ${x} = ${E1s} J (or ½kx² = ½ × ${k2} × ${x}²)',
  V='Elastic potential energy = ½Fx = ½kx² = area under the force–extension graph. Substitute the values and show the final value to at least the given number of significant figures.'))
parts.append(dict(pi=4,type='calculation',K=lab('(b)(iv)')+'Assume that the spring has not exceeded its elastic limit when the block is in the position from which it is released.<br><br>Calculate the additional elastic potential energy stored in the spring when the block moves from its equilibrium position to the position from which it is released.',
  C1='${E2_ans}|½k(x+d)²|½k(x+d)^2|0.5k(x+d)²|1/2k(x+d)²|½kx²|0.5kx²|1/2kx²|½fx|0.5fx|1/2fx',
  A='${Eadd_ans}',tolerance='4',
  U='Extension at release = ${x} + ${d} m. E = ½kx² = ½ × ${k2} × (${x} + ${d})² = ${E2_ans} J. Additional energy = ${E2_ans} − ${E1s} = ${Eadd_ans} J',
  V='Find the elastic potential energy at the new, larger extension and subtract the energy at equilibrium. Method mark for the energy at release (error carried forward from your k).'))
parts.append(dict(pi=5,type='calculation',K=lab('(b)(v)')+'Use the principle of conservation of energy to determine the kinetic energy of the block as it passes the equilibrium position moving upwards.',
  C1='${dG_ans}|mgΔh|mg∆h|mgh|mgδh|mg×0.0|change in gpe|gravitational potential energy',
  A='${KE_ans}',tolerance='20',
  U='Gain in gravitational potential energy = mgΔh = ${m} × 9.81 × ${d} = ${dG_ans} J. Kinetic energy = additional elastic energy − gain in gravitational potential energy = ${Eadd_ans} − ${dG_ans} = ${KE_ans} J',
  V='Energy released from the spring is shared between the gain in gravitational potential energy of the block and its kinetic energy. This is the difference of two similar numbers, so only about 1 significant figure is reliable; answers within 20% are accepted.'))
parts.append(dict(pi=6,type='explain',K=lab('(c)')+'Suggest, with a reason, how the answer in 2(b)(iv) is affected if the spring in 2(b) has exceeded its elastic limit when the block is at the position from which it is released.',
  B=kw('plastic','permanent','permanently','not return to its original','does not return','doesn’t return','not return to original','not return to the original','will not return','energy lost','energy is lost','thermal','heat','deform','dissipat','inelastic','not elastic','work done in deforming','lost to'),
  B2=kw('less','smaller','decrease','reduc','lower','not as much','not as large','not as great'),
  U='Some of the energy is used for plastic (permanent) deformation of the spring, so the additional elastic potential energy is less.',
  V='Beyond the elastic limit the spring does not return to its original length: some of the work done is transferred by plastic deformation (and thermal energy), so less is stored as elastic potential energy.'))
ALL+=question(LV,'9702-26-21-Q2',PAPER,'definition','Materials,Energy,Measurement',P2,G2,'Question 2',parts)

# =====================================================================  Q3
G3={
 'wave31':WAVE31,
 'T2':'+Tp.toPrecision(2)','v':'Math.round(vp)','lam':'+(v*T2).toPrecision(3)','twoLam':'+(2*lam).toPrecision(3)',
 'pp':'2*Math.round(ppp/2)','L':'+(2.5*lam).toPrecision(3)','tq':'+(T2/4).toPrecision(2)','twoT2':'+(2*T2).toPrecision(2)',
 'fig31':'wave31(twoLam,pp)',
 'T2s':'T2.toFixed(2)','tqs':'tq.toPrecision(2)','twoT2s':'twoT2.toPrecision(2)',
}
P3={'Tp':[0.20,0.40],'vp':[60,90],'ppp':[16,30]}
parts=[]
parts.append(dict(pi=0,type='definition',K=lab('(a)')+'State what is meant by a progressive wave.',
  B=kw('transfers energy','transfer of energy','transfers the energy','transports energy','carries energy','propagates energy','moves energy','transmits energy','energy is transferred','energy transferred','energy is transported','energy is carried','energy is propagated','transfer energy','transports the energy','energy transfer'),
  U='A progressive wave is a wave that transfers energy (in the direction of propagation).',V='A progressive wave transfers energy from one place to another without transferring matter.'))
parts.append(dict(pi=1,type='calculation',
  K=lab('(b)(i)')+'A transverse progressive wave travels along a long string PQ from P to Q.<br><br>Figure 3.1 shows the string at time <i>t</i> = 0.${fig31}A point on the string is labelled X. At <i>t</i> = 0, point X is at its equilibrium position. The speed of the wave on the string is ${v} cm s<sup>−1</sup>.<br><br>Show that the period of the wave is ${T2} s.',
  C1=kw('v=λ/t','v=fλ','t=1/f','t=λ/v','λ=vt','v=λf','f=v/λ','f=1/t','λ=v/f','${lam}/${v}','${lam}÷${v}','${lam} / ${v}','${twoLam}/2/${v}','speed=wavelength/period','v=wavelength/period'),
  A=andor(['${lam}','${twoLam}/2','${twoLam}÷2','${twoLam} / 2'],['${v}'],['${T2}']),
  U='The distance between the two peaks is two wavelengths, so λ = ${twoLam} / 2 = ${lam} cm. T = λ / v = ${lam} / ${v} = ${T2} s',
  V='The 3rd and 1st peaks are two wavelengths apart, so the wavelength is half of the labelled distance. Use v = λ/T (or v = fλ and T = 1/f). The halving must be shown.'))
parts.append(dict(pi=2,type='imageChoice',
  K=lab('(b)(ii)')+'Which graph correctly shows the variation of the displacement from the equilibrium position of point X with <i>t</i> between <i>t</i> = 0 and <i>t</i> = ${twoT2} s? (<i>A</i> is the amplitude of the wave and <i>T</i> is its period.)',
  answerType='imageChoice',
  imageOptions=['as2621_q3bii_b.svg','as2621_q3bii_c.svg','as2621_q3bii_a.svg','as2621_q3bii_d.svg'],
  correctImageIndex='2',imageChoiceMarks='3',
  U='Two complete cycles from t = 0 to 2T with amplitude A, starting at zero displacement and going negative first (X moves downwards because the wave travels from P to Q).',
  V='Three marks: two full cycles in the time 2T; amplitude A (half the peak-to-trough height); correct phase. The wave moves from P to Q, so the part of the string to the left of X (a trough) arrives at X first: X moves downwards first, giving a negative sine curve.'))
parts.append(dict(pi=3,type='explain',
  K=lab('(c)(i)')+'The string in 3(b) is now fixed to walls at ends P and Q. An oscillator causes transverse oscillations of the string of period ${T2} s. The speed of waves on the string is still ${v} cm s<sup>−1</sup>.<br><br>The distance between P and Q is ${L} cm.<br><br>Explain how a stationary wave is formed on the string.',
  B=kw('reflect','reflection','reflected','bounces','bounce back','bounces back','rebound'),
  B2=andor(['incident','original','initial','two waves','waves travelling in opposite','opposite direction','opposite directions','reflected','wave from p','wave from the oscillator','both waves','the waves'],['superpos','superimpos','interfer','overlap','combine','add together','adds together','sum']),
  U='The wave is reflected at the fixed end (wall). The incident and reflected waves (travelling in opposite directions) superpose, forming a stationary wave.',
  V='Two marks: reflection at the end/wall; superposition of the incident and reflected waves.'))
parts.append(dict(pi=4,type='imageChoice',
  K=lab('(c)(ii)')+'The string in 3(c) is shown at one instant in time with its ends P and Q fixed. Which diagram shows a possible appearance of the string a time ${tq} s later?',
  answerType='imageChoice',
  imageOptions=['as2621_q3cii_c.svg','as2621_q3cii_a.svg','as2621_q3cii_d.svg','as2621_q3cii_b.svg'],
  correctImageIndex='1',imageChoiceMarks='2',
  U='The string forms a sinusoidal shape with nodes at P and Q and 5 half‑wavelength loops, so the line crosses the equilibrium position 4 times between P and Q.',
  V='The wavelength is λ = v × T = ${v} × ${T2} = ${lam} cm, so the length PQ = ${L} cm is 2.5 wavelengths: five loops, with a node at each fixed end and the string crossing the equilibrium line four times between P and Q.'))
parts.append(dict(pi=5,type='imageChoice',
  K=lab('(c)(iii)')+'On the string in 3(c), one point is labelled N and one is labelled A. Which diagram correctly labels one point at a node (N) and one point at an antinode (A)?',
  answerType='imageChoice',
  imageOptions=['as2621_q3ciii_d.svg','as2621_q3ciii_b.svg','as2621_q3ciii_c.svg','as2621_q3ciii_a.svg'],
  correctImageIndex='3',imageChoiceMarks='2',
  U='N is at a point where the string stays at its equilibrium position (a node); A is at a peak or trough of a loop (an antinode).',
  V='A node has zero amplitude (the string crosses the dashed equilibrium line there, including the fixed ends); an antinode is the point of maximum amplitude at the centre of a loop.'))
ALL+=question(LV,'9702-26-21-Q3',PAPER,'definition','Waves',P3,G3,'Question 3',parts)

# =====================================================================  Q4
G4={
 'sci':SCI,'gsvg':GSVG,
 'rho0':'rho0p*1e-8','alpha':'alp*1e-3','th1':'Math.round(thp/5)*5',
 'L2':'+Lp.toPrecision(2)','d2':'+dp.toPrecision(2)',
 'A':'Math.PI*Math.pow(d2*1e-3/2,2)','A2':'+A.toPrecision(2)','A2e':'A2.toExponential(1)','A2m':"A2e.split('e')[0]",
 'rho_f':'(th)=>rho0*(1+alpha*th)','rho1':'rho_f(th1)','R':'rho1*L2/A2',
 'R_ans':'R.toPrecision(3)','rho1_ans':'rho1.toExponential(2)','rho0m':'(rho0*1e8).toFixed(2)','rho0e':'rho0.toExponential(2)',
 'alp_ans':'alpha.toExponential(2)','alp_rng':"(alpha*0.8).toFixed(5)+' to '+(alpha*1.3).toFixed(5)",
 'I2':'+Ip.toPrecision(2)','n2':'+np.toPrecision(2)','n':'n2*1e28','vd':'I2/(n*A2*1.6e-19)','vd_ans':'vd.toExponential(2)',
 'rad':'+(d2/2).toPrecision(3)','I2s':'I2.toFixed(1)','n2s':'n2.toFixed(1)','L2s':'L2.toFixed(1)','d2s':'d2.toFixed(2)',
 'pts4':'[[0,+(rho0*1e8).toFixed(3)],[120,+(rho_f(120)*1e8).toFixed(3)]]',
 'fig41':"gsvg({x0:0,x1:120,y0:0,y1:3,mx:4,my:0.1,Mx:20,My:1,xl:'temperature / °C',yl:'resistivity / 10⁻⁸ Ω m',pts:pts4,cap:'Figure 4.1',H:400})",
}
P4={'rho0p':[1.50,1.70],'alp':[3.50,4.50],'thp':[15,45],'Lp':[1.5,3.0],'dp':[0.40,0.80],'Ip':[3.0,8.0],'np':[8.0,9.0]}
parts=[]
parts.append(dict(pi=0,type='definition',K=lab('(a)')+'Define resistance.',
  B=kw('potential difference per unit current','p.d. per unit current','pd per unit current','voltage per unit current','potential difference divided by current','potential difference / current','potential difference ÷ current','potential difference over current','ratio of potential difference to current','ratio of p.d. to current','ratio of pd to current','ratio of voltage to current','ratio of potential difference and current','ratio between p.d. and current','ratio between potential difference and current','p.d. over current','p.d. divided by current','p.d. / current','p.d./current','voltage divided by current','voltage / current','voltage/current','potential difference per current','p.d. per current','voltage per current','potential difference/current'),
  U='Resistance is the potential difference per unit current.',V='R = V/I: the ratio of the potential difference across a component to the current in it.'))
parts.append(dict(pi=1,type='calculation',
  K=lab('(b)(i)')+'Figure 4.1 shows the variation with temperature of the resistivity of copper.${fig41}A copper wire has a length of ${L2} m and a diameter of ${d2} mm.<br><br>Show that the cross‑sectional area of the wire is ${A2e} m².',
  A='${A2e}',tolerance='3',
  U='A = π × (½ × ${d2} × 10<sup>−3</sup>)² = π × (${rad} × 10<sup>−3</sup>)² = ${A2e} m²',
  V='The cross‑section is a circle: A = πr² = π(d/2)². Convert millimetres to metres.'))
parts.append(dict(pi=2,type='calculation',K=lab('(b)(ii)')+'Determine the resistance of the wire at ${th1} °C.',
  C1=kw('r=ρl/a','r=ρ l/a','r=ρ×l/a','r=ρl÷a','ρl/a','ρ×l/a','rho l/a','r=pl/a','r=rho','ρ×l÷a','${rho1_ans}','ρl/a'),
  A='${R_ans}',tolerance='4',
  U='From Figure 4.1, ρ at ${th1} °C = ${rho1_ans} Ω m. R = ρL/A = (${rho1_ans} × ${L2}) / ${A2e} = ${R_ans} Ω',
  V='Read the resistivity at ${th1} °C from the graph, then use R = ρL/A with the cross‑sectional area from (b)(i).'))
parts.append(dict(pi=3,type='explain',
  K=lab('(b)(iii)')+'A different copper wire has the same resistance as the answer in 4(b)(ii). This wire also has a diameter of ${d2} mm but has a length that is greater than ${L2} m.<br><br>With reference to Figure 4.1, state and explain whether the temperature of this wire is less than, equal to or greater than ${th1} °C.',
  B=andor(['resistivity','ρ','rho'],['lower','less','smaller','decrease','reduc','smaller than','not as high']),
  B2=kw('less than','lower than','below','colder','cooler','lower temperature','less temperature','temperature is less','temperature is lower','temperature less','temperature lower','temperature is smaller','temperature decreases'),
  U='The resistance and cross‑sectional area are the same but the length is greater, so the resistivity is lower (R = ρL/A). From Figure 4.1 a lower resistivity means a lower temperature: the temperature is less than ${th1} °C.',
  V='R = ρL/A. With R and A unchanged, a longer wire must have a smaller resistivity. The graph shows that resistivity increases with temperature, so the temperature is below ${th1} °C.'))
parts.append(dict(pi=4,type='explain',K=lab('(b)(iv)')+'State one way in which the variation of resistance with temperature for a thermistor is different from that of a copper wire.',
  B=kw('resistance decreases','resistance of thermistor decreases','resistance of the thermistor decreases','resistance of a thermistor decreases','thermistor resistance decreases','decreases with temperature','decreases with increasing temperature','decreases as temperature','decreases as the temperature','resistance falls','resistance goes down','resistance reduces','resistance drops','inversely proportional','copper increases','copper resistance increases','resistance of copper increases','resistance of the copper increases','negative temperature coefficient','ntc','decrease with temperature','decrease with increasing temperature','decrease as temperature','goes down as temperature','falls as temperature','decreases when temperature','resistance gets smaller','resistance gets lower'),
  U='The resistance of a thermistor decreases with increasing temperature, whereas the resistance of copper increases.',
  V='An (NTC) thermistor’s resistance falls as temperature rises; a metal wire’s resistance rises as temperature rises.'))
parts.append(dict(pi=5,type='calculation',
  K=lab('(c)(i)')+'Each metal has a property known as its temperature coefficient of resistivity <i>α</i>. This is given by<br><br><i>α</i> = (change in resistivity) ÷ (initial resistivity × change in temperature).<br><br>Deduce the SI unit for <i>α</i>.',
  B=kw('k-1','k−1','k⁻¹','k^-1','k^−1','1/k','per k','/k','°c-1','°c−1','°c⁻¹','°c^-1','1/°c','per °c','/°c','kelvin-1','kelvin−1','kelvin⁻¹','per kelvin','1/kelvin'),
  U='K<sup>−1</sup> (accept °C<sup>−1</sup>)',V='The resistivity units cancel (change in resistivity ÷ initial resistivity), leaving 1 ÷ temperature, so the SI unit is K⁻¹.'))
parts.append(dict(pi=6,type='calculation',
  K=lab('(c)(ii)')+'Use Figure 4.1 to determine a value of <i>α</i>, in its SI unit, for copper at a temperature of 0 °C.',
  C1='${rho0m}|${rho0e}|α=(ρ-ρ0)/(ρ0∆θ)|α=(ρ−ρ0)/(ρ0Δθ)|gradient/ρ0|gradient/initial resistivity',
  A='${alp_rng}',tolerance='0',
  U='From Figure 4.1, ρ at 0 °C = ${rho0m} × 10<sup>−8</sup> Ω m. Taking a second point on the line: α = (change in ρ) / (ρ at 0 °C × Δθ) = gradient / ρ<sub>0</sub> ≈ ${alp_ans} K<sup>−1</sup>',
  V='Take two points on the line. α = (ρ − ρ₀) / (ρ₀ × Δθ), where ρ₀ is the resistivity at 0 °C. This equals the gradient of the line divided by ρ₀. Graph readings allow a range (about −20% to +30%) because the value depends on how you read the line.'))
parts.append(dict(pi=7,type='calculation',
  K=lab('(d)')+'There is a current of ${I2} A in the wire in 4(b). The number density of charge carriers (free electrons) for copper is ${n2} × 10<sup>28</sup> m<sup>−3</sup>.<br><br>Calculate the mean drift speed <i>v</i> of the charge carriers in the wire.',
  C1=andor(['${I2}'],['${n2}e28'],['${A2e}']),
  A='${vd_ans}',tolerance='3',
  U='I = Anvq, so v = I / (Anq) = ${I2} / (${A2e} × ${n2} × 10<sup>28</sup> × 1.60 × 10<sup>−19</sup>) = ${vd_ans} m s<sup>−1</sup>',
  V='Use I = Anvq with the cross‑sectional area from (b)(i) and q = e = 1.60 × 10⁻¹⁹ C.'))
ALL+=question(LV,'9702-26-21-Q4',PAPER,'definition','Electricity,Units',P4,G4,'Question 4',parts)

# =====================================================================  Q5
KW_B1=andor(['⅔','2/3','two thirds','two-thirds','2e/3','0.67','0.66'],['⅓','1/3','one third','one-third','e/3','0.33'])
G5={
 's':'sp<1?1:-1','ch1':"s>0?'+1e':'−1e'",
 'kwb2':"s>0?'[[\"quark\"],[\"antiquark\",\"anti-quark\",\"anti quark\",\"anti-down\",\"antidown\",\"anti down\",\"anti-strange\",\"antistrange\",\"anti-bottom\",\"antibottom\"],[\"⅔\",\"2/3\",\"two thirds\",\"up\",\"charm\",\"top\"],[\"⅓\",\"1/3\",\"one third\",\"anti-down\",\"antidown\",\"anti down\",\"anti-strange\",\"antistrange\",\"anti-bottom\",\"antibottom\"]]':'[[\"quark\"],[\"antiquark\",\"anti-quark\",\"anti quark\",\"anti-up\",\"antiup\",\"anti up\",\"anti-charm\",\"anti-top\"],[\"⅓\",\"1/3\",\"one third\",\"down\",\"strange\",\"bottom\"],[\"⅔\",\"2/3\",\"two thirds\",\"anti-up\",\"antiup\",\"anti up\",\"anti-charm\",\"anti-top\"]]'",
 'kwo2':"s>0?'[[\"−1\",\"-1\",\"minus 1\",\"minus one\",\"negative 1\",\"negative one\"],[\"⅔\",\"2/3\",\"⅓\",\"1/3\",\"two thirds\",\"one third\",\"down\",\"strange\",\"bottom\"]]':'[[\"+1\",\"plus 1\",\"plus one\",\"positive 1\",\"positive one\"],[\"⅔\",\"2/3\",\"⅓\",\"1/3\",\"two thirds\",\"one third\",\"up\",\"charm\",\"top\"]]'",
 'ans1':"s>0?'an up quark (+⅔e) and an anti-down quark (+⅓e): (+⅔e) + (+⅓e) = +1e':'a down quark (−⅓e) and an anti-up quark (−⅔e): (−⅓e) + (−⅔e) = −1e'",
 'oth_d':"s>0?'0 and −1e':'0 and +1e'",
 'ans2':"s>0?'0: e.g. an up quark (+⅔e) with an anti-up quark (−⅔e). −1e: a down quark (−⅓e) with an anti-up quark (−⅔e).':'0: e.g. an up quark (+⅔e) with an anti-up quark (−⅔e). +1e: an up quark (+⅔e) with an anti-down quark (+⅓e).'",
}
P5={'sp':[0,1.99]}
parts=[]
parts.append(dict(pi=0,type='definition',K=lab('(a)')+'The general quark composition of a meson is a quark and an antiquark.<br><br>State the general quark composition of a baryon.',
  B=kw('three quarks','3 quarks','qqq','three antiquarks','3 antiquarks','three quark','3 quark','q q q','three q','three anti','three anti-quarks','3 anti-quarks'),
  U='A baryon is made of three quarks (or three antiquarks).',V='Baryons are made of three quarks (antibaryons of three antiquarks).'))
parts.append(dict(pi=1,type='explain',K=lab('(b)(i)')+'Explain, in terms of quark composition, how a meson may have an overall charge of ${ch1}, where <i>e</i> is the elementary charge.',
  B=KW_B1,B2='${kwb2}',
  U='A meson is a quark and an antiquark: ${ans1}.',
  V='Quarks carry charges of ±⅔e (up, charm, top: +⅔e; down, strange, bottom: −⅓e) and antiquarks carry the opposite charge. Two marks: the quark charges (⅔e and ⅓e) and the correct assignment to the quark and the antiquark.'))
parts.append(dict(pi=2,type='explain',K=lab('(b)(ii)')+'State and explain the two other possible overall charges for a meson.',
  B=andor(['0','zero','neutral','no charge'],['⅔','2/3','⅓','1/3','two thirds','one third','up','down','charm','strange','top','bottom']),
  B2='${kwo2}',
  U='The other possible overall charges are ${oth_d}. ${ans2}',
  V='Pairing a quark with an antiquark of the same flavour gives zero charge. The remaining charge has the opposite sign to the one in (b)(i), found from the other quark–antiquark pairing.'))
parts.append(dict(pi=3,type='definition',K=lab('(c)')+'State the names of two particles that are classed as leptons.',
  B=kw('electron','positron','beta','antielectron','anti-electron','neutrino','antineutrino','muon','antimuon','tau','tauon','antitau'),
  B2=andor(['electron','beta'],['positron','antielectron','anti-electron','neutrino','antineutrino','muon','antimuon','tau','tauon','antitau']),
  U='Any two of: electron, positron, neutrino, antineutrino, muon, antimuon, tau, antitau.',
  V='Leptons include the electron, muon and tau, their neutrinos, and their antiparticles. Two different leptons are needed.'))
parts.append(dict(pi=4,type='explain',K=lab('(d)')+'A similarity between leptons and mesons is that they both have the same possible overall charges as those described in 5(b)(i) and 5(b)(ii).<br><br>State one difference between leptons and mesons.',
  B=kw('fundamental','elementary','made of quarks','made from quarks','made up of quarks','contain quarks','contains quarks','have quarks','composed of quarks','consist of quarks','consists of quarks','internal structure','smaller particles','hadron','strong force','strong nuclear force','boson','fermion','spin','different masses','different mass','mesons are made','mesons are composed','leptons are not made','leptons do not','leptons are not composed','quark composition','quark content','mesons have'),
  U='Leptons are fundamental particles, but mesons are made of quarks (a quark and an antiquark).',
  V='Possible differences: leptons are fundamental (mesons are made of quarks); mesons are hadrons and feel the strong nuclear force (leptons do not); mesons are bosons and leptons are fermions; their masses and spins differ.'))
ALL+=question(LV,'9702-26-21-Q5',PAPER,'definition','Particle physics',P5,G5,'Question 5',parts)

POST={
 '9702-26-21-Q1':[('${M6}','${M6s}'),('${r4}','${r4s}'),('${a0}','${a0s}'),('${ue_ans} m s','${sci(ue,3)} m s'),('${h_ans}','${h_disp}')],
 '9702-26-21-Q2':[('${m}','${ms}'),('${x}','${xs}'),('${d}','${ds}')],
 '9702-26-21-Q3':[('${T2}','${T2s}'),('${tq}','${tqs}'),('${twoT2}','${twoT2s}')],
 '9702-26-21-Q4':[('${A2e}','${sci(A2,1)}'),('${rho1_ans}','${sci(rho1,2)}'),('${vd_ans}','${sci(vd,2)}'),('${alp_ans}','${sci(alpha,2)}'),('${I2}','${I2s}'),('${n2}','${n2s}'),('${L2}','${L2s}'),('${d2}','${d2s}')],
}
TEXTCOLS=['mainText','partText','modelAnswer','explanation','tableRowLabels']
for r in ALL:
    for a,b in POST.get(r['id'],[]):
        for c in TEXTCOLS: r[c]=r[c].replace(a,b)
    # unit answer shown with unicode (no html) so it can be matched
    if r['id']=='9702-26-21-Q4' and r['partIndex']=='5': r['modelAnswer']='K⁻¹ (accept °C⁻¹)'

if __name__=='__main__':
    write_json(ALL,'new21.json',start=189)
    print(len(ALL),'rows')
    from collections import Counter
    print(Counter(r['id'] for r in ALL))
