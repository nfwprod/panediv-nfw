import pytest
from panediv import export


class TestExport:
    @pytest.fixture
    def layout_01(self):
        return r'{top,["echo \"test01\"",]}'

    def test_layout_01(self, layout_01):
        layout = export.simple_layout(layout_01)
        assert layout == '9d7f,80x20,0,0{39x20,0,0,40x20,40,0[40x9,40,0,40x10,40,10]}'

    def test_commands_01(self, layout_01):
        commands = export.simple_commands(layout_01)
        assert commands == '0: top\n1: echo "test01"\n2: '

    def test_matrix_01(self, layout_01):
        matrix = export.simple_matrix(layout_01)
        assert matrix == '  0,  1\n  0,  2\n'

