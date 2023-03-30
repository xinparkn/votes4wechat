import time
from selenium import webdriver
from bs4 import BeautifulSoup
from wxpy import *

# 初始化机器人，扫码登录
bot = Bot(console_qr=True)

# 设置WebDriver路径（以Chrome为例）
driver_path = 'path/to/chromedriver'

# 创建WebDriver实例
browser = webdriver.Chrome(executable_path=driver_path)

# 指定目标URL
target_url = 'http://tp.mnw.cn/new.php?s=/xmtvote/index.html'

# 导航到目标URL
browser.get(target_url)

# 等待页面加载
time.sleep(5)

# 获取页面源代码
page_source = browser.page_source

# 使用BeautifulSoup解析源代码
soup = BeautifulSoup(page_source, 'html.parser')

# 搜索包含关键字“城市管理局”的元素
keyword = '城市管理局'
target_element = soup.find(lambda tag: tag.name == 'div' and keyword in tag.text)

# 如果找到了目标元素
if target_element:
    # 获取目标元素的ID或类名，用于Selenium定位
    target_id = target_element.get('id')
    target_class = target_element.get('class')[0] if target_element.get('class') else None

    # 使用Selenium定位目标元素
    if target_id:
        target_element_selenium = browser.find_element_by_id(target_id)
    elif target_class:
        target_elements_selenium = browser.find_elements_by_class_name(target_class)
        for elem in target_elements_selenium:
            if keyword in elem.text:
                target_element_selenium = elem
                break
    else:
        print("无法定位目标元素")
        browser.quit()
        exit()

    # 对目标元素执行点击操作
    target_element_selenium.click()

    # 等待投票操作完成
    time.sleep(5)

    # 截图并保存
    browser.save_screenshot('vote_screenshot.png')

    print("投票成功并截图保存")
else:
    print("未找到包含关键字的元素")

# 关闭浏览器
browser.quit()

# 保持程序运行，以便接收微信消息
embed()
