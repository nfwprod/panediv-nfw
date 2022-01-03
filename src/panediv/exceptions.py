"""Exceptions.

"""


class LayoutFormatError(Exception):
    """Layout string format error.

    """
    def __init__(self, arg=None):
        print(f'Layout parse error at {arg}')
        print('Command might be wrong format.' +
              ' Please export tmuxinator config with -i option and' +
              ' write command to the config file later.')


class PaneNotArrangedError(Exception):
    """Call layout information before arrangement.

    """
    def __init__(self):
        print('Pane is not arragned yet.')


class PaneHierachyError(Exception):
    """{} contains {} or [] contains [].
    Horizontal layout and vertical layout must be arranged in turns.

    """
    def __init__(self):
        print('Horizontal layout and vertical layout' +
              ' must be arranged in turns.')


class PaneArrangeError(Exception):
    """Pane size error.
    Indicated size exceed or short the terminal size.

    """
    def __init__(self):
        print('Indicated size exceed or short the terminal size.')
