##v1
"""Symbolic supporting-figure primitives (black/white, CIE style, no answers shown)."""
import math
FONT='font-family="Arial,sans-serif" font-size="14"'
class C:
    def __init__(s,w,h): s.w=w;s.h=h;s.b=[]
    def add(s,x): s.b.append(x); return s
    def line(s,x1,y1,x2,y2,w=1.6,dash=None,col='#000',marker=None):
        d=' stroke-dasharray="%s"'%dash if dash else ''
        m=''
        if marker=='end': m=' marker-end="url(#ah)"'
        elif marker=='both': m=' marker-start="url(#ah)" marker-end="url(#ah)"'
        return s.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s%s/>'%(x1,y1,x2,y2,col,w,d,m))
    def arrow(s,x1,y1,x2,y2,w=1.8,dash=None): return s.line(x1,y1,x2,y2,w,dash,marker='end')
    def dim(s,x1,y1,x2,y2): return s.line(x1,y1,x2,y2,1.3,marker='both')
    def wire(s,pts,w=1.8,dash=None):
        d=' stroke-dasharray="%s"'%dash if dash else ''
        return s.add('<polyline fill="none" stroke="#000" stroke-width="%s"%s stroke-linejoin="round" points="%s"/>'%(w,d,' '.join('%.1f,%.1f'%p for p in pts)))
    def rect(s,x,y,w,h,fill='none',sw=1.8,dash=None,rx=0):
        d=' stroke-dasharray="%s"'%dash if dash else ''
        return s.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="#000" stroke-width="%s"%s/>'%(x,y,w,h,rx,fill,sw,d))
    def circ(s,x,y,r,fill='none',sw=1.8,dash=None):
        d=' stroke-dasharray="%s"'%dash if dash else ''
        return s.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="#000" stroke-width="%s"%s/>'%(x,y,r,fill,sw,d))
    def ell(s,x,y,rx,ry,fill='none',sw=1.6,dash=None):
        d=' stroke-dasharray="%s"'%dash if dash else ''
        return s.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="#000" stroke-width="%s"%s/>'%(x,y,rx,ry,fill,sw,d))
    def path(s,d,fill='none',sw=1.8,dash=None):
        da=' stroke-dasharray="%s"'%dash if dash else ''
        return s.add('<path d="%s" fill="%s" stroke="#000" stroke-width="%s"%s/>'%(d,fill,sw,da))
    def text(s,x,y,t,anchor='start',size=None,style=''):
        sz=' font-size="%s"'%size if size else ''
        return s.add('<text x="%.1f" y="%.1f" text-anchor="%s"%s %s>%s</text>'%(x,y,anchor,sz,style,t))
    def cap(s,t): # caption under figure
        return s.add('<text x="%.1f" y="%.1f" text-anchor="middle" font-weight="bold">%s</text>'%(s.w/2,s.h-8,t))
    def nts(s): return s.add('<text x="%.1f" y="%.1f" text-anchor="end" font-size="11" fill="#444">not to scale</text>'%(s.w-8,s.h-8))
    # ---- circuit symbols (horizontal unless v=True), centred at x,y, wire gap length L
    def cell(s,x,y,v=False,L=14):
        if not v:
            s.line(x-L/2,y-14,x-L/2,y+14,1.8); s.line(x+L/2,y-8,x+L/2,y+8,4.5)   # long plate left (+), short thick right (-)
        else:
            s.line(x-14,y-L/2,x+14,y-L/2,1.8); s.line(x-8,y+L/2,x+8,y+L/2,4.5)
    def resistor(s,x,y,v=False,w=44,h=18):
        if not v: s.rect(x-w/2,y-h/2,w,h,'#fff')
        else: s.rect(x-h/2,y-w/2,h,w,'#fff')
    def thermistor(s,x,y,v=False,w=44,h=18):
        s.resistor(x,y,v,w,h)
        if not v: s.wire([(x-w/2-4,y+h/2+10),(x-w/2+8,y+h/2+10),(x+w/2-4,y-h/2-10)],1.6)
        else: s.wire([(x-h/2-10,y+w/2+4),(x-h/2-10,y+w/2-8),(x+h/2+10,y-w/2+4)],1.6)
    def capacitor(s,x,y,v=False,g=10,L=24):
        if not v: s.line(x-g/2,y-L/2,x-g/2,y+L/2,2.4); s.line(x+g/2,y-L/2,x+g/2,y+L/2,2.4)
        else: s.line(x-L/2,y-g/2,x+L/2,y-g/2,2.4); s.line(x-L/2,y+g/2,x+L/2,y+g/2,2.4)
    def meter(s,x,y,t):
        s.circ(x,y,13,'#fff'); s.text(x,y+5,t,'middle',style='font-weight="bold"')
    def lamp(s,x,y):
        s.circ(x,y,13,'#fff'); s.line(x-9,y-9,x+9,y+9,1.4); s.line(x-9,y+9,x+9,y-9,1.4)
    def diode(s,x,y,v=False):  # conventional current left->right (or top->bottom)
        if not v:
            s.add('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="#fff" stroke="#000" stroke-width="1.8"/>'%(x-10,y-12,x-10,y+12,x+10,y)); s.line(x+10,y-12,x+10,y+12,2.2)
        else:
            s.add('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="#fff" stroke="#000" stroke-width="1.8"/>'%(x-12,y-10,x+12,y-10,x,y+10)); s.line(x-12,y+10,x+12,y+10,2.2)
    def dot(s,x,y,r=3.2): return s.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#000"/>'%(x,y,r))
    def cross(s,x,y,r=5): s.line(x-r,y-r,x+r,y+r,1.5); s.line(x-r,y+r,x+r,y-r,1.5)
    def out(s):
        defs='<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#000"/></marker></defs>'
        return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '+FONT+'><rect width="100%%" height="100%%" fill="#fff"/>')%(s.w,s.h,s.w,s.h)+defs+''.join(s.b)+'</svg>'
def save(outdir,name,c):
    import os
    os.makedirs(outdir,exist_ok=True)
    open(os.path.join(outdir,name),'w',encoding='utf-8').write(c.out())
