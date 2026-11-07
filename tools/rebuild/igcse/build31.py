##v1  IGCSE 0625/31 Core Paper 3 (May/June 2026), rebuilt from the real QP + MS.  python3 igcse/build31.py <startRow>
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from b31_common import *
PAPER='0625_m26_p31'; ID='0625-26-31M'
ALL=[]
def G(extra): d=dict(BASE); d.update(extra); return d

# ================================================================ Q1  speed-time graph
FIG11=r"""(v,t1,t2,xm,ym)=>{const o={W:520,H:340,x0:0,x1:xm,y0:0,y1:ym,mx:0.5,my:0.5,Mx:2,My:2,xl:'time / s',yl:'speed (m/s)',cap:'Figure 1.1',pts:[[0,0],[t1,v],[xm,v]]};return gsvg(o);}"""
Q1G=G({'gsvg':GSVG,'fig11':FIG11,'v':'Math.floor(vp)','t1':'Math.floor(t1p)','t2':'Math.floor(t2p)','xm':'2*Math.ceil((t2+2)/2)','ym':'2*Math.ceil((v+1)/2)',
 'd':'+(0.5*t1*v).toFixed(1)','ds':'sf(d,3)','rect':'t1*v','T':'Math.floor(Tp)','vs':'Math.floor(vsp)','Dc':'vs*T','f11':'fig11(v,t1,t2,xm,ym)'})
Q1P={'vp':[6,13.99],'t1p':[3,5.99],'t2p':[9,13.99],'Tp':[10,40.99],'vsp':[4,15.99]}
parts=[]
parts.append(dict(pi=0,type='calculation',
 K=lab('(a)')+'Figure 1.1 shows the speed–time graph for a person skiing.${f11}Calculate the distance travelled between time = 0 and time = ${t1}.0 s by the person skiing.',
 A='${ds}',tolerance='1',
 C2=kwv('½×${t1}×${v}','0.5×${t1}×${v}','1/2×${t1}×${v}','${t1}×${v}/2','${t1}×${v}÷2','${v}×${t1}/2','${v}×${t1}÷2','½×${t1}.0×${v}.0','${t1}×${v}×0.5','${v}×${t1}×0.5','${v}×${t1}×½'),
 C1=kwv('areaunderthegraph','areaunderagraph','areaunderthe','areaunder','½×b×h','½×base×height','½bh','1/2bh','1/2×b×h','1/2×base×height','0.5×b×h','0.5×base×height','0.5bh','d=s×t','s×t','speed×time','averagespeed×time','areaofthetriangle','areaoftriangle','distance=speed×time','${rect}'),
 U='distance = area under the graph = ½ × ${t1} × ${v} = ${ds} m',
 V='Distance travelled is the area under a speed–time graph. Between 0 and ${t1} s the graph is a triangle with base ${t1} s and height ${v} m/s.'))
parts.append(dict(pi=1,type='explain',
 K=lab('(b)(i)')+'Use information from the graph in Figure 1.1 to describe the speed of the person skiing between time = 0 and time = ${t1}.0 s.',
 B='increas|accelerat|speedingup|speedsup|gettingfaster|getsfaster|fasterandfaster|goesfaster|risingspeed|speedrises|speedgoesup|speedgetshigher',
 U='The speed increases (the person is accelerating).',V='The graph slopes upwards, so the speed is increasing.'))
parts.append(dict(pi=2,type='explain',
 K=lab('(b)(ii)')+'Use information from the graph in Figure 1.1 to describe the speed of the person skiing between time = ${t1}.0 s and time = ${t2} s.',
 B=kwv('constant','steady','notchanging','thesame','uniform','zeroacceleration','noacceleration','nochange','staysthesame','remainsthesame','unchanged','maximumspeed','topspeed','${v}m/s','${v}ms-1','${v}ms⁻¹','doesnotchange','doesntchange','levelled','levelledoff'),
 U='The speed is constant at ${v} m/s.',V='The graph is a horizontal line, so the speed is not changing.'))
parts.append(dict(pi=3,type='calculation',
 K=lab('(c)')+'Another person skiing travels a distance of ${Dc} m in a time of ${T} s.<br><br>Calculate the average speed of this person.',
 A='${vs}',tolerance='1',
 C2=kwv('${Dc}÷${T}','${Dc}/${T}'),
 C1=kwv('(total)distance÷(total)time','distance/time','distance÷time','d÷t','d/t','s=d/t','speed=distance/time','speed=distance÷time','averagespeed=distance','averagespeed=totaldistance','distancedividedbytime','totaldistance÷totaltime','totaldistance/totaltime'),
 U='average speed = distance ÷ time = ${Dc} ÷ ${T} = ${vs} m/s',
 V='Average speed is the total distance travelled divided by the total time taken.'))
ALL+=question(LV,ID+'-Q1',PAPER,'calculation','Motion',Q1P,Q1G,'Question 1',parts)

# ================================================================ Q2  stack of discs, density
FIG21=r"""(n)=>{const W=420,H=230;let s=hd(W,H);
for(let i=0;i<n;i++){const y=150-i*7;s+='<ellipse cx="210" cy="'+y+'" rx="90" ry="26" fill="'+(i%2?'#dcdcdc':'#f2f2f2')+'" stroke="#000" stroke-width="1.2"/>';}
const top=150-(n-1)*7;s+='<ellipse cx="210" cy="'+top+'" rx="90" ry="26" fill="#f6f6f6" stroke="#000" stroke-width="1.6"/><ellipse cx="210" cy="'+top+'" rx="14" ry="4.5" fill="#fff" stroke="#000"/>';
s+=tx(30,38,'stack of '+['','','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve'][n]+' discs');s+=ln(30,46,128,top-6);
return s+'</svg>'+capf('Figure 2.1');}"""
Q2G=G({'fig21':FIG21,'n':'Math.floor(np)+6','nw':"['','','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve'][n]",
 'V':'10*(Math.floor(Vp)+1)','rho':'+(Math.floor(rp*10)/10+0.5).toFixed(1)','m':'Math.round(rho*V)','rhoA':'+(m/V).toFixed(2)','rhos':'sf(m/V,2)','f21':'fig21(n)'})
Q2P={'np':[0,6.99],'Vp':[0,4.99],'rp':[0,7.5]}
parts=[]
parts.append(dict(pi=0,type='explain',
 K=lab('(a)')+'Figure 2.1 shows a stack of ${nw} identical discs.${f21}Describe how to obtain a value for the average thickness of <b>one</b> disc.',
 A=kwv('straighten','alignthediscs','alignthestack','measurefrom0','measurefromzero','zeroofthe','fromthezero','eyelevel','perpendicular','viewfromabove'),
 B=kwv('ruler','rule','metrerule','meterule','vernier','caliper','micrometer','metreruler'),
 B2=kwv('thicknessofthestack','heightofthestack','heightofdiscs','thicknessofallthe','thicknessofthediscs','thicknessofthewholestack','measurethethickness','measuretheheight','measurethewidth','measuretheheightofthe','measurethestack','measurethewholestack','lengthofthestack','totalthickness','totalheight','totallength','tallthediscs','tallthestack','measurethedepth'),
 B3=kwv('dividebythenumber','dividebythenumberofdiscs','divideby${n}','÷${n}','/${n}','dividethetotal','dividetheheight','dividethethickness','dividethelength','divideitby','averagethickness','dividedby${n}','divideby8','divided','dividethetotalthickness'),
 maxMarks='3',
 U='Stand the stack upright (straighten it) with its bottom at 0 on a ruler, measure the total thickness (height) of the stack with the ruler and divide by ${n}, the number of discs.',
 V='Measuring one thin disc directly is inaccurate. Measure the whole stack with a ruler, then divide by the number of discs (${n}). (Alternatively, measure one disc at several points with calipers or a micrometer and find the average.)'))
