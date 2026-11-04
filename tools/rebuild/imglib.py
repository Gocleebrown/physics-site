import math, os
HEAD='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" font-family="Arial,sans-serif" font-size="13"><rect width="100%%" height="100%%" fill="#fff"/>'
def svg(w,h,body): return (HEAD%(w,h,w,h))+body+'</svg>'
def poly(pts,sw=2,col='#000'): return '<polyline fill="none" stroke="%s" stroke-width="%s" points="%s"/>'%(col,sw,' '.join('%.1f,%.1f'%p for p in pts))

# ---- displacement-time graph of X (symbolic axes): between t=0 and 2T ----
def disp_time(kind):
    W,H=300,190; L,R,T,B=46,12,14,36; pw=W-L-R; ph=H-T-B; cy=T+ph/2; A=ph/2-6
    body=''
    # axes
    body+='<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#000"/>'%(L,T,L,T+ph)
    body+='<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#000"/>'%(L,cy,L+pw,cy)
    body+='<text x="%d" y="%.1f" text-anchor="end">+A</text><text x="%d" y="%.1f" text-anchor="end">&#8722;A</text><text x="%d" y="%.1f" text-anchor="end">0</text>'%(L-6,cy-A+4,L-6,cy+A+4,L-6,cy+4)
    body+='<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#999" stroke-dasharray="3,3"/><line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#999" stroke-dasharray="3,3"/>'%(L,cy-A,L+pw,cy-A,L,cy+A,L+pw,cy+A)
    labs=['0','T/2','T','3T/2','2T']
    for i,l in enumerate(labs):
        x=L+pw*i/4
        body+='<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#000"/><text x="%.1f" y="%d" text-anchor="middle">%s</text>'%(x,cy-3,x,cy+3,x,T+ph+16,l)
    body+='<text x="%d" y="%d" text-anchor="end">t</text>'%(L+pw,T+ph+32)
    pts=[]
    N=200
    for i in range(N+1):
        u=i/N  # 0..1 over 2T
        if kind=='a': y=-math.sin(2*math.pi*2*u)          # correct: negative sine, 2 cycles
        elif kind=='b': y=math.sin(2*math.pi*2*u)         # wrong phase
        elif kind=='c': y=-math.sin(2*math.pi*1*u)        # one cycle only (period 2T)
        else: y=math.cos(2*math.pi*2*u)                   # starts at maximum
        pts.append((L+pw*u, cy-A*y))
    return svg(W,H,body+poly(pts))

# ---- stationary wave on string PQ ----
def string(loops, ends='node', marks=None):
    W,H=300,130; x0,x1=24,276; cy=65; A=38
    body='<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#888" stroke-dasharray="4,3"/>'%(x0,cy,x1,cy)
    pts=[]
    N=300
    for i in range(N+1):
        u=i/N
        ph=math.pi*loops*u
        y=math.sin(ph) if ends=='node' else math.cos(ph)
        pts.append((x0+(x1-x0)*u, cy-A*y))
    body+=poly(pts)
    body+='<circle cx="%d" cy="%d" r="3.5"/><circle cx="%d" cy="%d" r="3.5"/>'%(x0,cy,x1,cy)
    body+='<text x="%d" y="%d" text-anchor="end">P</text><text x="%d" y="%d">Q</text>'%(x0-8,cy+5,x1+8,cy+5)
    for (u,ym,lab) in (marks or []):
        x=x0+(x1-x0)*u; y=cy-A*ym
        body+='<path d="M%.1f,%.1f l8,8 m0,-8 l-8,8" transform="translate(-4,-4)" stroke="#c00" stroke-width="2.2" fill="none"/>'%(x,y)
        body+='<text x="%.1f" y="%.1f" fill="#c00" font-weight="bold" text-anchor="middle">%s</text>'%(x,(y-9) if ym>=0 else (y+22),lab)
    return svg(W,H,body)

def save(outdir,name,content):
    os.makedirs(outdir,exist_ok=True)
    open(os.path.join(outdir,name),'w',encoding='utf-8').write(content)
