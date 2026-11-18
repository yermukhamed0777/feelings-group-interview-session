import os, math
import FreeCAD as App, Part
from FreeCAD import Vector as V
# Measured housing dimensions can be substituted here; all values in mm.
DISPLAY_W, DISPLAY_D, SCREEN_LEVEL = 140., 55., 300.
PAW_W, PAW_D = 27., 21.
CAM_W, CAM_D, CAM_H = 112., 44., 98.
out=os.path.join(os.getcwd(),"StandKit")
def box(w,d,h,x,y,z):
    return Part.makeBox(w,d,h,V(x,y,z))
def plate(w,d,h,z,r=4,y=0):
    a=box(w,d,h,-w/2,y-d/2,z)
    return a.makeFillet(r,[e for e in a.Edges if abs(e.Vertexes[0].Point.z-e.Vertexes[-1].Point.z)>h*.99])
def cyl(r,h,x,y,z):
    return Part.makeCylinder(r,h,V(x,y,z))
def bore_y(r,x,y,z,l):
    return Part.makeCylinder(r,l,V(x,y,z),V(0,1,0))
def join(*a):
    return a[0].multiFuse(list(a[1:])).removeSplitter()
def mounting(a,x,y,z,h):
    for xx in [-x,x]:
        for yy in [-y,y]: a=a.cut(cyl(2.8,h,xx,yy,z))
    return a
def begin(name):
    global doc, items
    doc=App.newDocument(name); items=[]
def item(name,shape):
    shape=shape.removeSplitter()
    assert shape.isValid() and len(shape.Solids)==1,name
    for other in items:
        assert other.Shape.common(shape).Volume<0.001,(name,other.Label)
    obj=doc.addObject("Part::Feature","Component");obj.Label=name;obj.Shape=shape;items.append(obj)
def finish():
    doc.recompute()
    path=os.path.join(out,doc.Name)
    doc.saveAs(path+".FCStd");Part.export(items,path+".step")
    print(doc.Name,[o.Label for o in items])
def socket(z):
    return plate(39,39,32,z,5).cut(box(30.6,30.6,34,-15.3,-15.3,z-1))
begin("DisplayStand")
base=mounting(plate(180,140,8,0,14),75,55,-1,10)
item("Anchor foot and lower mast socket",join(base,socket(8)).cut(bore_y(2.75,0,-22,24,44)))
top=SCREEN_LEVEL-5
mast=plate(30,30,top-8,8,2).cut(box(26,26,top-6,-13,-13,7))
for z in [24,top-16]:mast=mast.cut(bore_y(2.75,0,-22,z,44))
item("30 x 30 x 2 square tube - cut and drill",mast)
w=DISPLAY_W+1.2; d=DISPLAY_D+1.2
tray=plate(w+8,d+8,5,top,5)
back=box(w-4,4,32,-w/2+2,d/2,SCREEN_LEVEL)
features=[tray,back,socket(top-32)]
for sign in [-1,1]:
    x=sign*(w/2-10)
    features.append(box(16,4,6,x-8,-d/2-4,SCREEN_LEVEL))
    features.append(box(4,14,10,-w/2-4 if sign<0 else w/2,d/2-17,SCREEN_LEVEL))
item("Raised display saddle and upper socket",join(*features).cut(bore_y(2.75,0,-22,top-16,44)))
finish()
begin("PawDock")
w=PAW_W+1.2; d=PAW_D+1.2
base=plate(w+32,d+31,8,0,9)
# Bottom cable exits through the front of a raised, open-bottom pocket.
base=base.cut(box(14,(d+31)/2+5,10,-7,-(d+31)/2-1,-1))
outer=plate(w+8,d+8,23,8,6)
pocket=outer.cut(plate(w,d,25,7,3)).cut(box(15,12,25,-7.5,-d/2-8,7))
ledges=[box(4,d-5,4,x,-d/2+2.5,8) for x in [-w/2,w/2-4]]
item("Bedside dock - lift-out pocket and cable exit",join(base,pocket,*ledges))
finish()
begin("CameraPanStand")
# Fixed base, vertical spindle with retaining nut, and manually drivable rotor.
R=max(53,CAM_W/2+4)
base=mounting(plate(2*R+28,2*R+18,7,0,12),R-1,R-5,-1,9)
base=join(base,cyl(18,8,0,0,7)).cut(cyl(4.1,17,0,0,-1))
base=base.cut(cyl(8,4,0,0,-1))
item("Anchor base - recessed pivot bolt seat",base)
item("Thrust washer reference",cyl(16,1,0,0,15).cut(cyl(4.25,2,0,0,14.5)))
z=16
rot=cyl(R,6,0,0,z).cut(cyl(4.25,8,0,0,z-1))
# Four radial drive-link holes on the outer rim for limited-angle actuation.
for ang in (45,135,225,315):
    a=math.radians(ang);rot=rot.cut(cyl(2.1,8,(R-6)*math.cos(a),(R-6)*math.sin(a),z-1))
dw=CAM_D+1.2
# Two inclined rails form a V seat, with front/rear fences and strap slots.
def rail(sign):
    points=[(8,0),(CAM_W*.48,0),(CAM_W*.48, CAM_H*.36),(8,5)]
    v=[V(sign*x,-dw/2,z+6+h) for x,h in points]
    face=Part.Face(Part.makePolygon(v+[v[0]]))
    return face.extrude(V(0,dw,0))
parts=[rot]
for sign in (-1,1):
    a=rail(sign)
    x=sign*CAM_W*.37
    a=a.cut(box(11,dw+2,3,x-5.5,-dw/2-1,z+12))
    for y in [-dw/2-3,dw/2]:
        a=join(a,box(12,3,CAM_H*.25,x-6,y,z+6))
    parts.append(a)
item("Pan rotor - V seat, strap slots and drive holes",join(*parts))
# Example remotely driven crank-rocker layout, servo shaft vertical.
# A removable carrier shares the two right-side base anchor bolts.
pin=(R-6)/math.sqrt(2)
shaft_x=R+64
shaft_y=pin-18
carrier=plate(68,54,5,7,5,shaft_y)
carrier.translate(V(shaft_x,0,0))
carrier=carrier.cut(box(41,21,7,shaft_x-20.5,shaft_y-10.5,6))
for dx in (-24.5,24.5):
    for dy in (-5,5):
        carrier=carrier.cut(cyl(1.7,7,shaft_x+dx,shaft_y+dy,6))
flange=box(14,2*R,5,R-8,-R,7)
for yy in (-R+5,R-5):flange=flange.cut(cyl(2.8,7,R-1,yy,6))
bridge=box(shaft_x-33-(R+3),12,5,R+3,shaft_y-6,7)
item("Servo carrier - verify body and horn offset",join(carrier,flange,bridge))
# Link located above rotor and below the cable strap. Hardware sets this level.
def link(x1,x2,y,z,r,h):
    a=join(cyl(r,h,x1,y,z),cyl(r,h,x2,y,z),box(x2-x1,2*r,h,x1,y-r,z))
    for x in (x1,x2):a=a.cut(cyl(2.1,h+2,x,y,z-1))
    return a
item("Servo pushrod - neutral pose",link(pin,shaft_x,pin,23,4,3))
# Clearance for the servo body beneath its mounting flange.
for xx in (-R+1,R-1):
    for yy in (-R+5,R-5):
        foot=cyl(9,40,xx,yy,-40).cut(cyl(2.8,42,xx,yy,-41))
        item("Through-bolted 40 mm spacer",foot)
finish()