parts.append(dict(pi=1,type='calculation',
 K=lab('(b)')+'The mass of one disc is ${m} g. The volume of the disc is ${V} cm<sup>3</sup>.<br><br>Calculate the density of the disc.',
 A='${rhoA}|${rhos}',tolerance='1',
 C2=kwv('${m}÷${V}','${m}/${V}'),
 C1=kwv('mass÷volume','mass/volume','m/v','m÷v','density=mass','d=m/v','ρ=m/v','ρ=m÷v','massdividedbyvolume','massoververvolume','massovervolume'),
 U='density = mass ÷ volume = ${m} ÷ ${V} = ${rhoA} g/cm³',
 V='Density is mass divided by volume.'))
ALL+=question(LV,ID+'-Q2',PAPER,'calculation','Measurement,Density and pressure',Q2P,Q2G,'Question 2',parts)

# ================================================================ Q3  stability, pressure, ball in oil
FIG31=r"""()=>{const W=520,H=250;let s=hd(W,H);
s+='<rect x="40" y="130" width="190" height="90" fill="#cfe6f7" stroke="#000" stroke-width="1.6"/><rect x="40" y="130" width="190" height="14" fill="#fff" stroke="none"/>'+ln(40,144,230,144)+tx(135,240,'container A','middle');
s+='<rect x="340" y="30" width="60" height="190" fill="#cfe6f7" stroke="#000" stroke-width="1.6"/><rect x="340" y="30" width="60" height="14" fill="#fff" stroke="none"/>'+ln(340,44,400,44)+tx(370,240,'container B','middle');
s+=ln(20,220,500,220);
return s+'</svg>'+capf('Figure 3.1');}"""
FIG32=r"""(w)=>{const W=420,H=280;let s=hd(W,H);
s+='<rect x="100" y="20" width="260" height="240" fill="#f5e6a8" stroke="#000" stroke-width="1.6"/>'+tx(130,40,'oil');
s+='<circle cx="210" cy="120" r="24" fill="#bbb" stroke="#000" stroke-width="1.6"/>'+tx(210,125,'ball','middle');
s+=ln(210,146,210,220,' marker-end="url(#ah)"')+tx(222,200,'weight = '+w+' N');
return s+'</svg>'+capf('Figure 3.2');}"""
Q3G=G({'fig31':FIG31,'fig32':FIG32,'F':'4*Math.floor(Fp)','Ar':'Math.floor(Ap)','pr':'F/Ar','pa':'sf(pr,3)','pb':'sf(pr,2)','W':'+(Math.floor(Wp)/10).toFixed(1)','f31':'fig31()','f32':'fig32(W)'})
Q3P={'Fp':[8,24.99],'Ap':[8,20.99],'Wp':[5,30.99]}
parts=[]
parts.append(dict(pi=0,type='explain',
 K=lab('(a)')+'Two containers, A and B, each contain water. Figure 3.1 shows the containers on a horizontal surface.${f31}Container A is more stable than container B.<br><br>Explain why container A is more stable than container B.',
 B=kwv('centreofgravitylower','centreofmasslower','lowercentreofgravity','lowercentreofmass','lowerc.o.g','lowercog','lowerc.o.m','cogislower','centreofgravityislower','centreofmassislower','cogisnearertheground','lowcentreofgravity','lowcentreofmass','lowerweightdistribution','lowerinheight','closertotheground'),
 B2=kwv('basebigger','baselarger','biggerbase','largerbase','widerbase','basewider','biggerareaofbase','largerareaofbase','baseareabigger','baseislarger','baseisbigger','baseiswider','widerbaseare','greaterbase','biggerarea','largerarea','areaofbase','widerat','widerthan','Aiswider','Awider','widerarea','moresurfacearea','largersurfacearea','biggersurfacearea','surfaceareaofbase'),
 B3=kwv('largertilt','biggertilt','greatertilt','tiltedmore','tiltmore','moretilt','tiltfurther','tiltedfurther','largerpush','biggerpush','greaterpush','morepush','morepushed','pushedmore','tobetopple','harder to topple','hardertotopple','hardertotip','hardertotilt','hardertopush','lesslikelytotopple','lesslikelytotip','toppleless','verticallinethroughthecentre','verticallinethroughthecog','linefrom','linethroughthe','fallovermore','fallover'),
 maxMarks='2',
 U='Any two from: the centre of gravity of A is lower; the base of A has a larger area; A has to be tilted through a larger angle (or needs a larger push) before it topples.',
 V='A container topples when the vertical line through its centre of gravity falls outside its base. A low centre of gravity and a wide base mean a larger tilt is needed before this happens.'))
parts.append(dict(pi=1,type='calculation',
 K=lab('(b)')+'The container rests on the surface with a force of ${F} N acting on an area of ${Ar} cm<sup>2</sup>.<br><br>Calculate the pressure exerted by the container on the surface. Give your answer in N/cm<sup>2</sup>.',
 A='${pa}|${pb}',tolerance='1',
 C2=kwv('${F}÷${Ar}','${F}/${Ar}'),
 C1=kwv('force÷area','force/area','f/a','f÷a','p=f/a','p=f÷a','pressure=force/area','pressure=force÷area','forcedividedbyarea','forceoverarea'),
 U='pressure = force ÷ area = ${F} ÷ ${Ar} = ${pa} N/cm²',
 V='Pressure is the force acting per unit area.'))
parts.append(dict(pi=2,type='explain',
 K=lab('(c)')+'A metal ball of weight ${W} N is dropped into a tank of oil. After a short time it falls at a constant speed. Figure 3.2 shows the ball with its weight.${f32}Draw an upward arrow on Figure 3.2 to show the other force on the ball. State the name of this force and its size.',
 B=kwv('drag','friction','resistive','resistance','viscous','upthrust','frictional','airresistance','dragforce','oilresistance','resistiveforce'),
 B2=kwv('${W}N','${W}newton','${W}newtons','${W}'),
 U='An upward arrow labelled drag (resistive/friction force) of ${W} N.',
 V='The ball falls at constant speed, so the forces are balanced: the upward drag force from the oil equals the weight, ${W} N.'))
