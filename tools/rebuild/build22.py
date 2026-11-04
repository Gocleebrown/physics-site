import json, sys
sys.path.insert(0,'.')
from rowlib import *
from jshelpers import *

LV='AS'; PAPER='9702_s26_p22'
def lab(s): return '<b>'+s+'</b> '
ALL=[]
EX="(x,d)=>x.toExponential(d).replace('e+','e')"
SF="(x,n)=>String(+x.toPrecision(n))"
KEFORM=['ek=½mv²','ek=1/2mv²','ek=0.5mv²','½mv²','1/2mv²','0.5mv²','½mv^2','0.5mv^2','1/2mv^2','e=½mv²','ke=½mv²','½×m×v²','0.5×m×v','½×m×v','1/2×m×v','v²=2ek/m','v^2=2ek/m','v=√(2ek/m)','v=sqrt(2ek/m)','v²=2e/m','v^2=2e/m','2ek/m','2e/m']

# ===================================================================== Q1
G1={'sf':SF,'sci':SCI,'gsvg':GSVG,'ex':EX,
 't1':'Math.round(t1p)','v1':'Math.round(v1p)','t2':'Math.round(t2p)','d3':'40-t2',
 'tP':'Math.round(t1+2+tpr*(t2-t1-4))','a2':'+a2p.toPrecision(2)','a2s':'a2.toFixed(2)',
 'dist40':'0.5*t1*v1+v1*(t2-t1)+0.5*v1*d3','dist_ans':'String(Math.round(dist40))',
 'amax':'Math.max(v1/t1,v1/d3)','amax_ans':'sf(amax,2)',
 'D':'+(v1*(t2-tP)+0.5*v1*d3).toPrecision(3)','Ds':'String(D)',
 'v2sq':'2*a2*D','v2sq_ans':'sf(v2sq,2)','vret':'Math.sqrt(v2sq)','vret_ans':'sf(vret,2)',
 'tret':'Math.sqrt(2*D/a2)','tret_ans':'sf(tret,3)',
 'pts1':'[[0,0],[t1,v1],[t2,v1],[40,0],[80,-a2*40]]',
 'fig11':"gsvg({x0:0,x1:80,y0:-15,y1:15,mx:1,my:1,Mx:10,My:5,xl:'t / s',yl:'v / m s⁻¹',pts:pts1,cap:'Figure 1.1',H:420})",
}
P1={'t1p':[9,12],'v1p':[10,14],'t2p':[32,36],'tpr':[0,1],'a2p':[0.20,0.30]}
parts=[]
parts.append(dict(pi=0,type='definition',
 K=lab('(a)')+'The quantities amplitude, force, momentum and power are each either a scalar or a vector. State which of these quantities are scalars and which are vectors.',
 B=andor(['amplitude'],['power']), B2=andor(['force'],['momentum']),
 U='Scalars: amplitude and power. Vectors: force and momentum.',
 V='A vector has direction as well as magnitude (force, momentum). A scalar has magnitude only (amplitude, power). One mark for identifying the two scalars and one for the two vectors.'))
parts.append(dict(pi=1,type='explain',
 K=lab('(b)(i)')+'A car moves in a straight line along a road. Figure 1.1 shows the variation with time <i>t</i> of the velocity <i>v</i> of the car.${fig11}State the feature of the graph that represents the distance travelled by the car between <i>t</i> = 0 and <i>t</i> = 40 s.',
 B=kw('area','the area under','the area between','area under the graph','area beneath'),
 U='The area under the graph (between the graph line and the time axis).',
 V='Distance is the area under a velocity–time graph (the gradient gives acceleration).'))
parts.append(dict(pi=2,type='calculation',
 K=lab('(b)(ii)')+'Calculate the distance travelled by the car between <i>t</i> = 0 and <i>t</i> = 40 s.',
 A='${dist_ans}',tolerance='2.5',
 U='Area under the graph = ½ × ${t1} × ${v1} + ${v1} × (${t2} − ${t1}) + ½ × ${d3} × ${v1} = ${dist_ans} m',
 V='Split the area under the graph into a triangle, a rectangle and a second triangle and add them. Read the corner times and the maximum velocity from the grid.'))
parts.append(dict(pi=3,type='calculation',
 K=lab('(b)(iii)')+'Determine the maximum magnitude of the acceleration of the car.',
 C1=kw('a=(v-u)/t','a=(v–u)/t','a=(v−u)/t','a=(u-v)/t','a=v/t','a=δv/δt','a=∆v/∆t','a=δv/t','gradient','slope','${v1}/${d3}','${v1}/${t1}','(0-${v1})/${d3}','(0−${v1})/${d3}','(0–${v1})/${d3}'),
 A='${amax_ans}',tolerance='3',
 U='The steepest gradient is the decrease from ${v1} m s⁻¹ to zero between t = ${t2} s and t = 40 s. a = (v − u) / t = (0 − ${v1}) / ${d3} = −${amax_ans} m s⁻², so the maximum magnitude is ${amax_ans} m s⁻²',
 V='Acceleration is the gradient of a velocity–time graph. Compare the gradients of the three sloping sections: the steepest section gives the maximum magnitude.'))
