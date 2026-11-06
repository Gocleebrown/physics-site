const fs=require('fs');const h=require('/home/claude/physics-site/tools/harness.js')('/home/claude/physics-site/scripts');
const rows=JSON.parse(fs.readFileSync('new42m.json'));
const strip=s=>String(s).replace(/<[^>]+>/g,'');
const ids=[...new Set(rows.map(r=>r.id))];const bad={};const st={};const note=(k,v)=>{(st[k]=st[k]||[]).push(v)};
for(const id of ids){const rs=rows.filter(r=>r.id===id);const params=JSON.parse(rs[0].params);
 for(let it=0;it<3000;it++){
  const q=h.win.genericBuilder({id,type:'x',params,parts:rs.map(r=>Object.assign({},r))});
  q.parts.forEach((p,i)=>{const blob=JSON.stringify([p.partText||'',p.text||'',p.modelAnswer||'',p.explanation||'',p.marks.map(m=>m.keywords),(p.imageOptions||[]).map(o=>String(o).slice(0,12)),p.tableCellKeywords||'']).replace(/data:image\/svg\+xml[^"]*/g,'');
   if(/\bnull\b|undefined|NaN|Infinity/.test(blob)){const k=id.slice(-3)+' p'+i;bad[k]=(bad[k]||0)+1;}});
  const m=q.parts.map(p=>strip(p.modelAnswer));
  if(id.endsWith('Q3'))note('Q3 theta',+m[2].match(/θ = ([\d.]+) °C/)[1]);
  if(id.endsWith('Q4')){note('Q4 Q',+m[4].match(/= (-?[\d.]+) kJ/)[1]);note('Q4 W',+m[1].match(/= (\d+) J/)[1]);}
  if(id.endsWith('Q8')){note('Q8 obs',+m[3].match(/= ([\d.]+) nm$/)[1]);}
  if(id.endsWith('Q9')){note('Q9 A',+m[2].match(/= ([\d.e+]+) Bq/)[1]);}
  if(id.endsWith('Q10')){note('Q10 R',+m[3].match(/= ([\d.]+)$/)[1]);}
 }}
console.log('null/undefined leaks:',JSON.stringify(bad));
for(const k in st){const a=st[k];console.log(k,'min',Math.min(...a),'max',Math.max(...a));}
