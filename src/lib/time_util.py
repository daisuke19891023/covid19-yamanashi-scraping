import datetime
import re

from typing import Tuple, Optional, List, Union


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

    def get_wareki(self, dt_wareki: str) -> Tuple[Optional[str], Optional[str]]:
        m = re.match(self.wareki_pattern, dt_wareki)
        if m is not None:
            wareki = m.group()
            other = dt_wareki[m.end():]
            return wareki, other
        else:
            return None, None

    def get_ymd_int_each(self, dt_other: str, need_year: bool = True) -> List[int]:
        result = []
        tmp = dt_other
        str_tuple = ('年', '月', '日') if need_year else ('月', '日')
        for a in str_tuple:
            # は年月日を表す文字列が複数入っていた際、後半を切り捨てる
            ans, tmp, *_ = tmp.split(a)
            result.append(int(ans))
        return result

    def parse_date_span(self, date_char: str) -> List[str]:
        return list(map(lambda x: x.strip().strip('～'), date_char.split('\n')))

    def get_ad_dt_fmt(self, wareki: str, y: int, m: int, d: int) -> str:
        base = self.WAREKI_FORMAT[wareki]
        base_y = base.year
        result = datetime.datetime(
            base_y + y - 1, m, d, tzinfo=self.tz_jst_name)
        return result.isoformat()

    def get_ad_date_iso_fmt(self, m: int, d: int) -> str:
        return self.get_ad_default_year_dt_fmt(m, d).isoformat()

    def get_ad_default_year_dt_fmt(self, m: int, d: int) -> datetime.datetime:
        base_y = self.default_year
        return datetime.datetime(base_y, m, d, tzinfo=self.tz_jst_name)

    def convert_wareki_to_ad(self, datetime_string: str) -> str:
        wareki, other = self.get_wareki(datetime_string)
        if wareki is not None and other is not None:
            y, m, d = self.get_ymd_int_each(other)
            return self.get_ad_dt_fmt(wareki, y, m, d)
        else:
            raise ValueError("不正な和歴です")

    def create_dt_dict(self, end: datetime.datetime, start: datetime.datetime = None, need_day: bool = False) -> List[dict]:
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

    def get_dt_dict_from_text(self, date_char: str) -> List[dict]:
        # 文字列を分割
        tmp = self.parse_date_span(date_char)
        tmp_list = []
        # 西暦に変換
        for t in tmp:
            m, d = self.get_ymd_int_each(t, need_year=False)
            tmp_list.append(self.get_ad_default_year_dt_fmt(
                m, d))
        # 日ごとの連想配列を作成（小計のデフォルト値は0）
        start = tmp_list[0]
        end = tmp_list[1]
        return self.create_dt_dict(end, start, need_day=True)
