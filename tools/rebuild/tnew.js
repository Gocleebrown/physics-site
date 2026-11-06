// Tests for engine ##v5 / builders ##v3 features: generated image options, maxMarks, text normalisation.
const h=require('/home/claude/physics-site/tools/harness.js')('/home/claude/physics-site/scripts');
let bad=0;const ok=(c,m)=>{if(!c){bad++;console.log('FAIL',m)}};
const score=(q,i,t)=>{const p=q.parts[i];p.marks.forEach(m=>m.awarded=false);h.win.currentParts=q.parts;h.win.applyCieMarking(p.marks,t);return h.win.markEarned(p.marks)};
// 1. generated image options
const G={mk:"(y)=>'<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 10 10\"><line x1=\"0\" y1=\"0\" x2=\"10\" y2=\"'+y+'\"/></svg>'",
 'ci':'Math.floor(cip)','oa':'mk(2)','ob':'mk(5)','oc':'mk(8)'};
const P={cip:[0,2.99]};
const row=(o)=>Object.assign({id:'t1',partIndex:0,type:'definition',params:JSON.stringify(P),computedValues:JSON.stringify(G),mainText:'Q',partText:'p',answerType:'imageChoice',imageOptions:'["${oa}","${ob}","${oc}"]',correctImageIndex:'${ci}',imageChoiceMarks:'1',modelAnswer:'m',explanation:'e'},o);
const seen=new Set();
for(let i=0;i<200;i++){const q=h.win.genericBuilder({id:'t1',type:'x',params:P,parts:[row({})]});const p=q.parts[0];
 ok(p.imageOptions.length===3&&p.imageOptions.every(o=>o.startsWith('data:image/svg+xml')),'options are data URIs');
 ok(decodeURIComponent(p.imageOptions[0].split(',')[1]).includes('y2="2"'),'option interpolated');
 ok(p.correctImageIndex>=0&&p.correctImageIndex<=2,'index in range '+p.correctImageIndex);seen.add(p.correctImageIndex)}
ok(seen.size===3,'correct index varies: '+[...seen]);
ok(h.win.resolveAssetSrc('data:image/svg+xml;charset=utf-8,abc')==='data:image/svg+xml;charset=utf-8,abc','data uri kept');
ok(h.win.resolveAssetSrc('foo.svg')==='assets/foo.svg'&&h.win.resolveAssetSrc('foo')==='assets/foo.png','file names unchanged');
const q0=h.win.genericBuilder({id:'t0',type:'x',params:{},parts:[row({id:'t0',params:'{}',computedValues:'',imageOptions:'["a.svg","b.svg"]',correctImageIndex:'1'})]});
ok(JSON.stringify(q0.parts[0].imageOptions)==='["a.svg","b.svg"]'&&q0.parts[0].correctImageIndex===1,'plain file options unchanged');
// 2. maxMarks
const t2=(cap)=>h.win.genericBuilder({id:'t2',type:'x',params:{},parts:[{id:'t2',partIndex:0,type:'explain',params:'{}',mainText:'Q',partText:'any 2',modelAnswer:'m',explanation:'e',B_keywords:'alpha',B2_keywords:'beta',B3_keywords:'gamma',C1_keywords:'delta',maxMarks:cap}]});
let q=t2('2');ok(q.parts[0].marks.cap===2,'cap set');
ok(score(q,0,'alpha beta gamma delta')===2,'3+ points capped at 2');ok(score(q,0,'alpha')===1,'1 point =1');ok(score(q,0,'')===0,'blank 0');ok(score(q,0,'beta gamma')===2,'any two');
ok(h.win.markTotal(q.parts[0].marks)===2,'total 2');
q=t2('');ok(!q.parts[0].marks.cap&&score(q,0,'alpha beta gamma delta')===4&&h.win.markTotal(q.parts[0].marks)===4,'blank cap = old behaviour');
for(const bad of ['0','5','-1','2.5','abc',' x ']){q=t2(bad);ok(!q.parts[0].marks.cap,'invalid cap ignored: '+bad)}
q=t2('4');ok(q.parts[0].marks.cap===4,'cap = number of marks allowed');
// 3. normalisation
const m=(kw,ans)=>{const q=h.win.genericBuilder({id:'t3',type:'x',params:{},parts:[{id:'t3',partIndex:0,type:'definition',params:'{}',mainText:'Q',partText:'p',modelAnswer:'m',explanation:'e',B_keywords:kw}]});return score(q,0,ans)===1};
ok(m('g0','g₀ is 9.81'),'subscript digit -> plain');ok(m('g₀','g0'),'keyword subscript');ok(m('e_k','Ek'),'underscore removed');ok(m('ek','E_k'),'underscore student');
ok(m('4x','4×'),'times sign');ok(m('4×','4x'),'times sign keyword');ok(m('φ','ϕ'),'phi');ok(m('μ','µ'),'micro');ok(m('vx','vₓ'),'subscript letter');
ok(m('2.0','v₂ = 2.0'),'numbers unaffected');
// number extraction ignores subscripts exactly as before
ok(JSON.stringify(h.win.extractNumbers('v₂ = 5.0'))===JSON.stringify([{value:5,sf:2}]),'subscript not read as a number');
ok(!m('2','v₂ = 5'),'subscript digit is not a numeric answer');
console.log(bad?bad+' FAILURES':'all new-feature tests pass');
