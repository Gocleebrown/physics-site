// MS-quality / partial / wrong answers at the real paper's values.  node tpaper23.js new23.json
const fs=require('fs');const load=require('/home/claude/physics-site/tools/harness.js');
const h=load('/home/claude/physics-site/scripts');
const rows=JSON.parse(fs.readFileSync(process.argv[2]||'new23.json','utf8'));
const FIX={
'9702-26-23-Q1':{mxp:0.15,up:1.6,wp:0.8,tAp:9,dtp:3},
'9702-26-23-Q2':{mp:0.018,Anp:2.6,rhop:960,Enp:8.0},
'9702-26-23-Q3':{lamp:560,a5p:1.4,Dp:0.43},
'9702-26-23-Q4':{Ep:4.90,Rp:230,rp:5.8},
'9702-26-23-Q5':{A_p:18,pair_p:2}};
// [partIndex, answer, expected marks]
const T={
'9702-26-23-Q1':[
 [0,'product of mass and velocity',1],[0,'mass x speed',0],[0,'force x time',0],
 [1,'a = (-0.8 - 1.6)/(0.12-0.09) = -80, so 80 m s-2',2],[1,'80',2],[1,'-80 m/s2',2],[1,'a = (v-u)/t',1],[1,'2.4',0],[1,'800',0],
 [2,'change in momentum = 0.15 × (-0.8 - 1.6) = -0.36, magnitude 0.36 kg m s-1',2],[2,'0.36',2],[2,'-0.36',2],[2,'0.15 × 1.6 = 0.24',1],[2,'0.12',0],
 [3,'0.016 + 0.004 = 0.020 m',2],[3,'0.02',2],[3,'0.020',2],[3,'0.12',0],
 [4,'relative speed of approach = relative speed of separation. speed of separation is 1.6 so vY - (-0.80) = 1.6, vY = 0.80',2],[4,'relative speed of approach equals relative speed of separation',1],[4,'vY = 1.6/2 = 0.8',0],
 [6,'0.15 × 1.6 = 0.15 × (-0.80) + 0.80m, m = 0.45 kg',2],[6,'0.45',2],[6,'0.15 × 1.6 = 0.15 × (-0.80) + 0.80m',1],[6,'0.30',0],[6,'0.15',0]],
'9702-26-23-Q2':[
 [0,'stress per unit strain',1],[0,'stress divided by strain',1],[0,'stress / strain',1],[0,'force per unit area',0],[0,'stiffness',0],
 [1,'density = m/V so V = 0.018/960 = 1.875e-5; L = V/A = 1.875e-5/2.6e-6 = 7.2 m',2],[1,'L = 0.018 / (960 × 2.6 × 10^-6) = 7.2 m',2],[1,'7.2 m',0],
 [2,'stress = F/A = (0.018 × 9.81) / (2.6 × 10^-6) = 6.8 × 10^4 Pa',2],[2,'stress = force / area',1],[2,'6.8e4',0],
 [3,'The weight of thread below a point decreases as the distance from the top increases. The cross-section is uniform so the stress is proportional to the weight below the point.',2],
 [3,'weight decreases with distance',1],[3,'because it is a straight line',0],
 [4,'x = σL/E = 7.2 × 6.8e4 / 8.0e8 = 6.1 × 10^-4 m',2],[4,'6.12e-4',2],[4,'0.00061',2],[4,'6.1',0],[4,'E = σ/ε',1],
 [5,'E = ½Fx = 0.5 × 6.8e4 × 2.6e-6 × 6.1e-4 = 5.4 × 10^-5 J',2],[5,'5.4e-5',2],[5,'5.39e-5',2],[5,'½Fx',1],[5,'5.4',0],
 [6,'less, because the stress in the vertical thread is less except at the top',1],[6,'greater because the stress is greater',0],[6,'equal because the force is the same',0],[6,'less',0]],
'9702-26-23-Q3':[
 [0,'when two waves meet, the resultant displacement is the sum of the individual displacements',2],[0,'waves meet and the resultant displacement is the sum of the displacements of each wave',2],[0,'two waves meet',1],[0,'the resultant amplitude is the sum of the amplitudes',0],
 [1,'constant phase difference',1],[1,'same frequency',0],[1,'in phase',0],
 [2,'the light diffracts',1],[2,'it spreads out',0],
 [3,'waves from each slit meet at X and superpose. The path difference is zero so they are in phase. Constructive interference gives maximum amplitude',3],
 [3,'constructive interference',1],[3,'the waves are in phase so bright',1],[3,'destructive interference',0],
 [4,'x = λD/a = 560e-9 × 0.43 / 1.4e-5 = 0.017, XY = 0.017/2 = 0.0086 m',3],[4,'0.0086',3],[4,'0.0085',3],[4,'8.6e-3',3],[4,'0.017',1],[4,'0.0172',1],[4,'0.017 m',1],
 [7,'c = fλ, f = 3.00e8 / 560e-9 = 5.4 × 10^14 Hz',2],[7,'5.36e14',2],[7,'5.4e14',2],[7,'5.4e8',0],[7,'1.9e-15',0]],
'9702-26-23-Q4':[
 [1,'zero error',1],[1,'calibration error',1],[1,'contact resistance in connections',1],[1,'parallax error',0],[1,'the voltmeter is not accurate',0],
 [2,'P = V^2/R = 4.78^2/230 = 0.099 W',2],[2,'0.099',2],[2,'0.0993',2],[2,'0.1',0],[2,'1.1',0],
 [3,'E = V + Ir; I = 4.78/230; r = (4.90 - 4.78)/(4.78/230) = 5.8 ohm',2],[3,'5.8',2],[3,'5.77',2],[3,'0.12',0],[3,'E = V + Ir',1]],
'9702-26-23-Q5':[
 [0,'one quark and one antiquark',1],[0,'a quark and an antiquark',1],[0,'two quarks',0],[0,'three quarks',0],
 [1,'quark charges are +2/3e and -1/3e. -1e: ddd (-1/3 each). +2e: uuu (+2/3 each)',3],[1,'ddd and uuu',2],[1,'-1e: three down; +2e: three up',2],
 [2,'P = 18, Q = 8, R = 0, S = 1',2],[2,'P = 18 Q = 8 R = 0 S = +1',2],[2,'P=18, Q=8',1],[2,'P=18 Q=9 R=0 S=-1',0],[2,'18 7 0 1',0],
 [3,'electron neutrino',1],[3,'neutrino',1],[3,'antineutrino',0],[3,'electron',0],[3,'the neutrino',1],[3,'νe',1],[3,'an electron antineutrino',0],
 [4,'up to down',1],[4,'one up quark changes to a down quark',1],[4,'down to up',0],
 [5,'total energy is constant. Z takes some of the energy so the energy is shared between Z and the positron differently each time',2],
 [5,'the neutrino takes some of the energy',1],[5,'because of the different masses',0]]};
