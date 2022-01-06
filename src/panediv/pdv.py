"""Terminal interface.

"""
import os
import math
import shutil
import argparse
import subprocess


def split_vertical(num):
    """Split current pane vertically.

    Args:
        num(int): Split number.

    """
    _, total = shutil.get_terminal_size((80, 20))
    valid = total - num + 1
    unit = math.floor(valid / num)
    remains = valid - unit * num
    sizes = [unit] * (num - remains) + [unit + 1] * remains

    args = ['tmux']
    for i in range(1, num):
        size = total - sum(sizes[0:i]) - i
        args += ['split-window', '-l', f'{size}', ';']

    subprocess.call(args)


def split_horizontal(num):
    """Split current pane horizontally.

    Args:
        num(int): Split number.

    """
    total, _ = shutil.get_terminal_size((80, 20))
    valid = total - num + 1
    unit = math.floor(valid / num)
    remains = valid - unit * num
    sizes = [unit] * (num - remains) + [unit + 1] * remains

    args = ['tmux']
    for i in range(1, num):
        size = total - sum(sizes[0:i]) - i
        args += ['split-window', '-h', '-l', f'{size}', ';']

    subprocess.call(args)


def run():
    """Split running tmux pane.

    """
    parser = argparse.ArgumentParser(
                description='Split pane evenly.')
    parser.add_argument('num',
                        type=int,
                        help='Divide pane into num. default: horiszontally.')
    parser.add_argument('--vertical', '-v',
                        action='store_true',
                        default=False,
                        help='Divide vertically.')
    args = parser.parse_args()

    # Run
    if 'TMUX' not in os.environ.keys():
        print('Run this command in TMUX pane.')
        return

    try:
        if args.vertical:
            split_vertical(args.num)
        else:
            split_horizontal(args.num)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    run()
