## @package gimath
# Some simple data structures for holding math types.
# All arguments to trig functions are in radians.

from math import *

## @var EPSILON
# Used to fudge equalities to account for floating point innacuracies.
EPSILON = .0001

## A class representing a ray from an origin with a direction.
class Ray:

    def __init__(self, _origin, _direction):
        ## Constructer
        # @param _origin where the ray starts.
        # @param _direction the direction in which the ray points.
        self.origin = _origin
        self.direction = self.normalize(_direction)

    def normalize(self, _point):
        ## Returns a normalized point.
        # assumes the point is x, y
        mag = sqrt(_point[0] * _point[0] + _point[1] * _point[1])
        return (_point[0] / mag, _point[1] / mag)

    def getY(self, _x):
        ## Returns a y value for a given x
        # @param _x the x value.

        # check if we are vertical.
        if self.direction[0] == 0:
            print("getY() called on vertical ray")
            return None
        else:
            return (_x - self.origin[0]) * (self.direction[1] / self.direction[0]) + self.origin[1]

    def getX(self, _y):
        ## Returns an x value for a given y.
        # @param _y the y value.

        # check if horizontal.
        if self.direction[1] == 0:
            print("getX() called on horizontal ray")
            return None
        else:
            return (_y - self.origin[1]) * (self.direction[0] / self.direction[1]) + self.origin[0]

    def translate(self, _x, _y):
        ## Translates the given line by _x and _y.
        # @param _x how much to translate in x.
        # @param _y how much to translate in y.
        self.origin = (self.origin[0] + _x, self.origin[1] + _y)

    def dot(self, _ray):
        ## The dot product of this ray with another.
        # because all directions are normalized. This is a normalized dot product.
        # @param _ray the ray to be dot producted with.

        return self.direction[0] * _ray.direction[0] + self.direction[1] * _ray.direction[1]

    def rotate(self, _theta):
        ## rotate the vector by _theta.
        # @param the number of radians to rotate counterclockwise.
        dirX = (cos(_theta) * self.direction[0] - sin(_theta) * self.direction[1])
        dirY = (sin(_theta) * self.direction[0] + cos(_theta) * self.direction[1])

        self.direction = self.normalize((dirX, dirY))

    def findIntersection(self, _ray):
        ## Returns the point at which the two rays intersect.
        # Returns None if the rays are parallel.
        # @param _ray the ray to intersect with.

        if self.dot(_ray) == 1:
            print("find_intersection(): given parallel rays")
            return None

        delta1 = self.direction[1] / self.direction[0]
        delta2 = _ray.direction[1] / _ray.direction[0]
        x = (self.origin[1] - delta1 * self.origin[0]) - (_ray.origin[1] - delta2 * _ray.origin[0])
        x = x / (delta2 - delta1)
        y = self.getY(x)

        return (x, y)

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

        return Ray((_x, _y), (_x - self.x1, _y - self.y1))


## Some helper functions
class Utils:

    def findAngle(_ray1, _ray2):
        ## Returns the angle between the two lines.
        # This is the angle that is in the same direction as both lines.
        # TF the order of the arguments does not matter.
        # @param _line1 the first line.
        # @param _line2 the second line.
        return acos(_ray1.dot(_ray2))

    def snells(_theta1, _n1, _n2):
        ## Returns the resulting angle from Snell's Law.
        # @param _theta1 the incident angle.
        # @param _n1 the initial index of refraction.
        # @param _n2 the secondary index of refraction.
        return asin(_n1 * sin(_theta1) / _n2)

    def snells2(_ray, _normal, _n1, _n2):
        ## Returns a new line that results from this ray refracting into this material.
        # @param _ray the incident ray of light.
        # @param _normal the normal line to the lense.
        # @param _n1 the index of refraction for the initial material.
        # @param _n2 the index of refraction for the refracting material.

        # we take the magnitude here because we assume that the angle of incidence
        # is accute.
        dot = abs(_ray.dot(_normal))

        if abs(dot) < EPSILON:
            print("snells2(): incident ray is orthogonal to normal")
            exit()

        # find the angle of the new line wr to the original line.
        theta_initial = acos(dot)
        theta_diff = theta_initial - Utils.snells(theta_initial, _n1, _n2)

        retval1 = Ray(_normal.origin, _ray.direction)
        retval2 = Ray(_normal.origin, _ray.direction)
        retval1.rotate(theta_diff)
        retval2.rotate(-theta_diff)


        if theta_diff > 0:
            # This means that we are getting closer to the norm.
            # Therefore we rotate a vector both ways and see which is more in line
            # with the norm.
            if abs(retval1.dot(_normal)) > abs(dot):
                return retval1
            else:
                return retval2
        else:
            # This means that we are getting farther from the norm.
            # Therefore we rotate a vector both ways and see which is less in line
            # with the norm.
            if abs(retval1.dot(_normal)) < abs(dot):
                return retval1
            else:
                return retval2

    def findIntersection(_circle, _ray):
        ## Finds the set of points in which the ray intersects with the circle.
        # @param _circle the circle.
        # @param _ray the incident ray.
        # @return the point farther to the right is always returned first.

        # make the center of the circle the new origin
        origin = (_circle.x1, _circle.y1)

        circle_centered = Circle(0, 0, _circle.r)
        ray_centered = Ray(_ray.origin, _ray.direction)
        ray_centered.translate(-origin[0], -origin[1])

        # put ray in slope intercept form.
        m = ray_centered.direction[1] / ray_centered.direction[0]
        b = ray_centered.getY(0)

        # Substuting y = mx + b into x**2 + y**2 = r**2 we get.
        # x**2 + (mx + b)**2 = r**2
        # We then use the quadratic formula on this.
        r = circle_centered.r
        D = (4 * ((m * b) ** 2)) - (4 * (1 + m * m) * (b * b - r * r))

        if D < 0:
            print("findIntersection() found no intersection between circle and ray")
            return None
        elif D == 0:
            print("findIntersection() given a ray tangent to circle")
            x = (-(2 * m * b)) / (2 * (1 + m * m))
            return (x + origin[0], _ray.getY(x) + origin[1])
        else:
            x1 = ((-2 * m * b) + sqrt(D)) / (2 * (1 + m * m))
            x2 = ((-2 * m * b) - sqrt(D)) / (2 * (1 + m * m))
            y1 = ray_centered.getY(x1)
            y2 = ray_centered.getY(x2)
            return [(x1 + origin[0], y1 + origin[1]), (x2 + origin[0], y2 + origin[1])]
