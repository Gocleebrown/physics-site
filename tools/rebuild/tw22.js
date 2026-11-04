const fs=require('fs');const load=require('/home/claude/gocleebrown/physics-site/tools/harness.js');
const h=load('/home/claude/gocleebrown/physics-site/scripts');
const rows=JSON.parse(fs.readFileSync(process.argv[2]||'new22.json','utf8'));
const FIX={
'9702-26-22-Q1':{t1p:10,v1p:12,t2p:35,tpr:13/21,a2p:0.25},
'9702-26-22-Q2':{mbp:8.1,mpp:4.5},
'9702-26-22-Q3':{fp:3.0,kc:4/3,lamp:1.5,bpp:2.4,mp3:0.44,amp0:15},
'9702-26-22-Q4':{m4p:1.5,k5p:1.3,tp:52,P5p:1.1,E1p:7.4,F0:555,Vp:1400,eta0:83},
'9702-26-22-Q5':{Ep:12,Rwp:2.8,Awp:6.1,n28p:8.5,kc:5/(12/2.8)},
'9702-26-22-Q6':{u6p:5.60,dup:5,ip:0}};
const W={
'9702-26-22-Q1':{2:'420 m',3:'1.2',4:'v = 8.8 m s-1',0:'amplitude and force are scalars'},
'9702-26-22-Q2':{2:'R = 36 N',3:'Newtons law',4:'the ropes stretch'},
'9702-26-22-Q3':{1:'3.0 s',2:'v = 3.0 × 3.9 = 11.7',3:'E = 0.44 × 9.81 × 0.15 = 0.65 J',4:'the amplitude increases'},
'9702-26-22-Q4':{0:'v = 17.3',2:'F = 1.1e5 / 4.2 = 26000 N',3:'81%'},
'9702-26-22-Q5':{1:'4.3 A',2:'1.0e-4 m s-1',3:'thermistor',4:'8.6 ohms',5:'the light intensity increased'},
'9702-26-22-Q6':{1:'3.2e-20',2:'4500 m s-1',3:'1.8%',4:'2',5:'three quarks'}};
const score=(q,i,txt)=>{const p=q.parts[i];p.marks.forEach(m=>m.awarded=false);h.win.currentParts=q.parts;h.win.applyCieMarking(p.marks,txt);return p.marks.filter(m=>m.awarded).length+'/'+p.marks.length};
for(const id in W){const rs=rows.filter(r=>r.id===id);const q=h.win.genericBuilder({id,type:'x',params:FIX[id],parts:rs.map(r=>Object.assign({},r))});
const sorted=rs.slice().sort((a,b)=>+a.partIndex-+b.partIndex);const out=[];
q.parts.forEach((p,i)=>{const a=W[id][+sorted[i].partIndex];if(a!==undefined)out.push(sorted[i].partIndex+':'+score(q,i,a))});console.log(id,out.join('  '))}
