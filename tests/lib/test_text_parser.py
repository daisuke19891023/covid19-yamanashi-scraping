import pytest
from src.lib.text_parser import TextParser
import os


@pytest.fixture(scope="module", autouse=True)
def base_path():
    base_path = os.path.join(os.getcwd(), 'tests', 'data')
    yield base_path


class TestTextParser:
    def test_text2dict_normal(self, base_path):
        target_path = os.path.join(
            base_path, 'text_parser_pattern_normal.txt')
        result = TextParser.text2dict('100例目', target_path)
        assert result == {'年代': '10代', '性別': '男', '居住地': '山梨県'}

    @pytest.mark.parametrize('input_number, input_path, expected', [('10001例目', 'text_parser_pattern_duplicated.txt', {'年代': '10代', '性別': '女', '居住地': '山梨県'}), ('10002例目', 'text_parser_pattern_duplicated.txt', {'年代': '30代', '性別': '男', '居住地': '山梨県'})])
    def test_text2dict_duplicated(self, base_path,input_number, input_path, expected):
        target_path = os.path.join(
            base_path, input_path)
        result = TextParser.text2dict(input_number, target_path)
        assert result == expected
