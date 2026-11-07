const {T,FIX,run}=require('./tpaper31_core.js');
const P='0625-26-31M-';
FIX[P+'Q1']={vp:8,t1p:4,t2p:12,Tp:20,vsp:10};
T[P+'Q1']=[
 [0,'area under graph = 1/2 x 4 x 8 = 16 m',3],[0,'16',3],[0,'0.5 x 4 x 8',2],[0,'area under the graph',1],[0,'32',1],[0,'8',0],[0,'distance = speed x time',1],
 [1,'the speed increases',1],[1,'it is accelerating',1],[1,'constant',0],[1,'decreases',0],
 [2,'the speed is constant',1],[2,'steady at 8 m/s',1],[2,'it increases',0],
 [3,'200/20 = 10 m/s',3],[3,'10',3],[3,'200 / 20',2],[3,'speed = distance / time',1],[3,'4000',0]];
FIX[P+'Q2']={np:2,Vp:1,rp:2};
T[P+'Q2']=[
 [0,'Use a ruler to measure the height of the stack of discs and divide by 8',3],[0,'measure the thickness of the stack with a ruler. divide by the number of discs',3],[0,'measure one disc with a ruler',1],[0,'divide by 8',1],[0,'weigh them',0],
 [1,'density = mass/volume = 50/20 = 2.5 g/cm3',3],[1,'2.5',3],[1,'50/20',2],[1,'density = mass / volume',1],[1,'1000',0]];
FIX[P+'Q3']={Fp:16.5,Ap:12,Wp:12};
T[P+'Q3']=[
 [0,'A has a lower centre of gravity and a larger base',2],[0,'A is wider',1],[0,'A has a bigger base and needs to be tilted more before it topples',2],[0,'B is taller',0],
 [1,'64/12 = 5.3 N/cm2',3],[1,'5.3',3],[1,'5.33',3],[1,'64/12',2],[1,'force / area',1],[1,'768',0],[1,'5',0],
 [2,'upward drag force of 1.2 N',2],[2,'friction, 1.2 N',2],[2,'drag',1],[2,'1.2',1],[2,'gravity 1.2 N',1]];
FIX[P+'Q4']={Ip:12,Vp:24,tp:6};
T[P+'Q4']=[
 [0,'kinetic',1],[0,'thermal',0],[0,'gravitational',0],
 [1,'E = 1.2 x 24 x 30 = 864 J',3],[1,'860',3],[1,'864',3],[1,'900',3],[1,'1.2 x 24 x 30',2],[1,'e = ivt',1],[1,'28.8',1],[1,'86',0],
 [2,'thermal energy is transferred to the surroundings',2],[2,'heat is lost due to friction',2],[2,'sound',1],
 [3,'The fuel is burnt to heat water. Steam is produced which turns a turbine. The turbine drives a generator.',4],[3,'burn fuel, boils water, turbine, generator',4],[3,'coal is burnt',1],[3,'nuclear fission heats water to steam, turbine, generator',3],
 [4,'pollution and non-renewable',2],[4,'releases carbon dioxide, will run out',2],[4,'it is expensive',0],[4,'pollution',1],[4,'acid rain and global warming',1]];
FIX[P+'Q5']={Tp:24};
T[P+'Q5']=[
 [0,'The air expands and becomes less dense',2],[0,'less dense',1],[0,'the hot air is lighter',0],[0,'air particles move apart and density decreases',2],
 [1,'The particles move fast and collide with the balloon, exerting a force. pressure = force/area',3],[1,'particles collide with the surface',1],[1,'the particles are hot',0],
 [2,'120 + 273 = 393 K',2],[2,'393',2],[2,'393.15',2],[2,'390',2],[2,'120',0],[2,'+273',1],[2,'-153',0]];
