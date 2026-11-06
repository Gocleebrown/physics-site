const fs=require('fs');const load=require('/home/claude/physics-site/tools/harness.js');
const h=load('/home/claude/physics-site/scripts');
const rows=JSON.parse(fs.readFileSync(process.argv[2]||'new22m.json','utf8'));
const P='9702-26-22M-';
const FIX={};
FIX[P+'Q1']={kei:0.5};
FIX[P+'Q2']={Mp:160,mp:23,up:3.4,rp:1015};
FIX[P+'Q3']={mp:280,KExp:16.1,KEyp:1.3,sp:23,Wp:5.1};
FIX[P+'Q4']={wp:19,rp:0.73,dp:0.80,Ep:9.3,hp:1.6,cip:0.5};
FIX[P+'Q5']={kLp:32.5,fp:25,nip:1.5,lgp:4.5,Nf:0.84,cip:0.5};
FIX[P+'Q6']={ei:1.5,ri:3.5,Rwp:0.82,Rp:0.09,Lp:6.8,Ap:2.0,cip:0.5};
FIX[P+'Q7']={Zp:92,kap:0.5,kbp:1.5,pip:0.5};
const T={};
T[P+'Q1']=[
 [0,'rate of change of momentum',1],[0,'change in momentum per unit time',1],[0,'mass × acceleration',0],[0,'momentum',0],
 [1,'momentum = kg m s^-1, force = (kg m s^-1)/s = kg m s^-2',1],[1,'kg m s-1 / s = kg m s-2',1],[1,'F = ma = kg m s^-2',0],
 [2,'F = kg m s^-2, m = kg, A = m^2. RHS = kg m s^-2 × m^2 s^-1 / (kg m^2) = m s^-3. LHS = m s^-1. Not homogeneous.',2],
 [2,'not homogeneous because RHS has units m s^-3 but LHS is m s^-1',2],[2,'the equation is homogeneous',0],[2,'It is homogeneous because both sides are m s^-1',0],[2,'F = kg m s^-2',1]];
T[P+'Q2']=[
 [0,'The total momentum of a system is constant provided there is no external force (isolated system)',2],[0,'total momentum before = total momentum after',1],[0,'momentum is conserved',0],[0,'no external forces',1],
 [1,'23 × 3.4 = (160 + 23) v; v = 0.43 m s-1',2],[1,'0.43',2],[1,'0.427',2],[1,'0.4',0],[1,'0.55',0],[1,'mu = (M+m)v',1],
 [2,'E1 = 1/2 × 23 × 3.4^2 = 133 J; E2 = 1/2 × 183 × 0.43^2 = 17 J; ratio = 0.13',3],[2,'0.13',3],[2,'0.126',3],[2,'0.127',3],[2,'0.5',0],[2,'1/2 m v^2',1],
 [3,'inelastic because the kinetic energy after is less than before',1],[3,'inelastic',0],[3,'elastic because kinetic energy is conserved',0],[3,'inelastic, kinetic energy is lost',1],
 [4,'upthrust = weight = (160 + 23) × 9.81 = 1795 = 1800 N',1],[4,'183 × 9.81 = 1800',1],[4,'1800',0],
 [5,'density = 183 / (1.80e5 × 1e-6) = 1.02 × 10^3 kg m-3',2],[5,'1020',2],[5,'1017',2],[5,'1.02e3',2],[5,'1000',0],[5,'1.02',0],[5,'m/V',1]];
T[P+'Q3']=[
 [0,'F = W/d = 5.1e3/23 = 220 N',2],[0,'220',2],[0,'222',2],[0,'0.22',0],[0,'work = force × distance',1],
 [1,'Ep = 16.1 - 1.3 - 5.1 = 9.7 kJ; E = mgh; h = 9700/(280 × 9.81) = 3.5 m',3],[1,'3.5',3],[1,'3.53',3],[1,'9.7',2],[1,'35',0],[1,'0.035',0],
 [2,'speed at Z is less than at X because work is done against resistive forces so kinetic energy is lost',1],[2,'less because of resistive forces',1],[2,'less',0],[2,'faster because there is less friction',0],[2,'same',0]];
