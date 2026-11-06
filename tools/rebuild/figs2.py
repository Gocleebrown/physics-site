##v1  supporting figures, batch 2. Run: python3 figs2.py ../../assets
import sys,math
from figlib import C,save
OUT=sys.argv[1] if len(sys.argv)>1 else '../../assets'
F={}
SUB=lambda t:'<tspan font-size="10" dy="3">%s</tspan>'%t

def hatom():   # proton, midpoint P, electron; separation 2x
    c=C(480,170); y=80; xp,xe=90,390; xm=(xp+xe)/2
    c.circ(xp,y,16,'#fff',2); c.text(xp,y+5,'+','middle',style='font-weight="bold"')
    c.circ(xe,y,9,'#fff',2); c.text(xe,y+5,'–','middle',style='font-weight="bold"')
    c.text(xp,y-28,'proton','middle'); c.text(xe,y-24,'electron','middle')
    c.line(xp+16,y,xe-9,y,1.2,'5,4'); c.dot(xm,y,4); c.text(xm,y-12,'P','middle')
    c.dim(xp,y+40,xm,y+40); c.dim(xm,y+40,xe,y+40); c.text((xp+xm)/2,y+60,'x','middle'); c.text((xm+xe)/2,y+60,'x','middle')
    c.nts(); return c

def capPar():
    c=C(420,250); xl,xr,yt,yb=70,350,50,200
    c.wire([(xl,yt),(xr,yt)]); c.wire([(xl,yb),(xr,yb)])
    c.wire([(xl,yt),(xl,110)]); c.wire([(xl,150),(xl,yb)]); c.cell(xl,130,True)
    for x,l in ((180,'X'),(290,'Y')):
        c.wire([(x,yt),(x,119)]); c.wire([(x,141),(x,yb)]); c.capacitor(x,130,True); c.text(x+22,135,'C'+SUB(l))
    c.dot(180,yt);c.dot(180,yb);c.dot(290,yt);c.dot(290,yb)
    c.text(xl-16,134,'E','end'); c.nts(); return c

def capSer():
    c=C(480,260); xl,xr,yt,yb=70,420,50,200
    c.wire([(xl,yt),(xr,yt)]); c.wire([(xr,yt),(xr,yb)]); c.wire([(xl,yb),(xr,yb)])
    c.wire([(xl,yt),(xl,115)]); c.wire([(xl,145),(xl,yb)]); c.cell(xl,130,True)
    # series capacitors on the top wire: break the wire (draw over with white)
    c.rect(200,yt-3,130,6,'#fff',0)
    for x,l in ((225,'C'),(305,'2C')):
        c.line(x-14,yt,x-5,yt,1.8); c.line(x+5,yt,x+14,yt,1.8) if False else None
    c.add('<rect x="170" y="%d" width="170" height="8" fill="#fff"/>'%(yt-4))
    c.wire([(120,yt),(200,yt)]); c.wire([(300,yt),(305,yt)])
    c.wire([(xl,yt),(200,yt)]); c.capacitor(210,yt,False); c.wire([(215,yt),(290,yt)]); c.capacitor(300,yt,False); c.wire([(305,yt),(xr,yt)])
    c.text(210,yt-24,'C','middle'); c.text(300,yt-24,'2C','middle'); c.text(xl-16,134,'supply','end',size=13)
    c.nts(); return c

def spectrometer():
    c=C(460,340); x0,x1,yt,yb=40,420,50,270; yx=210
    c.rect(x0,yt,x1-x0,yb-yt,'#f3f8fb',1.4)
    for i in range(5):
        for j in range(3): c.dot(110+i*70,80+j*45,2.6); c.circ(110+i*70,80+j*45,6,'none',1)
    c.text(x0,yt-12,'region of uniform magnetic field B (out of the plane of the page)',size=13)
    c.line(x0,yx,x1,yx,1.0,'3,4')
    c.arrow(x0+30,yx+56,x0+30,yx-4,2.4); c.text(x0+42,yx+52,'beam of charged particles',size=13)
    c.add('<polygon points="%d,%d %d,%d %d,%d" fill="#000"/>'%(x0,yx-8,x0,yx+8,x0+12,yx)); c.text(x0-8,yx+4,'X','end',style='font-weight="bold"')
    xy=340; c.rect(xy-8,yx-8,16,16,'#000'); c.text(xy+14,yx+5,'Y',style='font-weight="bold"'); c.text(xy,yx-16,'detector','middle',12)
    c.dim(x0+14,yx+28,xy-12,yx+28); c.text((x0+xy)/2+20,yx+20,'XY','middle')
    c.nts(); return c

