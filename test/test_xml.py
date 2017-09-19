from pytest import raises
from io import BytesIO

from svgast.ast import Svg, G, Rect, Circle, Text
from svgast.units import px
from svgast.xml import serialise, write


example_ast = Svg(
    G(
        Rect(x=1, y="2", width=px(3), height=4),
        Text('Hello', Rect(), 'World')
    ),
    G(
        Circle(),
        Circle()
    )
)
expected_xml = '\n'.join((
    '<svg version="{}" xmlns="{}">'.format(
        example_ast.version, example_ast.xmlns),
    '  <g>',
    '    <rect height="4" width="3px" x="1" y="2" />',
    '    <text>',
    '      Hello',
    '      <rect />',
    '      World',
    '    </text>',
    '  </g>',
    '  <g>',
    '    <circle />',
    '    <circle />',
    '  </g>',
    '</svg>',
))
expected_file = (
    b'<?xml version="1.0" encoding="utf-8" ?>\n' +
    expected_xml.encode('utf-8'))


def test_serialise():
    assert serialise(example_ast) == expected_xml
    assert serialise(example_ast, indent=3) == expected_xml.replace(
        '  ', '   ')


def test_bad_serialisation_type():
    raises(TypeError, serialise, Svg(Rect(), {}, Circle()))


def test_write_file_obj():
    f = BytesIO()
    write(example_ast, f)
    assert f.getvalue() == expected_file


def test_write_path(tmpdir):
    # tmpdir provides pytest.LocalPath, which is... different to normal IO
    path = tmpdir.join('example.svg')
    write(example_ast, str(path))
    assert path.read('rb') == expected_file


def test_bad_write_type():
    raises(TypeError, write, Rect(), None)
