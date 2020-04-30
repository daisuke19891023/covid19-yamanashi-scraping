import pytest
from src.lib.string_util import StringUtil


@pytest.fixture(scope="module", autouse=True)
def stu_object():
    stu = StringUtil()
    yield stu


class TestStringUtil:
    @pytest.mark.parametrize("test_input, expected", [('県外一例目', False), ('県内1例目', True), ('県内2外', True)])
    def test_exclude_outside(self, stu_object, test_input, expected):
        result = stu_object.exclude_outside(test_input)
        assert result == expected

    @pytest.mark.parametrize("test_input, expected_bool, expected_list", [('県内一例目', False, '県内一例目'), ('県内3,4例目', True, ['県内3例目', '県内4例目'])])
    def test_is_duplicate_data(self, stu_object, test_input, expected_bool, expected_list):
        result_bool, result_list = stu_object.is_duplicate_data(test_input)
        assert result_bool == expected_bool
        assert result_list == expected_list


if __name__ == '__main__':
    pytest.main(['-v', __file__])
