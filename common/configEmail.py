"将性能测试结果文件发送邮件给制定人员邮箱！"

import os,sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
base_dir=os.path.dirname(os.path.abspath(__file__))[:-11]
sys.path.append(base_dir)

class SendEmail():
    def send_attach(self,file_name):
        msg_from='928566418@qq.com'
        pwd='gmdkgzvrulqpbfia'
        to='349255950@qq.com'
        message=MIMEMultipart()
        #发件人名字
        message['From']=Header('系统测试','utf-8')
        #收件人名字
        message['To']=Header('emilee','utf-8')
        #邮件标题
        subject='Python 自动化测试报告'
        file_path=os.path.join(base_dir+'data/'+file_name)
        message['Subject']=Header(subject,'utf-8')
        #邮件内容
        message.attach(MIMEText('这是自动化测试脚本邮件。。','plain','utf-8'))
        att=MIMEText(open(file_path,'rb').read(),'base64','utf-8')
        att["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中附件显示什么名字
        att["Content-Disposition"] = 'attachment; filename="report.html"'
        message.attach(att)
        try:
            # 连接smtp服务器，明文/SSL/TLS三种方式，根据你使用的SMTP支持情况选择一种
            # 纯粹的ssl加密方式，通信过程加密，邮件数据安全
            smtp = smtplib.SMTP_SSL('imap.gmail.com',465)
            smtp.ehlo()
            smtp.login(msg_from, pwd)
            smtp.sendmail(msg_from, to, message.as_string())
            print('success')


            # 普通方式，通信过程不加密
            # smtp = smtplib.SMTP(smtpHost,smtpPort)
            # smtp.ehlo()
            # smtp.login(username,password)


            # tls加密方式，通信过程加密，邮件数据安全，使用正常的smtp端口
            # 使用正常的smtp端口smtp = smtplib.SMTP(smtpHost, smtpPort)
            # smtp.set_debuglevel(True)
            # smtp.ehlo()
            # smtp.starttls()
            # smtp.ehlo()
            # smtp.login(username, password)

        except Exception as e :
            print(e)

if __name__=='__main__':
    SendEmail().send_attach('report.html')
