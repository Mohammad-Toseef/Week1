import math


class Line():
    def __init__(self,coordinate1,coordinate2):
        self.x1 = coordinate1[0]
        self.y1 = coordinate1[1]
        self.x2 = coordinate2[0]
        self.y2 = coordinate2[1]
    def distance(self):
        return math.sqrt(math.pow(self.x2-self.x1,2)+math.pow(self.y2-self.y1,2))
    def slope(self):
        return (self.y2-self.y1)/(self.x2-self.x1)
class Cylinder:
    def __init__(self,height,radius):
        self.height = height
        self.radius = radius
    def volume(self):
        return math.pi*math.pow(self.radius,2)*self.height
    def surface_area(self):
        return (2*math.pi*self.radius*self.height)+(2*math.pi*math.pow(self.radius,2))

coordinate1 = (3,2)
coordinate2 = (8,10)
coordinate1
li = Line(coordinate1,coordinate2)
print("Distance is {}".format(li.distance()))
print("Slope is {}".format(li.slope()))
c = Cylinder(2,3)
print("Cylinder Volume is {}".format(c.volume()))
print("Cylinder SA is {}".format(c.surface_area()))