ALL+=question(LV,ID+'-Q3',PAPER,'calculation','Density and pressure,Forces',Q3P,Q3G,'Question 3',parts)

# ================================================================ Q4  motor, power station
Q4G=G({'I':'+(Math.floor(Ip)/10).toFixed(1)','V':'Math.floor(Vp)','t':'5*Math.floor(tp)','E':'Math.round(I*V*t)','Es':'sf(E,2)','Ef':'String(+(I*V*t).toFixed(1))'})
Q4P={'Ip':[5,30.99],'Vp':[6,24.99],'tp':[4,12.99]}
parts=[]
parts.append(dict(pi=0,type='definition',
 K=lab('(a)(i)')+'An electric motor turns a wheel. State the name of the store of energy that increases as the wheel turns faster.',
 B=kwv('kinetic','movement'),
 U='Kinetic energy store.',V='The faster the wheel turns, the more energy is stored as kinetic energy.'))
parts.append(dict(pi=1,type='calculation',
 K=lab('(a)(ii)')+'The current in the motor is ${I} A and the potential difference across it is ${V} V. The motor operates for ${t} s.<br><br>Calculate the electrical energy transferred to the motor.',
 A='${E}|${Es}|${Ef}',tolerance='5',
 C2=kwv('${I}×${V}×${t}','${I}×${t}×${V}','${V}×${I}×${t}','${V}×${t}×${I}','${t}×${I}×${V}','${t}×${V}×${I}'),
 C1=kwv('i×t×v','v×i×t','e=ivt','e=vit','e=i×v×t','e=v×i×t','energy=current×voltage×time','energy=voltage×current×time','p=i×v','p=iv','p=v×i','p=vi','power=current×voltage','power=voltage×current','${I}×${V}','${V}×${I}','${I*V}'),
 U='E = I × V × t = ${I} × ${V} × ${t} = ${E} J',
 V='Electrical power P = IV, and energy = power × time.'))
parts.append(dict(pi=2,type='explain',
 K=lab('(a)(iii)')+'Some of the energy supplied to the motor is wasted.<br><br>Explain one way in which energy is wasted.',
 B=kwv('thermal','heat','internal','sound','heatenergy','thermalenergy','internalenergy','wasteheat'),
 B2=kwv('surroundings','air','environment','friction','motor','drivebelt','belt','dissipated','transferredto','lostto','warms','heatsup','heatingup','heating','bearings','wires','coil'),
 U='Energy is transferred as thermal energy (heat) to the surroundings (e.g. due to friction in the motor).',
 V='Not all the electrical energy becomes useful kinetic energy: friction and resistance heat the motor, which transfers thermal energy to the surroundings.'))
parts.append(dict(pi=3,type='explain',
 K=lab('(b)(i)')+'A power station generates electricity by burning a fossil fuel.<br><br>Describe how electricity is generated in this power station.',
 A=kwv('burn','combust','fuelisburnt','burningfuel','burntfuel','burnsfuel','fuelburns','burnedfuel','firedfuel','fossilfuelburnt','coalburn','gasburn','oilburn','chemicalenergy','chemicalstore','chemicalenergystore'),
 B=kwv('steam','boil','boiler','vapour','heatwater','heatthewater','heatswater','heatedwater','heatingwater','waterisheated','waterheated','waterboil','boilwater','boilthewater','waterturnsto','thermalenergy','heatenergy','heat'),
 B2=kwv('turbine'),
 B3=kwv('generator','dynamo','alternator','coilmagnet','coilofwire','magnetsandcoils','electromagneticinduction','induced','rotatesthegenerator','drivesthegenerator','turnsthegenerator'),
 maxMarks='4',
 U='Burning the fuel releases thermal energy, which boils water to make steam; the steam drives a turbine, and the turbine drives a generator that produces electricity.',
 V='Chemical energy in the fuel becomes thermal energy, then kinetic energy of the steam, then kinetic energy of the turbine, and finally electrical energy in the generator.'))
parts.append(dict(pi=4,type='explain',
 K=lab('(b)(ii)')+'State two disadvantages of using fossil fuels to generate electricity. Do not refer to cost.',
 B=kwv('pollut','acidrain','sulfurdioxide','sulphurdioxide','so2','smog','smoke','soot','particulates','nitrogenoxide','nox','globalwarming','climatechange','greenhouse','co2','carbondioxide','carbonemissions','emitscarbon','warmingtheplanet','environmentalimpact','damagetotheenvironment'),
 B2=kwv('non-renewable','nonrenewable','notrenewable','runout','willrunout','finite','cannotbereplaced','cantbereplaced','nolongerbeavailable','usedup','limitedsupply','dependsonsupplies','canbeusedup','toolongtoform','takemillions','limitedamount','limitedresource','running out','notinfinite'),
 U='Any two from: the burning causes (air) pollution / acid rain; carbon dioxide is released (global warming / climate change); fossil fuels are non-renewable and will run out.',
 V='Fossil fuels release carbon dioxide and other polluting gases when burned, and once used they cannot be replaced on a human timescale.'))
ALL+=question(LV,ID+'-Q4',PAPER,'calculation','Energy and power,Electricity',Q4P,Q4G,'Question 4',parts)

# ================================================================ Q5  hot-air balloon
FIG51=r"""()=>{const W=420,H=300;let s=hd(W,H);
s+='<path d="M210 20 C 90 20 70 130 130 200 L 150 225 L 270 225 L 290 200 C 350 130 330 20 210 20 Z" fill="#f3b6a0" stroke="#000" stroke-width="1.6"/>';
s+=ln(150,225,170,258)+ln(270,225,250,258)+'<rect x="170" y="258" width="80" height="32" fill="#c9a26b" stroke="#000" stroke-width="1.4"/>';
s+='<rect x="195" y="228" width="30" height="24" rx="6" fill="#f7d070" stroke="#000"/>'+tx(210,110,'hot air','middle');
return s+'</svg>'+capf('Figure 5.1');}"""
Q5G=G({'fig51':FIG51,'Tc':'5*Math.floor(Tp)','K':'Tc+273','K2':'Tc+273.15','Ks':'sf(K,2)','f51':'fig51()'})
Q5P={'Tp':[14,32.99]}
parts=[]
parts.append(dict(pi=0,type='explain',
 K=lab('(a)')+'A hot-air balloon rises when the air inside it is heated by a burner. Figure 5.1 shows the balloon.${f51}Explain why the hot air makes the balloon rise.',
 B=kwv('expand','particlesmoveapart','particlesspreadout','spreadout','furtherapart','volumeincreases','volumeincrease','biggervolume','largervolume','takesupmorespace','takesupmorevolume','moveapart','moresspace'),
 B2=kwv('lessdense','densitydecreases','densityislower','lowerdensity','densitygoesdown','densityreduces','decreaseddensity','densityisless','densitydecrease','densitydropped','lowerindensity','lessmassperunit'),
 U='The hot air expands (its particles move further apart) and so becomes less dense than the cooler air outside.',
 V='Heating makes the air expand, so the same mass occupies a larger volume. The air inside is less dense than the surrounding air, so the balloon floats upwards.'))
