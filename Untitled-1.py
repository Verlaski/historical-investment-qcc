from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
import os
import pandas as pd
from io import StringIO
import pdfplumber
import camelot
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams



file_list=os.listdir(os.getcwd())
for i in file_list:
    if '.pdf' not in i:
        file_list.pop(file_list.index(i))
print(file_list)

def convert_pdf_2_text(path):

    rsrcmgr = PDFResourceManager()
    retstr = StringIO()

    device = TextConverter(rsrcmgr, retstr, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    with open(path, 'rb') as fp:
        for page in PDFPage.get_pages(fp, set()):
            interpreter.process_page(page)
        text = retstr.getvalue()

    device.close()
    retstr.close()

    return text
company=[]
person=[]
people=['魏清莲','陈斌波','秦千雅','王京','郑豫','吴德龙','易蕾莉','张玉霞','刘艳春','王景立','叶国强','柳卓之','郭良辉','康齐正','冉青荣','傅相林']
'''
for i in file_list:
    t=convert_pdf_2_text(i)
    t=t.split('分支机构')[1]
    count=0
    for j in people:
        if j in t:
            print("在"+i.split('.')[0]+"中发现 "+j+"有任职")
            count+=1
            company.append(i)
            person.append(j)
    if count==0:
        print(i.split('.')[0]+" 无董高核心技术人员任职")

df=pd.DataFrame({'公司':company,"人员":person})
df.to_csv('董高在控股股东企业任职.csv',encoding='utf-8')

'''
name='湖州恒沅股权投资有限公司.pdf'
#t=convert_pdf_2_text(name)
#t=t.split('三、企业对外投资')[2]
#print(t)
#with open('file.txt','w',encoding='utf-8')as f:
#    f.write(t)
have_invest=[]
file_list=['东台精玖旺硬质合金科技有限公司.pdf', '嘉兴敏凯汽车零部件有限公司.pdf', '嘉兴裕廷物业服务管理有限公司.pdf', '展图中国投资有限公司.pdf', '湖州宏硕汽车零部件有限公司.pdf']
output_df=pd.DataFrame()
for name in file_list:
    pdf=pdfplumber.open(name)
    for page in pdf.pages:
        if_invest=False
        if page.page_number in [1,2,3]:
            continue
        page_text=page.extract_text()
        if '历史对外投资' in page_text:
            if '暂无历史对外投资' in page_text:
                print(name,'\t没有历史对外投资')
                continue
            else:
                tables=camelot.read_pdf(name,pages=str(page.page_number),flavor='lattice')
                print(len(tables))
                for table in tables:
                    if '注册资本' in table.df.values:
                        print(table.df)
                        output_df=pd.concat([output_df,table.df],ignore_index=True)
            if_invest=True
            #print(str(page.page_number))
            #tables=camelot.read_pdf(name,pages=str(page.page_number),flavor='lattice')
            #print(len(tables))
            #tables[1].to_csv('test1.csv',encoding='ANSI')
            #break
        if if_invest:
            print(name,'\t有又有')
            have_invest.append(name)
output_df.to_csv('investments.csv',encoding='ANSI')
        

#tables=camelot.read_pdf(name,pages='4',flavor='stream')
#print(tables[0].df)
#tables[0].to_csv('test.csv',encoding='ANSI')