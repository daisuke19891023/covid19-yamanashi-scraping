import datetime
import re

class TimeUtil:
    def __init__(self):
        self.WAREKI_FORMAT = {
            '令和': datetime.datetime(2019, 5, 1),
            '平成': datetime.datetime(1989, 1, 8)
        }
        self.wareki_pattern = r'令和|平成'
        self.tz_jst_name = datetime.timezone(datetime.timedelta(hours=9), name='JST')
        self.start_date = datetime.datetime(2020, 3, 1 ,tzinfo=self.tz_jst_name)


    def getWareki(self, dt_wareki):
        m =  re.match(self.wareki_pattern, dt_wareki)
        if m != None:
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

    def convertToAD(self, wareki, y, m, d):
        base = self.WAREKI_FORMAT[wareki]
        base_y = base.year
        result = datetime.datetime(base_y + y -1, m, d,tzinfo=self.tz_jst_name)
        return result.isoformat()
    def executeConvert(self, datetime_string):
        wareki, other = self.getWareki(datetime_string)
        if wareki != None:
            y, m, d = self.getYMD(other)
            return self.convertToAD(wareki, y, m, d)
        else:
            return ""
    def createDatetimeDict(self, N):
        end_date = N.astimezone(self.tz_jst_name)
        time_span = (end_date - self.start_date).days
        return [{"日付":(self.start_date + datetime.timedelta(days=i)).isoformat(), "小計":0} for i in range(time_span)]
    

class StringUtil:
    def __init__(self):
        super().__init__()
        self.exclude_char = r'県外'
    def exclude_outside(self, full_with_str):
        if re.search(self.exclude_char, full_with_str):
            return False
        else:
            return True


if __name__ == '__main__':
    tm = TimeUtil()
    print(tm.createDatetimeDict(datetime.datetime.now()))