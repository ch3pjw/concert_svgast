from svgast.ast import Svg, Rect, Circle, Path, M, l, z, Text
from svgast.units import mm


def test_view_box():
    svg = Svg(viewBox=(0, mm(1), 10, 11))
    assert svg.viewBox.ox == 0
    assert svg.viewBox.oy == mm(1)
    assert svg.viewBox.width == 10
    assert svg.viewBox.height == 11
    assert str(svg.viewBox) == '0 1mm 10 11'


def test_element_getitem():
    c = Circle()
    svg = Svg(Rect(), c, Circle())
    assert svg[1] is c


def test_path():
    p = Path(d=(M(0, 0), l(1, 0), l(0, mm(1)), z))
    assert p.d[0].x == 0
    assert p.d[0].rel is False
    assert p.d[2].y == mm(1)
    assert p.d[2].rel is True
    assert p.d[3] is z
    assert str(p.d) == 'M 0 0  l 1 0  l 0 1mm  Z'


def test_text():
    t = Text(dx=(1, 2, mm(3), 4))
    assert t.dx[0] == 1
    assert str(t.dx) == '1 2 3mm 4'


def test_z():
    assert z() is z
