const fs=require('fs');const load=require('/home/claude/physics-site/tools/harness.js');
const h=load('/home/claude/physics-site/scripts');
const rows=JSON.parse(fs.readFileSync(process.argv[2]||'new42m.json','utf8'));
const P='9702-26-42M-';
const FIX={};
FIX[P+'Q1']={vp:2.4,wp:0.75};
FIX[P+'Q2']={poli:0.5,Vp:4800,xp:0.024,nqp:3.5,cip:0.5};
FIX[P+'Q3']={mip:15.6,tip:18,mwp:132.4,twp:34};
FIX[P+'Q4']={kk:4.5,pp:2.0,v2p:0.012,t1p:560,u2p:3.6};
FIX[P+'Q5']={vp:0.46,np:1.6,gip:0.5};
FIX[P+'Q6']={ap:3.2,wp:6.9,bp:0.047,hp:6.0,dp:4.0,cip:0.5};
FIX[P+'Q7']={rp:26,pp:6.4,tp:1.5,cip:0.5};
FIX[P+'Q8']={dp:6.7,hp:2.1,cip:3.5};
FIX[P+'Q9']={thp:12.0,ap:5.8,tp:20.0,cip:1.5};
FIX[P+'Q10']={zap:4.39,zwp:1.49,zgp:9.98,rp:998};
const T={};
T[P+'Q1']=[
 [0,'angle subtended at the centre of a circle when the arc length equals the radius',1],[0,'angle',0],[0,'the angle in degrees',0],
 [1,'v = rω so r = 2.4/0.75 = 3.2 m',2],[1,'3.2',2],[1,'3.20',2],[1,'1.8',0],[1,'r = v/ω',1],
 [2,'f = ω/2π = 0.75/2π = 0.12 Hz',2],[2,'0.12',2],[2,'0.119',2],[2,'0.75',0],[2,'ω = 2πf',1],
 [3,'a = rω² = (2/3 × 3.2) × 0.75² = 1.2 m s-2',2],[3,'1.2',2],[3,'1.20',2],[3,'1.8',0],[3,'a = rω^2',1]];
T[P+'Q2']=[
 [0,'force per unit positive charge',1],[0,'force',0],[0,'force per unit mass',0],
 [2,'The weight acts downwards so the electric force is upwards, the field is upwards so Q is positive',2],[2,'positive',0],[2,'negative',0],[2,'the weight is balanced by an upward electric force',1],
 [3,'E = V/x',1],[3,'V/x',1],[3,'Qx/V',0],
 [4,'W = QV/x',1],[4,'QV/x',1],[4,'Q/Vx',0],
 [5,'mg = QV/x; m = 3 × 1.6e-19 × 4800/(0.024 × 9.81) = 9.8e-15 kg',2],[5,'9.8e-15',2],[5,'9.79e-15',2],[5,'9.8e-14',0],[5,'mg = QE',1],
 [6,'both forces now act downwards so the droplet accelerates downwards',2],[6,'it falls',1],[6,'it accelerates upwards',0]];
T[P+'Q3']=[
 [0,'The energy per unit mass to change a solid to a liquid without a change in temperature',2],[0,'energy per unit mass',1],[0,'energy required to melt a solid',0],
 [1,'the volume change is greater so more work is done against the atmosphere',2],[1,'work against the atmosphere',1],[1,'less friction',0],
 [2,'21',4],[2,'21.0',4],[2,'20',0],[2,'Q = mcΔθ',1],[2,'energy lost by water = energy gained by ice',2],[2,'15.6 × 336 = 5240',3]];
T[P+'Q4']=[
 [0,'ΔU is the increase in internal energy of the system, Q is the thermal energy transferred to the system',2],[0,'change in internal energy',1],[0,'Q is heat',0],
 [1,'W = pΔV = 2.0e5 × (0.048 − 0.012) = 7200 J',2],[1,'7200',2],[1,'p ΔV',1],[1,'14400',0],
 [2,'positive because the gas is compressed',1],[2,'negative',0],[2,'positive',0],
 [3,'volume is proportional to temperature so T quarters; U is proportional to temperature so U quarters',2],[3,'V ∝ T',1],[3,'the gas is compressed',0],
 [4,'Q = ΔU − W = (3.6 − 14.4) − 7.2 = −18.0 kJ',2],[4,'-18.0 kJ',2],[4,'-18000 J',2],[4,'18.0',1],[4,'Q = ΔU − W',1]];
T[P+'Q5']=[
 [0,'number of particles per mole',1],[0,'the number of atoms in one mole of carbon-12',1],[0,'number of moles',0],
 [1,'ideal gas; V = 0.46 m3; mass of molecule = 6.6e-27 kg',3],[1,'V = 0.46',1],[1,'the gas is ideal',1],[1,'it is helium; 1.6e24 molecules',2],[1,'V = 0.9',0],[1,'p is proportional to NT',1],
 [2,'yes because the gas is ideal',1],[2,'no',0],
 [3,'random motion of molecules; elastic collisions',2],[3,'elastic collisions',1],[3,'molecules have no volume',0],[3,'no intermolecular forces except during collisions',1]];
