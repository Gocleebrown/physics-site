// Student-simulation test for a rebuilt paper.  node t40.js <scriptsDir> <sheet.json> <idPrefix> [loads]
const fs=require('fs');const load=require('/home/claude/physics-site/tools/harness.js');
const h=load(process.argv[2]);const rows=JSON.parse(fs.readFileSync(process.argv[3],'utf8')).filter(r=>r.id.startsWith(process.argv[4]));
const LOADS=+process.argv[5]||100;
const groups={};rows.forEach(r=>{(groups[r.id]=groups[r.id]||[]).push(r)});
const clean=s=>s.replace(/<sup>(.*?)<\/sup>/g,'^$1').replace(/<sub>(.*?)<\/sub>/g,'$1').replace(/<br\s*\/?>/g,' ').replace(/<[^>]+>/g,'');
const out={fail:{},blank:{},wrongA:{},n:0};
const score=(q,i,txt)=>{const p=q.parts[i];p.marks.forEach(m=>m.awarded=false);h.win.currentParts=q.parts;h.win.applyCieMarking(p.marks,txt);return p.marks.filter(m=>m.awarded).length};
for(const id in groups){
  const g=groups[id].slice().sort((a,b)=>+a.partIndex-+b.partIndex);
  const params=g[0].params?JSON.parse(g[0].params):{};
  for(let it=0;it<LOADS;it++){
    const q=h.win.genericBuilder({id,type:'x',params,parts:groups[id].map(r=>Object.assign({},r))});
    out.n++;
    q.parts.forEach((p,i)=>{
      const key=id+' pi'+g[i].partIndex+' r'+g[i]._r;
      const tot=p.marks.length;
      if(p.answerType==='imageChoice'){ // correct index must be in range
        if(!(p.correctImageIndex>=0&&p.imageOptions.length>=2)) out.fail[key]=(out.fail[key]||0)+1; return;}
      if(p.answerType==='table'){
        let k=0;let ok=0;
        p.tableRowLabels.forEach((rl,r)=>p.tableColLabels.forEach((cl,c)=>{const ans=p.tableCellAnswers[r][c];if(h.win.matchesKeywordGroups(p.tableCellKeywords[r][c],ans))ok++;k++}));
        if(ok!==tot||k!==tot) out.fail[key]=(out.fail[key]||0)+1; return;}
      const ma=clean(p.modelAnswer);
      if(score(q,i,ma)!==tot) out.fail[key]=(out.fail[key]||0)+1;
      if(score(q,i,'')!==0||score(q,i,'I do not know')!==0) out.blank[key]=(out.blank[key]||0)+1;
      // wrong numeric answer: if this part has an A mark, a number 1.7x too big must not earn it
      const ai=p.marks.findIndex(m=>m.type==='A');
      if(ai>=0){const nums=ma.match(/[-+]?\d*\.?\d+(?:e[-+]?\d+)?/gi);
        if(nums){const wrong='= '+(parseFloat(nums[nums.length-1])*1.7+0.37)+'';score(q,i,wrong);if(p.marks[ai].awarded) out.wrongA[key]=(out.wrongA[key]||0)+1;}}
    });
  }
}
console.log(JSON.stringify({loads:out.n,notFullOnModel:out.fail,blankAwarded:out.blank,wrongNumberAwardedA:out.wrongA}));
