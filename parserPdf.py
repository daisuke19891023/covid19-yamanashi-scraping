import os
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
                #numberで返される'n例目'以降の文字列を読み込む
                if read_flg:
                    check = re.search(book_mark, text)
                    print("book_mark:{} check:{} text:{}".format(book_mark, check, text))
                    if check == None:
                        continue
                    else:
                        read_flg = False
                if text != '': 
                    m = re.search(self.pattern,text)
                    #print(text)
                    if m != None:
                        key = m.group()
                        value = text[m.end()+1:]
                        data_dict[key] = value
                        continue
        return data_dict
if __name__ == '__main__':
    parser = ParserPdf()
    #print(parser.text2dict('./ttt.txt'))
    for path in glob.glob('./text/*'):
        print(parser.text2dict('県内1例目', path))