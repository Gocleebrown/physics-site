const fs=require('fs');const load=require('/home/claude/physics-site/tools/harness.js');
const h=load('/home/claude/physics-site/scripts');
const rows=JSON.parse(fs.readFileSync(process.argv[2]||'new22.json','utf8'));
const FIX={
'9702-26-22-Q1':{t1p:10,v1p:12,t2p:35,tpr:13/21,a2p:0.25},
'9702-26-22-Q2':{mbp:8.1,mpp:4.5},
'9702-26-22-Q3':{fp:3.0,kc:4/3,lamp:1.5,bpp:2.4,mp3:0.44,amp0:15},
'9702-26-22-Q4':{m4p:1.5,k5p:1.3,tp:52,P5p:1.1,E1p:7.4,F0:555,Vp:1400,eta0:83},
'9702-26-22-Q5':{Ep:12,Rwp:2.8,Awp:6.1,n28p:8.5,kc:5/(12/2.8)},
'9702-26-22-Q6':{u6p:5.60,dup:5,ip:0}};
const ANS={
'9702-26-22-Q1':{0:'amplitude and power are scalars; force and momentum are vectors',1:'area under the graph',2:'distance = 390 m',3:'a = (v - u)/t = (0 - 12)/5 = -2.4, so 2.4 m s-2',4:'v^2 = 2 × 0.25 × 150 = 75, v = 8.7 m s-1'},
'9702-26-22-Q2':{0:'the resultant force is zero and the resultant moment (torque) about any point is zero',1:'for the plank 2Tcosθ = R + WP; for the block 2Tcosθ + R = WB; so R + WP = WB - R',2:'2R = 8.1 × 9.81 - 4.5 × 9.81, R = 18 N',3:"Hooke's law",4:'when the tension is removed the ropes return to their original length'},
'9702-26-22-Q3':{0:'a wave that transfers energy',1:'T = 1/f = 0.33 s',2:'λ = 3.9 - 2.4 = 1.5 m; v = fλ = 3.0 × 1.5 = 4.5 m s-1',3:'ΔE = mgΔh = 0.44 × 9.81 × (0.15 × 2) = 1.3 J',4:'the path difference is not a whole number of wavelengths so the waves are not in phase and the amplitude decreases'},
'9702-26-22-Q4':{0:'EK = ½mv²; v² = 2 × 1.3e5 / 1.5e4 = 17.3; v = 4.2 m s-1',1:'work done per unit time',2:'W = Pt = 1.1e5 × 52; useful work = change in EP + Fs; F = 1.2e5 / (4.2 × 52) = 550 N',3:'P = IV = 95 × 1400 = 1.33e5; efficiency = 1.1e5 / 1.33e5 × 100 = 83%'},
'9702-26-22-Q5':{0:'IT = I1 + I2 + I3 and I = V/R so V/RT = V/R1 + V/R2 + V/R3, giving 1/RT = 1/R1 + 1/R2 + 1/R3',1:'RT = (1/2.8 + 1/2.8)^-1 = 1.4; I = 12/1.4 = 8.6 A',2:'v = I/Anq = (8.6/2) / (6.1e-6 × 8.5e28 × 1.6e-19) = 5.2e-5 m s-1',3:'light-dependent resistor',4:'I(X) = 5 - 12/2.8 = 0.71; R(top branch) = 12/0.71 = 16.8; R(X) = 16.8 - 2.8 = 14 Ω',5:'the resistance of X increased so the light intensity decreased'},
'9702-26-22-Q6':{0:'most of the alpha particles pass straight through',1:'p = mv = 4 × 1.66e-27 × 5.60e6 = 3.72e-20',2:'4u × 5.60e6 = 197u × v - 4u × 5.38e6; v = 2.2e5 m s-1',3:'absolute uncertainty = 5e4 + 5e4 = 1e5; percentage = 1e5/(5.60e6 + 5.38e6) × 100 = 0.9%',4:'3',5:'one quark and one antiquark'}};
const score=(q,i,txt)=>{const p=q.parts[i];p.marks.forEach(m=>m.awarded=false);h.win.currentParts=q.parts;h.win.applyCieMarking(p.marks,txt);return p.marks.filter(m=>m.awarded).length+'/'+p.marks.length};
for(const id in FIX){
  const rs=rows.filter(r=>r.id===id);
  const q=h.win.genericBuilder({id,type:'x',params:FIX[id],parts:rs.map(r=>Object.assign({},r))});
  const sorted=rs.slice().sort((a,b)=>+a.partIndex-+b.partIndex);
  const out=[];
  q.parts.forEach((p,i)=>{const a=ANS[id][+sorted[i].partIndex];if(a!==undefined)out.push(sorted[i].partIndex+':'+score(q,i,a))});
  console.log(id,out.join('  '));
}