parts.append(dict(pi=4,type='calculation',
 K=lab('(b)(iv)')+'At <i>t</i> = ${tP} s, the car is at a point P.<br>At <i>t</i> = 40 s, the car is at a distance of ${Ds} m from P.<br>After <i>t</i> = 40 s, the car travels with a constant acceleration of −${a2s} m s<sup>−2</sup> until the car is again at point P.<br><br>Calculate the speed of the car when it is at point P for the second time.',
 C1=kw('v²=2×${a2s}×${Ds}','v^2=2×${a2s}×${Ds}','2×${a2s}×${Ds}','2×−${a2s}×−${Ds}','2×-${a2s}×-${Ds}','2*${a2s}*${Ds}','2x${a2s}x${Ds}','${v2sq_ans}','${tret_ans}','0.5×${a2s}×t²','½×${a2s}×t²'),
 A='${vret_ans}',tolerance='0',
 U='v² = u² + 2as = 0 + 2 × ${a2s} × ${Ds} = ${v2sq_ans}, so the speed = ${vret_ans} m s⁻¹',
 V='After t = 40 s the car starts from rest (v = 0) and returns the distance to P with constant acceleration, so v² = 2as. Use the full distance from P to the car at t = 40 s.'))
parts.append(dict(pi=5,type='imageChoice',
 K=lab('(b)(v)')+'At <i>t</i> = 0, the displacement of the car is zero. Which sketch correctly shows the variation of the displacement of the car with <i>t</i> from <i>t</i> = 0 to <i>t</i> = 80 s? In each sketch, <i>t</i><sub>1</sub> = ${t1} s and <i>t</i><sub>2</sub> = ${t2} s are the times at which the gradient of the graph in Figure 1.1 changes.',
 answerType='imageChoice',
 imageOptions=['as2622_q1v_c.svg','as2622_q1v_d.svg','as2622_q1v_a.svg','as2622_q1v_b.svg'],
 correctImageIndex='2',imageChoiceMarks='3',
 U='The displacement increases to a maximum at t = 40 s then decreases to t = 80 s without crossing the time axis. The gradient (velocity) increases from 0 to t₁, is constant and positive from t₁ to t₂, and then decreases to zero at 40 s. After 40 s the gradient becomes more and more negative.',
 V='Displacement–time gradient = velocity. Between 0 and t₁ the velocity increases (curve getting steeper); between t₁ and t₂ it is constant (straight line); from t₂ to 40 s it decreases to zero (curve levelling off at the maximum displacement); after 40 s the velocity is negative and increasing in size, so the displacement falls with an increasingly steep gradient. The car never goes below its starting point in this time.'))
ALL+=question(LV,'9702-26-22-Q1',PAPER,'definition','Kinematics',P1,G1,'Question 1',parts)

# ===================================================================== Q2
G2={'sf':SF,'sci':SCI,'fig21':FIG21,'fig22':FIG22,
 'mB':'+mbp.toPrecision(2)','mP':'+mpp.toPrecision(2)','mBs':'mB.toFixed(1)','mPs':'mP.toFixed(1)',
 'g':'9.81','twoR':'(mB-mP)*g','twoR_ans':'sf(twoR,3)','R':'twoR/2','R_ans':'sf(R,2)',
 'f21':'fig21(mBs,mPs)','f22':'fig22()'}
P2={'mbp':[6.0,10.0],'mpp':[3.0,5.5]}
parts=[]
parts.append(dict(pi=0,type='definition',K=lab('(a)')+'State the conditions required for an object to be in equilibrium.',
 B=kw('resultant force','net force','sum of forces','sum of the forces','total force','sum of all the forces','forces sum to zero','f=0','force is zero','no resultant force','zero resultant force','forces in all directions','forces in every direction','vertical forces','horizontal forces'),
 B2=kw('moments about','moment about','moments is zero','moment is zero','moment=0','moments are zero','moments=0','resultant moment is zero','sum of moments','sum of the moments','sum of clockwise','clockwise moment','clockwise moments','clockwise','anticlockwise','anti-clockwise','torque','net moment is','total moment is','moments balance','moments are balanced'),
 U='The resultant force (in any direction) is zero and the resultant torque (moment) about any point is zero.',
 V='Two conditions: the vector sum of the forces is zero (no resultant force) and the sum of the moments about any point is zero (no resultant moment).'))
parts.append(dict(pi=1,type='explain',
 K=lab('(b)(i)')+'A block rests in equilibrium on the centre of a uniform horizontal plank. The block is attached to two ropes, each of which passes over a fixed pulley and then attaches to an end of the plank as shown in Figure 2.1.${f21}Where the ropes attach to the block and to the plank, the angle between the ropes and the vertical is <i>θ</i>. There is negligible friction between the pulleys and the ropes.<br><br>The mass of the block is ${mBs} kg. The mass of the plank is ${mPs} kg.<br><br>Figure 2.2 shows the directions of the forces acting on the plank and the block. The weight of the plank is <i>W</i><sub>P</sub>, the weight of the block is <i>W</i><sub>B</sub>, the tension in each rope is <i>T</i> and the forces that the plank and the block exert on each other each have magnitude <i>R</i>.${f22}Use Figure 2.2 to show that<br><br><i>R</i> + <i>W</i><sub>P</sub> = <i>W</i><sub>B</sub> − <i>R</i>.',
 M=kw('2tcos','2t cos','2t×cos','2×tcos','2t*cos','2tsin(90'),
 A=andor(['wb'],['wp'],['r']),
 U='For the plank: 2T cos θ = R + W<sub>P</sub> (the two rope tensions pull the plank up; R and its weight act down). For the block: 2T cos θ + R = W<sub>B</sub>. Equating 2T cos θ: R + W<sub>P</sub> = W<sub>B</sub> − R',
 V='Resolve vertically for each object. The vertical component of each tension is T cos θ, so the two ropes give 2T cos θ on each object. Plank: upward 2T cos θ equals downward R + W_P. Block: upward 2T cos θ + R equals downward W_B. Equate the two expressions for 2T cos θ.'))
