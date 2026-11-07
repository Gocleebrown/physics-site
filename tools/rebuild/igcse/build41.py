##v1  IGCSE 0625/41 Extended Paper 4 (May/June 2026), rebuilt from the real QP + MS.  python3 igcse/build41.py <startRow>
import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))
from b31_common import *
PAPER='0625_m26_p41'; ID='0625-26-41M'
ALL=[]
def G(extra): d=dict(BASE); d.update(extra); return d
def cells(*rows):
    """rows: list of lists of accepted whole-answer strings -> tableCellKeywords string (1 column)"""
    return '['+','.join('[['+','.join('"exact:'+a+'"' for a in r)+']]' for r in rows)+']'
def answers(*rows): return '['+','.join('["'+r+'"]' for r in rows)+']'
SUP="(n)=>String(n).split('').map(c=>'⁰¹²³⁴⁵⁶⁷⁸⁹'[+c]).join('')"
SUB="(n)=>String(n).split('').map(c=>'₀₁₂₃₄₅₆₇₈₉'[+c]).join('')"
WORDS="['','one','two','three','four','five','six','seven','eight','nine','ten']"

# ================================================================ Q1 ball dropped
FIG1=r"""(h)=>{const W=480,H=300;let s=hd(W,H);
s+=ln(40,262,440,262)+'<rect x="40" y="262" width="400" height="10" fill="#ccc" stroke="#000"/>'+tx(240,292,'hard floor','middle');
s+='<circle cx="240" cy="62" r="16" fill="#e07a5f" stroke="#000" stroke-width="1.6"/>'+tx(268,66,'rubber ball');
s+=ln(130,62,130,262,' marker-start="url(#ah)" marker-end="url(#ah)"')+tx(138,170,h+' m');
s+='<circle cx="190" cy="52" r="10" fill="#fff" stroke="#000" stroke-width="1.6"/>'+ln(190,62,190,130)+ln(190,130,170,190)+ln(190,130,210,190)+ln(190,80,225,70)+tx(168,36,'student','end');
return s+'</svg>'+capf('Figure 1.1');}"""
Q1G=G({'fig1':FIG1,'m':'Math.floor(mp)/100','h':'Math.floor(hp)/10','W':'+(m*9.8).toFixed(2)','Ws':'sf(m*9.8,2)','E':'m*9.8*h','Er':'sf(E,2)','Ev':'+Er','v1':'sf(Math.sqrt(2*Ev/m),2)','v2':'sf(Math.sqrt(2*E/m),2)','f1':'fig1(h)'})
Q1P={'mp':[10,40.99],'hp':[8,20.99]}
parts=[]
parts.append(dict(pi=0,type='definition',K=lab('(a)')+'Figure 1.1 shows a student holding a rubber ball ${h} m above a hard floor. The mass of the ball is ${m} kg.${f1}State what is meant by the mass of the ball.',
 B=kwv('quantityofmatter','amountofmatter','amountofstuff','amountof','inertia','amountofparticles','howmuchmatter','measureofthematter','matterintheball','quantityofsubstance','amountofsubstance'),
 U='The mass is a measure of the quantity of matter in the ball.',V='Mass is the quantity of matter in an object; it is also a measure of its inertia.'))
parts.append(dict(pi=1,type='definition',K=lab('(b)(i)')+'The student releases the ball. The ball accelerates downwards due to a force W.<br><br>State the name of force W.',
 B=kwv('weight','gravitationalforce','gravitationalpull','gravity','forceduetotheearthsgravitationalfield','forceduetogravity','gravitationalattraction','pullofgravity','gravitationalfieldforce'),
 U='weight (gravitational force)',V='The downward force on the ball due to the Earth\'s gravitational field is its weight.'))
parts.append(dict(pi=2,type='calculation',K=lab('(b)(ii)')+'Calculate W. State the equation you use. (Take the acceleration of free fall to be 9.8 m/s<sup>2</sup>.)',
 A='${W}|${Ws}',tolerance='1',
 C1=kwv('w=mg','weight=mass×g','weight=massxg','w=m×g','w=mxg','mg','weight=mass×gravity','weight=mass×gravitationalfieldstrength','weight=mass×9.8','w=m×9.8','f=ma','f=m×a','f=mxa','m×g','mxg','mass×g','massxg','mass×gravity','massxgravity','mass×9.8','massx9.8','${m}×9.8','${m}x9.8','${m}*9.8','9.8×${m}','9.8x${m}'),
 U='W = mg = ${m} × 9.8 = ${W} N',V='Weight = mass × acceleration of free fall (gravitational field strength).'))
parts.append(dict(pi=3,type='calculation',K=lab('(b)(iii)')+'The ball falls ${h} m. Energy is transferred from the gravitational potential energy store of the ball.<br><br>Show that the energy transferred is ${Er} J.',
 B=kwv('ep=mgh','e=mgh','gpe=mgh','mgh','mg∆h','mgδh','mg∆h','wh','w×h','wxh','fd','f×d','fxd','energy=mgh','e=mg∆h','ep=mg∆h','gpe=mass×g×height','gpe=mass×gravity×height','mass×g×h','mass×g×height','weight×height','weight×h','force×distance','weightxheight','massxgxh','massxgxheight','ep=weight×height','pe=mgh','e=wh','ep=wh','pe=wh','gravitationalpotentialenergy=mgh'),
 B2=kwv('${m}×9.8×${h}','${m}x9.8x${h}','${m}*9.8*${h}','${m}×${h}×9.8','${m}x${h}x9.8','${m}*${h}*9.8','9.8×${m}×${h}','9.8x${m}x${h}','9.8*${m}*${h}','9.8×${h}×${m}','9.8x${h}x${m}','${h}×${m}×9.8','${h}x${m}x9.8','${h}×9.8×${m}','${h}x9.8x${m}','${W}×${h}','${W}x${h}','${W}*${h}','${h}×${W}','${h}x${W}','${m}×10×${h}','${m}x10x${h}'),
 U='Ep = mgΔh = ${m} × 9.8 × ${h} = ${Er} J',V='The gravitational potential energy lost when falling through a height h is mgh.'))
parts.append(dict(pi=4,type='calculation',K=lab('(b)(iv)')+'The energy in (b)(iii) is all transferred to the kinetic energy store of the ball.<br><br>Calculate the velocity of the ball.',
 A='${v1}|${v2}',tolerance='1',
 C2=kwv('√(2×${Er}÷${m})','√(2×${Er}/${m})','sqrt(2×${Er}/${m})','sqrt(2x${Er}/${m})','sqrt(2×${Er}÷${m})','sqrt(2*${Er}/${m})','√(2x${Er}/${m})','√(2*${Er}/${m})','(2×${Er}/${m})^0.5','(2x${Er}/${m})^0.5','√(2×${E}/${m})','sqrt(2×${E}/${m})','sqrt(2*${E}/${m})','√(2×9.8×${h})','sqrt(2×9.8×${h})','sqrt(2*9.8*${h})','2×${Er}/${m}','2x${Er}/${m}','2*${Er}/${m}','2×${Er}÷${m}','${Er}×2/${m}','${Er}x2/${m}'),
 C1=kwv('ek=½mv²','ek=½mv2','ek=1/2mv2','ek=1/2mv²','ke=½mv²','ke=1/2mv²','ke=½mv2','ke=1/2mv2','e=½mv²','e=1/2mv²','½mv²','½mv2','1/2mv2','1/2mv²','0.5mv2','0.5mv²','v=√(2ek/m)','v=sqrt(2ek/m)','v=√(2e/m)','v=sqrt(2e/m)','v²=2gh','v2=2gh','v^2=2gh','v=√(2gh)','v=sqrt(2gh)','v²=2ek/m','v2=2ek/m','v^2=2ek/m','kineticenergy=½mv²','kineticenergy=1/2mv2','ke=0.5mv2','ek=0.5mv2','ek=0.5mv²','ke=0.5mv²'),
 U='Ek = ½mv²; v = √(2Ek/m) = √(2 × ${Er} / ${m}) = ${v1} m/s',V='All the gravitational potential energy is transferred to kinetic energy, so ½mv² = ${Er} J.'))
