from itertools import chain

from .ast import get_tag_name, get_attr_dict, Element, Svg

DEFAULT_INDENT_SIZE = 2


def serialise(root_element, indent=DEFAULT_INDENT_SIZE):
    '''
    Serialise the given element to a string
    '''
    return '\n'.join(_serialise(root_element, indent_size=indent))


def _serialise(element, indent_size, current_indent=0):
    indent_string = ' ' * current_indent
    if isinstance(element, Element):
        if element:
            yield indent_string + open_tag_str(element)
            for child in element:
                yield from _serialise(
                    child, indent_size, current_indent + indent_size)
            yield indent_string + close_tag_str(element)
        else:
            yield indent_string + open_close_tag_str(element)
    elif isinstance(element, str):
        yield indent_string + element
    else:
        raise TypeError(
            'Could not serialise object of type {!r} to xml'.format(
                type(element).__name__))


def open_tag_str(element):
    return '<{}{}>'.format(get_tag_name(element), attr_dict_str(element))


def close_tag_str(element):
    return '</{}>'.format(get_tag_name(element))


def open_close_tag_str(element):
    return '<{}{} />'.format(get_tag_name(element), attr_dict_str(element))


def attr_dict_str(element):
    d = get_attr_dict(element)
    string = ' '.join(
        '{}="{}"'.format(k.replace('_', '-'), v) for k, v in sorted(d.items()))
    return ' ' + string if string else string


def xml_declaration_str(encoding):
    return '<?xml version="1.0" encoding="{}" ?>'.format(encoding)


def write(
        root_element, file_or_path, indent_size=DEFAULT_INDENT_SIZE,
        root_type=Svg):
    encoding = 'utf-8'
    if not isinstance(root_element, root_type):
        raise TypeError(
            'Must use an {} element as document root, got {!r}'.format(
                root_type.__name__,
                type(root_element).__name__))
    xml_str = '\n'.join(chain(
        (xml_declaration_str(encoding),),
        _serialise(root_element, indent_size)))
    do_write = lambda f: f.write(xml_str.encode(encoding))
    if isinstance(file_or_path, str):
        with open(file_or_path, 'wb') as f:
            do_write(f)
    else:
        do_write(file_or_path)