parts.append(dict(pi=2,type='calculation',K=lab('(b)(ii)')+'Use the equation in 2(b)(i) to calculate the magnitude of <i>R</i>.',
 C1=kw('2r=wb-wp','2r=wb−wp','2r=wb–wp','r=(wb-wp)/2','2r=${mBs}×9.81−${mPs}×9.81','2r=${mBs}×9.81-${mPs}×9.81','2r=${mBs}g−${mPs}g','2r=${mBs}g-${mPs}g','2r=${twoR_ans}','${twoR_ans}'),
 A='${R_ans}',tolerance='2.6',
 U='2R = W<sub>B</sub> − W<sub>P</sub> = ${mBs} × 9.81 − ${mPs} × 9.81, so R = ${R_ans} N',
 V='Rearrange R + W_P = W_B − R to 2R = W_B − W_P, then use W = mg for each weight and halve the result.'))
parts.append(dict(pi=3,type='definition',K=lab('(c)(i)')+'The extension of each rope in 2(b) is proportional to the force applied to it.<br><br>State the name of the law that describes this behaviour.',
 B=kw('hooke','hook','huk','hookie'),U='Hooke’s law',V='Hooke’s law: the extension of a material is proportional to the applied force, up to the limit of proportionality.'))
parts.append(dict(pi=4,type='definition',K=lab('(c)(ii)')+'The ropes have elastic deformation. State what is meant by elastic deformation.',
 B=andor(['removed','released','unloaded','remove','no longer','taken off','taken away','take away','stops','stopped','when the force','when the load','when the tension','when the stress'],['original','initial','unstretched','returns','return','regain','back to','zero extension','extension is zero','not deformed','no deformation','no permanent']),
 U='When the tension (force) is removed, the ropes return to their original length (the extension becomes zero).',
 V='Elastic deformation is reversible: once the force causing it is removed, the object goes back to its original shape and size. Plastic deformation is permanent.'))
ALL+=question(LV,'9702-26-22-Q2',PAPER,'definition','Dynamics,Materials',P2,G2,'Question 2',parts)

# ===================================================================== Q3
G3={'sf':SF,'sci':SCI,'fig31':FIG31,'ex':EX,
 'f':'+fp.toPrecision(2)','fs':'f.toFixed(1)','kf':'kc','f2':'+(f*kc).toPrecision(2)','f2s':'f2.toFixed(1)',
 'lam':'+lamp.toPrecision(2)','lams':'lam.toFixed(1)','dBP':'+bpp.toPrecision(2)','dAP':'+(dBP+lam).toFixed(2)',
 'dBPs':'dBP.toFixed(1)','dAPs':'dAP.toFixed(2).replace(/0$/,\'\')',
 'T':'1/f','T_ans':'sf(T,2)','v':'f*lam','v_ans':'sf(v,2)',
 'm':'+mp3.toPrecision(2)','ms':'m.toFixed(2)','amp':'Math.round(amp0)','dh':'2*amp/100','dhs':'dh.toFixed(2)','dE':'m*9.81*dh','dE_ans':'sf(dE,2)',
 'f3':'fig31()'}
P3={'fp':[2.0,4.0],'kc':[1.25,1.6],'lamp':[1.2,2.0],'bpp':[2.0,3.2],'mp3':[0.30,0.60],'amp0':[10,20]}
parts=[]
parts.append(dict(pi=0,type='definition',
 K=lab('(a)')+'Two oscillating dippers are used to create progressive transverse water waves on the surface of a lake. The waves are shown from above in Figure 3.1.${f3}Wave crests are represented by a solid line. Wave troughs are represented by a dashed line. The waves superpose and an interference pattern is formed on the surface of the water.<br><br>The dippers oscillate in phase with each other and with a frequency of ${fs} Hz.<br><br>State what is meant by a progressive wave.',
 B=kw('transfers energy','transfer of energy','transfers the energy','transports energy','carries energy','propagates energy','moves energy','transmits energy','energy is transferred','energy transferred','energy is transported','energy is carried','energy is propagated','transfer energy','energy transfer','propagates','carries the energy'),
 U='A progressive wave is a wave that transfers energy (in the direction of propagation).',V='A progressive wave transfers energy from one place to another without transferring matter.'))
parts.append(dict(pi=1,type='calculation',K=lab('(b)(i)')+'Calculate the period of the waves.',
 A='${T_ans}',tolerance='2',
 U='T = 1 / f = 1 / ${fs} = ${T_ans} s',V='Period is the reciprocal of frequency: T = 1/f.'))