T[P+'Q4']=[
 [0,'force × perpendicular distance from the pivot',1],[0,'force times perpendicular distance',1],[0,'force',0],
 [1,'the line of action of the weight passes through P so the perpendicular distance is zero',1],[1,'perpendicular distance is zero',1],[1,'the weight is small',0],
 [2,'2T sinθ = W; sinθ = 19/(2 × 13); θ = 47°',2],[2,'47',2],[2,'46.9',2],[2,'0.73',1],[2,'43',0],
 [3,'A = π(0.4e-3)^2 = 5.0e-7; stress = 13/5.0e-7 = 2.6e7; strain = 2.6e7/9.3e10 = 2.8e-4',3],[3,'2.8e-4',3],[3,'2.8 × 10^-4',3],[3,'2.8e-5',0],[3,'strain = stress / E',1],
 [4,'s = 1/2 g t^2; t = sqrt(2 × 1.6/9.81) = 0.57 s',2],[4,'0.57',2],[4,'0.571',2],[4,'0.33',0]];
T[P+'Q5']=[
 [0,'time taken for one complete oscillation',1],[0,'time for one cycle',1],[0,'frequency',0],
 [1,'maximum displacement from the equilibrium position',1],[1,'maximum displacement',1],[1,'distance from peak to trough',0],
 [3,'λ = 2 × 0.96 / 3 = 0.64 m; v = fλ = 25 × 0.64 = 16 m s-1',3],[3,'v = fλ = 25 × 0.64 = 16',3],[3,'25 × 0.96 × 2/3 = 16',3],[3,'v = fλ',1],[3,'16',0],
 [4,'λ = v/f = 16/30 = 0.53 m. 2L/λ = 3.6 which is not a whole number, so no stationary wave',2],[4,'0.53',1],[4,'0.53 m, a stationary wave is formed since there are a whole number of half wavelengths',1],[4,'a stationary wave is formed',0],
 [5,'d = 1/6.7e5 = 1.5e-6 m; n = d sinθ / λ = 1.5e-6 × sin 37.1 / 4.5e-7 = 2.0',3],[5,'2',3],[5,'2.0',3],[5,'1.996',3],[5,'1.6',0],[5,'3',0],[5,'d sinθ = nλ',1],
 [6,'decreases',1],[6,'the distance between spots gets smaller',1],[6,'increases',0]];
T[P+'Q6']=[
 [0,'the rate of flow of charge',1],[0,'flow of charge carriers',1],[0,'flow of electrons',1],[0,'voltage',0],
 [2,'ρ = RA/L = 0.82 × 2.0e-7 / 6.8 = 2.4e-8 Ω m',2],[2,'2.4e-8',2],[2,'2.41 × 10^-8',2],[2,'2.4e-7',0],[2,'ρ = RA/L',1],
 [3,'V = 1.50 - 1.8 × 0.75 = 0.15 V; I in X = 0.15/0.82 = 0.18 A; I in R = 1.8 - 0.18 = 1.6 A; R = 0.15/1.6 = 0.093 Ω',3],[3,'0.093',3],[3,'0.0928',3],[3,'0.09',3],[3,'0.15',2],[3,'0.93',0],[3,'0.82',0],
 [4,'P = I^2 r = 1.8^2 × 0.75 = 2.4 W',2],[4,'2.4',2],[4,'2.43',2],[4,'P = IV',1],[4,'4.9',0]];
T[P+'Q7']=[
 [0,'a nucleus containing protons and neutrons, surrounded by electrons',2],[0,'a nucleus of protons and neutrons',1],[0,'electrons orbit the nucleus',1],[0,'electrons',0],
 [1,'alpha',1],[1,'α-particle',1],[1,'beta-minus',0],[1,'beta',0],[1,'positron',0],
 [2,'beta-minus',1],[2,'β-',1],[2,'electron',1],[2,'beta-plus',0],[2,'alpha',0],[2,'positron',0],
 [3,'mass = 1.60e-19 / 1.76e11 = 9.09e-31 kg; X is a positron',2],[3,'9.09e-31, positron',2],[3,'9.09e-31',1],[3,'positron',1],[3,'electron',0],[3,'9.1e-31 kg, a positron',2],[3,'1.67e-27, proton',0]];
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
