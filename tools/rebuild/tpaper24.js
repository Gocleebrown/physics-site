const fs=require('fs');const load=require('/home/claude/physics-site/tools/harness.js');
const h=load('/home/claude/physics-site/scripts');
const rows=JSON.parse(fs.readFileSync(process.argv[2]||'new24.json','utf8'));
const FIX={
'9702-26-24-Q1':{mp:1400,up:15,sp:35,r1:0.1,r2:0.1,r3:0.1,r4:0.1,r5:0.1,r6:0.1,r7:0.2,r8:0.3,r9:0.4,r10:0.5},
'9702-26-24-Q2':{L0p:2.1,Lfp:14.0,dlp:0.1,dmp:0.005,Mp:0.30},
'9702-26-24-Q3':{Lp:1.8,fp:26},
'9702-26-24-Q4':{mop:0.070,Vop:1.0,rlp:1100},
'9702-26-24-Q5':{v1i:2,i1i:1,i2i:3},
'9702-26-24-Q6':{Anp:5.7,Vqp:230,Pkp:1.0,rnp:1.3,vdp:5.4},
'9702-26-24-Q7':{ei:0,ap:0.75,kp:1.5}};
const T={
'9702-26-24-Q1':[
 [1,'KE = 1/2 × 1400 × 15^2 = 1.6 × 10^5 J',2],[1,'157500',2],[1,'1.6e5',2],[1,'1.575e5',2],[1,'1/2mv^2',1],[1,'21000',0],[1,'15750',0],
 [2,'v^2 = u^2 + 2as; 0 = 15^2 + 2 × a × 35; a = -3.2 m s-2',2],[2,'-3.2',2],[2,'−3.2',2],[2,'-3.21',2],[2,'3.2',1],[2,'0 = 15^2 + 2 × a × 35',1],[2,'-6.4',0],
 [3,'F = ma = 1400 × 3.2 = 4500 N',2],[3,'4500',2],[3,'4480',2],[3,'4600',2],[3,'F = ma',1],[3,'1400',0],[3,'157500',0],
 [4,'the acceleration is the same because the force and mass are unchanged',1],[4,'it stays the same',0],[4,'it doubles',0],
 [5,'the kinetic energy is four times greater so the distance is four times greater',2],[5,'distance is 4 times greater',1],[5,'the distance doubles',0]],
'9702-26-24-Q2':[
 [0,'extension is directly proportional to the force',1],[0,'force is proportional to extension',1],[0,'extension is proportional',0],[0,'force',0],
 [1,'11.9 ± 0.2',1],[1,'11.9, 0.2',1],[1,'11.9',0],[1,'(11.9 ± 0.1)',0],
 [2,'k = F/x = (0.300 × 9.81)/0.119 = 24.7 N m-1',3],[2,'24.7',3],[2,'25',3],[2,'24.73',3],[2,'k = F/x',1],[2,'0.247',0],[2,'2470',0],
 [3,'(0.2/11.9 + 0.005/0.300) × 100 = 3.3%',2],[3,'3',2],[3,'3.3',2],[3,'3.35',2],[3,'0.2/11.9 + 0.005/0.300',1],[3,'0.2',0],
 [4,'the extension is less because the spring constant of Y is greater',1],[4,'less',0],[4,'greater',0],
 [5,'the elastic potential energy is less because the extension is less and E = 1/2 F x',2],[5,'less energy',1],[5,'greater',0]],
'9702-26-24-Q3':[
 [0,'the wave from the generator is reflected at the fixed point. the incident and reflected waves superpose',2],[0,'reflection',1],[0,'waves interfere',0],
 [2,'lambda = 1.8/2 = 0.90 m; v = f lambda = 26 × 0.90 = 23 m s-1',3],[2,'23',3],[2,'23.4',3],[2,'v = f lambda',1],[2,'47',0],[2,'12',0]],
'9702-26-24-Q4':[
 [1,'W = D + U',1],[1,'W = D - U',0],[1,'D = W - U',1],[1,'U = W − D',1],[1,'W = U',0],
 [2,'W = 0.070 × 9.81 = 0.687; U = 1100 × 9.81 × 1.0e-5 = 0.108; D = 0.58 N',3],[2,'0.58',3],[2,'0.579',3],[2,'0.69',0],[2,'0.11',0],[2,'U = rho g V',1]],
'9702-26-24-Q5':[
 [0,'diode',1],[0,'light-emitting diode',1],[0,'led',1],[0,'resistor',0],[0,'thermistor',0],[0,'a diode',1],
 [2,'p.d. across X is 0.70 V at 5.0 mA. p.d. across R = 0.005 × 20 = 0.10 V. e.m.f. = 0.70 + 0.10 = 0.80 V',3],[2,'0.70 + 0.10 = 0.80',2],[2,'0.7',1],[2,'0.80',0],
 [3,'0 A',1],[3,'zero',1],[3,'0',1],[3,'0.80',0],[3,'5.0 mA',0],
 [4,'current in resistor = 0.80/20 = 0.040 A; current in X at 0.80 V = 40 mA = 0.040 A; total = 0.080 A',3],[4,'0.080',3],[4,'0.08',3],[4,'0.04',1],[4,'0.040 A',1],[4,'0.8',0]],
'9702-26-24-Q6':[
 [0,'P = V^2/R so R = 230^2/1000 = 53 ohm',2],[0,'R = V^2/P = 52.9',2],[0,'53',0],[0,'P = V^2/R',1],
 [1,'R = rho L / A; L = 53 × 5.7e-8 / 1.3e-6 = 2.3 m',2],[1,'2.3',2],[1,'2.32',2],[1,'2.3 m',2],[1,'0.0023',0],[1,'rho = RA/L',1],
 [2,'I = P/V = 1000/230 = 4.3 A; n = I/(Avq) = 4.3/(5.7e-8 × 5.4e-3 × 1.6e-19) = 8.8 × 10^28 m-3',3],[2,'8.8e28',3],[2,'8.9e28',3],[2,'8.8 × 10^28',3],[2,'I = Anvq',1],[2,'4.3',1],[2,'8.8e25',0]],
'9702-26-24-Q7':[
 [0,'same number of protons but different number of neutrons',2],[0,'same proton number, different nucleon number',2],[0,'same number of protons',1],[0,'different number of neutrons',1],[0,'same number of neutrons',0],
 [1,'alpha = 1, beta = 2',2],[1,'1 alpha and 2 beta',2],[1,'alpha 2 beta 1',0],[1,'1',0],
 [2,'nucleon number 228, proton number 90',2],[2,'228 and 90',2],[2,'228',1],[2,'232 and 90',0],
 [3,'uud',1],[3,'two up and one down',1],[3,'udd',0],[3,'up up down',1],[3,'down down up',0],
 [4,'an up quark changes to a down quark',1],[4,'u to d',1],[4,'down to up',0],[4,'uud to udd',1]]};
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
if(process.argv[3]){for(const id in FIX){const rs=rows.filter(r=>r.id===id);const q=h.win.genericBuilder({id,type:'x',params:FIX[id],parts:rs.map(r=>Object.assign({},r))});
 console.log('\n=====',id);q.parts.forEach((p,i)=>console.log('['+i+']',(p.partText||p.text||'').replace(/<svg[\s\S]*?<\/svg>/g,'[SVG]').replace(/<[^>]+>/g,'').slice(0,500),'\n   MODEL:',String(p.modelAnswer).replace(/<[^>]+>/g,'').slice(0,250)));}}