parts.append(dict(pi=2,type='calculation',
 K=lab('(b)(ii)')+'Points A and B are at the centre of the dippers. Point P is shown on Figure 3.1. The distance from A to P is ${dAPs} m. The distance from B to P is ${dBPs} m.<br><br>Determine the speed of the waves.',
 C2=kw('v=fλ','v=f×λ','v=λf','v=λ×f','v=fl','c=fλ','v=f*λ','v=λ/t','v=λ/T','v=λ/period'),
 C1='${lams}',
 A='${v_ans}',tolerance='2.5',
 U='λ = ${dAPs} − ${dBPs} = ${lams} m. v = fλ = ${fs} × ${lams} = ${v_ans} m s⁻¹',
 V='P is on a line of constructive interference: crests from A and B arrive together, and the path difference AP − BP is one whole wavelength (the first line of maximum on each side of the centre line). So λ = AP − BP. Then use v = fλ.'))
parts.append(dict(pi=3,type='calculation',
 K=lab('(c)(i)')+'A ball of mass ${ms} kg is placed at P, where it floats on the surface of the lake. The amplitude of the vertical oscillation of the ball is ${amp} cm.<br><br>Calculate the difference in the gravitational potential energy Δ<i>E</i> of the ball between its highest and lowest points.',
 C2=kw('δe=mgδh','Δe=mgΔh','∆e=mg∆h','e=mgh','gpe=mgh','mgδh','mgΔh','mg∆h','mgh','ΔE=m×g×Δh'),
 C1='${dhs}|${amp}×2|2×${amp}',
 A='${dE_ans}',tolerance='3',
 U='The ball moves a total distance Δh = 2 × ${amp} cm = ${dhs} m between its highest and lowest points. ΔE = mgΔh = ${ms} × 9.81 × ${dhs} = ${dE_ans} J',
 V='The height difference between the highest and lowest points is twice the amplitude (peak to trough), not the amplitude. Convert centimetres to metres.'))
parts.append(dict(pi=4,type='explain',
 K=lab('(c)(ii)')+'The frequency of oscillation of the dippers is increased to ${f2s} Hz without changing their amplitude of oscillation. The ball remains at the same position on the surface of the lake.<br><br>State and explain whether the amplitude of the oscillation of the ball increases, decreases or remains the same.',
 B=kw('not in phase','out of phase','phase difference','not a whole number','not an integer','not whole','not a multiple','path difference','not constructive','less constructive','no longer constructive','wavelength changes','wavelength decreases','wavelength is shorter','wavelength becomes','λ decreases','λ changes','not exactly in phase','not integer'),
 B2=kw('decrease','less','smaller','reduce','lower','drops','falls','reduces'),
 U='The amplitude decreases. The wavelength changes (v = fλ), so the path difference (${lams} m) is no longer a whole number of wavelengths: the waves from A and B arrive at P out of phase and the superposition is no longer fully constructive.',
 V='The wave speed is unchanged, so a higher frequency gives a shorter wavelength. The path difference of ${lams} m was one whole wavelength before; now it is not a whole number of wavelengths, so the two waves at P are not in phase and the amplitude of the resultant oscillation decreases.'))
ALL+=question(LV,'9702-26-22-Q3',PAPER,'definition','Waves,Energy',P3,G3,'Question 3',parts)

# ===================================================================== Q4
FIG41='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 300" style="max-width:520px;width:100%;background:#fff;display:block;margin:10px 0" font-family="Arial,sans-serif" font-size="14"><line x1="40" y1="250" x2="480" y2="60" stroke="#000" stroke-width="1.6"/><g transform="translate(150,206) rotate(-23.4)"><rect x="-70" y="-34" width="140" height="34" rx="12" fill="#fff" stroke="#000" stroke-width="1.6"/><rect x="-58" y="-28" width="10" height="16" fill="none" stroke="#000"/><rect x="-42" y="-28" width="10" height="16" fill="none" stroke="#000"/><rect x="-26" y="-28" width="10" height="16" fill="none" stroke="#000"/><rect x="-10" y="-28" width="10" height="16" fill="none" stroke="#000"/><rect x="6" y="-28" width="10" height="16" fill="none" stroke="#000"/><rect x="22" y="-28" width="10" height="16" fill="none" stroke="#000"/><rect x="38" y="-28" width="10" height="16" fill="none" stroke="#000"/></g><text x="176" y="236">X</text><circle cx="176" cy="226" r="3"/><text x="445" y="58">Y</text><circle cx="450" cy="78" r="3"/><text x="96" y="130">train</text><line x1="122" y1="136" x2="146" y2="164" stroke="#000"/></svg><p style="text-align:center;margin:0 0 10px"><b>Figure 4.1</b></p>'''
G4={'sf':SF,'sci':SCI,'ex':EX,
 'm4':'+m4p.toPrecision(2)','m':'m4*1e4','k5':'+k5p.toPrecision(2)','KE':'k5*1e5','t':'Math.round(tp)',
 'P5':'+P5p.toPrecision(2)','P':'P5*1e5','v':'Math.sqrt(2*KE/m)','v_ans':'sf(v,2)','v2_ans':'sf(2*KE/m,3)',
 'E1':'+E1p.toPrecision(2)','E1s':'E1.toFixed(1)','dEt':'(P*t-F0*v*t)/1e6','E2':'+(E1+dEt).toFixed(1)','E2s':'E2.toFixed(1)',
 'dEmj':'+(E2-E1).toFixed(1)','dEmjs':'dEmj.toFixed(1)','dE':'dEmj*1e6','dE_ans':'ex(dE,1)',
 'F':'(P*t-dE)/(v*t)','F_ans':'sf(F,2)',
 'V':'+Vp.toPrecision(2)','I':'Math.round(P/(eta0/100*V))','IV':'I*V','IV_ans':'ex(IV,2)','eff':'P/IV*100','eff_ans':'sf(eff,2)',
 'm4s':'m4.toFixed(1)','k5s':'k5.toFixed(1)','P5s':'P5.toFixed(1)','Pwork':'P*t'}
