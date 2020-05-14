import pytest
from src.lib.time_util import TimeUtil
import datetime


@pytest.fixture(scope="module", autouse=True)
def tmu_object():
    tmu = TimeUtil()
    yield tmu


class TestTimeUtil:
    @pytest.mark.parametrize("test_input, expected_wareki, expected_other", [(
        '令和2年10月31日',
        '令和',
        '2年10月31日'
    ),
        ('平成30年1月31日', '平成', '30年1月31日'), ('大正1年1月31日', None, None)])
    def test_get_wareki(self, tmu_object, test_input, expected_wareki, expected_other):
        wareki, other = tmu_object.get_wareki(test_input)
        assert wareki == expected_wareki
        assert other == expected_other

    def test_get_ymd_int_each(self, tmu_object):
        result = tmu_object.get_ymd_int_each('2年3月9日')
        assert result == [2, 3, 9]

    def test_get_ymd_int_each_2020(self, tmu_object):
        result = tmu_object.get_ymd_int_each('3月1日', need_year=False)
        assert result == [3, 1]

    def test_parse_date_span(self, tmu_object):
        target_char = "test1～ \ntest2"
        result = tmu_object.parse_date_span(target_char)
        assert result == ["test1", "test2"]

    def test_get_ad_dt_fmt(self, tmu_object):
        iso_format = tmu_object.get_ad_dt_fmt('令和', 2, 4, 29)
        assert iso_format == "2020-04-29T00:00:00+09:00"

    def test_get_ad_date_iso_fmt(self, tmu_object):
        iso_format = tmu_object.get_ad_date_iso_fmt(4, 3)
        assert iso_format == "2020-04-03T00:00:00+09:00"

    def test_get_ad_default_year_dt_fmt(self, tmu_object):
        datetime_format = tmu_object.get_ad_default_year_dt_fmt(4, 3)
        assert datetime_format == datetime.datetime(
            2020, 4, 3, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(0, 32400), 'JST'))

    def test_convert_wareki_to_ad(self, tmu_object):
        result = tmu_object.convert_wareki_to_ad('令和2年10月23日')
        assert result == "2020-10-23T00:00:00+09:00"

    def test_convert_wareki_to_ad_error(self, tmu_object):
        with pytest.raises(ValueError):
            tmu_object.convert_wareki_to_ad('大正2年10月23日')

    @pytest.mark.parametrize(
        "pattern, end, start, need_day, expected", [
            ("No_start_No_needDay", datetime.datetime(2020, 3, 2), None, False,  [{"日付": "2020-03-01T00:00:00+09:00",
                                                                                   "小計": 0}, {"日付": "2020-03-02T00:00:00+09:00", "小計": 0}]),
            ("start_No_needDay", datetime.datetime(
                2020, 3, 2), datetime.datetime(2020, 3, 1, 0, 0, 0, 0, tzinfo=datetime.timezone(
                    datetime.timedelta(hours=9), name='JST')), False,  [{"日付": "2020-03-01T00:00:00+09:00",
                                                                         "小計": 0}, {"日付": "2020-03-02T00:00:00+09:00", "小計": 0}]),
            ("start_needDay", datetime.datetime(
                2020, 3, 2), datetime.datetime(2020, 3, 1, 0, 0, 0, 0, tzinfo=datetime.timezone(
                    datetime.timedelta(hours=9), name='JST')), True, [{"日付": "2020-03-01T00:00:00+09:00", "day": 1,
                                                                       "小計": 0}, {"日付": "2020-03-02T00:00:00+09:00", "小計": 0, "day": 2}]),
            ("NO_start_needDay", datetime.datetime(
                2020, 3, 2), None, True, [{"日付": "2020-03-01T00:00:00+09:00", "day": 1,
                                           "小計": 0}, {"日付": "2020-03-02T00:00:00+09:00", "小計": 0, "day": 2}])
        ]
    )
    def test_create_dt_dict(self, tmu_object, pattern, end, start, need_day, expected):
        print(pattern)
        result = tmu_object.create_dt_dict(
            end, start=start, need_day=need_day)
        assert result == expected

    def test_get_dt_dict_from_text(self, tmu_object):
        target_char = "3月1日～    \n3月2日"
        result = tmu_object.get_dt_dict_from_text(target_char)
        assert result == [{"日付": "2020-03-01T00:00:00+09:00", "day": 1,
                           "小計": 0}, {"日付": "2020-03-02T00:00:00+09:00", "小計": 0, "day": 2}]


if __name__ == '__main__':
    pytest.main(['-v', __file__])