def aircraft():
    c=C(400,330); cx,cy=200,170; R=110
    c.circ(cx,cy,R,'none',1.6,'6,4'); c.dot(cx,cy,3.5); c.text(cx-24,cy+22,'centre',size=12)
    a=math.radians(-35); ax,ay=cx+R*math.cos(a),cy+R*math.sin(a)
    tx,ty=-math.sin(a),math.cos(a)
    c.add('<g transform="translate(%.1f,%.1f) rotate(%.1f) scale(1.5)"><ellipse cx="0" cy="0" rx="17" ry="3.5" fill="#ddd" stroke="#000"/><path d="M0,-3 L-9,-20 L-4,-20 L6,-3 Z M0,3 L-9,20 L-4,20 L6,3 Z M-13,-2 L-17,-9 L-13,-9 L-9,-2 Z M-13,2 L-17,9 L-13,9 L-9,2 Z" fill="#ddd" stroke="#000"/></g>'%(ax,ay,math.degrees(math.atan2(ty,tx))))
    c.arrow(ax+tx*34,ay+ty*34,ax+tx*86,ay+ty*86,2.2); c.text(ax+tx*86+8,ay+ty*86+6,'speed v')
    c.line(cx,cy,ax-8*math.cos(a),ay-8*math.sin(a),1.4); c.text(cx+34,cy-40,'r')
    c.text(cx,cy+R+38,'path of the aircraft viewed from above','middle'); c.nts(); return c

def boxParticle():
    c=C(440,360)
    dx,dy=70,-50; x0,y0,s=90,110,150
    # cube drawn in oblique projection
    def P(x,y,z): return (x0+x*s+z*dx*s/150, y0+(1-y)*s - z*(-dy)*s/150 + 0)
    c.rect(x0,y0+50,s,s,'#fff',1.8)
    c.wire([(x0,y0+50),(x0+dx,y0),(x0+dx+s,y0),(x0+s,y0+50)],1.8); c.wire([(x0+dx+s,y0),(x0+dx+s,y0+s)],1.8); c.wire([(x0+s,y0+50+s),(x0+dx+s,y0+s)],1.8)
    c.line(x0+dx,y0,x0+dx,y0+s,1,'4,3'); c.line(x0+dx,y0+s,x0,y0+50+s,1,'4,3'); c.line(x0+dx,y0+s,x0+dx+s,y0+s,1,'4,3')
    yy=y0+50+s/2-10
    c.circ(x0+s/2+dx/2-20,yy,7,'#444',2)
    c.arrow(x0+s/2+dx/2-14,yy,x0+s/2+dx/2+46,yy,2.2); c.text(x0+s/2+dx/2+10,yy-12,'u'); c.text(x0+s/2+dx/2-34,yy-12,'m')
    c.dim(x0,y0+50+s+22,x0+s,y0+50+s+22); c.text(x0+s/2,y0+50+s+42,'L','middle')
    c.text(x0+s+dx+12,y0+s/2+22,'cubic box'); c.nts(); return c

def springBlock(tag=''):
    c=C(380,340); x=150
    c.line(90,36,210,36,3); 
    for i in range(10): c.line(90+i*13,36,80+i*13,26,1)
    # spring (zigzag) from y=36 to 160
    pts=[(x,36),(x,52)]
    n=10
    for i in range(n): pts.append((x+(14 if i%2==0 else -14),52+ (i+0.5)*(106/n)))
    pts+=[(x,158),(x,172)]; c.wire(pts,2)
    c.rect(x-34,172,68,50,'#aaa',2); c.text(x,203,'block','middle')
    c.nts(); return c

def sphere():
    c=C(380,300); cx,cy,R=190,150,70
    c.circ(cx,cy,R,'#e8e8e8',2); c.text(cx,cy-4,'+Q','middle',style='font-weight="bold"'); c.text(cx,cy+16,'conducting sphere','middle',size=12)
    c.line(cx,cy,cx+R,cy,1.6); c.text(cx+R/2,cy-18,'R','middle') if False else None
    c.text(cx+R/2,cy-6,'R','middle')
    c.text(190,278,'isolated, in a vacuum','middle',12); c.nts(); return c