parts.append(dict(pi=1,type='explain',
 K=lab('(b)')+'The air inside the balloon exerts a pressure on the inside surface of the balloon.<br><br>Explain, in terms of the particles of air, how the air exerts a pressure on the inside surface of the balloon.',
 B=kwv('move','fast','kineticenergy','speed','velocity','random','motion','movingaround','moving'),
 B2=kwv('collide','hit','bounce','strike','collision','impact','bombard','crash','knock','bumpinto','collidewith','hitting'),
 B3=kwv('force','p=f/a','p=f÷a','force÷area','force/area','pressure=force','pressureisforce','pressureisthe','momentum','changeinmomentum'),
 U='Air particles move randomly with high speed / kinetic energy, collide with the surface of the balloon and exert a force on it; pressure = force ÷ area.',
 V='Pressure is force per unit area. Fast-moving air particles hit the inside of the balloon and each collision exerts a force on the surface.'))
parts.append(dict(pi=2,type='calculation',
 K=lab('(c)')+'The temperature of the air inside the balloon is ${Tc} °C.<br><br>Calculate this temperature in kelvin.',
 A='${K}|${K2}|${Ks}',tolerance='1',
 C1=kwv('${Tc}+273','${Tc}+273.15','273+${Tc}','273.15+${Tc}','c+273','°c+273','celsius+273','temperature+273','add273','+273','+273.15'),
 U='temperature = ${Tc} + 273 = ${K} K',
 V='To convert from degrees Celsius to kelvin, add 273.'))
ALL+=question(LV,ID+'-Q5',PAPER,'calculation','Thermal physics',Q5P,Q5G,'Question 5',parts)

# ================================================================ Q6  EM spectrum
FIG61=r"""()=>{const W=560,H=120;let s=hd(W,H);const n=['gamma rays','X-rays','ultraviolet','visible light','infrared','microwaves','radio waves'];
for(let i=0;i<7;i++){s+='<rect x="'+(10+i*76)+'" y="20" width="74" height="44" fill="#f4f4f4" stroke="#000" stroke-width="1.4"/>';const w=n[i].split(' ');
 if(w.length>1){s+=tx(47+i*76,38,w[0],'middle')+tx(47+i*76,55,w[1],'middle');}else{s+=tx(47+i*76,46,w[0],'middle');}}
s+=ln(20,96,540,96,' marker-end="url(#ah)"');
return s+'</svg>'+capf('Figure 6.1');}"""
Q6G=G({'fig61':FIG61,'fa':'Math.floor(fp)/10','fe':'sf(fa,2)','fs':"String(fa)",'f':'fa*1e15','c':'3.0e8','lam':'c/f','le1':'ex(lam,1)','le2':'ex(lam,2)','ls1':'sf(lam,2)','ls2':'sf(lam,3)',
 'f61':'fig61()'})
Q6P={'fp':[21,98.99]}
parts=[]
parts.append(dict(pi=0,type='definition',
 K=lab('(a)(i)')+'Figure 6.1 shows the seven regions of the electromagnetic spectrum in order. The arrow below the regions points from gamma rays towards radio waves.${f61}State the quantity that increases in the direction of the arrow.',
 B=kwv('wavelength','wavelengths','λ','lambda'),
 U='wavelength',V='From gamma rays to radio waves the wavelength increases and the frequency decreases. All electromagnetic waves travel at the same speed in a vacuum.'))
parts.append(dict(pi=1,type='explain',
 K=lab('(a)(ii)')+'Electromagnetic waves are transverse waves.<br><br>Describe the direction in which the vibrations occur in a transverse wave.',
 B=kwv('perpendicular','rightangle','90','atrightangles','normalto','orthogonal','90°'),
 B2=andor(['perpendicular','rightangle','90','atrightangles','normalto','orthogonal','90°'],['directionofpropagation','directionoftravel','directionofwave','directionofenergy','directionofthewave','directionwavetravels','directionthewavetravels','waveisgoing','wavetravels','wavetravelling','wavemoving','directionofmotion','directionofmovement','directionoftransfer','wavedirection','propagation','directionofenergytransfer','directionofpropogation','travel','energytransfer','transferofenergy','progress','movementofthewave']),
 U='The vibrations are perpendicular (at right angles) to the direction of travel of the wave (direction of energy transfer).',
 V='In a transverse wave the particles or fields vibrate at 90° to the direction in which the wave transfers energy.'))
parts.append(dict(pi=2,type='calculation',
 K=lab('(a)(iii)')+'A gamma ray has a frequency of ${fs} × 10<sup>15</sup> Hz. The speed of electromagnetic waves in a vacuum is 3.0 × 10<sup>8</sup> m/s.<br><br>Calculate the wavelength of the gamma ray.',
 A='${le1}|${le2}|${ls1}|${ls2}',tolerance='2',
 C2=kwv('3.0×10^8÷${fs}×10^15','3.0×10^8/${fs}×10^15','3.0e8/${fs}e15','3.0e8÷${fs}e15','3×10^8/${fs}×10^15','3e8/${fs}e15','3x10^8/${fs}x10^15','3.0x10^8/${fs}x10^15','3e8÷${fs}e15','3×10^8÷${fs}×10^15','3.0×10^8/(${fs}×10^15)','3×10^8/(${fs}×10^15)','3.0×10^8÷(${fs}×10^15)','3×10^8÷(${fs}×10^15)','3.0e8/${f}','3e8/${f}','300000000/${f}','3.0e8÷${f}','3e8÷${f}'),
 C1=kwv('v=fλ','v=fxλ','v=f×λ','v=fl','v=fλ','λ=v/f','λ=v÷f','wavelength=speed/frequency','wavelength=speed÷frequency','wavelength=v/f','wavespeed=frequency×wavelength','speed=frequency×wavelength','v=f×wavelength','l=v/f','lambda=v/f'),
 U='wavelength = v ÷ f = 3.0 × 10⁸ ÷ (${fs} × 10¹⁵) = ${le2} m',
 V='Use wave speed = frequency × wavelength, rearranged to wavelength = speed ÷ frequency.'))
parts.append(dict(pi=3,type='definition',
 K=lab('(b)(i)')+'State one medical use of gamma rays.',
 B=kwv('cancer','sterilis','sterilize','tumour','tumor','radiotherapy','killcancer','killingcancer','killcells','killbacteria','destroycells','killsharmfulcells','killsmicrobes','killgerms','tracer','imaging','scan','pet','detectcancer','treatingcancer','medicalinstruments','equipment'),
 U='Treatment of cancer, detection of cancer or sterilising medical equipment.',V='Gamma rays can kill cancer cells and bacteria, and the radiation is also used in tracers to detect cancer.'))