parts.append(dict(pi=5,type='explain',K=lab('(c)')+'The ball hits the floor and moves upwards. The magnitude of the velocity is less than the value calculated in (b)(iv).<br><br>State one other way the velocity of the ball is different from the velocity calculated in (b)(iv).',
 B=kwv('direction','negative','opposite','upwards','up','reversed','reverse','isup','movesup'),
 U='The velocity is in a different (opposite) direction (upwards).',V='Velocity is a vector: after the bounce the ball moves upwards, opposite to its direction when it hit the floor.'))
ALL+=question(LV,ID+'-Q1',PAPER,'calculation','Forces,Energy and power,Motion',Q1P,Q1G,'Question 1',parts)

# ================================================================ Q2 sphere density
Q2G=G({'V':'Math.floor(Vp)','rho':'+(Math.floor(rp)/10).toFixed(1)','m':'Math.round(rho*V)','r1':'sf(m/V,2)','r1x':'sf(m/V,3)','r2':'sf(1000*m/V,2)','r2x':'sf(1000*m/V,3)','r2f':'String(Math.round(1000*m/V))'})
Q2P={'Vp':[18,50.99],'rp':[25,90.99]}
UNITG=lambda val,units: '|'.join(val+u for u in units)
GU=['g/cm3','g/cm³','gcm-3','gcm−3','gcm⁻³','g/cm^3','gpercm3','gpercm³']
KU=['kg/m3','kg/m³','kgm-3','kgm−3','kgm⁻³','kg/m^3','kgperm3','kgperm³']
parts=[]
parts.append(dict(pi=0,type='calculation',K=lab('(a)')+'A solid metal sphere has a volume of ${V} cm<sup>3</sup>. The mass of the metal sphere is ${m} g.<br><br>Calculate the density of the metal. State the unit.',
 A='|'.join([UNITG('${r1}',GU),UNITG('${r1x}',GU),UNITG('${r2}',KU),UNITG('${r2x}',KU),UNITG('${r2f}',KU)]),tolerance='1',
 C2=kwv('${m}÷${V}','${m}/${V}'),
 C1=kwv(*(GU+KU+['g/cm','gpercm','kgperm','g/ml','gml-1'])),
 U='density = m ÷ V = ${m} ÷ ${V} = ${r1} g/cm³ (= ${r2f} kg/m³)',V='Density is mass divided by volume. With mass in g and volume in cm³ the unit is g/cm³.'))
parts.append(dict(pi=1,type='explain',K=lab('(b)')+'Describe how a student determines the volume of the sphere using a measuring cylinder.',
 B=kwv('addwater','putwater','pourwater','fillthecylinder','waterinthecylinder','waterinthemeasuring','knownvolumeofwater','somewater','waterisadded','fillthemeasuring','fillitwithwater','filledwithwater','waterinthe','measurethevolumeofwater','readthevolume','recordthevolume','initialvolume','originalvolume','startingvolume','v1','eurekacan','overflow','displaced'),
 B2=kwv('afterthesphere','spherewasadded','spherehasbeenadded','spheredropped','dropthesphere','putthesphere','placethesphere','lowerthesphere','addthesphere','addsphere','submerge','immerse','spherein','spherehasbeenplaced','whenthesphere','newvolume','finalvolume','secondvolume','v2','risen','rises','rise','level'),
 B3=kwv('difference','subtract','change','v2−v1','v2-v1','v2–v1','minus','takeaway','takingaway','increase','risein','riseinwaterlevel','displacedwater','volumeofdisplaced','equalstothevolume','equaltothevolume','thevolumeofthesphere='),
 maxMarks='3',
 U='Add water to the measuring cylinder and read the volume; add the sphere and read the new volume; the volume of the sphere is the difference between the two volumes.',V='The sphere displaces its own volume of water, so the rise in the water level equals the volume of the sphere.'))
ALL+=question(LV,ID+'-Q2',PAPER,'calculation','Measurement,Density and pressure',Q2P,Q2G,'Question 2',parts)

# ================================================================ Q3 rope wave, laser
FIG3=r"""(n)=>{const W=520,H=200;let s=hd(W,H);let pts=[];for(let i=0;i<=200;i++){const x=70+i*2;const y=100-38*Math.sin(Math.PI*n*i/200);pts.push(x+','+y);}
s+='<polyline fill="none" stroke="#000" stroke-width="1.8" points="'+pts.join(' ')+'"/>';
s+='<rect x="472" y="30" width="14" height="140" fill="#ddd" stroke="#000" stroke-width="1.4"/>'+tx(479,190,'wall','middle');
s+='<circle cx="62" cy="100" r="9" fill="#fff" stroke="#000" stroke-width="1.6"/>'+tx(62,128,"student's hand",'middle');
s+=tx(20,22,'rope seen from above');
return s+'</svg>'+capf('Figure 3.1');}"""
Q3G=G({'fig3':FIG3,'ex':EX,'n':'2*Math.floor(np)+1','lam':'+(Math.floor(lp)/100).toFixed(2)','D':'+(n/2*lam).toFixed(2)','Ds':'String(D)','nw':'String(n/2)','wl':'Math.floor(wp)','fq':'3.0e8/(wl*1e-9)','fm':'+(fq/Math.pow(10,Math.floor(Math.log10(fq)))).toFixed(1)','fx':'Math.floor(Math.log10(fq))','fm2':'+(fq/Math.pow(10,Math.floor(Math.log10(fq)))).toFixed(2)','wlm':'+(wl/1000).toFixed(3)','f3':'fig3(n)'})
Q3P={'np':[0,2.99],'lp':[40,120.99],'wp':[400,700.99]}
UH=['hz','hertz']
parts=[]
parts.append(dict(pi=0,type='explain',K=lab('(a)(i)')+'A student produces a transverse wave with a rope. The wave travels along the rope. Figure 3.1 shows the wave as seen from above.${f3}Describe how the student produces the transverse wave.',
 B=kwv('vibrat','oscillat','wobble','shake','moveup','upanddown','flick','wiggle','moverope','movetherope','moveoneend','movesone','waggle'),
 B2=kwv('parallelto','inlinewith','sideways','sidetoside','lefttoright','leftandright','backandforth','perpendiculartothedirection','atrightanglestothedirection','atrightanglestothe','fromsidetoside'),
 maxMarks='2',
 U='Move (vibrate) one end of the rope parallel to the wall (from side to side, in the plane shown).',V='A transverse wave is made by oscillating the end of the rope at right angles to the direction in which the wave travels.'))
