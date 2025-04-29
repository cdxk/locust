#webdriver+chrome_driver实现滚动页面保存为图片
from selenium import webdriver
from time import sleep
import os,sys,os.path
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

base_dir=os.path.dirname(os.path.abspath(__file__))[:-7]
sys.path.append(base_dir)
file_path=os.path.join("file://"+base_dir+"/testCase/report/report2.html")
img_path=os.path.join(base_dir+"/testCase/report/report.png")


def webshot(url):
    options = webdriver.ChromeOptions()
    #selenium无头模式（即后台运行，不弹出浏览器框）
    options.add_argument('--headless')
    #禁用gpu
    options.add_argument('--disable-gpu')
    #关闭chrome浏览器沙盒
    options.add_argument('--no-sandbox')
    chromedriver = r'/Users/admin/Documents/tools/chrome Driver/chromedriver-mac-x64/chromedriver'
    service=Service(executable_path=chromedriver)
    driver = webdriver.Chrome(service= service, options=options)
    
    #最大化窗口
    driver.maximize_window()
    # 返回网页的高度的js代码,返回元素body的高度
    js_height = "return document.body.clientHeight"
    link = url
    try:
        driver.get(link)
        sleep(2)
        k = 1
        height = driver.execute_script(js_height)
        while True:
            if k * 500 < height:
                js_move = "window.scrollTo(0,{})".format(k * 500)
                driver.execute_script(js_move)
                sleep(1)
                height = driver.execute_script(js_height)
                k += 1
            else:
                break
        #返回有滚动条时的元素高度和宽度，有滚动时scrollHeight与clientHeight不等；无滚动时scrollHeight与clientHeight相等
        scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
        scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(scroll_width, scroll_height)
        driver.get_screenshot_as_file(img_path)

        print("Process {} get one pic !!!".format(os.getpid()))
        sleep(0.1)
    except Exception as e:
        print(f"截图失败: {e}")
    finally:
        driver.quit()
#
#截屏为图片
# chrome_driver='/Users/caidan/tool/tool/chromedriver'
# driver=webdriver.Chrome(executable_path=chrome_driver)
# #读取本地文件file://必不可少
# driver.get("file:///Users/caidan/tool/cai/pycharmProject/locust/testCase/report/report.html")
# #缩放浏览器内容
# driver.execute_script("document.body.style.zoom='28%'")
# sleep(2)
# driver.get_screenshot_as_file(img_path)
# driver.quit()

if __name__=='__main__':
    webshot(file_path)
