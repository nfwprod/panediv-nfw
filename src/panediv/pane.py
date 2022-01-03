"""TMUX Pane classes.

"""
import math
from .exceptions import PaneNotArrangedError
from .exceptions import PaneHierachyError
from .exceptions import PaneArrangeError


class PaneMatrix():
    """Pane index matrix.

    """
    def __init__(self, index):
        self.matrix = [[index]]

    @property
    def width(self):
        """Return columns of this pane.

        """
        return len(self.matrix[0])

    @property
    def height(self):
        """Return lines of this pane.

        """
        return len(self.matrix)

    def extend_horizontal(self, width):
        """Extend matrix columns to match other matrix size.

        Args:
            width(int): Extend this matrix width to this size.

        """
        if self.width == width:
            return
        for row in self.matrix:
            row += [row[-1] * width - self.width]

    def extend_vertical(self, height):
        """Extend matrix rows to match other matrix size.

        Args:
            height(int): Extend this matrix height to this size.

        """
        if self.height == height:
            return
        for _ in range(0, height - self.height):
            self.matrix.append(self.matrix[-1].copy())

    def append_horizontal(self, matrix):
        """Append matrix to the right of self.

        Args:
            matrix(PaneMatrix): Appended matrix.

        """
        if self.height > matrix.height:
            matrix.extend_vertical(self.height)
        elif self.height < matrix.height:
            self.extend_vertical(matrix.height)
        for i in range(0, self.height):
            self.matrix[i] += matrix.matrix[i]

    def append_vertical(self, matrix):
        """Append matrix to the bottom of self.

        Args:
            matrix(PaneMatrix): Appended matrix.

        """
        if self.width > matrix.width:
            matrix.extend_horizontal(self.width)
        elif self.width < matrix.width:
            self.extend_horizontal(matrix.height)
        self.matrix += matrix.matrix


class Pane():
    """Single Pane.

    Args:
        command(str): Command for this pane. Default:None.
        size(int): Size of this pane. Default:None.
        percent(int): Size of this pane. Default:None.

    Attributes:
        width(int): Actual size decided by parent.
        height(int): Actual size decided by parent.
        pos_x(int): x_position.
        pos_y(int): y_position.
        index(int): Index of this pane.

    Notes:
        Actual size are decided by parent pane.
        If both size and percent defined, size is preferred.

    """

    def __init__(self, command='', size=None, percent=None):
        self.command = command
        self.size = size
        self.percent = percent
        self.arranged = False
        self.width = None
        self.height = None
        self.pos_x = None
        self.pos_y = None
        self.index = None

    @property
    def matrix(self):
        """Return pane matrix.

        Returns:
            PaneMatrix: PaneMatrix of child panes.

        Note:
            Details are implemented in child class in _matrix method.
        """
        if not self.arranged:
            raise PaneNotArrangedError()
        return PaneMatrix(self.index)

    @property
    def layout(self):
        """Return layout string

        Returns:
            str: String format layout.

        """
        if not self.arranged:
            raise PaneNotArrangedError()
        layout = f'{self.width}x{self.height},{self.pos_x},{self.pos_y}'
        return layout

    @property
    def commands(self):
        """Return list of commands with index.

        Returns:
            list: list of command set. (<command(str)>, <index(int)>).

        """
        if not self.arranged:
            raise PaneNotArrangedError()
        return [(self.command, self.index)]

    def arrange(self, width, height, pos_x, pos_y, index):
        """Set size and position of this pane.

        Args:
            width(int): Columns of this pane.
            height(int): Lines of this pane.
            pos_x(int): Horizontal position.
            pos_y(int): Vertical position.
            index(int): Index of this pane.

        Returns:
            int: Next index.

        """
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.index = index
        self.arranged = True
        return index + 1