parts.append(dict(pi=1,type='calculation',K=lab('(a)(ii)')+'The wavelength of the wave is ${lam} m.<br><br>Determine the distance between the wall and the student\'s hand.',
 A='${D}|${Ds}',tolerance='1',
 C1=kwv('${nw}×${lam}','${nw}x${lam}','${nw}*${lam}','${lam}×${nw}','${lam}x${nw}','${lam}*${nw}','${n}/2×${lam}','${n}/2x${lam}','${n}×${lam}/2','${n}x${lam}/2','${n}÷2×${lam}','${n}halfwavelengths','${nw}wavelengths','${nw}timesthewavelength','${nw}timesthe wavelength'),
 U='distance = ${nw} × ${lam} = ${D} m',V='The wave in Figure 3.1 contains ${n} half-wavelengths, which is ${nw} wavelengths.'))
parts.append(dict(pi=2,type='definition',K=lab('(b)(i)')+'A laser produces a beam of red light with a wavelength of ${wl} nm in air.<br><br>State the approximate speed of light in air.',
 B=kwv('3.0e8','3e8','3.0×10^8','3×10^8','3.0x10^8','3x10^8','3.0×10⁸','3×10⁸','300000000','3.00×10^8','3.00e8','2.99e8','2.998e8','2.99792458e8','299792458','300,000,000'),
 U='3.0 × 10⁸ m/s',V='Light travels through air at approximately 3.0 × 10⁸ m/s.'))
parts.append(dict(pi=3,type='calculation',K=lab('(b)(ii)')+'Calculate the frequency of the red light. State the unit.',
 A='[["${fm}e${fx}","${fm}×10^${fx}","${fm}x10^${fx}","${fm}*10^${fx}","${fm2}e${fx}","${fm2}×10^${fx}","${fm2}x10^${fx}","${fm2}*10^${fx}"],["hz","hertz"]]',tolerance='2',
 C2=kwv('3.0×10^8÷${wl}×10^-9','3.0×10^8/${wl}×10^-9','3e8/${wl}e-9','3.0e8/${wl}e-9','3.0e8÷${wl}e-9','3×10^8/(${wl}×10^-9)','3.0×10^8/(${wl}×10^-9)','3x10^8/(${wl}x10^-9)','3.0x10^8/(${wl}x10^-9)','3×10^8÷(${wl}×10^-9)','3.0×10^8÷(${wl}×10^-9)','3e8/(${wl}e-9)','3.0e8/(${wl}e-9)','3e8÷(${wl}e-9)','3×10^8/${wl}×10^-9','3x10^8/${wl}x10^-9','3e8/${wl}x10^-9','3.0e8/${wlm}e-6','3e8/${wlm}e-6','3.0×10^8/${wlm}×10^-6','3e8/${wlm}×10^-6','v=fλ','f=v/λ','f=v÷λ','f=speed/wavelength','f=speed÷wavelength','v=f×λ','v=fxλ'),
 C1=kwv('hz','hertz','khz','mhz','ghz','thz','${wl}×10^-9','${wl}x10^-9','${wl}e-9','${wlm}×10^-6','${wlm}e-6','${wl}×10-9'),
 U='f = v ÷ λ = 3.0 × 10⁸ ÷ (${wl} × 10⁻⁹) = ${fm2} × 10^${fx} Hz',V='Use wave speed = frequency × wavelength with the wavelength converted from nm to m.'))
parts.append(dict(pi=4,type='definition',K=lab('(b)(iii)')+'Complete the sentence.<br><br>Light of a single frequency is described as ________ light.',
 B=kwv('monochromatic','monochromic'),
 U='monochromatic',V='Light of a single frequency (and so a single colour) is monochromatic.'))
ALL+=question(LV,ID+'-Q3',PAPER,'calculation','Waves,Light',Q3P,Q3G,'Question 3',parts)

# ================================================================ Q4 plotting compasses, induction
FIG4=r"""(nr)=>{const W=520,H=300;let s=hd(W,H);const L=['N','S'][nr],R=['S','N'][nr];
s+='<rect x="190" y="110" width="140" height="44" fill="#f4f4f4" stroke="#000" stroke-width="1.8"/>'+ln(260,110,260,154)+tx(225,138,L,'middle')+tx(295,138,R,'middle')+tx(260,100,'bar magnet','middle');
const c=(x,y,k)=>'<circle cx="'+x+'" cy="'+y+'" r="20" fill="#fff" stroke="#000" stroke-width="1.6"/>'+tx(x+30,y+5,k);
s+=c(120,132,'1')+c(260,206,'2')+c(260,262,'3');
return s+'</svg>'+capf('Figure 4.1');}"""
Q4G=G({'fig4':FIG4,'nr':'Math.floor(nrp)','a1':"['left','right'][nr]",'a2':"['right','left'][nr]",'f4':'fig4(nr)'})
Q4P={'nrp':[0,1.99]}
def lr(a): return ['${'+a+'}','to the ${'+a+'}','towards the ${'+a+'}','${'+a+'}wards','pointing ${'+a+'}','points ${'+a+'}','pointing to the ${'+a+'}','points to the ${'+a+'}']
parts=[]
parts.append(dict(pi=0,type='definition',K=lab('(a)')+'Three plotting compasses are placed in the magnetic field of a bar magnet. The circles in Figure 4.1 show the positions of the plotting compasses.${f4}State the effect that a magnetic field has on a magnetic pole.',
 B=kwv('force','attract','repel','pushes','pulls','exertsaforce','forceonit','actsonit'),
 U='A magnetic pole experiences a force.',V='A magnetic field is a region where a magnetic pole experiences a force.'))
parts.append(dict(pi=1,type='definition',answerType='table',
 K=lab('(b)')+'The needle of a plotting compass points in the direction of the magnetic field. For each of the plotting compasses 1, 2 and 3 in Figure 4.1, state whether the needle points to the left or to the right of the page.',
 tableRowLabels='["Compass 1","Compass 2","Compass 3"]',tableColLabels='["Direction of needle"]',
 tableCellKeywords='[[['+','.join('"exact:'+x+'"' for x in lr('a1'))+']],[['+','.join('"exact:'+x+'"' for x in lr('a2'))+']],[['+','.join('"exact:'+x+'"' for x in lr('a2'))+']]]',
 tableCellAnswers='[["${a1}"],["${a2}"],["${a2}"]]',maxMarks='2',
 U='1: ${a1}; 2: ${a2}; 3: ${a2}',V='Outside the magnet the field lines run from the north pole to the south pole, and a compass needle points along them.'))
parts.append(dict(pi=2,type='definition',K=lab('(c)')+'State how the magnetic field at circle 3 is different from the magnetic field at circle 2.',
 B=kwv('weaker','smaller','lessstrong','notasstrong','lower','decreased','reduced','fainter','weakeratcircle3','weakerat3','strongeratcircle2','strongerat2','2isstronger'),
 U='The field at circle 3 is weaker.',V='The field is strongest close to the magnet and gets weaker further away from it.'))
