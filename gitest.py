'''
    Some simple unit tests
'''
import pytest
from gimath import Ray, EPSILON
from math import pi, cos, sqrt

def soft_equal(arg1, arg2):
    return abs(arg1 - arg2) < EPSILON

def soft_equal_tuple(arg1, arg2):
    return abs(arg1[0] - arg2[0]) + abs(arg1[1] - arg2[1]) < 2 * EPSILON

# Testing Rays
def test_line():

    ray = Ray((0, 0), (1, 1))
    assert ray.getY(5) == 5
    assert ray.getX(5) == 5

    ray.translate(1, 0)
    assert ray.getY(6) == 5
    assert ray.getX(5) == 6

    ray.translate(0, 1)
    assert ray.getY(5) == 5
    assert ray.getX(5) == 5

    ray2 = Ray((0, 0), (1, -1))
    ray3 = Ray((0, 0), (1, 100000000000))
    assert ray.dot(ray2) == 0
    assert soft_equal(ray.dot(ray3), cos(pi / 4))

    ray  = Ray((0, 34.), (1., -1.42))
    ray2 = Ray((0, 2.2), (1., 1.234))
    intersect = ray.findIntersection(ray2)
    assert soft_equal(intersect[0], 11.982)
    assert soft_equal(intersect[1], 16.9856)


from gimath import Circle

def test_circle():

    circle1 = Circle(0, 0, 1)
    assert circle1.getY(0) == (1, -1)
    assert circle1.getX(0) == (1, -1)

    ray1 = circle1.getNormal(0, 1)
    assert ray1.direction == (0, 1)
    assert ray1.origin == (0, 1)
    assert ray1.getX(100) == 0

    #TODO write more.

from gimath import Utils

def test_utils():

    # Testing angle.
    ray1 = Ray((0, 0), (0, 1))
    ray2 = Ray((0, 0), (-1, 0))
    assert Utils.findAngle(ray1, ray2) == pi / 2

    ray1.translate(5, 5)
    assert Utils.findAngle(ray1, ray2) == pi / 2

    ray2 = Ray((0, 0), (1, 1))
    assert soft_equal(Utils.findAngle(ray1, ray2), pi / 4)

    # Testing snells. Numbers generated through wolfram.
    n1 = 1
    n2 = 1.2
    theta = pi / 4
    assert soft_equal(Utils.snells(theta, n1, n2), 0.6301372460645644)

    # Testing snells2. Numbers generated through wolfram.
    # Sanity check.
    n1 = 1
    n2 = 1
    ray = Ray((1, 1), (-1, -1))
    normal = Ray((0, 0), (1, 0))
    out = Utils.snells2(ray, normal, n1, n2)
    assert out.origin == (0, 0)
    assert soft_equal_tuple(out.direction, out.normalize((-1, -1)))

    n1 = 1
    n2 = 1.2
    calc_direction = out.normalize((-1, -0.7293249574894729))
    out = Utils.snells2(ray, normal, n1, n2)
    assert out.origin == (0, 0)
    assert soft_equal_tuple(out.direction, calc_direction)

    dir_ray = (-sqrt(3) / 2,  -1 / 2)
    dir_norm = (1 / 2, sqrt(3) / 2)
    ray_out = Utils.snells2(Ray((sqrt(3) / 2, 1 / 2), dir_ray), Ray((0, 0), dir_norm), n1, n2)
    assert ray_out.origin == (0, 0)
    norm_direction = ray_out.normalize((-1, -0.7100244090273644))
    assert soft_equal_tuple(norm_direction, ray_out.direction)
