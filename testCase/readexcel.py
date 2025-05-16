"读取excel中的数据封装到数据组中"
from openpyxl import load_workbook
import sys,os

base_dir=os.path.dirname(os.path.abspath(__file__))[:-9]
print(base_dir)
sys.path.append(base_dir)

class readexcel():
    def readexcel(self,excel_file):
        base_dir=os.path.dirname(os.path.abspath(__file__))[:-9]
        data_dir=base_dir+'/data'
        excel_file=data_dir+'/'+excel_file
        #获取excel表的指定sheet
        ws = load_workbook(excel_file)['Sheet1']
        #获取sheet中所有的行数据，并强制转为列表
        row_data = list(ws.rows)
        #获取表的第一行数据为titles
        titles=[title.value for title in row_data.pop(0)]
        all_row_dict=[]
        for a_row in row_data:
            for cell in a_row:
                if cell.value and isinstance(cell.value, str):
                    #去掉字符串中的换行符和制表符
                    cell.value = cell.value.replace('\n', '').replace('\t', '').strip()
                row_data=[cell.value for cell in a_row]
            #将表头和行数据组装成字典
            row_dict=dict(zip(titles,row_data))
            # print(row_dict)
            #将每行数据字段加到列表中
            all_row_dict.append(row_dict)
        return all_row_dict
        
    
    # print(all_row_dict)



# if __name__=='__main__':
#     readexcel().readexcel('interfacesmps.xlsx')