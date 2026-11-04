const fs=require('fs');const load=require('./harness.js');const S=process.argv[2];const FILE=process.argv[3];const MINROW=+process.argv[4]||189;
const rows=JSON.parse(fs.readFileSync(FILE,'utf8')).filter(r=>r._r>=MINROW);
const h=load(S);
const groups={};rows.forEach(r=>{(groups[r.id]=groups[r.id]||[]).push(r)});
const res={build:0,text:0,notfull:{},nomarks:{}};const probs=[];
for(const id in groups){
  const g=groups[id];const first=g[0];
  let params={};try{params=first.params?JSON.parse(first.params):{}}catch(e){probs.push('BAD F '+id);continue}
  for(let it=0;it<60;it++){
    let q;
    try{q=h.win.genericBuilder({id,type:'x',params,parts:g.map(r=>Object.assign({},r))});}catch(e){probs.push('BUILD FAIL '+id+': '+e.message);res.build++;break}
    const all=JSON.stringify(q);
    if(/NaN|undefined|Infinity|\$\{/.test(all)){probs.push('BAD TEXT '+id+' :: '+((all.match(/.{50}(NaN|undefined|Infinity|\$\{).{30}/)||[all.slice(0,80)])[0]));res.text++;break}
    // parts correspond to sorted g by partIndex
    const sorted=g.slice().sort((a,b)=>+a.partIndex-+b.partIndex);
    q.parts.forEach((p,i)=>{
      const r=sorted[i]._r;
      if(!p.marks.length){res.nomarks[r]=1;return}
      h.win.currentParts=q.parts;const m=p.marks;
      try{h.win.applyCieMarking(m,p.modelAnswer)}catch(e){return}
      if(m.filter(x=>x.awarded).length!==m.length) res.notfull[r]=(res.notfull[r]||0)+1;
    });
  }
}
console.log(JSON.stringify({questions:Object.keys(groups).length,buildFail:res.build,badText:res.text,notfullRows:Object.keys(res.notfull).length,nomarksRows:Object.keys(res.nomarks).length}));
probs.slice(0,40).forEach(p=>console.log(p));
fs.writeFileSync(process.argv[5],JSON.stringify({notfull:res.notfull,nomarks:Object.keys(res.nomarks).map(Number),probs}));