T[P+'Q6']=[
 [0,'acceleration proportional to displacement and in the opposite direction',2],[0,'acceleration is proportional to displacement',1],[0,'oscillation with constant period',0],
 [1,'T = 2π/ω = 2π/6.9 = 0.91 s',2],[1,'0.91',2],[1,'0.911',2],[1,'1.1',0],[1,'T = 2π/ω',1],
 [2,'v0 = ωx0 = 6.9 × 3.2 = 22 mm/s',2],[2,'22',2],[2,'22.1',2],[2,'2.2',0],[2,'v = ωx0',1],
 [3,'E = Blv = 0.047 × 2×0.060 × 0.022 = 1.2e-4 V',3],[3,'1.2e-4',3],[3,'1.2 × 10^-4',3],[3,'1.2e-5',0],[3,'E = BLv',1]];
T[P+'Q7']=[
 [0,'the direct current that dissipates the same mean power in a resistor',2],[0,'direct current',1],[0,'the square root of the mean of the squares',2],[0,'maximum value of current',0],
 [1,'3.2',1],[1,'3.20',1],[1,'6.4',0],[1,'1.6',0],
 [2,'P = I²R so I = sqrt(3.2/26) = 0.35 A',2],[2,'0.35',2],[2,'0.351',2],[2,'0.25',0],[2,'P = I^2 R',1],
 [3,'diode',1],[3,'rectifier',0],[3,'transistor',0],
 [5,'the mean power is halved, I = 0.25 A',2],[5,'0.25',1],[5,'power halves',1],[5,'0.35',0]];
T[P+'Q8']=[
 [0,'photons have discrete energies; photon energy is the difference between electron energy levels; so energy levels are discrete',3],[0,'photons have discrete energy',1],[0,'electron energy levels are discrete',1],[0,'the atom is excited',0],
 [1,'the galaxy is receding so the light is redshifted and the wavelength is longer',2],[1,'redshift',1],[1,'receding',1],[1,'blueshift',0],
 [3,'v = H0 d = 2.1e-18 × 6.7e24 = 1.4e7; Δλ = 656 × 1.4e7/3e8 = 31; 687 nm',3],[3,'687',3],[3,'686.8',3],[3,'31',2],[3,'1.4e7',1],[3,'656',0]];
T[P+'Q9']=[
 [0,'spontaneous emission of radiation from an unstable nucleus',2],[0,'random',0],[0,'spontaneous',1],
 [1,'λ = ln2/(12.0×60) = 9.63e-4 s-1',2],[1,'9.63e-4',2],[1,'0.0578 min-1',2],[1,'ln2/t',1],[1,'5.8e-14',0],
 [2,'A = A0 e^(-λt) = 5.8e14 × e^(-9.63e-4×1200) = 1.8e14',2],[2,'1.83e14',2],[2,'1.8e14',2],[2,'1.83e13',0],[2,'A = A0 e^(-λt)',1],
 [4,'radiation is emitted in all directions and some is absorbed in the air and some absorbed by the detector window',3],[4,'emitted in all directions',1],[4,'background radiation',0]];
T[P+'Q10']=[
 [0,'the ultrasound makes the crystal vibrate and an alternating e.m.f. is induced across it',2],[0,'crystal vibrates',1],[0,'absorbs sound',0],
 [1,'the product of density and the speed of sound in the medium',2],[1,'density × speed of sound',2],[1,'density',0],[1,'ρc',2],
 [2,'Z = ρc so c = 1.49e6/998 = 1490 m/s',2],[2,'1490',2],[2,'1493',2],[2,'1.49e6',0],[2,'Z = ρc',1],
 [3,'0.548',2],[3,'0.74',0],[3,'(Z2 - Z1)²/(Z2+Z1)²',1],
 [4,'the impedances are very different so the reflection coefficient is close to 1 so almost all of the sound is reflected and almost none is transmitted',4],[4,'most of the sound is reflected',1],[4,'it is absorbed',0]];
const score=(q,i,txt)=>{const p=q.parts[i];p.marks.forEach(m=>m.awarded=false);h.win.currentParts=q.parts;h.win.applyCieMarking(p.marks,txt);return [p.marks.filter(m=>m.awarded).length,p.marks.length]};
let bad=0,n=0;
for(const id in FIX){
  const rs=rows.filter(r=>r.id===id);
  const q=h.win.genericBuilder({id,type:'x',params:FIX[id],parts:rs.map(r=>Object.assign({},r))});
  const sorted=rs.slice().sort((a,b)=>+a.partIndex-+b.partIndex);
  for(const [pi,ans,exp] of (T[id]||[])){
    const i=sorted.findIndex(r=>+r.partIndex===pi);const [g,t]=score(q,i,ans);n++;
    if(g!==exp){bad++;console.log('MISMATCH',id.slice(-2),'pi'+pi,'got',g+'/'+t,'expected',exp,'|',ans.slice(0,80));}
  }
}
console.log('checked',n,'mismatches',bad);
if(process.argv[3]){for(const id in FIX){const rs=rows.filter(r=>r.id===id);const q=h.win.genericBuilder({id,type:'x',params:FIX[id],parts:rs.map(r=>Object.assign({},r))});
 console.log('\n=====',id);q.parts.forEach((p,i)=>console.log('['+i+']',(p.partText||p.text||'').replace(/<svg[\s\S]*?<\/svg>/g,'[SVG]').replace(/<[^>]+>/g,'').slice(0,600),'\n   MODEL:',String(p.modelAnswer).replace(/<[^>]+>/g,'').slice(0,300),'| marks',p.marks.length));}}