parts.append(dict(pi=4,type='definition',
 K=lab('(b)(ii)')+'State one harmful effect of gamma rays on the human body.',
 B=kwv('mutation','mutate','dna','damagecells','damagestocells','damagetocells','damagingcells','damagecell','cellsdamage','cellsdamaged','celldamage','destroycells','killcells','killscells','cancer','burn','hairloss','radiationsickness','radiationburn','tissuedamage','damagetissue','damagetheskin','damagetoskin','damageeyes','damagetoeyes','cataract','harmcells','harmscells','ionis','ioniz','damage'),
 U='Gamma rays can cause mutation (damage to DNA) or damage / kill living cells, which can lead to cancer.',V='Gamma radiation is ionising: it can damage DNA and cells, causing mutations, burns, radiation sickness or cancer.'))
ALL+=question(LV,ID+'-Q6',PAPER,'calculation','Waves',Q6P,Q6G,'Question 6',parts)

# ================================================================ Q7  prism, critical angle
FIG71=r"""(a)=>{const W=520,H=300;let s=hd(W,H);const i=(90-a)*Math.PI/180,L=170,bx=300,by=140;const ax=bx-L*Math.cos(i),ay=by+L*Math.sin(i);
s+='<polygon points="120,270 300,20 300,270" fill="#e8f0f7" stroke="#000" stroke-width="1.6"/>';
s+=ln(300,20,300,270);
s+=ln(ax,ay,bx,by)+tx(ax-6,ay+18,'A','end')+tx(bx+8,by-6,'B')+tx(bx+6,232,'D')+'<circle cx="300" cy="232" r="3"/>';
s+=ln(bx,by,bx+120,by-0.0,' stroke-dasharray="5,4" stroke-width="1" ').replace('stroke-width="1.6"','')+tx(bx+124,by+4,'normal');
const ex=bx+120*Math.cos(0.9),ey=by-120*Math.sin(0.9);
s+=ln(bx,by,ex,ey,' marker-end="url(#ah)"')+tx(ex+4,ey,'refracted ray');
return s+'</svg>'+capf('Figure 7.1');}"""
Q7G=G({'fig71':FIG71,'ap':'Math.floor(ap0)','inc':'90-ap','cc':'Math.floor(cp)','i2':'cc+Math.floor(dp)','f71':'fig71(ap)'})
Q7P={'ap0':[35,68.99],'cp':[36,44.99],'dp':[2,6.99]}
parts=[]
parts.append(dict(pi=0,type='calculation',
 K=lab('(a)(i)')+'A ray of red light travels through a glass prism. Figure 7.1 shows the ray AB meeting the surface at B. The line BD lies along the surface and angle ABD is ${ap}°. The normal to the surface at B is shown.${f71}Calculate the angle of incidence of the ray at B.',
 A='${inc}',tolerance='0',
 U='angle of incidence = 90 − ${ap} = ${inc}°',V='The angle of incidence is measured between the ray and the normal. The normal is at 90° to the surface, so angle of incidence = 90° − ${ap}°.'))
parts.append(dict(pi=1,type='definition',
 K=lab('(a)(ii)')+'The ray leaves the prism at B along the path shown in Figure 7.1.<br><br>State the name of the angle between the refracted ray and the normal.',
 B=kwv('angleofrefraction','refractionangle','refraction'),
 U='angle of refraction',V='The angle of refraction is measured between the refracted ray and the normal.'))
parts.append(dict(pi=2,type='definition',
 K=lab('(b)(i)')+'The critical angle for the glass of the prism is ${cc}°.<br><br>State what is meant by the critical angle.',
 B=andor(['angleofincidence','incidentangle','incidenceangle','anglebetweentheincident','angleincident'],['90','rightangle','alongthesurface','alongtheboundary','runsalongthe','travelsalong','travelsalongthesurface','notleavetheglass','nolightleaves','noraygoesout','doesnotleave','doesnotemerge','doesntleave','emergesalong','refractedraygoesalong']),
 U='The critical angle is the angle of incidence at which the angle of refraction is 90° (the refracted ray travels along the surface).',V='At the critical angle the refracted ray just skims along the boundary. For larger angles of incidence all the light is reflected.'))
parts.append(dict(pi=3,type='explain',
 K=lab('(b)(ii)')+'A different ray inside the prism meets the surface at an angle of incidence of ${i2}°.<br><br>State what happens to this ray at the surface.',
 B=kwv('totalinternalreflection','totallyinternallyreflected','totallyreflected','totalreflection','totalinternallyreflect','internallyreflect','reflected','reflects','reflect','tir'),
 U='The ray is totally internally reflected (it reflects back into the glass at ${i2}° to the normal).',V='${i2}° is greater than the critical angle of ${cc}°, so no light is refracted out and total internal reflection occurs.'))
ALL+=question(LV,ID+'-Q7',PAPER,'explain','Light',Q7P,Q7G,'Question 7',parts)

# ================================================================ Q8  lamp and thermistor
FIG81=r"""()=>{const W=520,H=250;let s=hd(W,H);
s+=ln(60,40,60,100)+ln(60,150,60,200)+ln(60,200,460,200)+ln(60,40,200,40)+ln(300,40,460,40)+ln(460,40,460,90)+ln(460,150,460,200);
s+=ln(48,100,72,100)+ln(54,112,66,112)+ln(48,150,72,150,'')+tx(80,112,'cell');
s+='<circle cx="250" cy="40" r="26" fill="#fff" stroke="#000" stroke-width="1.6"/>'+ln(232,22,268,58)+ln(268,22,232,58)+ln(200,40,224,40)+ln(276,40,300,40)+tx(250,88,'lamp','middle');
s+='<rect x="436" y="90" width="48" height="60" fill="#fff" stroke="#000" stroke-width="1.6"/>'+tx(460,172,'thermistor','middle');
return s+'</svg>'+capf('Figure 8.1');}"""
Q8G=G({'fig81':FIG81,'Vp1':'Math.floor(Vq)/10','Ip1':'Math.floor(Iq)/100','Vv':'Vp1','Ii':'Ip1','R':'Vv/Ii','Rs':'sf(R,2)','Rs3':'sf(R,3)','f81':'fig81()'})
Q8P={'Vq':[20,59.99],'Iq':[20,95.99]}
parts=[]
parts.append(dict(pi=0,type='explain',
 K=lab('(a)')+'Figure 8.1 shows a circuit containing a cell, a lamp and a thermistor in series.${f81}A voltmeter is added to the circuit to measure the potential difference across the lamp.<br><br>State how the voltmeter is connected to the lamp.',
 B=kwv('parallel','inparallelwith','acrossthelamp','overthelamp','oneithersideofthelamp','eithersideofthelamp','eithersideoflamp','bothsidesofthelamp','acrossthebulb','inparallel'),
 B2=andor(['parallel','across','overthe','eithersideof','bothsidesof','atthesameplaceas','acrossthe'],['lamp','bulb','light']),
 U='The voltmeter is connected in parallel with (across) the lamp.',V='A voltmeter measures the potential difference between two points, so it is connected in parallel with the component being measured.'))
