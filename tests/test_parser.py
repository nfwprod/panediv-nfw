import pytest
from panediv import parse


class TestLayoutEven:
    def test_vertical_simple_two_01(self):
        panes = parse('{,}')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0{49x100,0,0,50x100,50,0}'

    def test_vertical_simple_two_02(self):
        panes = parse('{2}')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0{49x100,0,0,50x100,50,0}'

    def test_vertical_simple_three_01(self):
        panes = parse('{,,}')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0{32x100,0,0,33x100,33,0,33x100,67,0}'

    def test_vertical_simple_three_02(self):
        panes = parse('{3}')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0{32x100,0,0,33x100,33,0,33x100,67,0}'

    def test_horizontal_simple_two_01(self):
        panes = parse('[,]')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0[100x49,0,0,100x50,0,50]'

    def test_horizontal_simple_two_02(self):
        panes = parse('[2]')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0[100x49,0,0,100x50,0,50]'

    def test_horizontal_simple_three_01(self):
        panes = parse('[,,]')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0[100x32,0,0,100x33,0,33,100x33,0,67]'

    def test_horizontal_simple_three_02(self):
        panes = parse('[3]')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0[100x32,0,0,100x33,0,33,100x33,0,67]'

    def test_horizontal_simple_three_02(self):
        panes = parse('[3]')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0[100x32,0,0,100x33,0,33,100x33,0,67]'

    def test_layout01_01(self):
        """
        Layout 01:
                 0,  1
                 0,  2
        """
        panes = parse('{,[,]}')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0{49x100,0,0,50x100,50,0[50x49,50,0,50x50,50,50]}'

    def test_layout01_02(self):
        panes = parse('{,[2]}')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0{49x100,0,0,50x100,50,0[50x49,50,0,50x50,50,50]}'

    def test_layout02_01(self):
        """
        Layout 02:
                 0,  2
                 1,  2
        """
        panes = parse('{[,],}')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0{49x100,0,0[49x49,0,0,49x50,0,50],50x100,50,0}'

    def test_layout02_02(self):
        panes = parse('{[2],}')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0{49x100,0,0[49x49,0,0,49x50,0,50],50x100,50,0}'

    def test_layout03_01(self):
        """
        Layout 03:
                 0,  0
                 1,  2
        """
        panes = parse('[,{,}]')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0[100x49,0,0,100x50,0,50{49x50,0,50,50x50,50,50}]'

    def test_layout03_02(self):
        panes = parse('[,{2}]')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0[100x49,0,0,100x50,0,50{49x50,0,50,50x50,50,50}]'

    def test_layout04_01(self):
        """
        Layout 04:
                 0,  1 
                 2,  2
        """
        panes = parse('[{,},]')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0[100x49,0,0{49x49,0,0,50x49,50,0},100x50,0,50]'

    def test_layout04_02(self):
        panes = parse('[{2},]')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0[100x49,0,0{49x49,0,0,50x49,50,0},100x50,0,50]'

    def test_error_hierachy_01(self):
        try:
            panes = parse('{,{,}}')
        except Exception as e:
            assert True
        else:
            assert False

    def test_error_hierachy_02(self):
        try:
            panes = parse('[,[,]]')
        except Exception as e:
            assert True
        else:
            assert False


class TestLayoutFixed:
    def test_vertical_three_01(self):
        panes = parse('{(,30),(,40),}')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0{30x100,0,0,40x100,31,0,28x100,72,0}'

    def test_vertical_three_02(self):
        panes = parse('{(,30),(,55%),}')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0{30x100,0,0,54x100,31,0,14x100,86,0}'

    def test_horizontal_three_01(self):
        panes = parse('[(,30),(,40),]')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0[100x30,0,0,100x40,0,31,100x28,0,72]'

    def test_horizontal_three_02(self):
        panes = parse('[(,30),(,55%),]')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0[100x30,0,0,100x54,0,31,100x14,0,86]'

    def test_vertical_four(self):
        panes = parse('{2,(,40),}')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0{19x100,0,0,19x100,20,0,40x100,40,0,19x100,81,0}'

    def test_horizontal_four(self):
        panes = parse('[2,(,40),]')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0[100x19,0,0,100x19,0,20,100x40,0,40,100x19,0,81]'

    def test_layout01_01(self):
        """
        Layout 01:
                 0,  1
                 0,  2
        """
        panes = parse('{(,20),[,]}')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0{20x100,0,0,79x100,21,0[79x49,21,0,79x50,21,50]}'

    def test_layout01_02(self):
        panes = parse('{,([,],40)}')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0{59x100,0,0,40x100,60,0[40x49,60,0,40x50,60,50]}'

    def test_layout01_03(self):
        panes = parse('{(,30%),[,]}')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0{30x100,0,0,69x100,31,0[69x49,31,0,69x50,31,50]}'

    def test_layout01_04(self):
        panes = parse('{,([,],55%)}')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0{44x100,0,0,55x100,45,0[55x49,45,0,55x50,45,50]}'

    def test_layout01_05(self):
        panes = parse('{(,20),[,(,30)]}')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0{20x100,0,0,79x100,21,0[79x69,21,0,79x30,21,70]}'

    def test_layout03_01(self):
        """
        Layout 01:
                 0,  0 
                 1,  2
        """
        panes = parse('[(,20),{,}]')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0[100x20,0,0,100x79,0,21{49x79,0,21,50x79,50,21}]'

    def test_layout03_02(self):
        panes = parse('[,({,},40)]')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0[100x59,0,0,100x40,0,60{49x40,0,60,50x40,50,60}]'

    def test_layout03_03(self):
        panes = parse('[(,30%),{,}]')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0[100x30,0,0,100x69,0,31{49x69,0,31,50x69,50,31}]'

    def test_layout03_04(self):
        panes = parse('[,({,},55%)]')
        panes.arrange(100,100)
        assert panes.layout ==  '100x100,0,0[100x44,0,0,100x55,0,45{49x55,0,45,50x55,50,45}]'

    def test_layout03_05(self):
        panes = parse('[(,20),{,(,30)}]')
        panes.arrange(100,100)
        assert panes.layout == '100x100,0,0[100x20,0,0,100x79,0,21{69x79,0,21,30x79,70,21}]'

    def test_error_size_01(self):
        panes = parse('{(,20),([,],90)}')
        try:
            panes.arrange(100,100)
        except Exception as e:
            assert True
        else:
            assert False

    def test_error_size_02(self):
        panes = parse('{(,20),([,],80%)}')
        try:
            panes.arrange(100,100)
        except Exception as e:
            assert True
        else:
            assert False
