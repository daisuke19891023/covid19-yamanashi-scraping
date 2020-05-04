import os

import pytest
from src.lib.json_checker import JsonChecker


@pytest.fixture(scope="module", autouse=True)
def jc_object():
    jc = JsonChecker()
    yield jc


class TestJsonChecker:
    def test_read_json(self, jc_object):
        target_dir = os.path.join(
            os.getcwd(), 'tests', 'data', 'read_test.json')
        result = jc_object.read_json(target_dir)
        assert result == {
            "lastUpdate": "2020/05/03 00:16",
            "patients": {
                "data": [
                    {
                        "年代": "10代",
                        "性別": "男",
                        "居住地": "",
                        "No": "県内1例目",
                        "リリース日": "1999-03-06T00:00:00+09:00",
                        "退院": None
                    },
                    {
                        "年代": "10代",
                        "性別": "男",
                        "居住地": "",
                        "No": "県内2例目",
                        "リリース日": "1999-03-07T00:00:00+09:00",
                        "退院": None
                    }
                ],
                "__comments": "陽性患者の属性",
                "date": "2020/05/03 00:16"
            }
        }

    def test_exclude_date_key(self, jc_object):
        target_dir = os.path.join(
            os.getcwd(), 'tests', 'data', 'read_test_input.json')
        target_result_dir = os.path.join(
            os.getcwd(), 'tests', 'data', 'read_test_output.json')
        input_json = jc_object.read_json(target_dir)
        result = jc_object.exclude_date_key(input_json)
        assert result == jc_object.read_json(target_result_dir)

    @pytest.mark.parametrize("input1, input2, expected", [({'patients': {'data': [1, 2, 3]}}, {'patients': {'data': [4, 5, 6]}}, True), ({'patients': {'data': [1, 2, 3]}}, {'patients': {'data': [1, 2, 3, 4]}}, False)])
    def test_check_list_count(self, jc_object, input1, input2, expected):
        result = jc_object.check_list_count(input1, input2, 'patients')
        assert result == expected

    @pytest.mark.parametrize("input1, input2, expected", [('check_nonzero_max_before.json', 'check_nonzero_max_after_same.json', True), ('check_nonzero_max_before.json', 'check_nonzero_max_after_differ.json', False)])
    def test_check_nonzero_max(self, jc_object, input1, input2, expected):
        target_dir1 = os.path.join(
            os.getcwd(), 'tests', 'data', input1)
        target_dir2 = os.path.join(
            os.getcwd(), 'tests', 'data', input2)
        input_json1 = jc_object.read_json(target_dir1)
        input_json2 = jc_object.read_json(target_dir2)
        result = jc_object.check_nonzero_max(
            input_json1, input_json2, 'contacts')
        assert result == expected

    def test_exclude_zero_max_date(self, jc_object):
        target_dir = os.path.join(
            os.getcwd(), 'tests', 'data', 'check_nonzero_max_after_same.json')
        input_json = jc_object.read_json(target_dir)
        result = jc_object.exclude_zero_max_date(
            input_json['contacts']['data'])
        assert result == [
            {
                "日付": "2020-01-29T00:00:00+09:00",
                "小計": 11
            },
            {
                "日付": "2020-01-30T00:00:00+09:00",
                "小計": 61
            },
            {
                "日付": "2020-01-31T00:00:00+09:00",
                "小計": 47
            }]
