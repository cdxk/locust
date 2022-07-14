"读取excel中的数据封装到数据组中"
from openpyxl import load_workbook
import sys,os

base_dir=os.path.dirname(os.path.abspath(__file__))[:-9]
print(base_dir)
sys.path.append(base_dir)

class readexcel():
    #获取excel表的指定sheet
    ws = load_workbook(base_dir+'/data/interfaces.xlsx')['Sheet1']
    #获取sheet中所有的行数据，并强制转为列表
    row_data = list(ws.rows)
    #获取表的第一行数据为titles
    titles=[title.value for title in row_data.pop(0)]
    all_row_dict=[]
    for a_row in row_data:
        #获取行数据
        row_data=[cell.value for cell in a_row]
        #将表头和行数据组装成字典
        row_dict=dict(zip(titles,row_data))
        #将每行数据字段加到列表中
        all_row_dict.append(row_dict)
    # print(all_row_dict)

# class verso():
#     print(greenlet.__version__)
#     print(gevent.__version__)

if __name__=='__main__':
    readexcel()