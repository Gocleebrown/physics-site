const fs=require('fs');const load=require('/home/claude/physics-site/tools/harness.js');
const h=load('/home/claude/physics-site/scripts');
const rows=JSON.parse(fs.readFileSync('new21.json','utf8'));
const FIX={ '9702-26-21-Q1':{M6:2.83,r4:2.0,a0:2.5,tbp:60},'9702-26-21-Q2':{mp:0.086,xp:0.026,dp:0.015},'9702-26-21-Q3':{Tp:0.24,vp:75,ppp:24},'9702-26-21-Q4':{rho0p:1.57,alp:4.2,thp:20,Lp:2.0,dp:0.60,Ip:5.6,np:8.5},'9702-26-21-Q5':{sp:0.5}};
// MS-quality answers by partIndex
const ANS={
'9702-26-21-Q1':{0:'Force is the rate of change of momentum',1:'The mass of the rocket decreases as fuel is burnt, thrust is constant so acceleration increases',2:'Find the gradient of the tangent drawn at t = 0',3:'F = ma, T - mg = ma, T = 2.83 × 10^6 × (2.5 + 9.81) = 3.5 × 10^7 N',4:'v = 362 m/s; m = 2.83e6 - 60 × 2.0e4 = 1.63 × 10^6 kg; Ek = ½mv² = ½ × 1.63e6 × 362² = 1.1 × 10^11 J',5:'height is the area under the graph; counting squares gives 8000 m',6:'F = Δp/Δt so T = (m/t) v; v = 3.5e7 / 2.0e4 = 1800 m s-1'},
'9702-26-21-Q2':{0:'force per unit extension',1:'parallax error when reading the ruler',2:'k = mg/x = 0.086 × 9.81 / 0.026 = 32 N m-1',3:'E = ½Fx = ½ × 0.086 × 9.81 × 0.026 = 0.011 J',4:'E = ½kx² = ½ × 32 × 0.041² = 0.027 J; additional = 0.027 - 0.011 = 0.016 J',5:'change in GPE = mgh = 0.086 × 9.81 × 0.015 = 0.013 J; KE = 0.016 - 0.013 = 0.003 J',6:'some energy is used for plastic deformation of the spring so the additional energy is less'},
'9702-26-21-Q3':{0:'a wave that transfers energy',1:'v = λ/T, λ = 36/2 = 18 cm, T = 18/75 = 0.24 s',3:'the wave is reflected at the wall; the incident and reflected waves superpose'},
'9702-26-21-Q4':{0:'potential difference per unit current',1:'A = π(0.30e-3)² = 2.8 × 10^-7 m²',2:'R = ρL/A = 1.7e-8 × 2.0 / 2.8e-7 = 0.12 Ω',3:'R = ρL/A so resistivity is lower; so temperature is less than 20 °C',4:'resistance of a thermistor decreases with temperature',5:'K-1',6:'α = (2.37 - 1.57) / (1.57 × 120) = 0.0042 K-1',7:'I = Anvq; v = 5.6/(2.8e-7 × 8.5e28 × 1.6e-19) = 1.5 × 10^-3 m s-1'},
'9702-26-21-Q5':{0:'three quarks',3:'electron and muon',4:'mesons are made of quarks but leptons are fundamental'},
};
const score=(q,i,txt)=>{const p=q.parts[i];p.marks.forEach(m=>m.awarded=false);h.win.currentParts=q.parts;h.win.applyCieMarking(p.marks,txt);return p.marks.filter(m=>m.awarded).length+'/'+p.marks.length};
for(const id in FIX){
  const rs=rows.filter(r=>r.id===id);
  const q=h.win.genericBuilder({id,type:'x',params:FIX[id],parts:rs.map(r=>Object.assign({},r))});
  const sorted=rs.slice().sort((a,b)=>+a.partIndex-+b.partIndex);
  const out=[];
  q.parts.forEach((p,i)=>{const a=ANS[id][+sorted[i].partIndex];if(a!==undefined)out.push(sorted[i].partIndex+':'+score(q,i,a))});
  console.log(id,out.join('  '));
}