parts.append(dict(pi=1,type='calculation',
 K=lab('(b)')+'The potential difference across the thermistor is ${Vv} V and the current in it is ${Ii} A.<br><br>Calculate the resistance of the thermistor.',
 A='${Rs}|${Rs3}',tolerance='1',
 C2=kwv('${Vv}÷${Ii}','${Vv}/${Ii}'),
 C1=kwv('v=ir','v÷i','v/i','r=v/i','r=v÷i','resistance=v/i','resistance=voltage/current','resistance=voltage÷current','resistance=potentialdifference/current','resistance=pd/current','voltage÷current','voltage/current','r=pd/i','pd÷i','pd/i','p.d./i'),
 U='R = V ÷ I = ${Vv} ÷ ${Ii} = ${Rs} Ω',V='Resistance is the potential difference across a component divided by the current in it.'))
parts.append(dict(pi=2,type='explain',
 K=lab('(c)')+'The circuit is moved from a warm room into a cold room. The resistance of the thermistor increases as its temperature decreases.<br><br>Explain what happens to the brightness of the lamp.',
 B=kwv('dimmer','dim','lessbright','dimmed','darker','gets dim','notasbright','less bright','getsdimmer','gointodim','duller','fainter','brightnessdecreases','decreasesinbrightness','dimmerlight','brightnessdecrease','becomesdimmer','getlessbright'),
 B2=kwv('currentdecreases','currentfalls','currentgoesdown','lesscurrent','smallercurrent','reducedcurrent','currentisreduced','currentislower','lowercurrent','currentreduces','currentdecrease','currentdrops','currentisless','currentgetssmaller'),
 B3=kwv('totalresistanceincreases','resistanceincreases','higherresistance','greaterresistance','moreresistance','resistanceisgreater','resistanceisbigger','resistanceofthecircuit','resistancegoesup','resistancerises','biggerresistance','increaseinresistance','resistanceisincreased','totalresistance','resistanceincrease','resistanceofthermistorincreases','pdacrossthelampdecreases','pdacrossthelampfalls','lesspd','lessvoltage','lowerpd','smallerpd','pdacrosslampdecreases'),
 U='The lamp becomes dimmer: the thermistor resistance increases so the total resistance of the circuit increases and the current in the lamp decreases.',
 V='More resistance in series means less current. A smaller current in the lamp makes the lamp dimmer.'))
ALL+=question(LV,ID+'-Q8',PAPER,'calculation','Electricity',Q8P,Q8G,'Question 8',parts)

# ================================================================ Q9  magnets and induction
FIG91=r"""(nl)=>{const W=520,H=300;let s=hd(W,H);
s+='<rect x="190" y="125" width="140" height="50" fill="#f4f4f4" stroke="#000" stroke-width="1.8"/>'+ln(260,125,260,175);
const dr=nl?1:-1; // arrows outside go from N to S: if N is left, arrows run left->right on top (dir +1)
const q=(k,sg)=>{const h=40+k*34;const p='M190 '+(150+sg*0)+' ';return '<path d="M190 '+(sg>0?125:175)+' C 190 '+(sg>0?125-h*1.2:175+h*1.2)+' 330 '+(sg>0?125-h*1.2:175+h*1.2)+' 330 '+(sg>0?125:175)+'" fill="none" stroke="#000" stroke-width="1.4"/>'};
for(let k=0;k<3;k++){for(const sg of [1,-1]){s+=q(k,sg);const h=40+k*34;const y=sg>0?125-h*0.9:175+h*0.9;const dx=nl?8:-8;s+='<polygon points="'+(260+dx)+','+y+' '+(260-dx)+','+(y-5)+' '+(260-dx)+','+(y+5)+'" fill="#000"/>';}}
return s+'</svg>'+capf('Figure 9.1');}"""
Q9G=G({'fig91':FIG91,'nl':'Math.floor(nlp)','pole':"nl?'north':'south'",'f91':'fig91(nl)',
 'pk':'Math.floor(pkp)','pl':"['south','north'][pk]",'opl':"['north','south'][pk]",'dirw':"['left','right'][Math.floor(dwp)]",'odirw':"['right','left'][Math.floor(dwp)]"})
Q9P={'nlp':[0,1.99],'pkp':[0,1.99],'dwp':[0,1.99]}
parts=[]
parts.append(dict(pi=0,type='definition',
 K=lab('(a)')+'Figure 9.1 shows the magnetic field around a bar magnet. The arrows show the direction of the field.${f91}State the name of the magnetic pole at the left-hand end of the magnet.',
 B='${pole}',
 U='${pole} pole',V='Outside a magnet the field lines point away from the north pole and towards the south pole.'))
parts.append(dict(pi=1,type='explain',
 K=lab('(b)')+'A soft-iron bar PQ is placed with end P near a ${opl} pole of a magnet. The bar and the magnet move towards each other.<br><br>Explain why the bar and the magnet move towards each other.',
 B=kwv('induced','temporarymagnet','becomesamagnet','becomemagnetised','becomesmagnetised','magnetised','magnetized','becomesamagnet','becomesmagnetic','isamagnet','magneticfield','inducedmagnet','inducedmagnetism','temporarilymagnetic','temporarilymagnetised','magnetisedbyinduction','becomemagnetic','magneticisedbyinduction'),
 B2=kwv('opposite','unlike','attract','northandsouth','southandnorth','northpoleandasouth','southpoleandanorth','northisattractedtosouth','nearestthe${opl}','${pl}pole','${pl}polenearest','polenearest','${pl}end','${pl}atP','p isa${pl}'),
 U='The soft iron becomes an induced (temporary) magnet; the end P nearest the ${opl} pole becomes a ${pl} pole, and unlike poles attract.',V='Soft iron is easily magnetised by induction. The nearest end becomes the opposite pole to the magnet pole, so the two attract.'))
parts.append(dict(pi=2,type='explain',
 K=lab('(c)(i)')+'A coil is connected to a sensitive ammeter. A ${pl} pole of a magnet is moved into the coil and the ammeter pointer deflects to the ${dirw}.<br><br>State two ways of increasing the deflection of the pointer to the ${dirw}.',
 B=kwv('fastermovement','movefaster','fasterspeed','increasethespeed','increasespeed','higherspeed','speedofmagnet','speedofthemagnet','quickly','morequickly','fastermagnet','fasterspeedofmagnet','speedupthemagnet','magnetmovesfaster','movingfaster','move it faster','fastermotion','greaterspeed','fastermovement','movethemagnetfaster','pushmagnetfaster'),
 B2=kwv('strongermagnet','strongermagnets','strongerfield','morepowerfulmagnet','greaterfieldstrength','strongermagneticfield','strongermagnetism','strongermagnetic','morepowerful','extramagnets','moremagnets','twomagnets','usestrongermagnet','amorepowerfulmagnet','strongermagnet'),
 B3=kwv('moreturns','moreloops','morecoils','moreturnsonthecoil','additionalturns','extraturns','morewire','morewindings','increasethenumberofturns','increasenumberofturns','increaseturns','moreturn','greaterturns','increasingthenumberofturns','morecoil','morewinds','coilwithmoreturns'),
 maxMarks='2',
 U='Any two from: move the magnet faster; use a stronger magnet; use a coil with more turns.',V='The induced e.m.f. (and so the current) is greater when the magnetic field cuts the coil faster, when the field is stronger, or when there are more turns.'))
