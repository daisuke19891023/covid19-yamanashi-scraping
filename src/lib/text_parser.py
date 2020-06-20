import re
from src.lib.string_util import StringUtil

class TextParser:
    @staticmethod
    def text2dict(target_number: str, text_file_path: str) -> dict:
        book_mark = re.sub(r'県内', '', target_number)
        data_dict = {}

        with open(text_file_path, 'rt', encoding='utf-8') as input_file:
            read_flg = True
            texts = [s.strip() for s in input_file.readlines()]
            for text in texts:
                # numberで返される'n例目'以降の文字列を読み込む
                if read_flg:
                    check = re.search(book_mark, text)
                    # print("book_mark:{} check:{} text:{}".format(
                    #     book_mark, check, text))
                    if check is None:
                        continue
                    else:
                        # テキスト情報として'n-1,n例目'と記載されている部分を除外する
                        tmp_check = text[check.start()-1]
                        # print(tmp_check)
                        if re.match(r',|、|､', tmp_check) is None:
                            read_flg = False
                if text != '':
                    # 年代|性別|発生判明日|居住地の情報をセットする
                    flg, key, value = StringUtil.set_key_value(text)
                    if flg and key not in data_dict:
                        data_dict[key] = value
        return data_dict
