"""Configurations export script for cli.

"""
import shutil
from .parse import parse


template = """# Pane Arrangement
{}
name: name
root: ~/
windows:
  - panename:
      layout: '{},{}'
      panes:
{}
"""


def _generate_panes(layout_in, cols=None, lines=None):
    if not (cols and lines):
        cols, lines = shutil.get_terminal_size((80, 20))
    panes = parse(layout_in)
    panes.arrange(cols, lines)
    return panes


def tmuxinator_config(layout_in):
    """Return layout and commands in TmuxInator configuration format.

    Args:
        layout_in(str): Simple layout string.

    Returns:
        str: TmuxInator configuration.

    """
    panes = _generate_panes(layout_in)
    layout = panes.layout
    csum = panes.csum
    commands = panes.commands
    matrix = panes.matrix

    comments = ''
    for row in matrix.matrix:
        comments += '#' + ','.join([f'{x:3d}' for x in row]) + '\n'

    commands_out = ''
    for command in commands:
        commands_out += f'        - {command[0]} #{command[1]}\n'

    tmuxinator_yml = template.format(comments, csum, layout, commands_out)

    return tmuxinator_yml


def simple_layout(layout_in, cols=None, lines=None):
    """Return complex layout string.

    Args:
        layout_in(str): Simple layout string.

    Returns:
        str: Complex layout string

    """
    panes = _generate_panes(layout_in, cols, lines)
    layout = panes.layout
    csum = panes.csum
    return (','.join([csum, layout]))


def simple_commands(layout_in):
    """Return list of commands with index.

    Args:
        layout_in(str): Simple layout string.

    Returns:
        str: Commands concatenated by \n.

    """
    panes = _generate_panes(layout_in)
    commands = panes.commands
    return '\n'.join([f'{x[1]}: {x[0]}' for x in commands])


def simple_matrix(layout_in):
    """Return index matrix string.

    Args:
        layout_in(str): Simple layout string.

    Returns:
        str: Index matrix.

    """
    panes = _generate_panes(layout_in)
    matrix = panes.matrix
    result = ''
    for row in matrix.matrix:
        result += ','.join([f'{x:3d}' for x in row]) + '\n'
    return result


def raw_commands(layout_in):
    """Return raw command set. (<command(str)>, <index(int)>).

    Args:
        layout_in(str): Simple layout string.

    """
    panes = _generate_panes(layout_in)
    return panes.commands
