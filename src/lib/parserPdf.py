import re
import glob


class ParserPdf:
    def __init__(self):
        self.pattern = r'年代|性別|退院|居住地'

    def text2dict(self, number, path):
        book_mark = re.sub(r'県内', '', number)
        data_dict = {}

        with open(path, 'rt', encoding='utf-8') as input_file:
            read_flg = True
            l = [s.strip() for s in input_file.readlines()]
            for text in l:
                # numberで返される'n例目'以降の文字列を読み込む
                if read_flg:
                    check = re.search(book_mark, text)
                    print("book_mark:{} check:{} text:{}".format(
                        book_mark, check, text))
                    if check == None:
                        continue
                    else:
                        # テキスト情報として'n-1,n例目'と記載されている部分を除外する
                        tmp_check = text[check.start()-1]
                        print(tmp_check)
                        if re.match(r',|、|､', tmp_check) == None:
                            read_flg = False
                if text != '':
                    # 事前に':'を削除する
                    text = re.sub(r':', '', text)
                    m = re.search(self.pattern, text)
                    # print(text)
                    if m != None:
                        key = m.group()
                        value = text[m.end():]
                        # 年代の表記ゆれの統一（歳代→代）
                        if key == '年代':
                            value = re.sub(r'歳', '', value)
                        # keyが存在しない場合のみ代入する
                        if key not in data_dict:
                            data_dict[key] = value
                        continue
        return data_dict


if __name__ == '__main__':
    parser = ParserPdf()
    # print(parser.text2dict('./ttt.txt'))
    for path in glob.glob('./text/*'):
        print(parser.text2dict('県内1例目', path))
