"""AS 26-24 answer-option SVGs (imageChoice). Run: python3 svg24.py ../../assets"""
import sys, os, math
sys.path.insert(0,'.')
from imglib import svg, poly, save
OUT=sys.argv[1] if len(sys.argv)>1 else '../../assets'

# ---------- Q3(b), Q3(d): string between two fixed points (4-loop figure; symbolic, no numbers) ----------
def string(n, cross=None, kind='sine'):
    """n loops. cross = (u, on_string_value) position of a red cross: u in 0..1 along the string, ym in -1..1"""
    W,H=320,170; x0,x1=30,290; cy=90; A=46
    body='<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#999" stroke-dasharray="4,3"/>'%(x0,cy,x1,cy)
    body+='<line x1="%d" y1="40" x2="%d" y2="%d" stroke="#000" stroke-dasharray="2,3"/><line x1="%d" y1="40" x2="%d" y2="%d" stroke="#000" stroke-dasharray="2,3"/>'%(x0,x0,cy+A+10,x1,x1,cy+A+10)
    body+='<text x="%d" y="30" text-anchor="middle">L</text><line x1="%d" y1="36" x2="%d" y2="36" stroke="#000"/>'%((x0+x1)//2,x0,x1)
    pts=[]
    N=320
    for i in range(N+1):
        u=i/N
        if kind=='sine': y=math.sin(math.pi*n*u)
        else:   # triangle wave (not sinusoidal)
            ph=(n*u)%2; y=(ph if ph<=1 else 2-ph)*2-1 if False else (1-abs(ph-1))*2-1  # zig-zag
            y=y*0+ (ph if ph<=1 else 2-ph)
        pts.append((x0+(x1-x0)*u, cy-A*y))
    body+=poly(pts)
    body+='<circle cx="%d" cy="%d" r="3.5"/><circle cx="%d" cy="%d" r="3.5"/>'%(x0,cy,x1,cy)
    body+='<text x="%d" y="%d" text-anchor="middle" font-size="12">fixed point</text><text x="%d" y="%d" text-anchor="middle" font-size="12">fixed point</text>'%(x0,cy+A+28,x1,cy+A+28)
    if cross:
        u,ym=cross
        x=x0+(x1-x0)*u; y=cy-A*ym
        body+='<path d="M%.1f,%.1f l12,12 m0,-12 l-12,12" transform="translate(-6,-6)" stroke="#c00" stroke-width="2.6" fill="none"/>'%(x,y)
    return svg(W,H,body)

# ---------- Q5(b): sketch of the I-V line of the 40 ohm conductor (axes as in Figure 5.1) ----------
def iv(kind):
    W,H=340,300; L,R,T,B=52,14,14,44; pw=W-L-R; ph=H-T-B
    sx=lambda v:L+pw*v/0.8; sy=lambda i:T+ph-ph*i/40.0
    body=''
    for k in range(0,41,2):
        body+='<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="%s"/>'%(L,sy(k),L+pw,sy(k),'#d9a0a0' if k%10==0 else '#efcaca','1' if k%10==0 else '0.5')
    for k in range(0,17):
        v=k*0.05
        body+='<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="%s"/>'%(sx(v),T,sx(v),T+ph,'#d9a0a0' if k%4==0 else '#efcaca','1' if k%4==0 else '0.5')
    for k in (0,10,20,30,40): body+='<text x="%d" y="%.1f" text-anchor="end">%d</text>'%(L-6,sy(k)+4,k)
    for v,l in ((0,'0'),(0.2,'0.2'),(0.4,'0.4'),(0.6,'0.6'),(0.8,'0.8')): body+='<text x="%.1f" y="%d" text-anchor="middle">%s</text>'%(sx(v),T+ph+16,l)
    body+='<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="#000"/>'%(L,T,pw,ph)
    body+='<text x="%d" y="%d" text-anchor="middle"><tspan font-style="italic">V</tspan> / V</text><text transform="translate(12,%d) rotate(-90)" text-anchor="middle"><tspan font-style="italic">I</tspan> / mA</text>'%(L+pw/2,H-8,T+ph/2)
    if kind=='a':   pts=[(sx(0),sy(0)),(sx(0.8),sy(20))]                         # correct: R = 40 ohm
    elif kind=='b': pts=[(sx(0),sy(0)),(sx(0.8),sy(40))]                         # R = 20 ohm
    elif kind=='c': pts=[(sx(0),sy(0)),(sx(0.8),sy(10))]                         # R = 80 ohm
    else:           pts=[(sx(0.8*i/60),sy(20*(i/60)**2)) for i in range(61)]     # curve through (0.8, 20)
    return svg(W,H,body+poly(pts,2.4))

if __name__=='__main__':
    # (b): node cross. correct = node at u=0.5 (zero displacement); wrong = antinode, between, at fixed point side
    for k,c in zip('abcd',((0.5,0),(0.125,1),(0.375,-1),(0.3,-0.588))): save(OUT,'as2624_q3b_%s.svg'%k,string(4,cross=c))
    # (d): halved frequency -> wavelength doubles -> 2 loops. correct = 2 loops
    save(OUT,'as2624_q3d_a.svg',string(2)); save(OUT,'as2624_q3d_b.svg',string(1)); save(OUT,'as2624_q3d_c.svg',string(4)); save(OUT,'as2624_q3d_d.svg',string(3))
    for k in 'abcd': save(OUT,'as2624_q5b_%s.svg'%k,iv(k))
    print(sorted(f for f in os.listdir(OUT) if f.startswith('as2624')))
