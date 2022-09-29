from htmlwebshot import WebShot
import os,sys,imgkit
base_dir=os.path.dirname(os.path.abspath(__file__))[:-7]
sys.path.append(base_dir)
file_path=os.path.join(base_dir+"/testCase/report/report.html")
img_path=os.path.join(base_dir+"/testCase/report/report.jpg")


class HtmlToImg():
    def createImage(self):
        shot = WebShot()
        shot.quality=100
        image=shot.create_pic(html=file_path)

    def createImage2(self):
        #使用imgkit转化，必须安装wkhtmltopdf包
        image=imgkit.from_file(filename=file_path,output_path=img_path)


if __name__=='__main__':
    HtmlToImg().createImage2()