P4={'m4p':[1.2,1.8],'k5p':[1.0,1.8],'tp':[40,60],'P5p':[1.0,1.4],'E1p':[6.0,9.0],'F0':[500,900],'Vp':[1200,1600],'eta0':[70,90]}
parts=[]
parts.append(dict(pi=0,type='calculation',
 K=lab('(a)')+'An electric train of mass ${m4s} × 10<sup>4</sup> kg travels up a slope at a constant speed as shown in Figure 4.1.'+FIG41+'At point X, the train has gravitational potential energy ${E1s} MJ.<br>At point Y, the train has gravitational potential energy ${E2s} MJ.<br>The train takes a time of ${t} s to move from X to Y.<br>The kinetic energy of the train is ${k5s} × 10<sup>5</sup> J.<br><br>Calculate the speed of the train.',
 C2=kw(*KEFORM), C1='${v2_ans}',
 A='${v_ans}',tolerance='2',
 U='E<sub>K</sub> = ½mv², so v² = 2 × ${k5s} × 10<sup>5</sup> / ${m4s} × 10<sup>4</sup> = ${v2_ans}, and v = ${v_ans} m s⁻¹',
 V='Rearrange E_K = ½mv² for v². Take the square root at the end: stopping at v² loses the accuracy mark.'))
parts.append(dict(pi=1,type='definition',K=lab('(b)(i)')+'The train is powered by an electric motor. The useful output power of the motor is ${P5s} × 10<sup>5</sup> W.<br><br>Define power.',
 B=kw('work done/time','work done / time','work/time','work done per unit time','work done per second','work per unit time','work done per time','rate of doing work','rate of work done','rate of work','rate of energy transfer','rate of energy transferred','rate of energy conversion','energy transferred per unit time','energy transferred/time','energy transferred / time','energy converted per unit time','energy converted/time','work done divided by time','work divided by time','work over time','work done over time','ratio of work done and time','ratio of work and time','change in energy/time','change in energy per unit time','energy transferred per second','energy transferred over time','work done in a time','energy transfer per unit time','energy transferred divided by time'),
 U='Power is the work done per unit time (the rate of doing work).',V='Power = work done / time taken, or the rate of energy transfer.'))
parts.append(dict(pi=2,type='calculation',K=lab('(b)(ii)')+'Determine the resistive force <i>F</i> acting on the train as it moves from point X to point Y.',
 C2=kw('w=fs','w=fvt','w=pt','p=fv','e=pt','f=p/v','pt=','fvt','p×t','p*t'), C1='${dE_ans}|${dEmjs}',
 A='${F_ans}',tolerance='3',
 U='Useful work done by the motor = P × t = ${P5s} × 10<sup>5</sup> × ${t} = ${sci(Pwork,2)} J. Work done against resistive force = ${sci(Pwork,2)} − (${E2s} − ${E1s}) × 10<sup>6</sup> = F × v × t, so F = ${F_ans} N',
 V='The useful work from the motor does two jobs: it raises the train (increase in gravitational potential energy, ${dEmjs} MJ, which must be converted to J) and it overcomes the resistive force (F × distance, distance = v × t). Kinetic energy is constant because the speed is constant.'))
parts.append(dict(pi=3,type='calculation',K=lab('(b)(iii)')+'The current in the motor is ${I} A. The potential difference (p.d.) across the motor is ${V} V.<br><br>Calculate the percentage efficiency of the motor.',
 C2=kw('p=iv','p=vi','p=i×v','p=v×i','iv=','vi=','i×v','v×i','p=i*v'), C1='${IV_ans}',
 A='${eff_ans}',tolerance='1.2',
 U='Input power = IV = ${I} × ${V} = ${sci(IV,2)} W. Efficiency = useful output power / input power × 100 = ${P5s} × 10<sup>5</sup> / ${sci(IV,2)} × 100 = ${eff_ans}%',
 V='Efficiency = useful power output / total power input. The total power input to the motor is the electrical power IV. The useful power output is the value given in the question.'))
ALL+=question(LV,'9702-26-22-Q4',PAPER,'definition','Energy,Electricity,Dynamics',P4,G4,'Question 4',parts)

