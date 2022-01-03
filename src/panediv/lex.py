"""Lexer for simple format layout string.

"""
import ply.lex
from .exceptions import LayoutFormatError


tokens = [
    'PERCENT',
    'NUMBER',
    'COMMAND_DQ',
    'COMMAND_SQ',
    'COMMAND_SIMPLE',
]

t_COMMAND_SIMPLE = r'[-_/.\w]+'

literals = ['(', ')', ',', '[', ']', '{', '}']
t_ignore = ' \t'


def t_COMMAND_DQ(t):
    r'(?<=[\{\[\(, ])\".*?[^\\](\\\\)*\"'
    t.value = t.value[1:-1]
    t.value = t.value.encode().decode('unicode-escape')
    return t


def t_COMMAND_SQ(t):
    r'(?<=[\{\[\(, ])\'.*?[^\\](\\\\)*\''
    t.value = t.value[1:-1]
    t.value = t.value.encode().decode('unicode-escape')
    return t


def t_PERCENT(t):
    '[0-9]+%'
    t.value = int(t.value[:-1])
    return t


def t_NUMBER(t):
    '[0-9]+'
    t.value = int(t.value)
    return t


def t_error(t):
    """Handle Error.

    """
    raise LayoutFormatError(t)


lexer = ply.lex.lex()
