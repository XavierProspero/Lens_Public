## @package gimath
# Some simple data structures for holding math types.
# All arguments to trig functions are in radians.

from math import sqrt, sin, asin

## @var EPSILON
# Used to fudge equalities to account for floating point innacuracies.
EPSILON = .001

## A class representing a linear equation of the form: y = mx + b.
class Line:

    def __init__(self, _m, _b, _vertical=False, _x=0):
        ## Constructer
        # @param _m the slope.
        # @param _b the y intersect.
        # @param _veritcal special case if slope is undefined.
        # @param _x only defined if we have a vertical line.
        self.m = _m
        self.b = _b
        self.vertical = _vertical
        self.x = _x

    def getY(self, _x):
        ## Returns a y value for a given x
        # @param _x the x value.
        if self.vertical:
            return None
        else:
            return self.m * _x + self.b

    def getX(self, _y):
        ## Returns an x value for a given y.
        # @param _y the y value.
        if self.vertical:
            return self.x
        else:
            return (_y - self.b) / self.m

    def translate(self, _x, _y):
        ## Translates the given line by _x and _y.
        # @param _x how much to translate in x.
        # @param _y how much to translate in y.
        self.b = -self.m * _x + self.b + _y


## A class representing a circle of the form (x - x1)^2 + (y - y1)^2 = r^2
class Circle:

    def __init__(self, _x1, _y1, _r):
        ## Constructer
        # @param _x1 the center in x.
        # @param _y1 the center in y.
        # @param _r the radius.
        self.x1 = _x1
        self.y1 = _y1
        self.r  = _r

    def getY(self, _x):
        ## Returns a tuple of y's for the given x.
        # @param _x the x value.
        radicand = sqrt((self.r * self.r - (_x - self.x1) * (_x - self.x1)))
        return (self.y1 + radicand, self.y1 - radicand)

    def getX(self, _y):
        ## Returns a tuple of x's for the given y.
        # @param _y the y value.
        radicand = sqrt(self.r * self.r - (_y - self.y1) * (_y - self.y1))
        return (self.x1 + radicand, self.x1 - radicand)

    def isPointOnCircle(self, _x, _y):
        ## A helper function that returns if the point lies on the circle.
        # @param _x the x component.
        # @param _y the y component
        return EPSILON > abs((_x - self.x1) * (_x - self.x1) + (_y - self.y1) * (_y - self.y1) - self.r * self.r)

    def getNormal(self, _x, _y):
        ## Finds the normal line on the point at the edge of the circle.
        # @param _x the x position on the edge.
        # @param _y the y position on the edge.
        assert self.isPointOnCircle(_x, _y)

        if _x == self.x1:
            return Line(0, 0, True, _x)
        else:
            m = (_y - self.y1) / (_x - self.x1)
            b = _y - m * _x
            return Line(m, b)


## Some helper functions
class Utils:

    def findAngle(_line1, _line2):
        #TODO

    def snells(_theta1, _n1, _n2):
        ## Returns the resulting angle from Snell's Law.
        # @param _theta1 the incident angle.
        # @param _n1 the initial index of refraction.
        # @param _n2 the secondary index of refraction.
        return asin(_n2 / _n1 * sin(_theta1))

    def snells2():
        #TODO