# ===================================================================== Q5
G5={'sf':SF,'sci':SCI,'fig51':FIG51,'ckt':CKT,'ex':EX,
 'E':'Math.round(Ep)','Rw':'+Rwp.toPrecision(2)','Rws':'Rw.toFixed(1)','RT':'Rw/2','RT_ans':'sf(RT,2)','Ib':'E/RT','Ib_ans':'sf(Ib,2)',
 'Iw':'E/Rw','Iw_ans':'sf(Iw,2)',
 'Aw5':'+Awp.toPrecision(2)','Aw5s':'Aw5.toFixed(1)','Aw':'Aw5*1e-6','n28':'+n28p.toPrecision(2)','n28s':'n28.toFixed(1)',
 'vd':'Iw/(Aw*n28*1e28*1.6e-19)','vd_ans':'ex(vd,1)',
 'Itot':'+(E/Rw*kc).toPrecision(2)','Itots':'Itot.toPrecision(2)','IX':'Itot-E/Rw','IX_ans':'sf(IX,2)','Rtop':'E/IX','Rtop_ans':'sf(Rtop,3)',
 'RX':'Rtop-Rw','RX_ans':'sf(RX,2)','RT2':'E/Itot','RT2_ans':'sf(RT2,2)',
 'f51':'fig51()','f52':'ckt(E,0,false)','f53':'ckt(E,Itots,true)'}
P5={'Ep':[6,24],'Rwp':[2.0,4.0],'Awp':[4.0,8.0],'n28p':[6.0,9.0],'kc':[1.15,1.8]}
parts=[]
parts.append(dict(pi=0,type='explain',
 K=lab('(a)')+'Three resistors of resistances <i>R</i><sub>1</sub>, <i>R</i><sub>2</sub> and <i>R</i><sub>3</sub> are connected in a network in parallel as shown in Figure 5.1.${f51}The currents in the resistors are <i>I</i><sub>1</sub>, <i>I</i><sub>2</sub> and <i>I</i><sub>3</sub> respectively. The total current entering the network is <i>I</i><sub>T</sub>. The potential difference (p.d.) across the resistors is <i>V</i>.<br><br>Derive the equation<br><br>1 / <i>R</i><sub>T</sub> = 1 / <i>R</i><sub>1</sub> + 1 / <i>R</i><sub>2</sub> + 1 / <i>R</i><sub>3</sub><br><br>where <i>R</i><sub>T</sub> is the total resistance of the network.',
 B=kw('it=i1+i2+i3','i=i1+i2+i3','i1+i2+i3','it=i₁+i₂+i₃','i₁+i₂+i₃','sum of the currents','sum of currents','currents add','currents sum','total current is the sum','total current equals the sum','current splits','current is shared','current divides','current is divided'),
 B2=andor(['v/r','i=v/r','v=ir','ir','v/rt'],['1/rt','1/r','1/r1','1/r₁','rt','same p.d','same potential difference','same voltage','same v','cancel','divide']),
 U='The p.d. across each resistor is the same (V). The total current is the sum of the currents: I<sub>T</sub> = I<sub>1</sub> + I<sub>2</sub> + I<sub>3</sub>. Using I = V / R for each: V / R<sub>T</sub> = V / R<sub>1</sub> + V / R<sub>2</sub> + V / R<sub>3</sub>. Dividing by V gives 1 / R<sub>T</sub> = 1 / R<sub>1</sub> + 1 / R<sub>2</sub> + 1 / R<sub>3</sub>.',
 V='Two marks: (1) the current entering the junction equals the sum of the currents in the branches (conservation of charge); (2) substitute I = V/R for each current, noting the p.d. V is the same across every branch, and cancel V.'))
parts.append(dict(pi=1,type='calculation',
 K=lab('(b)(i)')+'Two identical resistance wires, each of resistance ${Rws} Ω, are connected in parallel to a battery with negligible internal resistance and electromotive force (e.m.f.) ${E} V as shown in Figure 5.2.${f52}Calculate the current in the battery.',
 C1='${RT_ans}|${Iw_ans}|1/rt=1/${Rws}+1/${Rws}',
 A='${Ib_ans}',tolerance='2',
 U='R<sub>T</sub> = (1 / ${Rws} + 1 / ${Rws})⁻¹ = ${RT_ans} Ω. Current = V / R<sub>T</sub> = ${E} / ${RT_ans} = ${Ib_ans} A',
 V='Find the total resistance of the two wires in parallel (1/R_T = 1/R + 1/R), then use I = V/R_T. Alternatively the current in each wire is E/R and the battery supplies the sum of the two.'))
parts.append(dict(pi=2,type='calculation',
 K=lab('(b)(ii)')+'Each resistance wire has a cross-sectional area of ${Aw5s} × 10<sup>−6</sup> m<sup>2</sup>. The wires are made from a metal with a number density of charge carriers (free electrons) of ${n28s} × 10<sup>28</sup> m<sup>−3</sup>.<br><br>Calculate the average drift speed of the charge carriers in the wires.',
 C1='${Iw_ans}',
 A='${vd_ans}',tolerance='3',
 U='The current in each wire = ${Ib_ans} / 2 = ${Iw_ans} A. v = I / Anq = ${Iw_ans} / (${Aw5s} × 10⁻⁶ × ${n28s} × 10²⁸ × 1.6 × 10⁻¹⁹) = ${sci(vd,2)} m s⁻¹',
 V='The current in the equation I = Anvq is the current in ONE wire (the cross-sectional area given is for one wire), so halve the battery current. Using the whole battery current gives double the correct answer.'))
