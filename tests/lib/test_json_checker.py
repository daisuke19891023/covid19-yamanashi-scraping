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
            os.getcwd(), 'tests', 'data', 'read_test.json')
        input_json = jc_object.read_json(target_dir)
        result = jc_object.exclude_date_key(input_json)
        assert result == {
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
                "__comments": "陽性患者の属性"
            }
        }
