##v1  supporting figures, batch 1 (static symbolic SVGs). Run: python3 figs1.py ../../assets
import sys,math
from figlib import C,save
OUT=sys.argv[1] if len(sys.argv)>1 else '../../assets'
F={}

def pump():
    c=C(460,250)
    c.rect(130,80,170,48,'#f4f4f4'); c.text(215,72,'pump barrel','middle')
    c.rect(196,84,12,40,'#bbb'); c.line(208,104,100,104,3); c.line(100,88,100,120,4)
    c.text(100,76,'handle','middle'); c.line(202,82,202,50,1.2); c.text(202,44,'piston','middle')
    c.wire([(300,104),(340,104),(340,150),(374,150)],3)
    c.text(330,176,'hose','middle')
    c.circ(405,150,36); c.circ(405,150,20); c.text(405,214,'bicycle tyre','middle')
    c.nts(); return c

def kettle():
    c=C(420,240)
    c.path('M120,70 L120,170 Q120,190 140,190 L260,190 Q280,190 280,170 L280,70 Z','#fff')
    c.path('M122,110 Q140,102 160,110 T200,110 T240,110 T278,110 L278,170 Q278,188 260,188 L140,188 Q122,188 122,170 Z','#e8e8e8',1)
    c.text(200,150,'water at 100 °C','middle')
    c.path('M280,90 L330,60 L335,70 L282,104','#fff')
    c.line(120,66,280,66,1.6)
    c.wire([(140,198),(165,206),(190,198),(215,206),(240,198),(260,204)],2.2)
    c.text(200,230,'heater','middle')
    c.arrow(60,150,112,150); c.text(14,142,'thermal'); c.text(14,158,'energy')
    c.text(14,174,'supplied'); c.nts(); return c

def satellite():
    c=C(440,330); cx,cy=190,165
    c.circ(cx,cy,64,'#eee'); c.text(cx,cy+5,'planet','middle')
    c.line(cx,cy,cx-64*math.cos(math.radians(40)),cy+64*math.sin(math.radians(40)),1.6)
    c.text(cx-52,cy+20,'R')
    r1,r2=96,134
    c.circ(cx,cy,r1,'none',1.6,'6,4'); c.circ(cx,cy,r2,'none',1.6,'2,4')
    sx,sy=cx+r1,cy
    c.circ(sx,sy,6,'#000'); c.text(sx+10,sy-8,'satellite')
    c.dim(cx+64,cy+14,cx+r1,cy+14); c.text((cx+64+cx+r1)/2,cy+32,'h<tspan font-size="10" dy="3">1</tspan>','middle')
    c.dim(cx+r1+2,cy+44,cx+r2,cy+44)
    c.text(cx+r1+(r2-r1)/2+2,cy+62,'h<tspan font-size="10" dy="3">2</tspan>','middle')
    c.line(cx+r1,cy+8,cx+r1,cy+48,0.8,'2,3'); c.line(cx+r2,cy+38,cx+r2,cy+50,0.8,'2,3')
    c.text(cx,318,'h<tspan font-size="10" dy="3">1</tspan> and h<tspan font-size="10" dy="3">2</tspan> are heights above the surface of the planet','middle',12)
    c.nts(); return c

def iceBeaker():
    c=C(380,260)
    c.path('M110,50 L110,200 Q110,220 130,220 L250,220 Q270,220 270,200 L270,50','#fff')
    c.path('M112,110 L268,110 L268,200 Q268,218 250,218 L130,218 Q112,218 112,200 Z','#e6eef6',1)
    c.text(190,196,'water','middle')
    c.rect(168,96,40,40,'#fff',1.8); c.text(188,121,'ice','middle')
    c.text(190,36,'beaker','middle')
    c.nts(); return c

def cone():
    c=C(420,320); ax=210; ay=250
    th=40; t=math.radians(th); L=190
    c.line(ax,ay,ax-L*math.cos(t),ay-L*math.sin(t),2.4); c.line(ax,ay,ax+L*math.cos(t),ay-L*math.sin(t),2.4)
    bx=ax+130; by=ay-130*math.tan(t)
    rr=bx-ax
    c.ell(ax,by,rr,22,'none',1.6,'6,4')
    c.line(ax,by-70,ax,ay,1.2,'3,3')
    c.circ(bx,by,11,'#999',2)
    c.dim(ax,by,bx-12,by); c.text((ax+bx)/2,by+18,'r','middle')
    c.line(ax,ay,ax+150,ay,1.4)
    c.path('M%.1f,%.1f A60,60 0 0 0 %.1f,%.1f'%(ax+60,ay,ax+60*math.cos(t),ay-60*math.sin(t)),'none',1.4)
    c.text(ax+66,ay-8,'θ'); c.text(210,300,'hollow circular cone','middle'); c.text(bx+16,by-16,'steel ball')
    c.text(ax-6,by-76,'axis','end'); c.nts(); return c

def selector():
    c=C(480,260); x0,x1=90,380; yt,yb=70,190
    c.rect(x0,yt-6,x1-x0,6,'#bbb'); c.rect(x0,yb,x1-x0,6,'#bbb')
    c.rect(x0,yt,x1-x0,yb-yt,'none',1,'4,4')
    c.text(x0+8,yt+22,'uniform magnetic field B'); c.text(x0+8,yt+40,'and uniform electric field E')
    c.dim(x1+40,yt,x1+40,yb); c.text(x1+50,(yt+yb)/2+5,'d')
    c.text((x0+x1)/2,yt-20,'metal plates, p.d. V','middle')
    c.arrow(20,130,x0-8,130); c.text(20,112,'positive ions',size=13); c.text(20,152,'speed u')
    c.arrow(x0+4,130,x1+20,130,1.4,'8,5')
    c.text(x1-6,222,'ions leave the selector','end'); c.nts(); return c