parts.append(dict(pi=3,type='definition',
 K=lab('(c)(i)')+'A component X is added to the circuit in 5(b) as shown in Figure 5.3.${f53}The current in the battery is now ${Itots} A. The resistance of each resistance wire remains ${Rws} Ω.<br><br>State the name of component X.',
 B=kw('light-dependent resistor','light dependent resistor','light-dependant resistor','light dependant resistor','ldr','photoresistor','photo resistor','photo-resistor','light sensitive resistor','light-sensitive resistor'),
 U='Light-dependent resistor (LDR)',V='The symbol, with two arrows pointing at the resistor, is a light-dependent resistor (LDR).'))
parts.append(dict(pi=4,type='calculation',K=lab('(c)(ii)')+'Determine the resistance of component X.',
 C2='${IX_ans}|${RT2_ans}', C1='${Rtop_ans}',
 A='${RX_ans}',tolerance='4',
 U='Current in the wire branch = ${E} / ${Rws} = ${Iw_ans} A, so the current in the branch with X = ${Itots} − ${Iw_ans} = ${IX_ans} A. Resistance of that branch = ${E} / ${IX_ans} = ${Rtop_ans} Ω. R<sub>X</sub> = ${Rtop_ans} − ${Rws} = ${RX_ans} Ω',
 V='The branch with X is in parallel with the other wire, so each branch has the full e.m.f. across it. Find the current in the wire (E/R), subtract it from the battery current to get the current in X’s branch, find that branch’s resistance and subtract the resistance of the wire in series with X.'))
parts.append(dict(pi=5,type='explain',K=lab('(c)(iii)')+'A change in the environment of component X causes the current in the battery to decrease. The resistance of the resistance wires remains constant.<br><br>State and explain how the environment of X has changed.',
 M=kw('resistance of x increase','resistance increase','resistance is greater','resistance rises','resistance goes up','resistance gets higher','resistance has increased','increased resistance','higher resistance','resistance becomes greater','resistance of the ldr increase','ldr resistance increase','r increase','resistance is higher','greater resistance','resistance of the ldr is higher','resistance of the ldr is greater','resistance gets bigger','resistance increases'),
 A=kw('darker','dimmer','less light','light intensity decrease','lower light','less bright','light decrease','decrease in light','intensity decrease','intensity of light decrease','light level decrease','light intensity is lower','light intensity has decreased','fewer photons','less intense','intensity is lower','lower intensity','decrease in intensity','less illumination','decrease in light intensity'),
 U='The current in the battery decreased, so the total resistance increased, so the resistance of X increased. The light intensity incident on X decreased (it is darker).',
 V='Smaller current for the same e.m.f. means greater total resistance, and since the wires are unchanged, the resistance of X has increased. The resistance of an LDR increases when the light intensity decreases.'))
ALL+=question(LV,'9702-26-22-Q5',PAPER,'definition','Electricity,Units',P5,G5,'Question 5',parts)

# ===================================================================== Q6
ISO="[['H',1,2],['H',1,3],['He',2,3],['He',2,4],['Li',3,6],['Li',3,7],['Be',4,9],['B',5,10],['B',5,11],['C',6,12]]"
G6={'sf':SF,'sci':SCI,'ex':EX,
 'u6':'+u6p.toPrecision(3)','v1':'+(u6*193/201).toPrecision(3)','u':'u6*1e6','vb':'v1*1e6',
 'p':'4*1.66e-27*u','p_ans':'ex(p,2)','vAu':'4*(u+vb)/197','vAu_ans':'ex(vAu,1)',
 'du':'Math.round(dup)','dabs':'2*du*1e4','dabs_ans':'ex(dabs,1)','pct':'dabs/(u+vb)*100','pct_ans':'sf(pct,2)',
 'iso':ISO,'ix':'Math.min(9,Math.floor(ip))','S':'iso[ix][0]','Zn':'iso[ix][1]','An':'iso[ix][2]',
 'nucl':"'<sup>'+An+'</sup><sub>'+Zn+'</sub>'+S",'nup':'Zn+An',
 'u6s':'u6.toFixed(2)','v1s':'v1.toFixed(2)','dus':'String(du)'}
P6={'u6p':[5.00,6.50],'dup':[3,8],'ip':[0,10]}
parts=[]
parts.append(dict(pi=0,type='explain',K=lab('(a)')+'One of the conclusions from the α-particle scattering experiment was that the atom is mostly empty space.<br><br>State the observation from the experiment that provides evidence for this conclusion.',
 B=andor(['most','majority','nearly all','large proportion','almost all','large fraction','vast majority'],['straight through','pass through','passed through','undeviated','no deviation','small deviation','not deflected','small angle','small deflection','no deflection','through the foil','through the gold','through the atom','little deviation','not deviated','without deviation','passes straight','pass straight','went through','go through','goes through','small deflect','slight']),
 U='Most of the α-particles pass straight through the (gold foil) atoms with little or no deviation.',
 V='If most of the volume of an atom were occupied, many α-particles would be scattered through large angles. The observation that most pass straight through (or are deviated only slightly) shows the atom is mostly empty space. Only a very small proportion are deflected through large angles.'))
