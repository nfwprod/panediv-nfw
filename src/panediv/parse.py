"""Parser for simple format layout string.

"""
import ply.yacc
from .lex import tokens
from .pane import Pane, HorizontalPanes, VerticalPanes
from .exceptions import LayoutFormatError


def parse(layout, debug=False):
    """Parser.

    """
    psr = ply.yacc.yacc(debug=debug, write_tables=False)
    return psr.parse(layout, debug=debug)


def p_pane_command(psr):
    """pane : COMMAND_SIMPLE
            | COMMAND_SQ
            | COMMAND_DQ
            | '(' COMMAND_SIMPLE ')'
            | '(' COMMAND_SQ ')'
            | '(' COMMAND_DQ ')'
            | '(' COMMAND_SIMPLE ',' ')'
            | '(' COMMAND_SQ ','  ')'
            | '(' COMMAND_DQ ',' ')'"""
    if len(psr) == 2:
        psr[0] = Pane(psr[1])
    else:
        psr[0] = Pane(psr[2])


def p_pane_number(psr):
    """pane : '(' ',' NUMBER ')'"""
    psr[0] = Pane(size=psr[3])


def p_pane_percent(psr):
    """pane : '(' ',' PERCENT ')'"""
    psr[0] = Pane(percent=psr[3])


def p_pane_command_and_number(psr):
    """pane : '(' COMMAND_SIMPLE ',' NUMBER ')'
            | '(' COMMAND_SQ ',' NUMBER ')'
            | '(' COMMAND_DQ ',' NUMBER ')'"""
    psr[0] = Pane(psr[2], size=psr[4])


def p_pane_command_and_percent(psr):
    """pane : '(' COMMAND_SIMPLE ',' PERCENT ')'
            | '(' COMMAND_SQ ',' PERCENT ')'
            | '(' COMMAND_DQ ',' PERCENT ')'"""
    psr[0] = Pane(psr[2], percent=psr[4])


def p_pane_vertical(psr):
    """pane : vpanes"""
    psr[0] = psr[1]


def p_pane_horizontal(psr):
    """pane : hpanes"""
    psr[0] = psr[1]


def p_panes_single(psr):
    """panes : pane"""
    psr[0] = [psr[1]]  # Add two blank pane


def p_panes_number(psr):
    """panes : NUMBER"""
    panes = []
    for _ in range(0, psr[1]):
        panes.append(Pane())
    psr[0] = panes


def p_panes_start_with_conmma(psr):
    """panes : ',' panes"""
    psr[0] = [Pane()] + psr[2]  # Add two blank pane


def p_panes_conmma_only(psr):
    """panes : ','"""
    psr[0] = [Pane(), Pane()]  # Add two blank pane


def p_panes_start_with_pane(psr):
    """panes : pane ','"""
    psr[0] = [psr[1], Pane()]  # Add two blank pane


def p_panes_mid_01(psr):
    """panes : pane ',' panes"""
    psr[0] = [psr[1]] + psr[3]


def p_panes_mid_02(psr):
    """panes : panes ',' pane"""
    psr[0] = psr[1] + [psr[3]]


def p_panes_mid_03(psr):
    """panes : panes ',' panes"""
    psr[0] = psr[1] + psr[3]


def p_panes_last(psr):
    """panes : panes ','"""
    psr[0] = psr[1] + [Pane()]


def p_hpanes(psr):
    """hpanes : '{' panes '}'"""
    psr[0] = HorizontalPanes(psr[2])


def p_hpanes_and_number(psr):
    """hpanes : '(' '{' panes '}' ',' NUMBER ')'"""
    psr[0] = HorizontalPanes(psr[3], size=psr[6])


def p_hpanes_and_percent(psr):
    """hpanes : '(' '{' panes '}' ',' PERCENT ')'"""
    psr[0] = HorizontalPanes(psr[3], percent=psr[6])


def p_vpanes(psr):
    """vpanes : '[' panes ']'"""
    psr[0] = VerticalPanes(psr[2])


def p_vpanes_and_number(psr):
    """hpanes : '(' '[' panes ']' ',' NUMBER ')'"""
    psr[0] = VerticalPanes(psr[3], size=psr[6])


def p_vpanes_and_percent(psr):
    """vpanes : '(' '[' panes ']' ',' PERCENT ')'"""
    psr[0] = VerticalPanes(psr[3], percent=psr[6])


def p_error(psr):
    """Handle Error.

    """
    raise LayoutFormatError(psr)