parts.append(dict(pi=3,type='definition',answerType='table',
 K=lab('(d)')+'The bar magnet is moved into a coil of wire. As the magnet moves into the coil, the coil experiences a changing magnetic field. Complete the sentences to explain what happens.<br><br>An e.m.f. is <b>(1)</b> in the coil. This causes a <b>(2)</b> in the coil which produces a magnetic field around the coil. The magnetic field opposes <b>(3)</b>.<br><br>Type the missing words (1), (2) and (3) in Table 4.1.',
 tableRowLabels='["(1)","(2)","(3)"]',tableColLabels='["Table 4.1: missing words"]',
 tableCellKeywords=cells(['induced','generated','produced','created','set up'],['current','induced current','electric current'],['the change causing it','the change','the movement of the magnet','the movement of the bar magnet','the magnet moving','the motion of the magnet','the magnet\'s movement','the magnetic field of the magnet','the magnetic field of the bar magnet','the magnets field','the magnet field','the magnet','the induced e.m.f.','the induced current','change in magnetic field','the change in the magnetic field','the change in flux','change in flux','the changing magnetic field','the changing field','the change in field','the motion of the bar magnet','magnet movement']),
 tableCellAnswers=answers('induced','current','the change causing it'),
 U='(1) induced; (2) current; (3) the change causing it (the movement of the magnet)',V='By Lenz\'s law the induced current produces a field that opposes the change (the movement of the magnet) that causes it.'))
ALL+=question(LV,ID+'-Q4',PAPER,'definition','Magnetism',Q4P,Q4G,'Question 4',parts)

# ================================================================ Q5 dust particles, gas pressure
Q5G=G({'K':'Math.floor(Kp)','C':'K-273','Cx':'String(+(K-273.15).toFixed(2))','Cs':'String(+(K-273.15).toFixed(1))'})
Q5P={'Kp':[281,340.99]}
parts=[]
parts.append(dict(pi=0,type='definition',answerType='table',
 K=lab('(a)')+'A box contains small dust particles suspended in air. The dust particles move in a random motion.<br><br>Complete the sentences to explain the motion of the dust particles.<br><br>Air molecules inside the box are very small and move freely. The air molecules also move <b>(1)</b> and <b>(2)</b>. Air molecules hit dust particles causing the dust particles to <b>(3)</b>.<br><br>Type the missing words in Table 5.1.',
 tableRowLabels='["(1)","(2)","(3)"]',tableColLabels='["Table 5.1: missing words"]',
 tableCellKeywords=cells(['fast','quickly','very fast','very quickly','rapidly','randomly','random','in all directions','in random directions','in straight lines','zig zag','zig-zag','in any direction','in different directions'],['fast','quickly','very fast','very quickly','rapidly','randomly','random','in all directions','in random directions','in straight lines','zig zag','zig-zag','in any direction','in different directions'],['change direction','move in a different direction','change momentum','move randomly','changes direction','change their direction','move in different directions','move differently','change velocity','change the direction','alter direction','change speed','change course','change the momentum','move in a random direction','move in random directions']),
 tableCellAnswers=answers('fast','randomly','change direction'),maxMarks='3',
 U='(1) very fast (quickly); (2) randomly (in all directions); (3) change direction (momentum)',V='Fast, random air molecules collide with a dust particle from different directions; each collision changes its direction and momentum.'))
parts.append(dict(pi=1,type='explain',K=lab('(b)')+'The temperature of the air inside the box increases.<br><br>State and explain, in terms of particles, the effect on the air pressure inside the box.',
 A=kwv('pressureincreases','pressureincrease','pressureincreased','pressureisincreased','pressurerises','pressureisgreater','pressuregoesup','increasedpressure','higherpressure','pressuregetshigher','greaterpressure','pressureincreasesasthe','increase','rise','goesup','biggerpressure','largerpressure','pressureishigher','pressurewillincrease','pressurewouldincrease','pressureisincreasing','moreairpressure','higherairpressure'),
 B=kwv('fasterparticles','particlesmovefaster','particlesmovequicker','particlesspeedup','ke','kineticenergy','particleshavemoreenergy','particleshavegreaterspeed','moreenergy','faster','greaterspeed','higherspeed','quicker','morekineticenergy','speedincreases','speedofparticlesincreases','moveatagreaterspeed','highervelocity','fastermolecules','moleculesmovefaster'),
 B2=kwv('morefrequent','morecollisions','morehits','morefrequently','collidemoreoften','hitmoreoften','collisionsincrease','increasedcollisions','collidewithmoreforce','hitswithmoreforce','moreforce','greaterforce','biggerforce','largerforce','largerchangeinmomentum','biggerchangeinmomentum','greaterchangeinmomentum','changeinmomentumislarger','changeinmomentum','harder','morerapidcollisions','morecollisionspersecond','higherfrequencyofcollisions','collidemoreoftenwith','collisionsarefaster','collisionsmore','collisionsofparticleswithwallsmore','impactharder','hitthewallsmoreoften','hitthewallsharder','hardercollisions','morefrequentcollisions','forceofcollisions'),
 U='The pressure increases. The air particles move faster; they collide more often with the box and with more force (larger change in momentum).',V='Higher temperature means a greater average kinetic energy, so particles hit the walls more frequently and with more force, which increases the pressure.'))
parts.append(dict(pi=2,type='calculation',K=lab('(c)')+'The air temperature inside the box is ${K} K.<br><br>Calculate the air temperature in °C.',
 A='${C}|${Cx}|${Cs}',tolerance='0',
 C1=kwv('${K}-273','${K}−273','${K}–273','${K}-273.15','${K}−273.15','k-273','k−273','kelvin-273','kelvin−273','subtract273','minus273','−273','-273'),
 U='temperature = ${K} − 273 = ${C} °C',V='To convert from kelvin to degrees Celsius subtract 273.'))
ALL+=question(LV,ID+'-Q5',PAPER,'explain','Thermal physics',Q5P,Q5G,'Question 5',parts)

# ================================================================ Q6 electric field, charged sphere
FIG6=r"""(att)=>{const W=520,H=300;let s=hd(W,H);const dx=att?-40:40;
s+='<rect x="320" y="22" width="80" height="8" fill="#ddd" stroke="#000"/>'+ln(360,30,360+dx,200)+'<circle cx="'+(360+dx)+'" cy="214" r="16" fill="#cfe0f0" stroke="#000" stroke-width="1.6"/>';
s+=tx(360+dx+22,238,'charged metal sphere')+tx(410,26,'insulating thread');
s+='<rect x="60" y="205" width="170" height="18" fill="#cfcfcf" stroke="#000" stroke-width="1.4"/><rect x="20" y="200" width="40" height="28" fill="#fff" stroke="#000" stroke-width="1.4"/>';
s+=tx(145,198,'metal rod','middle')+tx(20,250,'insulating handle');
return s+'</svg>'+capf('Figure 6.1');}"""
Q6G=G({'fig6':FIG6,'rk':'Math.floor(rkp)','rs':"['negative','positive'][rk]",'ss':"['positive','negative'][rk]",'ef':"['from the rod to the sphere','from the sphere to the rod'][rk]",'ef2':"['rodtothesphere','spheretotherod'][rk]",'f6':'fig6(1)'})
Q6P={'rkp':[0,1.99]}
parts=[]
parts.append(dict(pi=0,type='definition',K=lab('(a)')+'A metal sphere is suspended vertically by an insulating thread. The sphere is charged. The charge causes an electric field around the sphere.<br><br>Complete the definition of an electric field: An electric field is a region where <b>(1)</b> experiences <b>(2)</b>.<br><br>Type the missing words (1) and (2) in Table 6.1.',
 answerType='table',tableRowLabels='["(1)","(2)"]',tableColLabels='["Table 6.1: missing words"]',
 tableCellKeywords=cells(['charge','a charge','charged particle','a charged particle','an electric charge','electric charge','charges','a charged object','charged object','a charged body','a charged sphere','an electron','a proton','an ion','a positive charge','a negative charge','positive charge','negative charge','a positive or negative charge'],['a force','force','an electrostatic force','electrostatic force','an electric force','electric force','attraction','repulsion','attraction or repulsion','a push or pull','a force on it']),
 tableCellAnswers=answers('a charge','a force'),
 U='(1) a charge (charged particle); (2) a force (electrostatic force)',V='An electric field is a region where an electric charge experiences an (electrostatic) force.'))
