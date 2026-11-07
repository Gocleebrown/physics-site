// shared harness for IGCSE builds: node tpaper31.js rows.json [show]
const fs=require('fs');const load=require('/home/claude/physics-site/tools/harness.js');
const h=load('/home/claude/physics-site/scripts');
const T={},FIX={};
module.exports={h,T,FIX,run(rowsFile,show){
 const rows=JSON.parse(fs.readFileSync(rowsFile,'utf8'));
 const score=(q,i,txt)=>{const p=q.parts[i];p.marks.forEach(m=>m.awarded=false);h.win.currentParts=q.parts;h.win.applyCieMarking(p.marks,txt);return [p.marks.filter(m=>m.awarded).length,p.marks.length]};
 let bad=0,n=0;
 for(const id in FIX){
  const rs=rows.filter(r=>r.id===id);
  if(!rs.length){console.log('NO ROWS',id);continue}
  const q=h.win.genericBuilder({id,type:'x',params:FIX[id],parts:rs.map(r=>Object.assign({},r))});
  const sorted=rs.slice().sort((a,b)=>+a.partIndex-+b.partIndex);
  for(const [pi,ans,exp] of (T[id]||[])){
    const i=sorted.findIndex(r=>+r.partIndex===pi);let g,t;if(Array.isArray(ans)){const pp=q.parts[i];g=0;t=pp.tableCellKeywords.length;pp.tableCellKeywords.forEach((rw,r)=>{if(ans[r]!==''&&h.win.matchesKeywordGroups(rw[0],ans[r]))g++;});}else{[g,t]=score(q,i,ans);}n++;
    if(g!==exp){bad++;console.log('MISMATCH',id.slice(-3),'pi'+pi,'got',g+'/'+t,'expected',exp,'|',ans.slice(0,80));}
  }
 }
 console.log('checked',n,'mismatches',bad);
 if(show){for(const id in FIX){const rs=rows.filter(r=>r.id===id);const q=h.win.genericBuilder({id,type:'x',params:FIX[id],parts:rs.map(r=>Object.assign({},r))});
  console.log('\n=====',id);q.parts.forEach((p,i)=>console.log('['+i+']',(p.partText||p.text||'').replace(/<svg[\s\S]*?<\/svg>/g,'[SVG]').replace(/<[^>]+>/g,'').slice(0,500),'\n   MODEL:',String(p.modelAnswer).replace(/<[^>]+>/g,'').slice(0,300),'| marks',p.marks.length));}}
}};
