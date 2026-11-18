//##v1
// Seeded before/after regression compare. Usage: node tools/regress_compare.js before.json after.json [scriptsDir] [loadsPerId]
// Builds every id N times with identical random seeds from both sheets and lists which question fields changed and whether
// model-answer marking changed. Only the fields you meant to change may appear. JSON files come from tools/csv_to_json.py.
const fs=require('fs'),path=require('path');
const load=require(path.join(__dirname,'harness.js'));
const [,,BF,AF,SD,NL]=process.argv;
if(!BF||!AF){console.error('usage: node regress_compare.js before.json after.json [scriptsDir] [loads]');process.exit(2)}
const h=load(SD||path.join(__dirname,'..','scripts'));const N=+NL||25;
function rng(seed){let s=seed>>>0;return()=>{s=(s+0x6D2B79F5)>>>0;let t=s;t=Math.imul(t^t>>>15,t|1);t^=t+Math.imul(t^t>>>7,t|61);return((t^t>>>14)>>>0)/4294967296}}
function hash(s){let x=2166136261;for(const c of s){x^=c.charCodeAt(0);x=Math.imul(x,16777619)}return x>>>0}
const grp=f=>{const g={};JSON.parse(fs.readFileSync(f,'utf8')).filter(r=>r._r>=2).forEach(r=>(g[r.id]=g[r.id]||[]).push(r));return g};
const B=grp(BF),A=grp(AF),real=Math.random;
function build(g,id,seed){Math.random=rng(seed);let p={};try{p=g[0].params?JSON.parse(g[0].params):{}}catch(e){}
  try{return h.win.genericBuilder({id,type:'x',params:p,parts:g.map(r=>Object.assign({},r))})}finally{Math.random=real}}
function walk(a,b,p,o){if(typeof a!==typeof b){o.push(p);return}
  if(a&&typeof a==='object'){for(const k of new Set([...Object.keys(a),...Object.keys(b||{})]))walk(a[k],(b||{})[k],p+'.'+k,o)}else if(a!==b)o.push(p)}
const paths={},changed=new Set();let markDiff=0,loads=0;
const ids=new Set([...Object.keys(B),...Object.keys(A)]);
for(const id of ids){if(!B[id]||!A[id]){console.log('id only in one file:',id);continue}
  for(let s=1;s<=N;s++){loads++;const seed=hash(id)+s,q1=build(B[id],id,seed),q2=build(A[id],id,seed),o=[];walk(q1,q2,'q',o);
    o.forEach(p=>{const k=p.replace(/\.\d+(?=\.|$)/g,'.#');paths[k]=(paths[k]||0)+1;changed.add(id)});
    q1.parts.forEach((p,i)=>{const f=m=>JSON.stringify(m.map(x=>Object.assign({},x,{awarded:false})));
      const m1=p.marks,m2=q2.parts[i].marks;h.win.currentParts=q1.parts;try{h.win.applyCieMarking(m1,p.modelAnswer)}catch(e){}
      h.win.currentParts=q2.parts;try{h.win.applyCieMarking(m2,q2.parts[i].modelAnswer)}catch(e){}
      if(m1.map(x=>x.awarded).join()!==m2.map(x=>x.awarded).join())markDiff++})}}
console.log(JSON.stringify({ids:ids.size,loads,changedIds:changed.size,markDiff}));console.log('changed field paths:',paths);console.log('changed ids:',[...changed].join(' '));
