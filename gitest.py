'''
    Some simple unit tests
'''
import pytest
from gimath import Line

# Testing Lines
def test_line():

    line = Line(1, 0)
    assert line.getY(5) == 5
    assert line.getX(5) == 5

    line.translate(1, 0)
    assert line.getY(6) == 5
    assert line.getX(5) == 6

    line.translate(0, 1)
    assert line.getY(5) == 5
    assert line.getX(5) == 5


from gimath import Circle

def test_circle():

    circle1 = Circle(0, 0, 1)
    assert circle1.getY(0) == (1, -1)
    assert circle1.getX(0) == (1, -1)

    line1 = circle1.getNormal(0, 1)
    assert line1.vertical
    assert line1.getX(100) == 0

    #TODO write more.