parts.append(dict(pi=1,type='explain',K=lab('(b)(i)')+'A ${rs}ly charged metal rod is brought close to the sphere. Figure 6.1 shows the charged rod and the charged sphere. The sphere is attracted towards the rod.${f6}State and explain whether the charge on the metal sphere is positive or negative.',
 B=andor(['${ss}'],['oppositecharges','unlikecharges','oppositecharge','unlikecharge','attract','opposite','unlike','oppositelycharged','attractedtotherod','attractedtothe']),
 U='The sphere is ${ss}, because opposite charges attract and the sphere is attracted to the rod.',V='Unlike (opposite) charges attract. The rod is ${rs}, so the sphere must carry the ${ss} charge.'))
parts.append(dict(pi=2,type='explain',K=lab('(b)(ii)')+'The metal sphere touches the rod.<br><br>State what happens to the sphere. Explain this in terms of the movement of particles.',
 B=kwv('swingsaway','movesaway','movesbackto','movesback','swingsback','isrepelled','repelled','repel','discharg','neutral','losesitscharge','losesallitscharge','nolongercharged','nolongerattracted','nolongerisattracted','awayfromtherod','losescharge','becomesneutral','becomesuncharged','uncharged','chargeisremoved'),
 B2=kwv('electronsmove','electronsmoveonto','electronsmovefrom','electronstransfer','electronsflow','electronsareremoved','electronsareadded','electronsmovefromthe','electronsleave','electronsgo','negativechargesmove','negativeparticlesmove','negativechargestransfer','electrons are transferred','electronsaretransferred','transferofelectrons','electronstravel','electronsgoonto','electronsgointo','electronsgoto','electronsjump','electronscross','electronsarepassed','electronspass','movementofelectrons','electronmoves','electron','negativecharges'),
 B3=andor(['electron','negativecharge'],['${ef2}','${ef}','from the ${ef2}']),
 U='The sphere is discharged (becomes neutral) and swings away from the rod: electrons move ${ef}.',V='Electrons are the charges that move. Charge flows ${ef} until the sphere is neutral.'))
ALL+=question(LV,ID+'-Q6',PAPER,'explain','Electricity',Q6P,Q6G,'Question 6',parts)

# ================================================================ Q7 battery, motor, resistor
FIG7=r"""(e)=>{const W=520,H=250;let s=hd(W,H);
s+=ln(60,40,200,40)+ln(300,40,460,40)+ln(460,40,460,90)+ln(460,150,460,200)+ln(60,200,200,200)+ln(300,200,460,200)+ln(60,40,60,100)+ln(60,150,60,200);
s+=ln(48,100,72,100)+ln(54,112,66,112)+ln(48,126,72,126)+ln(54,138,66,138)+ln(48,150,72,150,'')+tx(80,120,e+' V');
s+='<circle cx="250" cy="40" r="26" fill="#fff" stroke="#000" stroke-width="1.6"/>'+tx(250,46,'M','middle')+ln(200,40,224,40)+ln(276,40,300,40);
s+='<rect x="436" y="90" width="48" height="60" fill="#fff" stroke="#000" stroke-width="1.6"/>'+tx(430,125,'fixed resistor','end');
s+=ln(200,200,235,170)+ln(235,200,300,200)+'<circle cx="200" cy="200" r="3"/><circle cx="235" cy="200" r="3"/>'+tx(240,226,'switch','middle');
return s+'</svg>'+capf('Figure 7.1');}"""
Q7G=G({'fig7':FIG7,'E':'Math.floor(Ep)/10','Q':'100*Math.floor(Qp)','t':'Math.floor(tp)/10','R':'Math.floor(Rp)/10','W':'Math.round(E*Q)','Wk':'+(E*Q/1000).toFixed(1)','Ws':'sf(E*Q,2)','ts':'Math.round(t*3600)','I':'Q/(t*3600)','Is':'+I.toFixed(2)','Rm':'Math.round(R*10)/10','V1':'sf(E-(+I.toFixed(2))*R,2)','V2':'sf(E-I*R,2)','V1x':'+(E-(+I.toFixed(2))*R).toFixed(2)','VR1':'sf((+I.toFixed(2))*R,3)','VR2':'sf(I*R,3)','V1r':'String(Math.round((E-(+I.toFixed(2))*R)*10+1e-6)/10)','V2x':'+(E-I*R).toFixed(2)','f7':'fig7(E)'})
Q7P={'Ep':[60,120.99],'Qp':[15,50.99],'tp':[10,30.99],'Rp':[10,40.99]}
parts=[]
parts.append(dict(pi=0,type='definition',K=lab('(a)')+'Figure 7.1 shows a battery of e.m.f. ${E} V connected in series with a motor, a fixed resistor and a switch.${f7}Complete the equation that defines e.m.f. E.<br><br>E = ________ ÷ ________',
 B=andor(['work','energy'],['charge','coulomb']),
 U='E = work done (energy transferred) ÷ charge',V='The e.m.f. of a source is the work done (energy transferred) per unit charge that passes through it.'))
parts.append(dict(pi=1,type='calculation',K=lab('(b)(i)')+'The switch is closed. The battery moves ${Q} C around the circuit in ${t} h.<br><br>Calculate the work done by the battery.',
 A='${W}|${Ws}|${Wk}kj|${Wk}kJ',tolerance='1',
 C1=kwv('${E}×${Q}','${E}x${Q}','${E}*${Q}','${Q}×${E}','${Q}x${Q}','${Q}*${E}','w=eq','w=qe','e=w/q','w=e×q','w=exq','w=q×e','w=qxe','w=iqt','w=ivt','eq','e×q'),
 U='W = EQ = ${E} × ${Q} = ${W} J',V='From E = W ÷ Q, the work done is W = EQ.'))
parts.append(dict(pi=2,type='definition',K=lab('(b)(ii)')+'Complete the equation that defines electric current I.<br><br>I = ________ ÷ ________',
 B=andor(['charge','q','coulomb'],['time','t','seconds','second']),
 U='I = charge ÷ time',V='Electric current is the charge passing a point per unit time.'))
parts.append(dict(pi=3,type='calculation',K=lab('(b)(iii)')+'Show that the current in the motor is ${Is} A.',
 B=kwv('${Q}/(${t}×60×60)','${Q}/(${t}x60x60)','${Q}/(${t}*60*60)','${Q}÷(${t}×60×60)','${Q}÷(${t}x60x60)','${Q}/(${t}×3600)','${Q}/(${t}x3600)','${Q}/(${t}*3600)','${Q}÷(${t}×3600)','${Q}÷(${t}x3600)','${Q}/${ts}','${Q}÷${ts}','${Q}/(${t}×60×60)','${Q}/${t}×60×60','${Q}/${t}x60x60','${Q}/${t}/3600','${Q}/${t}÷3600','${Q}÷${t}÷3600','${Q}÷${t}÷60÷60','${Q}/${t}/60/60','${Q}÷(${ts})','${Q}/(${ts})','${Q}÷(${t}×60²)','${Q}/(${t}×60^2)','${Q}/(${t}x60^2)'),
 U='I = Q ÷ t = ${Q} ÷ (${t} × 60 × 60) = ${Is} A',V='Convert the time from hours to seconds (× 3600), then use I = Q ÷ t.'))
