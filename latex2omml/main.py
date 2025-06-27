# latex 2 omml
import latex2mathml.converter
from docx import shared
from docx.oxml.ns import qn
from docx import Document
from lxml import etree

# latex表达式
latex_input = r'\exp\left[\int d^{4}x g\phi\bar{\psi}\psi\right]=\sum_{n=0}^{\infty}\frac{g^{n}}{n!}\left(\int d^{4}x\phi\bar{\psi}\psi\right)^{n}'

# mathml格式
mathml_output = latex2mathml.converter.convert(latex_input)

print("mathml_output: ",mathml_output)

# mathml --> omml
# MML2OMML.XSL
tree = etree.fromstring(mathml_output)
xslt = etree.parse('MML2OMML.XSL')
transform = etree.XSLT(xslt)
#new_dom就是omml格式
new_dom = transform(tree)

print("result: ", new_dom)

doc = Document()
# 定义英文及数字文字字体
doc.styles['Normal'].font.name = 'Times New Roman'
# 定义中文文字字体
doc.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
# 定义字体大小
doc.styles['Normal'].font.size = shared.Pt(9)
paragraph = doc.add_paragraph(style=None)
# 没错，就是这步
paragraph._element.append(new_dom.getroot())

docx_path = '{}.docx'.format('test')
doc.save(docx_path)