def rod():
    c=C(440,270); xl,xr,yt,yb=80,360,50,210
    for i in range(6):
        for j in range(3):
            c.cross(100+i*50,yt+36+j*44,4)
    c.text(xr,yt-14,'uniform magnetic field B into the page','end')
    c.line(40,yt+10,xr+10,yt+10,2.4); c.line(40,yb-10,xr+10,yb-10,2.4)
    c.line(225,yt+10,225,yb-10,5)
    c.dim(22,yt+10,22,yb-10); c.text(8,134,'l')
    c.text(225,236,'metal rod','middle')
    c.arrow(240,246,330,246,2.4); c.text(336,251,'rod accelerates')
    c.text(40,yt-2,'metal rails'); c.nts(); return c

def ballOil():
    c=C(360,320)
    c.path('M90,30 L90,280 Q90,298 108,298 L192,298 Q210,298 210,280 L210,30','#fff')
    c.rect(92,90,116,206,'#efe9d8',1); c.line(92,90,208,90,1.6)
    c.text(150,120,'oil','middle'); c.text(222,94,'surface of oil')
    c.circ(150,190,18,'#8a8a8a',2.2); c.text(176,170,'steel ball')
    c.arrow(150,212,150,262,2.4); c.text(160,248,'v'); c.text(160,264,'(terminal speed)',size=11)
    c.nts(); return c

def grating():
    c=C(520,300); gx=150; cy=160; sx=400
    c.arrow(20,cy,gx-4,cy,2); c.text(20,cy-12,'monochromatic light')
    c.line(gx,40,gx,270,5); c.text(gx,30,'diffraction grating','middle')
    c.line(sx,40,sx,270,2.4); c.text(sx,30,'screen','middle')
    c.line(gx+1,cy,sx,cy,1.6); c.circ(sx,cy,4,'#000'); c.text(sx+10,cy+4,'zero order',size=12)
    for ang,rad,name,lab in ((18,50,'first-order maximum','θ<tspan font-size="10" dy="3">1</tspan>'),(40,84,'second-order maximum','θ<tspan font-size="10" dy="3">2</tspan>')):
        a=math.radians(ang); ey=cy-(sx-gx)*math.tan(a)
        if ey<46:
            ex=gx+(cy-46)/math.tan(a); c.line(gx,cy,ex,46,1.6); c.text(ex+8,50,name,size=12)
        else:
            c.line(gx,cy,sx,ey,1.6); c.circ(sx,ey,4,'#000'); c.text(sx+10,ey+4,name,size=12)
        c.path('M%.1f,%.1f A%d,%d 0 0 0 %.1f,%.1f'%(gx+rad,cy,rad,rad,gx+rad*math.cos(a),cy-rad*math.sin(a)),'none',1.2)
        c.text(gx+rad+6,cy-rad*math.sin(a)*0.5+4 if ang<30 else cy-rad*math.sin(a)-2,lab)
    c.text(gx+8,290,'grating line spacing d'); c.nts(); return c

def circ_r_t():
    c=C(440,300)
    # cell with internal resistance r in a dashed box
    c.rect(34,100,92,60,'none',1.2,'5,4')
    c.cell(60,130); c.resistor(100,130,False,30,14)
    c.text(78,92,'E','middle'); c.text(100,184,'r','middle')
    c.wire([(34,130),(34,40),(250,40),(250,260),(34,260),(34,130)],1.8) # outline
    # overwrite left side parts: draw cell on left vertical instead
    return c

def circuit5():
    c=C(460,300)
    # layout: left cell (vertical) with internal resistance box, top rail, two parallel branches
    xl,xa,xb,yt,yb=60,230,360,50,250
    c.wire([(xl,yt),(xb,yt)]); c.wire([(xl,yb),(xb,yb)])
    c.wire([(xa,yt),(xa,150-24)]); c.wire([(xa,150+24),(xb-0,yb)][:1]+[(xa,yb)])
    c.wire([(xb,yt),(xb,150-24)]); c.wire([(xb,150+24),(xb,yb)])
    c.wire([(xl,yt),(xl,95)]); c.wire([(xl,215),(xl,yb)])
    c.cell(xl,130,True); c.resistor(xl,180,True,40,16)
    c.wire([(xl,95),(xl,116)]); c.wire([(xl,130+7),(xl,160)]); c.wire([(xl,200),(xl,215)])
    c.rect(xl-34,100,68,118,'none',1.2,'5,4')
    c.text(xl-42,134,'E','end'); c.text(xl-42,186,'r','end')
    c.resistor(xa,150,True,48,18); c.thermistor(xb,150,True,48,18)
    c.text(xa+18,154,'R'); c.text(xb+22,154,'T')
    c.dot(xa,yt); c.dot(xa,yb); c.dot(xb,yt) ; c.dot(xb,yb)
    c.arrow(xa-30,90,xa-30,120,1.8) ; c.text(xa-70,110,'I<tspan font-size="10" dy="3">R</tspan>')
    c.text(xa-18,200,'')
    c.nts(); return c

for name,fn in (('pump',pump),('kettle',kettle),('satellite',satellite),('icebeaker',iceBeaker),('cone',cone),('selector',selector),('rod',rod),('balloil',ballOil),('grating',grating),('circuit5',circuit5)):
    F['as_fig_'+name+'.svg']=fn()
if __name__=='__main__':
    for k,c in F.items(): save(OUT,k,c)
    print(sorted(F))