def xray():
    c=C(500,330)
    c.path('M60,70 L60,230 Q60,250 80,250 L400,250 Q420,250 420,230 L420,70 Q420,50 400,50 L80,50 Q60,50 60,70 Z','#f7f7f7',2)
    c.text(240,40,'evacuated glass tube','middle',12)
    c.rect(100,120,18,60,'#fff',2); c.wire([(100,130),(112,140),(100,150),(112,160),(100,170)],1.4)
    c.text(109,198,'cathode','middle',12)
    c.path('M310,90 L350,110 L350,200 L310,220 Z','#999',2); c.text(320,242,'metal target','middle',12)
    c.arrow(334,196,440,300,2.2); c.text(446,304,'X-rays',size=13)
    c.wire([(60,200),(40,200),(40,310),(330,310),(330,222)],1.6); c.wire([(100,150),(80,150),(80,260),(130,260)],0.01); c.text(250,326,'high-voltage supply','middle',12)
    c.nts(); return c

def planetP():
    c=C(480,260); cx,cy=130,130; R=70
    c.circ(cx,cy,R,'#eee',2); c.text(cx+4,cy+22,'planet','middle')
    c.line(cx-R-60,cy,cx+R+240,cy,1.0,'4,4')
    c.line(cx,cy,cx+R*math.cos(math.radians(145)),cy-R*math.sin(math.radians(145)),1.4); c.text(cx-44,cy-28,'R')
    px=cx+250; c.dot(px,cy,4); c.text(px,cy-12,'P','middle'); c.dot(cx,cy,3)
    c.dim(cx,cy+46,px,cy+46); c.text((cx+px)/2,cy+66,'x','middle')
    c.nts(); return c

def hOrbit():
    c=C(400,300); cx,cy=200,150
    c.circ(cx,cy,100,'none',1.6,'6,4'); c.circ(cx,cy,10,'#fff',2); c.text(cx,cy+5,'+','middle',style='font-weight="bold"')
    c.text(cx,cy+30,'proton','middle',12)
    a=math.radians(35); ex,ey=cx+100*math.cos(a),cy-100*math.sin(a)
    c.circ(ex,ey,7,'#fff',2); c.text(ex+14,ey-6,'electron'); c.text(ex,ey+4,'–','middle',size=12)
    c.line(cx+10*math.cos(a),cy-10*math.sin(a),ex-7*math.cos(a),ey+7*math.sin(a),1.4); c.text(cx+46*math.cos(a)-12,cy-46*math.sin(a)-8,'r')
    c.nts(); return c

def geo():
    c=C(400,320); cx,cy=200,150
    c.circ(cx,cy,50,'#d9e6f2',2); c.text(cx,cy+5,'Earth','middle')
    R=110; c.circ(cx,cy,R,'none',1.6,'6,4')
    a=math.radians(50); sx,sy=cx+R*math.cos(a),cy-R*math.sin(a)
    c.rect(sx-7,sy-7,14,14,'#777',1.8); c.text(sx+12,sy-8,'satellite')
    c.dim(cx,cy,sx,sy) if False else c.line(cx,cy,sx-7*math.cos(a),sy+7*math.sin(a),1.4)
    c.text(cx+52*math.cos(a)-12,cy-52*math.sin(a)-6,'R')
    c.text(cx,300,'circular orbit of the satellite (dashed)','middle',12); c.nts(); return c

def springPlatform():
    c=C(380,340); x=190
    c.rect(100,24,180,16,'#ccc',2); c.text(290,38,'platform')
    pts=[(x,40),(x,56)]
    for i in range(10): pts.append((x+(14 if i%2==0 else -14),56+(i+0.5)*10.6))
    pts+=[(x,168),(x,182)]; c.wire(pts,2)
    c.circ(x,206,24,'#999',2); c.text(x+36,210,'metal ball')
    c.nts(); return c