parts.append(dict(pi=3,type='explain',
 K=lab('(c)(ii)')+'State two ways of making the pointer deflect to the ${odirw} instead.',
 B=kwv('${pl}poleout','${pl}pole outof','removethe${pl}pole','withdraw','moveitout','pullit out','pullout','takeout','moveout','removethemagnet','magnetoutofthecoil','outofthecoil','pulltheoutof','movingaway','movethe${pl}poleout','movethe${pl}poleaway','${pl}polemovedout','movethemagnetaway','movethemagnetout','reversethedirection','oppositedirection','movemagnetout'),
 B2=kwv('${opl}polein','${opl}poleinto','${opl}polein','usethe${opl}pole','insertthe${opl}','${opl}end','${opl}pole','movethe${opl}','otherpole','oppositepole','swapthepoles','otherendofthemagnet','turnmagnetround','turnthemagnetaround','flipthemagnet','reversethemagnet','reversethepole','reversepoles','otherendinto','oppositeendin'),
 B3=kwv('reversetheconnections','swapthewires','switchthewires','reversetheammeter','swaptheleads','reversethepolarity','connectionsreversed','swapthe connections','swaptheconnections','switchtheconnections','reverseconnections','reversethewires','reversetheleads','changetheconnections','connectionsswapped','swapleads','swapwires','switchleads','reversethecoil','swapthecoil','invertthecoil','turnthecoil','turnthecoilround','reversethecoilconnections','changewiring','connectedtheotherway','otherway round','otherwayround','reverseterminals','swapterminals'),
 maxMarks='2',
 U='Any two from: move the ${pl} pole out of the coil; move the ${opl} pole into the coil; reverse the connections to the ammeter (or coil).',V='Reversing the direction of the change of flux through the coil (pole direction in/out or opposite pole) or reversing the connections reverses the direction of the current.'))
ALL+=question(LV,ID+'-Q9',PAPER,'explain','Magnetism',Q9P,Q9G,'Question 9',parts)

# ================================================================ Q10  nuclide
NUC=[['americium','Am',95,241],['plutonium','Pu',94,239],['uranium','U',92,235],['radium','Ra',88,226],['polonium','Po',84,210],['thorium','Th',90,232],['cobalt','Co',27,60],['caesium','Cs',55,137],['iodine','I',53,131],['strontium','Sr',38,90]]
SUPJ="(n)=>String(n).split('').map(c=>'⁰¹²³⁴⁵⁶⁷⁸⁹'[+c]).join('')"
SUBJ="(n)=>String(n).split('').map(c=>'₀₁₂₃₄₅₆₇₈₉'[+c]).join('')"
Q10G=G({'sup':SUPJ,'sub':SUBJ,'tb':json.dumps(NUC),'nu':'tb[Math.floor(np)]','nm':'nu[0]','sy':'nu[1]','Z':'nu[2]','A':'nu[3]','Nn':'A-Z','A1':'A+1','nt':'sup(A1)+sub(Z)+sy'})
Q10P={'np':[0,9.99]}
parts=[]
parts.append(dict(pi=0,type='definition',
 K=lab('(a)(i)')+'An atom of ${nm}-${A} has a nucleon number of ${A} and a proton number of ${Z}.<br><br>State the number of protons in the nucleus of this atom.',
 B='${Z}',U='${Z}',V='The proton number is the number of protons in the nucleus.'))
parts.append(dict(pi=1,type='definition',
 K=lab('(a)(ii)')+'State the number of neutrons in the nucleus of this atom.',
 B='${Nn}',U='${Nn}',V='Neutrons = nucleon number − proton number = ${A} − ${Z}.'))
parts.append(dict(pi=2,type='definition',
 K=lab('(b)')+'Another isotope of ${nm} has one more neutron in its nucleus than ${nm}-${A}.<br><br>Write the nuclide notation for this isotope, using the symbol ${sy}.',
 B=kwv('${nt}','${A1}${Z}${sy}','${A1}/${Z}${sy}','${sy}-${A1}','${sy}${A1}','${A1}${sy}','${sy}${A1}${Z}','${A1}${sy}${Z}','${A1}(${Z})${sy}','${A1}over${Z}${sy}','${A1}_${Z}${sy}','${A1}^${Z}${sy}','^${A1}_${Z}${sy}','${A1}${Z}${sy}','${sy}(${A1},${Z})','${sy}-${A1}${Z}'),
 U='${nt}',V='The nucleon number increases by one to ${A1}; the proton number stays at ${Z} because it is the same element.'))
parts.append(dict(pi=3,type='explain',
 K=lab('(c)')+'Compare the ability of alpha particles and beta particles to pass through a sheet of paper.',
 B=andor(['stopped','absorbed','blocked','cannotpass','cannotpenetrate','doesnotpass','doesnotpenetrate','notpass','notpenetrate','cantpass','cantpenetrate','cannotgothrough','doesntpass','doesnotgothrough','arestopped','isstopped','donotpass','donotpenetrate','arenotable','isnotable'],['betapass','betaparticlespass','betapenetrate','betaparticlespenetrate','betacanpass','betacanpenetrate','betaparticlescanpass','betaparticlescanpenetrate','betagoes','betaparticlesgo','betapasses','betapenetrates','betagetsthrough','betaparticlesgetthrough','betagetthrough','betaparticlesarenot stopped','betaisnotstopped','betaarenotstopped','betadoes','betagoesthrough','betapassthrough','betapassesthrough','betapenetratethrough','betapenetratesthrough','canpassthrough','canpenetrate','whilebeta','butbeta','betaisnot','betanot']),
 U='Alpha particles are stopped by (cannot pass through) paper but beta particles pass through it.',V='Alpha particles are highly ionising but have a very short range in matter and are stopped by paper; beta particles are more penetrating and pass through paper (they are stopped by a few mm of aluminium).'))
ALL+=question(LV,ID+'-Q10',PAPER,'definition','Nuclear physics',Q10P,Q10G,'Question 10',parts)