class Panes():
    """Pane group

    Args:
        panes(list): List of panes
        size(int): Size of this pane.
        size(int): Size of this pane.

    """
    def __init__(self, panes, size=None, percent=None):
        for pane in panes:
            if isinstance(pane, type(self)):
                raise PaneHierachyError()

        self.size = size
        self.percent = percent
        self.panes = panes
        self.arranged = False
        self.width = None
        self.height = None
        self.pos_x = None
        self.pos_y = None
        self.index = None

    @property
    def matrix(self):
        """Return pane matrix.

        Returns:
            PaneMatrix: PaneMatrix of child panes.

        Note:
            Details are implemented in child class in _matrix method.

        """
        return self._matrix()

    @property
    def layout(self):
        """Return tmux layout string.

        Note:
            Details are implemented in child class.

        """
        raise NotImplementedError()

    @property
    def commands(self):
        """Return commands for all panes.

        """
        commands = []
        for pane in self.panes:
            commands += pane.commands
        return commands

    @property
    def csum(self):
        """Calculate check sum of layout.

        """
        if not self.arranged:
            raise PaneNotArrangedError()

        layout = self.layout
        csum = 0
        for char in layout:
            csum = (csum >> 1) + ((csum & 1) << 15)
            csum += int.from_bytes(char.encode(), byteorder='big')
            if csum >= 2 ** 16:
                csum -= 2**16

        return format(csum, '04x')

    def arrange(self, width, height, pos_x=0, pos_y=0, index=0):
        """Arrange child pane sizes based on the order from parent.

        Args:
            width(int): Width of this pane group.
            height(int): Height of this pane group.
            pos_x(int): X Position of this pane group, default:0.
            pos_y(int): Y Position of this pane group, default:0.
            index(int): Next index in this group, default:0.

        Output:
            int: The first index for next pane.

        Note:
            Details are implemented in child class in _arrange method.

        """
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.index = index

        return self._arrange()

    def _arrange(self):
        """Arrange child pane sizes based on the order from parent.
        Called by arrange method.

        """
        raise NotImplementedError()

    def _calculate_sizes(self, total):
        """Calculated child pane sizes based of size and percent.

        Args:
            total(int): Total width or height.

        Returns:
            list: List of pane sizes.

        Note:
            Total indicated sizes can exceed or short terminal max.
            Raise Exceptions for such cases.

        """
        def _adjust_sizes(total, sizes):
            remains = total - sum([x for x in sizes if x])
            blanks = len([x for x in sizes if x is None])
            base = math.floor(remains / blanks)
            adjustments = remains - base * blanks
            adjusted_sizes = []
            for size in reversed(sizes):
                if size:
                    adjusted_size = size
                elif adjustments:
                    adjusted_size = base + 1
                    adjustments -= 1
                else:
                    adjusted_size = base
                adjusted_sizes.insert(0, adjusted_size)

            return adjusted_sizes

        # Set indicated sizes and percents.
        sizes = []
        for pane in self.panes:
            if pane.size:
                size = pane.size
            elif pane.percent:
                size = math.ceil(total * pane.percent / 100)
            else:
                size = None
            sizes.append(size)

        if len([x for x in sizes if x is None]) == 0:
            adjusted_sizes = sizes
        else:
            adjusted_sizes = _adjust_sizes(total, sizes)

        if sum(adjusted_sizes) != total:
            raise PaneArrangeError()
        if len([x for x in adjusted_sizes if x <= 0]):
            raise PaneArrangeError()

        return adjusted_sizes

    def _matrix(self):
        """Generate pane index position matrix.

        """
        raise NotImplementedError()


class HorizontalPanes(Panes):
    """Horizontal pane group, layout {}

    """
    @property
    def layout(self):
        if not self.arranged:
            raise PaneNotArrangedError()
        layout_self = f'{self.width}x{self.height},{self.pos_x},{self.pos_y}'
        layout_children = ','.join([x.layout for x in self.panes])
        return f'{layout_self}{{{layout_children}}}'

    def _arrange(self):
        """Arrange child pane sizes based on the order from parent.
        Called by arrange method.

        """
        validsize = self.width - len(self.panes) + 1
        sizes = self._calculate_sizes(validsize)

        pos_x = self.pos_x
        index = self.index
        for i, pane in enumerate(self.panes, 0):
            size = sizes[i]
            index = pane.arrange(size, self.height,
                                 pos_x, self.pos_y, index)
            pos_x += size + 1

        self.arranged = True
        return index

    def _matrix(self):
        matrixes = [x.matrix for x in self.panes]
        matrix_out = matrixes.pop(0)
        for matrix in matrixes:
            matrix_out.append_horizontal(matrix)
        return matrix_out


class VerticalPanes(Panes):
    """Vertical pane group, layout []

    """
    @property
    def layout(self):
        if not self.arranged:
            raise PaneNotArrangedError()
        layout_self = f'{self.width}x{self.height},{self.pos_x},{self.pos_y}'
        layout_children = ','.join([x.layout for x in self.panes])
        return f'{layout_self}[{layout_children}]'

    def _arrange(self):
        """Arrange child pane sizes based on the order from parent.

        """
        validsize = self.height - len(self.panes) + 1
        sizes = self._calculate_sizes(validsize)

        pos_y = self.pos_y
        index = self.index
        for i, pane in enumerate(self.panes, 0):
            size = sizes[i]
            index = pane.arrange(self.width, size,
                                 self.pos_x, pos_y, index)
            pos_y += size + 1

        self.arranged = True
        return index

    def _matrix(self):
        matrixes = [x.matrix for x in self.panes]
        matrix_out = matrixes.pop(0)
        for matrix in matrixes:
            matrix_out.append_vertical(matrix)
        return matrix_out