def switchCirc():
    c=C(470,320); xl,yt,yb=60,50,270
    # cell on the left, top wire to terminal X
    c.wire([(xl,yt),(180,yt),(180,110)]); c.wire([(xl,yt),(xl,105)]); c.wire([(xl,155),(xl,yb)]); c.cell(xl,130,True); c.text(xl-14,134,'E','end')
    c.dot(180,110); c.text(170,106,'X','end',style='font-weight="bold"')
    # terminal Y -> resistor R -> bottom rail
    c.dot(340,110); c.text(350,106,'Y',style='font-weight="bold"'); c.wire([(340,110),(340,150)]); c.resistor(340,180,True,50,18); c.wire([(340,205),(340,yb)]); c.text(366,184,'R')
    # pole -> capacitor -> bottom rail
    px,py=260,180; c.dot(px,py); c.wire([(px,py),(px,200)]); c.capacitor(px,215,True); c.wire([(px,221),(px,yb)]); c.text(px+22,219,'C')
    c.wire([(xl,yb),(340,yb)])
    c.line(px,py,px,128,2.2); c.text(px+10,150,'S')
    c.add('<path d="M185,92 Q260,56 335,92" fill="none" stroke="#000" stroke-width="1.3" marker-start="url(#ah)" marker-end="url(#ah)"/>')
    c.nts(); return c

def alpha():
    c=C(480,250)
    c.text(20,28,'before collision',style='font-weight="bold"'); c.text(20,148,'after collision',style='font-weight="bold"')
    c.circ(60,70,9,'#666',2); c.arrow(72,70,150,70,2.4); c.text(100,56,'u'); c.text(40,98,'α-particle',size=12)
    c.circ(330,70,26,'#bbb',2); c.text(330,76,'Au','middle',13); c.text(330,116,'gold nucleus, at rest','middle',12)
    c.circ(240,190,9,'#666',2); c.arrow(228,190,150,190,2.4); c.text(190,176,'v'); c.text(240,218,'α-particle','middle',12)
    c.circ(330,190,26,'#bbb',2); c.text(330,196,'Au','middle',13)
    c.nts(); return c

def car():
    c=C(480,200)
    c.path('M70,120 L70,100 L110,100 L130,72 L200,72 L225,100 L260,100 L260,120 Z','#ddd',2)
    c.circ(110,124,14,'#666',2); c.circ(220,124,14,'#666',2)
    c.line(20,140,460,140,1.6)
    c.arrow(270,96,340,96,2.4); c.text(300,86,'u'); c.text(66,64,'car of mass m')
    c.dim(70,170,400,170); c.text(235,192,'s','middle'); c.text(412,176,'(brakes applied here)',size=11) if False else None
    c.line(400,140,400,176,1,'3,3'); c.line(70,140,70,176,1,'3,3')
    c.nts(); return c

def wireCirc():
    c=C(420,230); xl,xr,yt,yb=60,360,60,180
    c.wire([(xl,yt),(130,yt)]); c.wire([(290,yt),(xr,yt)]); c.wire([(xl,yb),(xr,yb)]); c.wire([(xr,yt),(xr,yb)]); c.wire([(xl,yt),(xl,110)]); c.wire([(xl,150),(xl,yb)])
    c.cell(xl,130,True); c.text(xl-12,134,'power supply','end',size=12) if False else None
    c.rect(130,yt-10,160,20,'#fff',2); c.text(210,yt-18,'nichrome wire','middle')
    c.text(xl,yb+28,'power supply','middle',12)
    c.nts(); return c

def cylinder():
    c=C(420,260)
    c.rect(130,80,170,110,'#f3f3f3',2); c.rect(140,70,12,130,'#bbb',2)
    c.line(152,135,152,135,0.01)
    c.line(148,135,60,135,3); c.line(60,110,60,160,4)
    c.text(230,138,'ideal gas','middle'); c.text(146,60,'piston','middle')
    c.text(215,222,'cylinder','middle'); c.nts(); return c

for name,fn in (('hatom',hatom),('cappar',capPar),('capser',capSer),('spectro',spectrometer),('aircraft',aircraft),('boxpart',boxParticle),('springblock',springBlock),('sphere',sphere),('xray',xray),('planetp',planetP),('horbit',hOrbit),('geo',geo),('springplat',springPlatform),('switchc',switchCirc),('alpha',alpha),('car',car),('wirec',wireCirc),('cylinder',cylinder)):
    F['as_fig_'+name+'.svg']=fn()
if __name__=='__main__':
    for k,c in F.items(): save(OUT,k,c)
    print(len(F))