parts.append(dict(pi=4,type='calculation',K=lab('(b)(iv)')+'The resistance of the fixed resistor is ${R} Ω.<br><br>Calculate the p.d. across the motor.',
 A='${V1}|${V2}|${V1x}|${V2x}|${V1r}',tolerance='2',
 C2=kwv('${E}-${Is}×${R}','${E}−${Is}×${R}','${E}–${Is}×${R}','${E}-${Is}x${R}','${E}−${Is}x${R}','${E}-${Is}*${R}','${E}-${R}×${Is}','${E}−${R}×${Is}','${E}-${R}x${Is}','${E}-${Is}×${R}','${E}-${I}×${R}','${E}−${I}×${R}','${E}-${I}x${R}','${E}-${I}*${R}','${E}-(${Is}×${R})','${E}−(${Is}×${R})','${E}-(${Is}x${R})','${E}-(${Is}*${R})','${E}-(${R}×${Is})','${E}−(${R}×${Is})'),
 C1=kwv('${VR1}','${VR2}','v=ir','v=i×r','v=ixr','r=v/i','r=v÷i','e−v','e-v','${E}−','${E}-','emf−pd','emf-pd','totalresistance=','e/i','${E}/${Is}','${E}÷${Is}','${Is}×${R}','${Is}x${R}','${R}×${Is}','${R}x${Is}','${Is}*${R}','${R}*${Is}','p.d.acrossresistor','pdacrossresistor','pdacrossthefixedresistor'),
 U='V across resistor = IR = ${Is} × ${R} = ${V2x}; p.d. across motor = ${E} − ${V2x} = ${V2} V',V='The p.d.s across the components in series add up to the e.m.f. of the battery, so the motor p.d. = E − IR.'))
ALL+=question(LV,ID+'-Q7',PAPER,'calculation','Electricity',Q7P,Q7G,'Question 7',parts)

# ================================================================ Q8 lawnmower, mains
Q8G=G({'P':'50*Math.floor(Pp)','Vm':'230','I':'+(P/Vm).toFixed(1)','Ix':'String(+(P/Vm).toFixed(2))','Ix1':'sf(P/Vm,2)','Ix3':'sf(P/Vm,3)','kw':'P/1000','t':'+(Math.floor(tp)/100).toFixed(2)','E':'+(kw*t).toFixed(3)','Es':'sf(kw*t,2)','Es3':'sf(kw*t,3)','Ej':'Math.round(P*t)','c':'+(Math.floor(cp)/100).toFixed(2)','cost':'+(kw*t*c).toFixed(2)','cost1':'+(+Es*c).toFixed(2)','cost2':'+(+Es3*c).toFixed(2)','costs':'sf(kw*t*c,2)'})
Q8P={'Pp':[16,40.99],'tp':[50,150.99],'cp':[20,50.99]}
parts=[]
parts.append(dict(pi=0,type='calculation',K=lab('(a)(i)')+'A person cuts grass with a lawnmower. The lawnmower is connected to the mains supply of 230 V. The power of the lawnmower is ${P} W.<br><br>Calculate the current in the lawnmower.',
 A='${I}|${Ix}|${Ix1}|${Ix3}',tolerance='1',
 C1=kwv('${P}÷${Vm}','${P}/${Vm}','p=iv','p=vi','i=p/v','i=p÷v','p=i×v','p=ixv','power=current×voltage','power=currentxvoltage','p/v','p÷v','current=power/voltage','current=power÷voltage','i=power/voltage'),
 U='I = P ÷ V = ${P} ÷ ${Vm} = ${I} A',V='Electrical power P = IV, so I = P ÷ V.'))
parts.append(dict(pi=1,type='explain',K=lab('(a)(ii)')+'The lawnmower circuit contains a trip switch.<br><br>Explain the purpose of the trip switch.',
 B=kwv('protect','safe','stopsthemanbeingelectrocuted','preventsdamage','safety','preventselectricshock','preventsfire','stopsdamage','protectstheuser','protectstheperson','protectstheman','protectsthelawnmower','protectsthemotor','protectsthecircuit','protectsthewiring','protectsthecable','protectsagainst'),
 B2=kwv('breaksthecircuit','stopsthecurrent','switchesoff','switchoff','turnsoff','turnoff','cutsoff','cutsthecurrent','cutthecurrent','stopsthecurrentflowing','breaksthecurrent','openthecircuit','opensthecircuit','disconnects','disconnect','tripsthecircuit','tripsandbreaks','current stops','currentstops','nocurrent','stopcurrent','breakthecircuit','stopstheflow','cutsoffthesupply','isolates','switchesthecircuitoff','turnsthecircuitoff'),
 B3=kwv('toohigh','toomuchcurrent','toolarge','toobig','highcurrent','largecurrent','excesscurrent','surge','overload','currentistoohigh','whenthecurrentistoohigh','currentexceeds','toomuch','currentincreases','currentgetstoohigh','currentrisesabove','greaterthan','toogreat','faulty','shortcircuit','fault'),
 maxMarks='2',
 U='Any two from: it protects a named part (e.g. the user); it breaks the circuit / stops the current; it trips when the current is too high.',V='A trip switch automatically opens when the current is too large, protecting the user and the equipment.'))
parts.append(dict(pi=2,type='definition',K=lab('(a)(iii)')+'State one advantage of using a trip switch instead of a fuse in the lawnmower circuit.',
 B=kwv('faster','quicker','moresensitive','sensitive','canbereset','reset','reused','reuse','canbeusedagain','canbeturnedbackon','doesnotneedreplacing','donotneedreplacing','doesntneedreplacing','swifter','respondsfaster','reactsfaster','tripsfaster','morereliable','notneedtobereplaced','nothavetobereplaced','noneedtoreplace','neednotbereplaced','quickertoreact','quickertorespond','quickertotrip','cuts offfaster','cutsofffaster','switchesofffaster','stopsthecurrentfaster'),
 U='A trip switch responds faster / is more sensitive / can be reset.',V='A fuse must be replaced after it blows, and it reacts more slowly than a trip switch.'))
parts.append(dict(pi=3,type='calculation',K=lab('(b)(i)')+'The person uses the lawnmower for ${t} h. One kilowatt-hour of energy costs $${c}.<br><br>Calculate the energy transferred to the lawnmower in ${t} h. Give your answer in kW h.',
 A='${E}|${Es}|${Es3}',tolerance='1',
 C2=kwv('${P}×${t}','${P}x${t}','${P}*${t}','${t}×${P}','${t}x${P}','${t}*${P}','${kw}×${t}','${kw}x${t}','${kw}*${t}','${t}×${kw}','${t}x${kw}','${t}*${kw}','${Ej}','${P}×${t}÷1000','${P}×${t}/1000','${P}x${t}/1000','${P}/1000×${t}','${P}÷1000×${t}','${Ix}×230×${t}','${I}×230×${t}','${I}x230x${t}'),
 C1=kwv('${kw}','${P}÷1000','${P}/1000','e=pt','e=p×t','e=pxt','e=ivt','energy=power×time','energy=powerxtime','power×time','powerxtime','pt','p×t','pxt','e=i×v×t','e=ixvxt','ivt','i×v×t','ixvxt'),
 U='E = Pt = ${kw} kW × ${t} h = ${E} kW h',V='Convert the power to kW (${P} W = ${kw} kW), then multiply by the time in hours.'))
