import re

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import time
import csv

from selenium.webdriver.support.wait import WebDriverWait

'''导入必要的模块：
re: 用于处理正则表达式的模块。
requests: 用于发送 HTTP 请求的模块。
selenium: 用于模拟浏览器操作的模块。
time: 用于添加延迟等待的模块。
csv: 用于读写 CSV 文件的模块。'''
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_driver_path = "D:\chromedriver-win64\chromedriver-win64\chromedriver.exe"
browser = webdriver.Chrome(options=chrome_options, executable_path=chrome_driver_path)
'''使用 Options() 对象设置 Chrome 浏览器的选项，其中包括 --headless，
这会使浏览器在无头模式下运行，即不会弹出可视化窗口。'''
# browser = webdriver.Chrome()
# 进入网站
browser.get('https://www.dpchallenge.com/')
wait = WebDriverWait(browser, 10)
# 使用显式等待 (WebDriverWait) 等待页面上一个元素可点击，然后执行点击操作。
# 点击图片
element = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[5]")))  # 替换为你要点击的元素的id或其他选择器方式
# 定位到需要点击的元素
element = browser.find_element_by_xpath('/html/body/div[1]/div[5]')
# 创建 ActionChains 实例
actions = ActionChains(browser)
# 模拟鼠标点击并停留在元素上
actions.click_and_hold(element).perform()
# time.sleep(3)
# 点击搜索，进入搜索页面
element2 = browser.find_element_by_xpath('/html/body/div[9]/div[4]')
element2.click()
# 在输入框搜索相关日期的图片
# 定位到搜索框元素
# WebDriverWait(browser, 10).until(
# EC.element_to_be_clickable((By.XPATH, '//input[@id="searchBox"]'))
# search_box = browser.find_element_by_xpath('/html/body/table[2]/tbody/tr/td[1]/table[1]/tbody/tr[2]/td/div/form/input[1]')

# 代码定义了 search() 和 txt_crawl() 函数
def search(word):
    search_box = browser.find_element_by_xpath('/html/body/table[2]/tbody/tr/td[1]/table[1]/tbody/tr[2]/td/div/form/input[1]')
    # 清除搜索框中的内容
    search_box.clear()
    # 输入搜索关键字 2019年2020年2021年2022年2023年
    search_box.send_keys(word)
    # 提交搜索表单，模拟点击搜索按钮
    search_box.submit()
def txt_crawl():
    elements = browser.find_elements_by_class_name("forum-post")
    with open("../data/comment/output.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # 遍历元素列表，提取文本内容并用csv.writer写入 CSV 文件
        for element in elements:
            text = element.text
            print(text)
            writer.writerow([text])
def img_crawl():
    img_element = browser.find_element_by_css_selector("#img_container > img:nth-child(2)")
    # 获取图片的 URL
    url = img_element.get_attribute("src")
    pattern = r"(\d+)\.jpg"
    match = re.search(pattern, url)
    if match:
        image_id = match.group(1)
        # print("image_id:", image_id)
    else:
        print("No match found.")
    file_name = image_id + ".jpg"
    file_path = "../data/image/" + file_name
    # 发送 GET 请求并获取图片内容
    response = requests.get(url)
    # 检查响应状态码
    if response.status_code == 200:
        # 保存图片到本地文件
        with open(file_path, "wb") as file:
            file.write(response.content)



years = ["2019", "2020", "2021", "2022", "2023"]
for y in years:
    # 搜索相应年份的图片
    search(y)
    # 进入每个图片页面
    wait = WebDriverWait(browser, 10)
    allye = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "/html/body/table[2]/tbody/tr/td[2]/div[2]/table[2]/tbody/tr/td/a[1]")))
    href_list = []
    for url in allye:
        href = url.get_attribute('href')
        href_list.append(href)
    for href in href_list:
        browser.get(href)
        # 进入页面后对评论和照片进行爬取
        txt_crawl()
        img_crawl()
        browser.back()
    # 翻页操作 爬取完当前页点击翻页
    element_turnover = browser.find_element_by_xpath(
        "/html/body/table[2]/tbody/tr/td[2]/div[2]/table[3]/tbody/tr/td[1]/table/tbody/tr/td[5]/a/img")
    body = browser.find_element_by_tag_name("body")
    element_turnover.click()
# 照片  //*[@id="img_container"]/img[1]
# 评论  class="forum-post"
browser.quit()



