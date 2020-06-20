import re
from typing import List, Tuple, Union


class StringUtil:
    def __init__(self):
        super().__init__()
        self.exclude_char = r'県外|再陽性|空港検疫で確認'

    def exclude_outside(self, full_with_str: str) -> bool:
        if re.search(self.exclude_char, full_with_str):
            return False
        else:
            return True

    def is_duplicate_data(self, number_char: str) -> Tuple[bool, Union[List[str], str]]:
        check = re.search(r',', number_char)
        if check is None:
            return False, number_char
        else:
            tmp = re.sub(r'県|内|例|目', '', number_char)
            return True, list(map(lambda x: '県内{}例目'.format(x), tmp.split(',')))
    @staticmethod
    def exclude_info_number(number_char: str) -> str:
        m = re.search(r'県内(\d{1,3})例目', number_char)
        if m is not None:
            return m.group()
        else:
            return number_char

    @staticmethod
    def normalize_age_exxpression(key:str,value:str) -> str:
        # 年代の表記ゆれの統一（歳代→代）
        if key == '年代':
            return re.sub(r'歳', '', value)  
        else:
            return value   

    @staticmethod
    def set_key_value(text:str) -> Tuple[bool,str,str]:
        pattern = r'年代|性別|発生判明日|居住地'
        text = re.sub(r':|︓|：', '', text)
        m = re.search(pattern, text)
        # print(text)
        if m is not None:
            key = m.group()
            value = text[m.end():]
            # 年代の表記ゆれの統一（歳代→代）
            if key == '年代':
                value = re.sub(r'歳', '', value)  
            return True, key, value
        else:
            return False, "",""