parts.append(dict(pi=1,type='calculation',
 K=lab('(b)(i)')+'An α-particle travelling with a speed of ${u6s} × 10<sup>6</sup> m s<sup>−1</sup> collides with a stationary gold nucleus of mass 197 u. After the collision, the α-particle is travelling with a speed of ${v1s} × 10<sup>6</sup> m s<sup>−1</sup> in the opposite direction to its initial motion.<br><br>No external forces act on this system.<br><br>Show that the momentum of the α-particle before the collision is ${sci(p,2)} kg m s<sup>−1</sup>.',
 C1=kw('p=mv','mv','4×1.66','4u×','4u','6.64×10⁻²⁷','6.64e-27','4×1.66e-27'),
 A='${p_ans}',tolerance='1',
 U='The α-particle has mass 4u = 4 × 1.66 × 10⁻²⁷ kg. p = mv = 4 × 1.66 × 10⁻²⁷ × ${u6s} × 10⁶ = ${sci(p,2)} kg m s⁻¹',
 V='An α-particle is a helium nucleus of mass number 4, so its mass is 4 u. Convert u to kg (1 u = 1.66 × 10⁻²⁷ kg). Show the substitution fully: a show-that answer needs the working.'))
parts.append(dict(pi=2,type='calculation',K=lab('(b)(ii)')+'Use conservation of momentum to calculate the speed of the gold nucleus after the collision.',
 C1=kw('momentum before=momentum after','momentum before = momentum after','p before=p after','conservation of momentum','mu=mv','4u×${u6s}','197u×v','197×1.66','197 u','197u','4×1.66×10⁻²⁷×${v1s}','4u×${v1s}','−4u','-4u','4(u)'),
 A='${vAu_ans}',tolerance='3',
 U='Taking the initial direction of the α-particle as positive: 4u × ${u6s} × 10⁶ = 197u × v − 4u × ${v1s} × 10⁶. So v = ${sci(vAu,2)} m s⁻¹',
 V='Momentum is a vector. The α-particle reverses direction, so its final momentum is negative. Momentum before (all in the α-particle) = momentum after (gold nucleus − α-particle). Alternatively, if the collision is elastic, speed of approach = speed of separation.'))
parts.append(dict(pi=3,type='calculation',K=lab('(b)(iii)')+'The absolute uncertainty in each of the measured speeds of the α-particle is ± ${dus} × 10<sup>4</sup> m s<sup>−1</sup>.<br><br>Calculate the percentage uncertainty in the change in velocity of the α-particle.',
 C1='${dabs_ans}',
 A='${pct_ans}',tolerance='4',
 U='Absolute uncertainty in the change in velocity = ${dus} × 10⁴ + ${dus} × 10⁴ = ${sci(dabs,1)} m s⁻¹. The change in velocity = ${u6s} × 10⁶ + ${v1s} × 10⁶ (the direction reverses). Percentage uncertainty = ${sci(dabs,1)} / (${u6s} × 10⁶ + ${v1s} × 10⁶) × 100 = ${pct_ans}%',
 V='Absolute uncertainties add when velocities are subtracted. The change in velocity is v − u with opposite signs, so its magnitude is the SUM of the two speeds, not the difference.'))
parts.append(dict(pi=4,type='calculation',K=lab('(c)')+'Determine the number of up quarks in a nucleus of ${nucl}.',
 A='${nup}',
 U='Each proton (uud) contains 2 up quarks; each neutron (udd) contains 1 up quark. The nucleus has ${Zn} protons and ${An-Zn} neutron(s): 2 × ${Zn} + ${An-Zn} = ${nup}',
 V='Number of protons = proton number; number of neutrons = nucleon number − proton number. Proton = uud, neutron = udd.'))
parts.append(dict(pi=5,type='definition',K=lab('(d)')+'Describe the general quark composition of a meson.',
 B=kw('quark and an antiquark','quark and antiquark','one quark and one antiquark','quark-antiquark','quark–antiquark','1 quark and 1 antiquark','quark + antiquark','a quark and an anti-quark','quark and anti-quark','quark and anti quark','antiquark and a quark','antiquark and quark','1 quark 1 antiquark','quark & antiquark','quark and an anti quark','quark anti-quark','quark antiquark','qq̄','q q̄','quark/antiquark','quark, antiquark','quark with an antiquark','quark and its antiquark'),
 U='A meson consists of one quark and one antiquark.',V='Mesons are hadrons made of a quark–antiquark pair. (Baryons contain three quarks.)'))
ALL+=question(LV,'9702-26-22-Q6',PAPER,'definition','Particle physics',P6,G6,'Question 6',parts)

# display strings: keep trailing zeros in numbers shown in questions
POST={
 '9702-26-22-Q1':[('At <i>t</i> = ${tP} s','At <i>t</i> = ${tP} s')],
}
TEXTCOLS=['mainText','partText','modelAnswer','explanation','tableRowLabels']
for r in ALL:
    for a,b in POST.get(r['id'],[]):
        for c in TEXTCOLS: r[c]=r[c].replace(a,b)

if __name__=='__main__':
    start=int(sys.argv[1]) if len(sys.argv)>1 else 223
    write_json(ALL,'new22.json',start=start)
    from collections import Counter
    print(len(ALL),'rows',Counter(r['id'] for r in ALL))
