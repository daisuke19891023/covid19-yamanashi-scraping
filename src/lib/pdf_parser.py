# -*- coding: utf-8 -*-
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import glob
import os
import re
import mojimoji
# PDF read


class PdfParser:
    @staticmethod
    def execute_pdf2text():
        for path in glob.glob('./pdf/*'):
            input_path = path
            output_file = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join('./text', output_file + '.txt')

            rsrcmgr = PDFResourceManager()
            codec = 'utf-8'
            params = LAParams()
            text = ""
            with StringIO() as output:
                device = TextConverter(
                    rsrcmgr, output, codec=codec, laparams=params)
                with open(input_path, 'rb') as input:
                    interpreter = PDFPageInterpreter(rsrcmgr, device)
                    for page in PDFPage.get_pages(input):
                        interpreter.process_page(page)

                    text += output.getvalue()
                device.close()
            output.close()
            # 半角空白が発生するため、trimする
            text = re.sub(r' |　', '', text.strip())
            text = mojimoji.zen_to_han(text)
            # output text
            with open(output_path, "wb") as f:
                f.write(text.encode('utf-8', "ignore"))


if __name__ == '__main__':
    convert_txt = PdfParser()
    convert_txt.executeConvert()
