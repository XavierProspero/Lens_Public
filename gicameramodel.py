'''
    A single lense model.
    Main components are:
    1. BiConvex lense.
    2. A point source light.
    3. A sensor of size h * h in mm and pixel dimension M * M
'''
import numpy as np
from math import sqrt
from gimath import *

## A sensor of size h * h in milimeters and M * M pixels.
# Some assumptions have been made. Notably.
# Arguments of the form x, y are assumed to be in milimiters.
# We assume samples are only taken in the y axis. Then we rotate the line
# by pi to obtain the rest of the samples.
class Sensor:
    def __init__(self, _h, _M):
        ## Constructer
        # @param _h the sensor height
        # @param _M the number of pixels along x or y
        self.h = _h
        self.M = _M
        self.sensor = np.zeros((self.M, self.M))

    def pixelAt(self, _x, _y):
        ## Returns the indices for the pixel at _x, _y.
        # @param _x the x coordinate in mm.
        # @param _y the y coordinate in mm.
        if abs(_x) > self.h / 2 or abs(_y) > self.h / 2:
            print("Sensor::pixelAt() given out of bounds pixel")
            return None

        pixelHeight = self.h / self.M
        # x and y are different here. This makes testing and visualization easier.
        # This is because np stores arrays in row major order.
        pixelX = (_x + self.h / 2) // pixelHeight
        pixelY = (self.h / 2 - _y) // pixelHeight
        return (int(pixelX), int(pixelY))

    def write(self, _y):
        ## A ray is incident at _y mm.
        # @param _y the location in y.
        pixel = self.pixelAt(0, _y)
        self.sensor[pixel[1]][pixel[0]] += 1

    def rotate(self):
        ## Takes all the readings on (0, y) and rotate them by pi.
        pixelHeight = self.h / self.M
        midX = int(self.M // 2)

        #TODO make this cleaner using a map function.
        for pixelX in range(self.M):
            # we don't need to rotate the center column.
            if pixelX == midX:
                continue
            xCentered = (pixelX - self.M // 2)

            for pixelY in range(self.M):
                yCentered = int(self.M // 2 - pixelY)
                mag = sqrt((xCentered * xCentered) + (yCentered * yCentered))

                # In the corners of the sensor we can't
                # get values because the rotation goes off sensor.
                if mag > (self.M // 2):
                    continue

                yAxisPixel = int(mag)
                if xCentered < 0:
                    # we check the top column of pixels.
                    self.sensor[pixelY][pixelX] += self.sensor[int(self.M // 2 - yAxisPixel)][midX]
                else:
                    # we check the bottom column of pixels.
                    self.sensor[pixelY][pixelX] += self.sensor[int(self.M // 2 + yAxisPixel)][midX]


## A BiConvex lense that models simple ray tracing optics.
# R1: Radius of lense on subject side.
# R2: Radius of lense on sensor side.
# T:  Thickness of lense at center
# OD: The aperture of the lense.
# We assume that index of refraction of air is 1.
class Lense:
    def __init__(self, _R1, _R2, _T, _OD):
        ## Constructer.
        # @param _R1 Radius of lense on subject side.
        # @param _R2 Radius of lense on sensor side.
        # @param _T  Thickness of lense at center
        # @param _OD The aperture of the lense.
        self.OD = _OD
        self.lense1 = Circle(-_R1 + (_T / 2), 0, _R1)
        self.lense2 = Circle(_R2 - (_T / 2), 0, _R2)
        self.n_air = 1.0
        self.n_glass = 1.5168
        print("lense1 {} {}, origin {}".format(self.lense1.x1, self.lense1.y1, self.lense1.r) )
        #TODO allow for refraction index based off of wavelength.

    def refract(self, _ray):
        ## refracts an incoming ray out.
        # We assume the ray is coming in from the right and out of the left.
        intersection1 = Utils.findIntersection(self.lense1, _ray)[0]
        normal1 = self.lense1.getNormal(intersection1[0], intersection1[1])
        inner_ray = Utils.snells2(_ray, normal1, self.n_air, self.n_glass)
        print("intersetction {}, inner_ray {}, {}".format(intersection1, inner_ray.origin, inner_ray.direction))

        # Now we calculate the ray that comes out of the left side.
        intersection2 = Utils.findIntersection(self.lense2, inner_ray)[1]
        normal2 = self.lense2.getNormal(intersection2[0], intersection2[1])
        exit_ray = Utils.snells2(inner_ray, normal2, self.n_glass, self.n_air)

        return exit_ray


## The lense, point source object and sensor all in one place.
