##v1  shared helpers for IGCSE 0625 builders
import sys, json
import os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from rowlib import *
from jshelpers import GSVG
LV='IGCSE'
def lab(s): return '<b>'+s+'</b> '
def X(s):
    """expand ops: x -> also * and x variants; / for ÷; - variants for minus"""
    out=[]
    for a in s:
        out.append(a)
        if '×' in a:
            out.append(a.replace('×','x')); out.append(a.replace('×','*'))
        if '÷' in a: out.append(a.replace('÷','/'))
    return out
def kwv(*alts):
    out=[]
    for a in X(alts):
        out.append(a)
        if '-' in a and any(ch.isdigit() for ch in a):
            out.append(a.replace('-','−')); out.append(a.replace('-','–'))
    return '|'.join(dict.fromkeys(out))
SF="(x,n)=>String(+x.toPrecision(n))"
EX="(x,d)=>x.toExponential(d).replace('e+','e')"
# svg building blocks (G helpers; define in this order)
HD="(W,H)=>'<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 '+W+' '+H+'\" style=\"max-width:'+W+'px;width:100%;background:#fff;display:block;margin:10px 0\" font-family=\"Arial,sans-serif\" font-size=\"14\"><defs><marker id=\"ah\" viewBox=\"0 0 10 10\" refX=\"9\" refY=\"5\" markerWidth=\"7\" markerHeight=\"7\" orient=\"auto-start-reverse\"><path d=\"M0,0 L10,5 L0,10 z\" fill=\"#000\"/></marker></defs>'"
LN="(a,b,c,d,x)=>'<line x1=\"'+a+'\" y1=\"'+b+'\" x2=\"'+c+'\" y2=\"'+d+'\" stroke=\"#000\" stroke-width=\"1.6\"'+(x||'')+'/>'"
TX="(x,y,t,a)=>'<text x=\"'+x+'\" y=\"'+y+'\"'+(a?' text-anchor=\"'+a+'\"':'')+'>'+t+'</text>'"
CAPF="(t)=>'<p style=\"text-align:center;margin:0 0 10px\"><b>'+t+'</b></p>'"
BASE={'sf':SF,'ex':EX,'hd':HD,'ln':LN,'tx':TX,'capf':CAPF}
NTS="'<text x=\"'+(W-10)+'\" y=\"'+(H-8)+'\" text-anchor=\"end\" font-size=\"11\" fill=\"#444\">not to scale</text>'"