FIX[P+'Q6']={fp:73.5};
T[P+'Q6']=[
 [0,'wavelength',1],[0,'frequency',0],[0,'energy',0],
 [1,'perpendicular to the direction of travel of the wave',2],[1,'at right angles to the direction of wave propagation',2],[1,'at right angles',1],[1,'parallel to the direction of travel',0],
 [2,'3.0e8 / 7.3e15 = 4.1e-8 m',3],[2,'4.1e-8',3],[2,'4.11 x 10^-8',3],[2,'3.0e8/7.3e15',2],[2,'v = f lambda',1],[2,'2.4e22',0],
 [3,'treatment of cancer',1],[3,'sterilising equipment',1],[3,'x-rays',0],[3,'cooking food',0],
 [4,'damage to cells which can cause cancer',1],[4,'mutation',1],[4,'it makes you hot',0]];
FIX[P+'Q7']={ap0:60,cp:38,dp:2};
T[P+'Q7']=[
 [0,'30',1],[0,'90 - 60 = 30 degrees',1],[0,'60',0],[0,'45',0],
 [1,'angle of refraction',1],[1,'refraction',1],[1,'angle of incidence',0],
 [2,'the angle of incidence for which the angle of refraction is 90 degrees',1],[2,'angle of incidence at which the refracted ray travels along the surface',1],[2,'the angle at which light is reflected',0],[2,'the angle of incidence',0],
 [3,'total internal reflection',1],[3,'it is reflected',1],[3,'it is refracted out',0]];
FIX[P+'Q8']={Vq:39,Iq:60};
T[P+'Q8']=[
 [0,'in parallel with the lamp',2],[0,'in parallel',1],[0,'across the lamp',2],[0,'in series with the lamp',0],
 [1,'3.9 / 0.60 = 6.5 ohm',3],[1,'6.5',3],[1,'3.9/0.6',2],[1,'v = i r',1],[1,'2.3',0],
 [2,'The lamp is dimmer because the total resistance increases so the current decreases',3],[2,'dimmer',1],[2,'the current decreases and the lamp gets dimmer',2],[2,'brighter',0],[2,'the lamp is brighter because the current increases',0]];
FIX[P+'Q9']={nlp:1,pkp:0,dwp:0};
T[P+'Q9']=[
 [0,'north',1],[0,'south',0],[0,'north pole',1],
 [1,'the soft iron becomes an induced magnet and the end P becomes a north pole. Unlike poles attract',2],[1,'induced magnet, opposite poles attract',2],[1,'it is magnetic',0],[1,'induced magnet',1],
 [2,'move the magnet faster and use more turns',2],[2,'use a stronger magnet, more turns on the coil',2],[2,'move the magnet faster',1],[2,'use a bigger coil',0],
 [3,'move the south pole out of the coil, reverse the connections to the ammeter',2],[3,'push the north pole in',1],[3,'move the south pole out and push the north pole in',2],[3,'move it faster',0]];
FIX[P+'Q10']={np:0};
T[P+'Q10']=[
 [0,'95',1],[0,'146',0],[0,'241',0],
 [1,'146',1],[1,'95',0],
 [2,'242/95 Am',1],[2,'Am-242',1],[2,'²⁴²₉₅Am',1],[2,'242 95 Am',1],[2,'Am-241',0],[2,'241/95 Am',0],
 [3,'alpha is stopped by paper but beta passes through',1],[3,'alpha cannot pass through paper, beta can pass through',1],[3,'beta is stopped by paper but alpha passes through',0],[3,'alpha can pass through paper but beta cannot',0],[3,'both are stopped',0]];
FIX[P+'Q11']={pp:0};
T[P+'Q11']=[
 [0,'x',0],
 [1,'asteroid belt',1],[1,'asteroids',1],[1,'kuiper belt',0],
 [2,'gravitational force',1],[2,'gravity',1],[2,'magnetic force',0],
 [3,'Redshift is an increase in wavelength of light from distant galaxies. The galaxies are moving away from us. The more distant galaxies show more redshift so they are moving away faster.',4],
 [3,'the light from galaxies is red shifted',1],[3,'wavelength increases because galaxies are moving away',2],[3,'the stars are moving closer',0]];
run(process.argv[2]||'igcse/new31.json',process.argv[3]);
