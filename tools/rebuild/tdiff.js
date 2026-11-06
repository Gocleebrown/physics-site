// Differential test: old engine dir vs new engine dir over every question in a sheet export.
// node tdiff.js <oldScripts> <newScripts> <sheet.json> [loads]
const fs=require('fs');const load=require('/home/claude/physics-site/tools/harness.js');
const [,,OLD,NEW,SHEET,L]=process.argv;const LOADS=+L||30;
const hO=load(OLD),hN=load(NEW);
const rows=JSON.parse(fs.readFileSync(SHEET,'utf8')).filter(r=>r.id&&r.id!=='id');
const groups={};rows.forEach(r=>{(groups[r.id]=groups[r.id]||[]).push(r)});
let seed=1;const rnd=()=>{seed=(seed*1664525+1013904223)%4294967296;return seed/4294967296};
const clean=s=>String(s).replace(/<sup>(.*?)<\/sup>/g,'^$1').replace(/<sub>(.*?)<\/sub>/g,'$1').replace(/<br\s*\/?>/g,' ').replace(/<[^>]+>/g,'');
const score=(h,q,i,txt)=>{const p=q.parts[i];p.marks.forEach(m=>m.awarded=false);h.win.currentParts=q.parts;h.win.applyCieMarking(p.marks,txt);return p.marks.filter(m=>m.awarded).length};
const diffs={};let n=0,checks=0;
const note=(k,m)=>{diffs[k]=diffs[k]||new Set();diffs[k].add(m)};
for(const id in groups){
  const g=groups[id];const params=g[0].params?JSON.parse(g[0].params):{};
  for(let it=0;it<LOADS;it++){
    const s0=Math.floor(rnd()*1e9)+1;
    const mk=(h)=>{seed=s0;const o=Math.random;Math.random=()=>rnd();try{return h.win.genericBuilder({id,type:'x',params,parts:g.map(r=>({...r}))})}finally{Math.random=o}};
    let a,b;try{a=mk(hO)}catch(e){a=null}try{b=mk(hN)}catch(e){b=null;note(id,'NEW BUILD FAILS '+e.message)}
    if(!a||!b)continue;n++;
    a.parts.forEach((pa,i)=>{const pb=b.parts[i];const key=id+' #'+i;
      for(const f of ['partText','modelAnswer','explanation','answerType','correctImageIndex']) if(JSON.stringify(pa[f])!==JSON.stringify(pb[f])) note(key,'field '+f);
      if(JSON.stringify(pa.imageOptions)!==JSON.stringify(pb.imageOptions)) note(key,'imageOptions');
      if(JSON.stringify(pa.marks)!==JSON.stringify(pb.marks)) note(key,'marks structure');
      if(pb.marks.cap) note(key,'cap present');
      if(pa.answerType==='imageChoice'||pa.answerType==='table'||!pa.marks.length) return;
      const m=clean(pa.modelAnswer);
      const probes=[m,'',m.replace(/×/g,'x'),m.replace(/\^2/g,'²'),m.toUpperCase(),'0','1','the','increases','proportional','zero',String(m).split(/[;.,]/)[0]];
      probes.forEach(t=>{checks++;const x=score(hO,a,i,t),y=score(hN,b,i,t);if(x!==y)note(key,`score ${x}->${y} for "${t.slice(0,50)}"`)});
    });
  }
}
console.log('loads compared',n,'score checks',checks,'questions',Object.keys(groups).length);
const ks=Object.keys(diffs);console.log('parts with any difference:',ks.length);
ks.slice(0,60).forEach(k=>console.log(k,[...diffs[k]].slice(0,4).join(' | ')));
