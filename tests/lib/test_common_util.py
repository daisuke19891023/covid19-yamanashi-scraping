import pytest
from src.lib.common_util import TimeUtil
import datetime


class TestTimeUtil:
    # def __init__(self):
    #     self.tmu = TimeUtil()

    def test_getWareki(self):
        tmu = TimeUtil()
        wareki, other = tmu.getWareki('令和2年10月31日')
        assert wareki == '令和'
        assert other == '2年10月31日'

    def test_getWareki_heisei(self):
        tmu = TimeUtil()
        wareki, other = tmu.getWareki('平成30年1月31日')
        assert wareki == '平成'
        assert other == '30年1月31日'

    def test_getWareki_None(self):
        tmu = TimeUtil()
        wareki, other = tmu.getWareki('大正1年1月31日')
        assert wareki == None
        assert other == None

    def test_getYMD(self):
        tmu = TimeUtil()
        result = tmu.getYMD('2年3月9日')
        assert result == [2, 3, 9]

    def test_getMDin2020(self):
        tmu = TimeUtil()
        result = tmu.getMDin2020('3月1日')
        assert result == [3, 1]

    def test_parseDateSpan(self):
        target_char = "test1～ \ntest2"
        tmu = TimeUtil()
        result = tmu.parseDateSpan(target_char)
        assert result == ["test1", "test2"]

    def test_convertToAD(self):
        tmu = TimeUtil()
        iso_format = tmu.convertToAD('令和', 2, 4, 29)
        assert iso_format == "2020-04-29T00:00:00+09:00"

    def test_convertToAD2020_ISO(self):
        tmu = TimeUtil()
        iso_format = tmu.convertToAD2020(4, 3)
        assert iso_format == "2020-04-03T00:00:00+09:00"

    def test_convertToAD2020_Not_ISO(self):
        tmu = TimeUtil()
        datetime_format = tmu.convertToAD2020(4, 3, string_format=False)
        assert datetime_format == datetime.datetime(
            2020, 4, 3, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(0, 32400), 'JST'))

    def test_executeConvert(self):
        tmu = TimeUtil()
        result = tmu.executeConvert('令和2年10月23日')
        assert result == "2020-10-23T00:00:00+09:00"

    def test_executeConvert_None(self):
        tmu = TimeUtil()
        result = tmu.executeConvert('大正2年10月23日')
        assert result == ''

    def test_createDatetimeDict_No_start_No_needDay(self):
        tmu = TimeUtil()
        result = tmu.createDatetimeDict(datetime.datetime(2020, 3, 2))
        assert result == [{"日付": "2020-03-01T00:00:00+09:00",
                           "小計": 0}, {"日付": "2020-03-02T00:00:00+09:00", "小計": 0}]

    def test_createDatetimeDict_start_No_needDay(self):
        tmu = TimeUtil()
        result = tmu.createDatetimeDict(datetime.datetime(
            2020, 3, 2), start=datetime.datetime(2020, 3, 1))
        assert result == [{"日付": "2020-03-01T00:00:00+09:00",
                           "小計": 0}, {"日付": "2020-03-02T00:00:00+09:00", "小計": 0}]

    def test_createDatetimeDict_start_needDay(self):
        tmu = TimeUtil()
        result = tmu.createDatetimeDict(datetime.datetime(
            2020, 3, 2), start=datetime.datetime(2020, 3, 1), need_day=True)
        assert result == [{"日付": "2020-03-01T00:00:00+09:00", "day": 1,
                           "小計": 0}, {"日付": "2020-03-02T00:00:00+09:00", "小計": 0, "day": 2}]

    def test_createDatetimeDict_O_start_needDay(self):
        tmu = TimeUtil()
        result = tmu.createDatetimeDict(datetime.datetime(
            2020, 3, 2), need_day=True)
        assert result == [{"日付": "2020-03-01T00:00:00+09:00", "day": 1,
                           "小計": 0}, {"日付": "2020-03-02T00:00:00+09:00", "小計": 0, "day": 2}]

    def test_getDatetimeDictFromString(self):
        target_char = "3月1日～    \n3月2日"
        tmu = TimeUtil()
        result = tmu.getDatetimeDictFromString(target_char)
        assert result == [{"日付": "2020-03-01T00:00:00+09:00", "day": 1,
                           "小計": 0}, {"日付": "2020-03-02T00:00:00+09:00", "小計": 0, "day": 2}]


if __name__ == '__main__':
    pytest.main(['-v', __file__])
