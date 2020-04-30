import datetime
import re


class TimeUtil:
    def __init__(self):
        self.WAREKI_FORMAT = {
            '令和': datetime.datetime(2019, 5, 1),
            '平成': datetime.datetime(1989, 1, 8)
        }
        self.wareki_pattern = r'令和|平成'
        self.tz_jst_name = datetime.timezone(
            datetime.timedelta(hours=9), name='JST')
        self.start_date = datetime.datetime(
            2020, 3, 1, tzinfo=self.tz_jst_name)
        self.default_year = 2020

    def getWareki(self, dt_wareki):
        m = re.match(self.wareki_pattern, dt_wareki)
        if m is not None:
            wareki = m.group()
            other = dt_wareki[m.end():]
            return wareki, other
        else:
            return None, None

    def getYMD(self, dt_other):
        result = []
        tmp = dt_other
        for a in ('年', '月', '日'):
            ans, tmp, *_ = tmp.split(a)
            result.append(int(ans))
        return result

    def getMDin2020(self, dt):
        result = []
        tmp = dt
        for a in ('月', '日'):
            ans, tmp, *_ = tmp.split(a)
            result.append(int(ans))
        return result

    def parseDateSpan(self, date_char):
        return list(map(lambda x: x.strip().strip('～'), date_char.split('\n')))

    def convertToAD(self, wareki, y, m, d):
        base = self.WAREKI_FORMAT[wareki]
        base_y = base.year
        result = datetime.datetime(
            base_y + y - 1, m, d, tzinfo=self.tz_jst_name)
        return result.isoformat()

    def convertToAD2020(self, m, d, string_format=True):
        base_y = self.default_year
        result = datetime.datetime(base_y, m, d, tzinfo=self.tz_jst_name)
        if string_format:
            return result.isoformat()
        else:
            return result

    def executeConvert(self, datetime_string):
        wareki, other = self.getWareki(datetime_string)
        if wareki is not None:
            y, m, d = self.getYMD(other)
            return self.convertToAD(wareki, y, m, d)
        else:
            return ""

    def createDatetimeDict(self, end, start=None, need_day=False):
        end_date = end.astimezone(self.tz_jst_name)
        if start is not None:
            start_date = start.astimezone(self.tz_jst_name)
        else:
            start_date = self.start_date
        time_span = (end_date - start_date).days + 1
        if need_day:
            return [{"日付": (start_date + datetime.timedelta(days=i)).isoformat(), "day": (start_date + datetime.timedelta(days=i)).day, "小計": 0} for i in range(time_span)]
        else:
            return [{"日付": (start_date + datetime.timedelta(days=i)).isoformat(), "小計": 0} for i in range(time_span)]

    def getDatetimeDictFromString(self, date_char):
        # 文字列を分割
        tmp = self.parseDateSpan(date_char)
        tmp_list = []
        # 西暦に変換
        for t in tmp:
            m, d = self.getMDin2020(t)
            tmp_list.append(self.convertToAD2020(m, d, string_format=False))
        # 日ごとの連想配列を作成（小計のデフォルト値は0）
        start = tmp_list[0]
        end = tmp_list[1]
        return self.createDatetimeDict(end, start, need_day=True)
