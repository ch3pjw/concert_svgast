from svgast.shapes import square, circle

# FIXME: these tests only really check the code executes


def test_square():
    square(5)
    square(1, x=2, y=3, anticlockwise=True)


def test_circle():
    circle(3)
    circle(5, cx=7, cy=9, anticlockwise=True)
