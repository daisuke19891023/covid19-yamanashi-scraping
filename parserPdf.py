import os
import re
import glob
class ParserPdf:
    def __init__(self):
        self.pattern = r'年代|性別|退院|居住地'
    def text2dict(self, path):
        data_dict = {}
        with open(path, 'rt', encoding='utf-8') as input_file:
            l = [s.strip() for s in input_file.readlines()]
            for text in l:
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
        print(parser.text2dict(path))