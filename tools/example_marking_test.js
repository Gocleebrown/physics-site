const fs=require('fs');const load=require('./harness.js');const h=load(process.argv[2]);
const rows=JSON.parse(fs.readFileSync(process.argv[3],'utf8')).filter(r=>r.id==='9702-26-23-Q5');
const first=rows[0];const params=JSON.parse(first.params);
function mk(){return h.win.genericBuilder({id:first.id,type:'x',params,parts:rows.map(r=>Object.assign({},r))})}
let n=0,fail=0;
for(let it=0;it<300;it++){
  const q=mk();const p1=q.parts[1],p2=q.parts[2];
  const t=p1.partText;
  const mm=t.match(/charges of (.*) and (.*)\.$/);
  const names={'−1e':'three down quarks','0':'one up quark and two down quarks','+1e':'two up quarks and one down quark','+2e':'three up quarks'};
  const right=`Quark charges are +2/3 and -1/3. ${mm[1]}: ${names[mm[1]]}. ${mm[2]}: ${names[mm[2]]}.`;
  const wrong=`${mm[1]}: ${names[mm[2]]}. ${mm[2]}: ${names[mm[1]]}.`; // swapped -> still both compositions mentioned
  const score=(p,ans)=>{p.marks.forEach(x=>{x.awarded=false});h.win.currentParts=q.parts;h.win.applyCieMarking(p.marks,ans);return p.marks.filter(x=>x.awarded).length};
  n++;
  if(score(p1,right)!==3){fail++;console.log('right<3',t,right)}
  if(score(p1,'I do not know')!==0){fail++;console.log('blank>0')}
  const ab=q.parts[2].modelAnswer.match(/P = (\d+), Q = (\d+)/);
  const P=+ab[1],Qn=+ab[2];
  if(score(p2,`P = ${P}, Q = ${Qn}, R = 0, S = +1`)!==2){fail++;console.log('p2 right fail',P,Qn)}
  if(score(p2,`P = ${P}, Q = ${Qn+2}, R = 0, S = +1`)!==1){fail++;console.log('p2 wrongQ not 1',P,Qn)}
  if(score(p2,`P = ${P}, Q = ${P/2|0}, R = 0, S = -1`)>=2){fail++;console.log('p2 wrong should <2')}
}
console.log('trials',n,'fails',fail);
