"""AS 26-23 answer-option SVGs (imageChoice). Run: python3 svg23.py ../../assets"""
import sys, os
sys.path.insert(0,'.')
from imglib import svg, poly, save

OUT=sys.argv[1] if len(sys.argv)>1 else '../../assets'

# ---------- Q1(c)(ii): velocity of Y against time (symbolic axes) ----------
def vy(kind):
    W,H=320,230; L,R,T,B=46,14,16,40; pw=W-L-R; ph=H-T-B; cy=T+ph/2; A=ph/2-22
    xt1,xt2=0.45,0.62
    X=lambda u:L+pw*u
    body='<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#000"/>'%(L,T,L,T+ph)
    body+='<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#000"/>'%(L,cy,L+pw,cy)
    body+='<text x="%d" y="%.1f" text-anchor="end">0</text>'%(L-6,cy+4)
    body+='<text x="%d" y="%.1f" text-anchor="end"><tspan font-style="italic">v</tspan></text>'%(L-6,cy-A+4)
    body+='<text x="%d" y="%.1f" text-anchor="end">&#8722;<tspan font-style="italic">v</tspan></text>'%(L-6,cy+A+4)
    body+='<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#aaa" stroke-dasharray="3,3"/><line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#aaa" stroke-dasharray="3,3"/>'%(L,cy-A,L+pw,cy-A,L,cy+A,L+pw,cy+A)
    for u,l in ((xt1,'t&#8321;'),(xt2,'t&#8322;'),(1.0,'0.20')):
        body+='<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000"/><text x="%.1f" y="%d" text-anchor="middle">%s</text>'%(X(u),cy-3,X(u),cy+3,X(u),T+ph+16,l)
    body+='<text x="%d" y="%d" text-anchor="middle">0</text>'%(L,T+ph+16)
    body+='<text x="%d" y="%d" text-anchor="end">time</text><text transform="translate(12,%d) rotate(-90)" text-anchor="middle">velocity of Y</text>'%(L+pw,T+ph+34,T+ph/2)
    if kind=='a':   pts=[(X(0),cy),(X(xt1),cy),(X(xt2),cy-A),(X(1),cy-A)]          # correct
    elif kind=='b': pts=[(X(0),cy),(X(xt1),cy),(X(xt1),cy-A),(X(1),cy-A)]          # instant jump
    elif kind=='c': pts=[(X(0),cy),(X(xt1),cy),(X(xt2),cy+A),(X(1),cy+A)]          # wrong sign
    else:           pts=[(X(0),cy),(X(xt2),cy-A),(X(1),cy-A)]                      # starts rising at t=0
    return svg(W,H,body+poly(pts))

# ---------- Q3(c): fringe positions on the screen ----------
def screen(kind,mark,label):
    """screen drawn vertically; X at centre, Y one unit above. mark = position in units of XY (+ up)"""
    W,H=240,300; cx=120; cy=150; d=40
    body='<line x1="%d" y1="14" x2="%d" y2="286" stroke="#000" stroke-width="2.2"/>'%(cx,cx)
    body+='<text x="%d" y="12" text-anchor="middle" font-size="12">screen</text>'%(cx)
    body+='<circle cx="%d" cy="%d" r="4"/><text x="%d" y="%d">X</text>'%(cx,cy,cx+12,cy+5)
    body+='<circle cx="%d" cy="%d" r="4"/><text x="%d" y="%d">Y</text>'%(cx,cy-d,cx+12,cy-d+5)
    y=cy-mark*d
    body+='<path d="M%.1f,%.1f l12,12 m0,-12 l-12,12" transform="translate(-6,-6)" stroke="#c00" stroke-width="2.4" fill="none"/>'%(cx-30,y)
    body+='<text x="%d" y="%.1f" fill="#c00" font-weight="bold">%s</text>'%(cx-52,y+5,label)
    body+='<text x="%d" y="%d" text-anchor="middle" font-size="11" fill="#555">not to scale</text>'%(W//2,H-4)
    return svg(W,H,body)

# ---------- Q4(a): circuit diagrams ----------
def circuit(kind):
    W,H=380,240
    ln=lambda a,b,c,d,w=1.8,x='':'<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#000" stroke-width="%s"%s/>'%(a,b,c,d,w,x)
    b=''
    # frame
    b+=ln(60,40,250,40)+ln(60,200,250,200)
    # --- cell side (x=60) ---
    if kind in ('a','b','c'):
        b+=ln(60,40,60,70)+'<rect x="30" y="70" width="60" height="100" fill="none" stroke="#000" stroke-dasharray="4,3"/>'
        b+=ln(60,70,60,84)+'<rect x="52" y="84" width="16" height="32" fill="#fff" stroke="#000" stroke-width="1.8"/>'+ln(60,116,60,136)
        b+=ln(46,136,74,136)+ln(52,146,68,146,5)+ln(60,146,60,200)
        b+='<text x="76" y="105" font-size="13"><tspan font-style="italic">r</tspan></text>'
    else:   # battery: two cells, no internal resistor
        b+=ln(60,40,60,92)+ln(46,92,74,92)+ln(52,102,68,102,5)+ln(46,116,74,116)+ln(52,126,68,126,5)+ln(60,126,60,200)
    # --- component side (x=250) ---
    if kind=='c':       # plain fixed resistor (no light arrows)
        b+=ln(250,40,250,82)+'<rect x="238" y="82" width="24" height="52" fill="#fff" stroke="#000" stroke-width="1.8"/>'+ln(250,134,250,200)
    else:               # LDR: resistor with two arrows pointing at it
        b+=ln(250,40,250,82)+'<rect x="238" y="82" width="24" height="52" fill="#fff" stroke="#000" stroke-width="1.8"/>'+ln(250,134,250,200)
        b+='<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker></defs>'
        b+=ln(205,70,232,92,1.4,' marker-end="url(#ah)"')+ln(215,60,242,82,1.4,' marker-end="url(#ah)"')
    # --- voltmeter ---
    if kind=='b':       # in series (wrong)
        b=b.replace(ln(60,40,250,40),ln(60,40,134,40)+ln(166,40,250,40))
        b+='<circle cx="150" cy="40" r="16" fill="#fff" stroke="#000" stroke-width="1.8"/><text x="150" y="46" text-anchor="middle" font-size="16">V</text>'
    else:               # in parallel with the LDR / resistor
        b+=ln(250,62,320,62)+ln(320,62,320,92)+'<circle cx="320" cy="108" r="16" fill="#fff" stroke="#000" stroke-width="1.8"/><text x="320" y="114" text-anchor="middle" font-size="16">V</text>'
        b+=ln(320,124,320,160)+ln(250,160,320,160)
        b+='<circle cx="250" cy="62" r="3"/><circle cx="250" cy="160" r="3"/>'
    return svg(W,H,b)

if __name__=='__main__':
    for k in 'abcd': save(OUT,'as2623_q1cii_%s.svg'%k,vy(k))
    # bright fringe B: correct = +2 (above Y by XY); wrong: at Y (+1), +3, -1.5
    for k,m in zip('abcd',(2,1,3,-1.5)): save(OUT,'as2623_q3ci_%s.svg'%k,screen(k,m,'B'))
    # dark fringe D: correct = -1 ; wrong: +2, -2, +0.5
    for k,m in zip('abcd',(-1,2,-2,0.5)): save(OUT,'as2623_q3cii_%s.svg'%k,screen(k,m,'D'))
    for k in 'abcd': save(OUT,'as2623_q4a_%s.svg'%k,circuit(k))
    print(sorted(f for f in os.listdir(OUT) if f.startswith('as2623')))
