const {T,FIX,run}=require('./tpaper31_core.js');
const P='0625-26-41M-';
FIX[P+'Q1']={mp:18,hp:14};
T[P+'Q1']=[
 [0,'the amount of matter in the ball',1],[0,'the quantity of matter',1],[0,'how heavy it is',0],[0,'the force of gravity on it',0],
 [1,'weight',1],[1,'gravitational force',1],[1,'upthrust',0],[1,'mass',0],
 [2,'W = mg = 0.18 x 9.8 = 1.8 N',2],[2,'1.8',2],[2,'1.76',2],[2,'W = mg',1],[2,'0.18',0],
 [3,'Ep = mgh = 0.18 x 9.8 x 1.4 = 2.5 J',2],[3,'mgh',1],[3,'0.18 x 9.8 x 1.4',1],[3,'2.5',0],
 [4,'Ek = 1/2 m v^2; v = sqrt(2 x 2.5/0.18) = 5.3 m/s',3],[4,'5.3',3],[4,'5.2',3],[4,'v = sqrt(2 x 2.5 / 0.18)',2],[4,'ek = 1/2mv2',1],[4,'6.9',0],
 [5,'the direction is different',1],[5,'upwards',1],[5,'it is negative',1],[5,'smaller',0]];
FIX[P+'Q2']={Vp:31,rp:28};
T[P+'Q2']=[
 [0,'87/31 = 2.8 g/cm3',3],[0,'2.8 g/cm3',3],[0,'2800 kg/m3',3],[0,'2.8',0],[0,'87/31',2],[0,'g/cm3',1],[0,'2.8 kg/m3',1],[0,'0.36',0],
 [1,'add water to the measuring cylinder and record the volume. add the sphere and record the new volume. the volume is the difference',3],[1,'fill a eureka can with water, add the sphere, collect the displaced water in a measuring cylinder',3],[1,'weigh it',0],[1,'put water in, drop sphere in, subtract the volumes',3]];
FIX[P+'Q3']={np:1,lp:80,wp:670};
T[P+'Q3']=[
 [0,'move the rope from side to side parallel to the wall',2],[0,'move the rope up and down',1],[0,'shake it',1],[0,'throw it',0],
 [1,'1.5 x 0.80 = 1.2 m',2],[1,'1.2',2],[1,'1.5 wavelengths',1],[1,'0.8',0],[1,'0.53',0],
 [2,'3.0 x 10^8 m/s',1],[2,'3e8',1],[2,'300000000',1],[2,'340',0],
 [3,'f = v/lambda = 3.0e8 / 670e-9 = 4.5e14 Hz',3],[3,'4.5e14 Hz',3],[3,'4.5 x 10^14 Hz',3],[3,'4.5e14',0],[3,'Hz',1],[3,'4.5e11 Hz',1],
 [4,'monochromatic',1],[4,'white',0]];
FIX[P+'Q4']={nrp:0};
T[P+'Q4']=[
 [0,'a force',1],[0,'it attracts or repels',1],[0,'it moves',0],
 [1,['left','right','right'],2],[1,['to the left','right','right'],2],[1,['left','left','right'],2],[1,['right','left','left'],0],
 [2,'weaker',1],[2,'the field is weaker at circle 3',1],[2,'stronger',0],
 [3,['induced','current','the change causing it'],3],[3,['induced','current','the movement of the magnet'],3],[3,['induced','voltage','the movement of the magnet'],2],[3,['','',''],0]];
FIX[P+'Q5']={Kp:296};
T[P+'Q5']=[
 [0,['very fast','randomly','change direction'],3],[0,['quickly','in all directions','move in a different direction'],3],[0,['slowly','randomly','stop'],1],
 [1,'the pressure increases because the particles move faster and collide with the box more often and with more force',3],[1,'pressure increases',1],[1,'the pressure decreases because the particles move slower',0],[1,'pressure increases because the particles move faster',2],
 [2,'296 - 273 = 23 C',1],[2,'23',1],[2,'22.85',1],[2,'22.9',1],[2,'569',0]];