const score=(q,i,txt)=>{const p=q.parts[i];p.marks.forEach(m=>m.awarded=false);h.win.currentParts=q.parts;h.win.applyCieMarking(p.marks,txt);return [p.marks.filter(m=>m.awarded).length,p.marks.length]};
let bad=0,n=0;
for(const id in FIX){
  const rs=rows.filter(r=>r.id===id);
  const q=h.win.genericBuilder({id,type:'x',params:FIX[id],parts:rs.map(r=>Object.assign({},r))});
  const sorted=rs.slice().sort((a,b)=>+a.partIndex-+b.partIndex);
  for(const [pi,ans,exp] of T[id]){
    const i=sorted.findIndex(r=>+r.partIndex===pi);const [g,t]=score(q,i,ans);n++;
    if(g!==exp){bad++;console.log('MISMATCH',id,'pi'+pi,'got',g+'/'+t,'expected',exp,'|',ans.slice(0,70));}
  }
}
console.log('checked',n,'mismatches',bad);
// print the question text at the paper's values for reading
if(process.argv[3]){for(const id in FIX){const rs=rows.filter(r=>r.id===id);const q=h.win.genericBuilder({id,type:'x',params:FIX[id],parts:rs.map(r=>Object.assign({},r))});
 console.log('\n=====',id);q.parts.forEach((p,i)=>console.log('['+i+']',(p.partText||p.text||'').replace(/<svg[\s\S]*?<\/svg>/g,'[SVG]').replace(/<[^>]+>/g,'').slice(0,600),'\n   MODEL:',String(p.modelAnswer).replace(/<[^>]+>/g,'').slice(0,300)));}}
