"""Terminal interface.


"""
import argparse
import subprocess
from panediv import export


def export_tmuxinator_configuration(layout, fname):
    """Print layout and commands in TmuxInator configuration format.

    Args:
        layout(str): Simple layout string.
        fname(str): Filename for export data.

    """
    with open(fname, 'w') as fd:
        fd.write(export.tmuxinator_config(layout))


def print_layout(layout):
    """Print complex layout string.

    Args:
        layout(str): Simple layout string.

    """
    print(export.simple_layout(layout))


def print_commands(layout):
    """Print commands.

    Args:
        layout(str): Simple layout string.

    """
    print(export.simple_commands(layout))


def print_matrix(layout):
    """Print index matrix.

    Args:
        layout(str): Simple layout string.

    """
    print(export.simple_matrix(layout))


def start_tmux(layout):
    """Run tmux directory.

    Args:
        layout(str): Simple layout string.

    """
    layout_string = export.simple_layout(layout)
    commands = export.raw_commands(layout)

    args = ['tmux', 'new-session']
    args += [';', 'splitw', '-d', ';', 'select-layout', 'tiled'] \
            * (len(commands) - 1)
    for command in commands:
        if command[0]:
            args += [';', 'send-keys', '-t',
                     str(command[1]), command[0], 'C-m']
    args += [';', 'select-layout', layout_string]

    subprocess.call(args)


def run():
    """Parse input from terminal.

    """
    parser = argparse.ArgumentParser(
                description='Generate layout string from simple format.')
    parser.add_argument('layout',
                        type=str,
                        help='Layout string, ex.) {,}.' +
                             ' Without other options, start tmux.')
    parser.add_argument('--tmuxinator', '-i',
                        type=str,
                        default=None,
                        help='Filename to export tmuxnator configuration.')
    parser.add_argument('--show_layout', '-l',
                        action='store_true',
                        default=False,
                        help='Print layout string.')
    parser.add_argument('--show_commands', '-c',
                        action='store_true',
                        default=False,
                        help='Print command list.')
    parser.add_argument('--show_matrix', '-m',
                        action='store_true',
                        default=False,
                        help='Print pane number matrix.')
    args = parser.parse_args()

    # Run
    try:
        if args.tmuxinator:
            export_tmuxinator_configuration(args.layout, args.tmuxinator)
        if args.show_layout:
            print_layout(args.layout)
        if args.show_commands:
            print_commands(args.layout)
        if args.show_matrix:
            print_matrix(args.layout)
        if not (args.tmuxinator or args.show_layout or
                args.show_commands or args.show_matrix):
            start_tmux(args.layout)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    run()