parts.append(dict(pi=4,type='calculation',K=lab('(b)(ii)')+'Calculate the cost of the energy calculated in (b)(i).',
 A='${cost}|${cost1}|${cost2}|${costs}',tolerance='4',
 U='cost = ${E} × ${c} = $${cost}',V='Cost = energy in kW h × cost per kW h.'))
ALL+=question(LV,ID+'-Q8',PAPER,'calculation','Electricity,Energy and power',Q8P,Q8G,'Question 8',parts)

# ================================================================ Q9 prism, spectrum, redshift
FIG9=r"""(fl)=>{const W=560,H=300;let s=hd(W,H);
s+='<polygon points="220,220 300,70 380,220" fill="#e8f0f7" stroke="#000" stroke-width="1.6"/>';
s+=ln(40,180,262,136)+tx(40,168,'white light');
const ys=[80,120,160,200];const ord=fl?[3,2,1,0]:[0,1,2,3];
for(let k=0;k<4;k++){s+=ln(336,140,340+0,140)+'';}
s+=ln(262,136,338,138);
for(let k=0;k<4;k++){const y=ys[k];s+=ln(338,138,456,y-0)+'<circle cx="456" cy="'+y+'" r="0"/>';}
s+=tx(444,60,'1','end');
return s+'</svg>'+capf('Figure 9.1');}"""
# simpler, clearer figure: rays leave the prism fan-shaped and are numbered 1-4 at the right edge
FIG9=r"""(fl)=>{const W=560,H=300;let s=hd(W,H);
s+='<polygon points="200,230 290,70 380,230" fill="#e8f0f7" stroke="#000" stroke-width="1.6"/>';
s+=ln(40,190,258,150)+tx(40,178,'white light');
s+=ln(258,150,330,150);
const ys=[100,140,180,220];
for(let k=0;k<4;k++){const y=ys[k];s+=ln(330,150,360,150+(k-1.5)*5)+ln(360,150+(k-1.5)*5,520,y);}
for(let k=0;k<4;k++){const n=fl?4-k:k+1;s+=tx(532,ys[k]+5,String(n));}
s+=tx(290,255,'prism','middle');
return s+'</svg>'+capf('Figure 9.1');}"""
Q9G=G({'fig9':FIG9,'fl':'Math.floor(flp)','gn':'fl?2:3','rn':'fl?4:1','inn':'fl?1:4','f9':'fig9(fl)','dia':'1e5'})
Q9P={'flp':[0,1.99]}
parts=[]
parts.append(dict(pi=0,type='definition',K=lab('(a)(i)')+'A beam of white light is dispersed in a glass prism. Figure 9.1 shows the paths taken by green, indigo, red and yellow light, numbered 1 to 4.${f9}State which of the rays, 1, 2, 3 or 4, is the green ray.',
 B='${gn}',
 U='ray ${gn}',V='Red light is refracted least and indigo (violet) most, so in order the rays are red, yellow, green, indigo.'))
parts.append(dict(pi=1,type='definition',K=lab('(a)(i)')+'State which of the rays, 1, 2, 3 or 4, is the red ray.',
 B='${rn}',
 U='ray ${rn}',V='Red light is refracted least by the prism.'))
parts.append(dict(pi=2,type='explain',K=lab('(a)(ii)')+'The light leaves the prism. Describe the paths of ray ${rn} and ray ${inn} after the light leaves the prism and enters the air.',
 B=kwv('awayfromthenormal','bendsaway','refractsaway','refractedaway','bentaway','awayfromnormal','awayfrom the normal','bendsawayfromthenormal','awaytothenormal','refract','bend'),
 B2=kwv('diverge','spreadout','spreadapart','furtherapart','separate','notparallel','getfartherapart','getfurtherapart','movefurtherapart','movefartherapart','fanout','fan','spread','widen','wider','greaterseparation','increaseseparation','moreseparated','apart','farther'),
 U='Both rays refract away from the normal as they enter the air, and the two rays diverge (spread apart).',V='When light passes from glass into air it bends away from the normal. Indigo is bent more than red, so the rays diverge.'))
parts.append(dict(pi=3,type='definition',K=lab('(b)(i)')+'The Sun emits most of its energy in three regions of the electromagnetic spectrum. Visible light is one region.<br><br>State the other two regions.',
 B=andor(['infrared','infra-red','infra red','ir radiation'],['ultraviolet','ultra-violet','ultra violet','uv']),
 U='infrared and ultraviolet',V='The Sun emits mostly infrared, visible and ultraviolet radiation.'))
parts.append(dict(pi=4,type='definition',K=lab('(b)(ii)')+'The Sun is a star in the Milky Way galaxy.<br><br>State the approximate diameter of the Milky Way. Give your answer in light-years.',
 A='100000|1e5|1×10^5|1x10^5|1×10⁵|100,000|100 000',tolerance='10',
 U='about 100 000 light-years',V='The Milky Way has a diameter of roughly 100 000 light-years.'))
parts.append(dict(pi=5,type='definition',K=lab('(c)(i)')+'Scientists on the Earth observe light emitted by a distant galaxy. The observed light is redshifted.<br><br>State what is meant by redshifted.',
 B=kwv('longerwavelength','increaseinwavelength','wavelengthincreases','wavelengthisincreased','wavelengthincreased','lowerfrequency','decreaseinfrequency','frequencydecreases','wavelengthstretched','stretchedwavelength','longerwavelengths','increasedwavelength','shiftedtowardsthered','shiftedtothered','towardstheredend','towardtheredend','frequencyislower','frequencyisreduced','wavelengthisgreater','wavelengthislonger','greaterwavelength','biggerwavelength','largerwavelength','wavelengthgetslonger','wavelengthgetslarger'),
 U='The observed wavelength is longer (frequency lower) than the wavelength emitted.',V='Redshift is an increase in the wavelength (decrease in frequency) of the light, shifting it towards the red end of the spectrum.'))
parts.append(dict(pi=6,type='explain',K=lab('(c)(ii)')+'Explain how redshift supports the Big Bang Theory.',
 B=kwv('galaxiesarereceding','galaxiesarerecedingfromus','galaxiesaremovingaway','galaxiesmoveaway','galaxiesarereceding','receding','recede','theuniverseisexpanding','universeisexpanding','universeexpands','expandinguniverse','expansion','moving away','movingaway','movesaway','moveaway','movingapart','moveapart','awayfromus','awayfromeachother','awayfromearth','gettingfurtherapart'),
 B2=kwv('moredistant','furtheraway','fartheraway','faster','morefaster','greaterredshift','moreredshifted','greaterspeed','higherspeed','recedefaster','recedingfaster','movingfaster','movefaster','larger redshift','largerredshift','biggerredshift','distantgalaxiesmove','distantgalaxiesrecede','distantgalaxiesarereceding'),
 B3=kwv('closertogether','werecloser','wasasmall','smalldense','singlepoint','onepoint','smallpoint','startedfromapoint','begansmall','beganassmall','thebigbang','smallerregion','smalldenseregion','smallandhot','denseregion','pointofdensity','beganfromapoint','beganatapoint','veryclosetogether','allinoneplace','alltogether'),
 maxMarks='2',
 U='Any two from: galaxies are receding (the Universe is expanding); more distant galaxies are receding faster; galaxies were closer together, so the Universe began in a small, dense region.',V='Redshift shows the Universe is expanding. Running this backwards, everything was once much closer together, as the Big Bang Theory states.'))
