# -*- coding: utf-8 -*-
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import sys

args = sys.argv

input_path = args[1]
output_path = args[2]

# PDF read
rsrcmgr = PDFResourceManager()
codec = 'cp932'
params = LAParams()
text = ""
with StringIO() as output:
    device = TextConverter(rsrcmgr, output, codec=codec, laparams=params)
    with open(input_path, 'rb') as input:
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(input):
            interpreter.process_page(page)
        text += output.getvalue()
    device.close()
output.close()

# Change of special character
table = str.maketrans({
    "’": "'",
    '。': '.',
    '・': '',
    '“': '"',
    '”': '"',
    'α': '\\alpha',
    'β': '\\beta',
    'γ': '\\gamma',
    'δ': '\\delta',
    'ϵ': '\\epsilon',
    'ζ': '\\zeta',
    'η': '\\eta',
    'θ': '\\theta',
    'ι': '\\iota',
    'κ': '\\kappa',
    'λ': '\\lambda',
    'μ': '\\mu',
    'ν': '\\nu',
    'ξ': '\\xi',
    'π': '\\pi',
    'ρ': '\\rho',
    'σ': '\\sigma',
    'τ': '\\tau',
    'υ': '\\upsilon',
    'ϕ': '\\phi',
    'χ': '\\chi',
    'ψ': '\\psi',
    'ω': '\\omega',
    'ε': '\\varepsilon',
    'ϑ': '\\vartheta',
    'ϱ': '\\varrho',
    'ς': '\\varsigma',
    'φ': '\\varphi',
    'Γ': '\\Gamma',
    'Δ': '\\Delta',
    'Θ': '\\Theta',
    'Λ': '\\Lambda',
    'Ξ': '\\Xi',
    'Π': '\\Pi',
    'Σ': '\\Sigma',
    'Υ': '\\Upsilon',
    'Φ': '\\Phi',
    'Ψ': '\\Psi',
    'Ω': '\\Omega',
    '∈': '\\in'
})
text = text.strip()
text = text.translate(table)

# output text
with open(output_path, "wb") as f:
    f.write(text.encode('cp932', "ignore"))