FIX[P+'Q6']={rkp:0};
T[P+'Q6']=[
 [0,['a charge','a force'],2],[0,['charged particle','electrostatic force'],2],[0,['mass','force'],1],
 [1,'positive because opposite charges attract',1],[1,'the sphere is positive as the rod is negative and unlike charges attract',1],[1,'negative because opposite charges attract',0],[1,'positive',0],
 [2,'the sphere is discharged and swings away because electrons move from the rod to the sphere',3],[2,'sphere becomes neutral',1],[2,'sphere swings away. electrons move from the sphere to the rod',2],[2,'it explodes',0]];
FIX[P+'Q7']={Ep:65,Qp:43,tp:18,Rp:25};
T[P+'Q7']=[
 [0,'work done / charge',1],[0,'energy transferred divided by charge',1],[0,'power / time',0],
 [1,'W = EQ = 6.5 x 4300 = 28000 J',2],[1,'28000',2],[1,'28 kJ',2],[1,'6.5 x 4300',1],[1,'W = EQ',1],[1,'2800',0],
 [2,'charge / time',1],[2,'Q/t',1],[2,'work / charge',0],
 [3,'I = 4300 / (1.8 x 60 x 60) = 0.66 A',1],[3,'4300 / 1.8 x 3600',0],[3,'4300/6480',1],[3,'0.66',0],
 [4,'p.d. across resistor = 0.66 x 2.5 = 1.65; motor = 6.5 - 1.65 = 4.9 V',3],[4,'4.9',3],[4,'4.8',3],[4,'6.5 - 0.66 x 2.5',2],[4,'1.65',1],[4,'6.5',0]];
FIX[P+'Q8']={Pp:24,tp:75,cp:34};
T[P+'Q8']=[
 [0,'I = P/V = 1200 / 230 = 5.2 A',2],[0,'5.2',2],[0,'5.22',2],[0,'1200/230',1],[0,'P = IV',1],[0,'276000',0],
 [1,'it protects the user by breaking the circuit when the current is too high',2],[1,'stops the current',1],[1,'cuts off the circuit when the current is too large',2],[1,'it is a switch',0],
 [2,'it can be reset',1],[2,'faster response',1],[2,'it is cheaper',0],
 [3,'E = 1.2 x 0.75 = 0.90 kWh',3],[3,'0.9',3],[3,'0.90',3],[3,'1200 x 0.75',2],[3,'900',2],[3,'1.2',1],[3,'0.5',0],
 [4,'0.90 x 0.34 = $0.31',1],[4,'0.31',1],[4,'0.30',1],[4,'0.34',0],[4,'3.1',0]];
FIX[P+'Q9']={flp:0};
T[P+'Q9']=[
 [0,'3',1],[0,'ray 3',1],[0,'1',0],[0,'2',0],
 [1,'1',1],[1,'4',0],[1,'ray 1',1],
 [2,'both rays refract away from the normal and they spread apart',2],[2,'they diverge',1],[2,'they bend away from the normal',1],[2,'they are reflected',0],
 [3,'infrared and ultraviolet',1],[3,'infrared',0],[3,'x-rays and gamma',0],
 [4,'100000',1],[4,'1e5',1],[4,'100 000 light years',1],[4,'1 million',0],[4,'1000',0],
 [5,'longer wavelength',1],[5,'lower frequency',1],[5,'shorter wavelength',0],[5,'blue',0],
 [6,'the galaxies are moving away and more distant galaxies move away faster',2],[6,'the universe is expanding and galaxies were closer together',2],[6,'the universe is expanding',1],[6,'stars are exploding',0]];
FIX[P+'Q10']={nnp:143,rp:16,vpp:5,npp:12};
T[P+'Q10']=[
 [0,'235/92 U',2],[0,'U-235',2],[0,'²³⁵₉₂U',2],[0,'235',1],[0,'92',1],[0,'U-238',0],
 [1,['neutron','nuclei','fission','water','generator'],3],[1,['neutron','fragments','fission','steam','generator'],3],[1,['proton','nuclei','fusion','water','generator'],3],[1,['neutron','','','',''],1],
 [2,'the current is lower so P = I2R is smaller',2],[2,'lower current and less heating',2],[2,'lower current',1],[2,'the resistance is lower',0],[2,'less heat is lost',1],
 [3,'Ns = 240 x 400000 / 25000 = 3840',2],[3,'3840',2],[3,'3800',2],[3,'240 x 400000/25000',1],[3,'0.0625',0]];
run(process.argv[2]||'igcse/new41.json',process.argv[3]);