ALL+=question(LV,ID+'-Q9',PAPER,'explain','Light,Space physics',Q9P,Q9G,'Question 9',parts)

# ================================================================ Q10 nuclear power, transformer
Q10G=G({'sup':SUP,'sub':SUB,'nn':'Math.floor(nnp)','A':'92+nn','nt':"sup(A)+sub(92)+'U'",'ratio':'Math.floor(rp)','Vp':'5000*Math.floor(vpp)','Vs':'Vp*ratio','Np':'20*Math.floor(npp)','Ns':'Np*ratio','Vps':'String(Vp)','Vss':'String(Vs)','fm':'x=>String(x).replace(/\\B(?=(\\d{3})+(?!\\d))/g," ")','Ns2':'sf(Ns,2)','Vpf':'fm(Vp)','Vsf':'fm(Vs)'})
Q10P={'nnp':[141,147.99],'rp':[8,20.99],'vpp':[3,8.99],'npp':[6,20.99]}
parts=[]
parts.append(dict(pi=0,type='definition',K=lab('(a)')+'Nuclear power stations use uranium as the fuel. An isotope of uranium has 92 protons and ${nn} neutrons in each nucleus.<br><br>Write the nuclide notation for this isotope in the form with nucleon number, proton number and the symbol U.',
 A='${nt}|${A}/92U|${A}92U|U-${A}|U${A}|${A}U92|U${A}92|U−${A}|U–${A}|${A}U',
 C1=kwv('${A}','92'),
 U='${nt}',V='Nucleon number = protons + neutrons = 92 + ${nn} = ${A}; the proton number is 92.'))
parts.append(dict(pi=1,type='definition',answerType='table',K=lab('(b)')+'Complete the following sentences. In a nuclear reactor, a slow-moving <b>(1)</b> hits a uranium nucleus. This causes the uranium nucleus to split into smaller <b>(2)</b>. This reaction is called nuclear <b>(3)</b>. The reaction releases a large amount of energy. This energy heats <b>(4)</b> to drive a turbine which turns a <b>(5)</b> to produce electricity.<br><br>Type the missing words in Table 10.1.',
 tableRowLabels='["(1)","(2)","(3)","(4)","(5)"]',tableColLabels='["Table 10.1: missing words"]',
 tableCellKeywords=cells(['neutron','a neutron','neutrons'],['nuclei','nucleus','fragments','parts','nuclides','pieces','daughter nuclei','smaller nuclei','elements','atoms'],['fission'],['water','steam','the water','a liquid'],['generator','a generator','dynamo','alternator']),
 tableCellAnswers=answers('neutron','nuclei','fission','water','generator'),maxMarks='3',
 U='(1) neutron; (2) nuclei (fragments); (3) fission; (4) water (steam); (5) generator',V='A slow neutron is absorbed by a uranium nucleus, which splits (fission). The energy released heats water to steam to turn a turbine connected to a generator.'))
parts.append(dict(pi=2,type='explain',K=lab('(c)(i)')+'Step-up transformers produce high-voltage electricity that is transmitted from the power station to consumers far away from the power station.<br><br>Explain why the power loss in the cables during electricity transmission is smaller when the transmission is at a high voltage.',
 B=kwv('lowercurrent','lesscurrent','smallercurrent','currentislower','currentissmaller','currentisless','currentdecreases','currentisreduced','reducedcurrent','lowcurrent','currentisreduced','currentislow','currentgetssmaller','lowerthecurrent','currentgoesdown','currentfalls','currentdrops','smallthecurrent','nolargecurrent','thecurrentissmaller','current decreases'),
 B2=kwv('p=i2r','p=i²r','p=i^2r','i2r','i²r','i^2r','lessheating','lessheat','lessthermalenergy','lessenergyislostasheat','lessenergyloss','lessenergyiswasted','lowerheatingeffect','lessheatingeffect','lowerpowerloss','lesspowerisloss','lessheatinglossinthecables','powerlossisproportionaltoi','powerlossisproportionaltoi2','lessthermal','lessenergylost','reducedheating','lowerheat','smallerheating','heatingeffectissmaller','smallerheatingeffect','lessresistanceheating','lessenergydissipated'),
 U='High voltage means a lower current; the power loss P = I²R (heating effect) is therefore smaller.',V='For the same power transmitted, a higher voltage means a smaller current, and the power lost as heat in the cables depends on I².'))
parts.append(dict(pi=3,type='calculation',K=lab('(c)(ii)')+'A transformer in the power station steps up the voltage from ${Vpf} V to ${Vsf} V. The transformer has ${Np} turns on the primary coil.<br><br>Calculate the number of turns on the secondary coil of the transformer.',
 A='${Ns}|${Ns2}',tolerance='0',
 C1=kwv('${Np}×${Vs}/${Vp}','${Np}x${Vs}/${Vp}','${Np}*${Vs}/${Vp}','${Np}×${Vs}÷${Vp}','${Np}x${Vs}÷${Vp}','${Np}*${Vs}÷${Vp}','${Vs}×${Np}/${Vp}','${Vs}x${Np}/${Vp}','${Vs}*${Np}/${Vp}','${Vs}×${Np}÷${Vp}','${Vs}/${Vp}×${Np}','${Vs}÷${Vp}×${Np}','${Np}×${ratio}','${Np}x${ratio}','${Np}*${ratio}','${ratio}×${Np}','${ratio}x${Np}','${ratio}*${Np}','vp/vs=np/ns','np/ns=vp/vs','np/vp=ns/vs','ns/np=vs/vp','vs/vp=ns/np','ns=npvs/vp','ns=np×vs/vp','ns=npxvs/vp','ns=np×vs÷vp','vp/np=vs/ns','np×vs/vp','npxvs/vp','np×vs÷vp'),
 U='Ns = Np × Vs ÷ Vp = ${Np} × ${Vs} ÷ ${Vp} = ${Ns}',V='For a transformer Vp / Vs = Np / Ns, so Ns = Np × Vs ÷ Vp.'))
ALL+=question(LV,ID+'-Q10',PAPER,'calculation','Nuclear physics,Electricity,Magnetism',Q10P,Q10G,'Question 10',parts)

if __name__=='__main__':
    start=int(sys.argv[1]) if len(sys.argv)>1 else 637
    for r in ALL:
        if r['computedValues']:
            g=json.loads(r['computedValues']);others=' '.join(str(x) for rr in ALL if rr['id']==r['id'] for kk,x in rr.items() if kk!='computedValues')
            for k in list(g):
                if k in ('sf','ex','hd','ln','tx','capf') and not re.search(r'(?<![A-Za-z0-9_])'+k+r'\(',' '.join(v for kk,v in g.items() if kk!=k)+' '+others): del g[k]
            r['computedValues']=json.dumps(g,ensure_ascii=False)
    write_json(ALL,'igcse/new41.json',start=start)
    from collections import Counter
    print(len(ALL),'rows',dict(Counter(r['id'] for r in ALL)))