# ================================================================ Q11  solar system, redshift
FIG111=r"""(lab)=>{const W=560,H=290,cx=280,cy=145;const R=[16,26,36,46,0,86,104,122];const nm=['Mercury','Venus','Earth','Mars','','Jupiter','Saturn','Uranus','Neptune'];let s=hd(W,H);
const rr=[18,30,42,54,88,106,124,140];
s+='<circle cx="'+cx+'" cy="'+cy+'" r="9" fill="#f7d070" stroke="#000"/>';
for(let i=0;i<8;i++){s+='<circle cx="'+cx+'" cy="'+cy+'" r="'+rr[i]+'" fill="none" stroke="#000" stroke-width="1"/>';}
const ang=[0.4,2.2,4.0,5.5,1.1,3.3,5.0,2.7];
for(let i=0;i<8;i++){const x=cx+rr[i]*Math.cos(ang[i]),y=cy-rr[i]*Math.sin(ang[i]);s+='<circle cx="'+x+'" cy="'+y+'" r="4.5" fill="#6a8fb8" stroke="#000"/>';
 const lx=x+(Math.cos(ang[i])>=0?9:-9),an=Math.cos(ang[i])>=0?'start':'end';s+=tx(lx,y+4,lab[i]?lab[i]:''+(i+1),an);}
// asteroid belt
for(let k=0;k<60;k++){const a=k*0.713,r=71+((k*7)%5)-2;s+='<circle cx="'+(cx+r*Math.cos(a))+'" cy="'+(cy-r*Math.sin(a))+'" r="1.4" fill="#444"/>';}
s+=tx(cx+74,cy-72,'X');
return s+'</svg>'+capf('Figure 11.1');}"""
PL="['Mercury','Venus','Earth','Mars','Jupiter','Saturn','Uranus','Neptune']"
Q11G=G({'fig111':FIG111,'PL':PL,'pats':'[[1,2,6,7],[1,3,5,7],[2,3,6,8],[1,4,5,8],[2,4,6,7],[1,3,6,8]]','pat':'pats[Math.floor(pp)]',
 'unk':'[1,2,3,4,5,6,7,8].filter(i=>pat.indexOf(i)<0)','n0':'PL[unk[0]-1]','n1':'PL[unk[1]-1]','n2':'PL[unk[2]-1]','n3':'PL[unk[3]-1]',
 'labs':"(()=>{const a=[];for(let i=0;i<8;i++){a.push(pat.indexOf(i+1)>=0?(i+1)+' '+PL[i]:'');}return a;})()",
 'given':"pat.map(i=>i+' = '+PL[i-1]).join(', ')",
 'f111':'fig111(labs)'})
Q11P={'pp':[0,5.99]}
parts=[]
parts.append(dict(pi=0,type='definition',answerType='table',
 K=lab('(a)(i)')+'Figure 11.1 shows the orbits of the eight planets around the Sun. The planets are numbered 1 to 8 in order of distance from the Sun. Planets ${given} are labelled on the figure.${f111}Complete Table 11.1 by naming the planets numbered ${unk[0]}, ${unk[1]}, ${unk[2]} and ${unk[3]}.',
 tableRowLabels='["Planet ${unk[0]}","Planet ${unk[1]}","Planet ${unk[2]}","Planet ${unk[3]}"]',
 tableColLabels='["Table 11.1: name"]',
 tableCellKeywords='[[["exact:${n0}"]],[["exact:${n1}"]],[["exact:${n2}"]],[["exact:${n3}"]]]',
 tableCellAnswers='[["${n0}"],["${n1}"],["${n2}"],["${n3}"]]',
 maxMarks='3',
 U='${unk[0]} = ${n0}; ${unk[1]} = ${n1}; ${unk[2]} = ${n2}; ${unk[3]} = ${n3}',V='The order from the Sun is Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune.'))
parts.append(dict(pi=1,type='definition',
 K=lab('(a)(ii)')+'State the name of the region labelled X on Figure 11.1.',
 B=kwv('asteroidbelt','asteroid','asteroids','thebelt','minorplanets','planetoids'),
 U='asteroid belt',V='The asteroid belt lies between the orbits of Mars and Jupiter.'))
parts.append(dict(pi=2,type='definition',
 K=lab('(a)(iii)')+'State the name of the force that keeps the planets in their orbits around the Sun.',
 B=kwv('gravit','gravity','gravitationalforce','gravitationalattraction'),
 U='gravitational force (gravity)',V='The Sun\'s gravitational attraction provides the centripetal force that keeps each planet in orbit.'))
parts.append(dict(pi=3,type='explain',
 K=lab('(b)')+'Scientists use observations of redshift as evidence that the Universe is expanding.<br><br>Describe how observations of redshift provide evidence for the expansion of the Universe.',
 A=kwv('increaseinwavelength','wavelengthincreases','wavelengthincreased','wavelengthisincreased','wavelengthisgreater','longerwavelength','wavelengthlonger','wavelengthstretched','wavelengthisstretched','stretchedwavelength','shiftedtowardsred','shiftedtowardred','towardstheredend','towardsred','shifttored','shifttowardred','shifttowardsred','redendofthespectrum','longerwavelengths','increasedwavelength','increasedwavelengths','decreaseinfrequency','frequencydecreases','frequencydecrease','lowerfrequency','frequencyislower','frequencyisreduced','frequencygoesdown'),
 B=kwv('light','electromagnetic','radiation','spectrum','spectral','em waves','emwaves','waves'),
 B2=kwv('movingaway','moveaway','movesaway','moveawayfrom','travelingaway','travellingaway','recede','receding','awayfromus','awayfromearth','awayfromtheearth','awayfromeachother','expanding','moving apart','movingapart','moveapart','speedingaway','goingaway','getting further away','gettingfurtheraway','furtheraway','farther away','fartheraway'),
 B3=kwv('moredistant','furtheraway','furthestaway','furtheraway','greaterredshift','moreredshift','greaterdistance','longerwavelengths','fasterspeed','movefaster','movingfaster','moving faster','fastest','faster','thefurther','furthergalaxies','distantgalaxies','furtherthegalaxy','furtherawaythegalaxy','moredistantgalaxies','farther','larger redshift','largerredshift','biggerredshift','greaterspeed'),
 maxMarks='4',
 U='Redshift is an increase in the observed wavelength of light (shifted towards the red end of the spectrum) from distant galaxies. It is caused by the galaxies moving away from us. The more distant the galaxy the greater the redshift, so the further galaxies are moving away faster, which shows the Universe is expanding.',
 V='Light from distant galaxies is observed to have longer wavelengths than expected. The redshift shows the galaxies are moving away, and the greater redshift of more distant galaxies means they are moving away faster.'))
ALL+=question(LV,ID+'-Q11',PAPER,'definition','Space physics',Q11P,Q11G,'Question 11',parts)

if __name__=='__main__':
    start=int(sys.argv[1]) if len(sys.argv)>1 else 596
    import re
    for r in ALL:
        if r['computedValues']:
            g=json.loads(r['computedValues']);rest=' '.join(v for k,v in g.items())+' '.join(str(x) for rr in ALL if rr['id']==r['id'] for x in rr.values())
            for k in list(g):
                if k in ('sf','ex','hd','ln','tx','capf','gsvg') and not re.search(r'(?<![A-Za-z0-9_])'+k+r'\(',' '.join(v for kk,v in g.items() if kk!=k)+' '.join(str(x) for rr in ALL if rr['id']==r['id'] for kk2,x in rr.items() if kk2!='computedValues') + ' '.join(re.sub(r'\$\{','${',v) for v in [''])):
                    del g[k]
            r['computedValues']=json.dumps(g,ensure_ascii=False)
    write_json(ALL,'igcse/new31.json',start=start)
    from collections import Counter
    print(len(ALL),'rows',dict(Counter(r['id'] for r in ALL)))
