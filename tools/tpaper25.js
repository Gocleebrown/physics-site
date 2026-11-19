const fs=require('fs');const load=require('/home/claude/purge/tools/harness.js');const h=load('/home/claude/purge/scripts');
const O=JSON.parse(fs.readFileSync('live8.json','utf8')).filter(r=>r._r>=2&&r.id),N=JSON.parse(fs.readFileSync('b25.json','utf8')).filter(r=>r._r>=2&&r.id);
const grp=a=>{const g={};a.forEach(r=>(g[r.id]=g[r.id]||[]).push(r));return g};const GO=grp(O),GN=grp(N);
const FIX={'9702_s25_p22_q2':{mp_:270,d1p:1.2,d2p:1.6,thp:25,pkp:150,cip:0,mp:0},'9702_s25_p22_q3':{aXp:10,aYp:20,lamp:.4,fp:16},'9702_s25_p22_q5':{Lp:.81,Ep:95,kp:1.25,x1p:2.0,x2p:3.0},'9702_s25_p22_q7':{ip:0.5},
'9702_s25_p23_q1':{Hp:10,up:3},'9702_s25_p23_q2':{Lbp:9,mAp:90,mCp:150,xBp:3,dp:1.8,ep:1.2},'9702_s25_p23_q3':{mp:1500,vp:30,thp:6,Fp:1600,},'9702_s25_p23_q5':{alp:20},'9702_s25_p23_q6':{lp:720,angp:52}};
const st=s=>String(s||'').replace(/<svg[\s\S]*?<\/svg>/g,'[svg]').replace(/<[^>]+>/g,' ').replace(/&times;/g,'×').replace(/&micro;/g,'µ').replace(/\s+/g,' ').trim();
let bad=0;
for(const id in FIX){const p={};for(const k in FIX[id])p[k]=[FIX[id][k],FIX[id][k]];
 const qo=h.win.genericBuilder({id,type:'x',params:{},parts:GO[id].map(r=>Object.assign({},r))});
 const qn=h.win.genericBuilder({id,type:'x',params:p,parts:GN[id].map(r=>Object.assign({},r))});
 const cmp=(a,b,l)=>{if(st(a)!==st(b)){bad++;console.log('DIFF',id,l,'\n  OLD:',st(a).slice(0,300),'\n  NEW:',st(b).slice(0,300))}};
 cmp(qo.mainText,qn.mainText,'main');qo.parts.forEach((pp,i)=>{cmp(pp.partText,qn.parts[i].partText,'part'+i);cmp(pp.modelAnswer,qn.parts[i].modelAnswer,'model'+i)});}
console.log('paper-value diffs:',bad);
