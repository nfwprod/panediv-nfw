"""Terminal interface.

"""
import os
import math
import shutil
import sys
import argparse
import subprocess


def run_vertical(commands, instant):
    """Split current pane vertically and run commands.

    Args:
        commands(list): List of commands.

    """
    _, total = shutil.get_terminal_size((80, 20))
    num = len(commands)
    valid = total - num + 1
    unit = math.floor(valid / num)
    remains = valid - unit * num
    sizes = [unit] * (num - remains) + [unit + 1] * remains

    args = ['tmux', 'send-keys', commands[0], 'C-m', ';']
    for i, command in enumerate(commands[1:], 1):
        size = total - sum(sizes[0:i]) - i
        if instant:
            args += ['split-window', '-l', f'{size}', command, ';']
        else:
            args += ['split-window', '-l', f'{size}', ';',
                     'send-keys', command, 'C-m', ';']

    subprocess.call(args)


def run_horizontal(commands, instant):
    """Split current pane horizontally and run commands.

    Args:
        commands(list):  List of commands.

    """
    total, _ = shutil.get_terminal_size((80, 20))
    num = len(commands)
    valid = total - num + 1
    unit = math.floor(valid / num)
    remains = valid - unit * num
    sizes = [unit] * (num - remains) + [unit + 1] * remains

    args = ['tmux', 'send-keys', commands[0], 'C-m', ';']
    for i, command in enumerate(commands[1:], 1):
        size = total - sum(sizes[0:i]) - i
        if instant:
            args += ['split-window', '-h', '-l', f'{size}', command, ';']
        else:
            args += ['split-window', '-h', '-l', f'{size}', ';',
                     'send-keys', command, 'C-m', ';']

    subprocess.call(args)


def run():
    """Split running tmux pane for commands.

    """
    parser = argparse.ArgumentParser(
            description='Split pane and run commands.' +
                        ' Input commands as args,' +
                        ' filename(-f) or from pipe.')
    parser.add_argument('commands', nargs='*',
                        help='Commands.')
    parser.add_argument('--file', '-f',
                        type=argparse.FileType('r'),
                        help='Commands file or \\n separated stdin')
    parser.add_argument('--vertical', '-v',
                        action='store_true',
                        default=False,
                        help='Divide vertically.')
    parser.add_argument('--instant', '-i',
                        action='store_true',
                        default=False,
                        help='Kill the pane when the command finished.')
    args = parser.parse_args()

    # Run
    if 'TMUX' not in os.environ.keys():
        print('Run this command in TMUX pane.')
        return

    if not sys.stdin.isatty():
        commands = sys.stdin.read().strip().split('\n')
    elif args.commands:
        commands = args.commands
    elif args.file:
        commands = args.file.readlines()
    else:
        parser.print_help()
        exit()

    # Run
    if not commands:
        parser.print_help()
        exit()
    try:
        if args.vertical:
            run_vertical(commands, args.instant)
        else:
            run_horizontal(commands, args.instant)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    run()
