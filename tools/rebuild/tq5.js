const fs=require('fs');const load=require('/home/claude/gocleebrown/physics-site/tools/harness.js');
const h=load('/home/claude/gocleebrown/physics-site/scripts');
const rows=JSON.parse(fs.readFileSync('new21.json','utf8'));
const score=(q,i,txt)=>{const p=q.parts[i];p.marks.forEach(m=>m.awarded=false);h.win.currentParts=q.parts;h.win.applyCieMarking(p.marks,txt);return p.marks.filter(m=>m.awarded).length+'/'+p.marks.length};
let bad=0;
function run(id,params,tests){const rs=rows.filter(r=>r.id===id);const q=h.win.genericBuilder({id,type:'x',params,parts:rs.map(r=>Object.assign({},r))});
 console.log('##',id,JSON.stringify(params),'|',q.parts[1].partText.replace(/<[^>]+>/g,'').slice(0,120));
 tests.forEach(([i,a,exp])=>{const r=score(q,i,a);if(r!==exp)bad++;console.log((r===exp?'ok   ':'FAIL ')+'part'+i+' got '+r+' exp '+exp+' :: '+a.slice(0,80))})}
run('9702-26-21-Q5',{sp:0.5},[
 [1,'a meson is a quark and an antiquark. The up quark has charge +2/3 and the anti-down has charge +1/3 so total +1e','2/2'],
 [1,'quarks have charges of 2/3 and 1/3','1/2'],
 [1,'a meson is made of two quarks','0/2'],
 [2,'0 and -1e. up and anti-up: +2/3 + -2/3 = 0. down and anti-up: -1/3 + -2/3 = -1','2/2'],
 [2,'+2e and -2e','0/2'],
 [3,'electron and neutrino','2/2'],[3,'muon and tau','1/2'],[3,'electron and muon','2/2'],[3,'electron neutrino','2/2'],[3,'positron and electron','2/2'],[3,'proton and neutron','0/2'],[3,'electron','1/2'],
 [4,'leptons are fundamental particles','1/1'],[4,'leptons have no charge','0/1'],
]);
run('9702-26-21-Q5',{sp:1.5},[
 [1,'a meson is a quark and an antiquark. The down quark has charge -1/3 and the anti-up has charge -2/3 so total -1e','2/2'],
 [1,'a meson is made of a quark and a antiquark','0/2'],
 [2,'0 and +1e. up and anti-up: 0; up and anti-down: +2/3 + +1/3 = +1','2/2'],
 [2,'0 and -1e','0/2'],
]);
run('9702-26-21-Q1',{M6:2.83,r4:2.0,a0:2.5,tbp:60},[
 [3,'F = ma = 2.83e6 x 2.5 = 7.1e6 N','1/2'],[3,'3.5e7 N','2/2'],[3,'3.5 x 10^7','2/2'],[3,'35 MN','0/2'],
 [2,'gradient','1/2'],[2,'tangent at t=0','1/2'],
 [1,'the rocket is burning fuel so the mass decreases, so the acceleration increases','2/2'],[1,'there is drag','0/2'],
 [4,'1.1 x 10^11 J','3/3'],[4,'0.5 x 1.63e6 x 362^2','2/3'],
 [5,'area under graph, 8000 m','2/2'],[5,'8000 m','1/2'],[5,'area under the graph','1/2'],[5,'area under graph, 2000 m','1/2'],
 [6,'1750 m/s','2/2'],[6,'350 m/s','0/2'],
]);
run('9702-26-21-Q2',{mp:0.086,xp:0.026,dp:0.015},[
 [0,'force per extension','1/1'],[0,'force','0/1'],[0,'the stiffness','0/1'],
 [2,'33 N/m (g=10)','2/2'],[2,'32','2/2'],[2,'0.086 x 9.81 / 0.026','1/2'],
 [5,'0.004 J','2/2'],[5,'0.003 J','2/2'],[5,'0.02 J','0/2'],
 [6,'energy is lost as thermal energy so it is less','2/2'],[6,'it is greater','0/2'],
]);
run('9702-26-21-Q4',{rho0p:1.57,alp:4.2,thp:20,Lp:2.0,dp:0.60,Ip:5.6,np:8.5},[
 [2,'0.12 ohm','2/2'],[2,'0.12','2/2'],[2,'1.2 ohm','0/2'],
 [3,'less than 20 because the resistivity is lower','2/2'],[3,'greater than 20','0/2'],
 [5,'K^-1','1/1'],[5,'per kelvin','1/1'],[5,'ohm m','0/1'],[5,'C-1','0/1'],
 [6,'4 x 10^-3 K-1','2/2'],[6,'5 x 10^-3','2/2'],[6,'0.04','0/2'],
 [7,'1.5e-3','2/2'],[7,'1.47 x 10^-3 m/s','2/2'],[7,'1.5e3','0/2'],
]);
console.log(bad?('FAILS: '+bad):'ALL OK');
