# 使用selenium+Chrome/PhantomJS   爬取爱彼迎酒店数据
# 使用selenium 自动化测试工具，支持多种浏览器 爬虫中主要用来解决JavaScript渲染的问题
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import keys模块
# from selenium.webdriver.common.keys import Keys
from pyquery import PyQuery
from bs4 import BeautifulSoup

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from config import *
# from pyvirtualdisplay import Display
#
# display = Display(visible=0, size=(800, 600))
# display.start()

# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# browser = webdriver.Chrome(chrome_options=chrome_options)
browser = webdriver.Chrome(service_args=SERIVER_ARGS)
browser.maximize_window()  # 窗口最大化
wait = WebDriverWait(browser, 30)

current_page = 1

def search():
    print('开始搜索')
    try:
        browser.get('https://www.airbnbchina.cn/')
        # 设置等待时间，等待网页响应
        # 提交按钮
        submit = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                        '//*[@id="site-content"]/div/div/div[2]/div[2]/div/div[1]/div/div/div[2]/div/div/div/div[1]/div/button')))
        # submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
        #                                                 '#site-content > div > div > div._ovebx1 > div:nth-child(2) > div > div:nth-child(1) > div > div > div:nth-child(3) > div > div > div > div:nth-child(1) > div > button')))
        submit.click()
        html1=browser.page_source
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#GeocompleteController-via-SearchBarV2-SearchBarV2')))
        input.send_keys('上海中山公园地铁站')
        # time.sleep(2)
        input.send_keys(Keys.ENTER)
        time.sleep(3)
        get_product()
    except TimeoutException:
        return search()


def get_total_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    page = soup.find_all('li', class_="_1am0dt")
    total_page = len(page) + 1
    return total_page


def get_product():
    print('获取产品此信息')
    wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="site-content"]/div/div/div[2]/div/div/div/div/div[3]/div[1]/div[1]/nav')))
    html = browser.page_source  # 整个网页
    total_page = get_total_page(html)
    doc = PyQuery(html)
    soup = BeautifulSoup(html, 'html.parser')
    class_name = soup.find_all('div', class_="_fhph4u")[0].find_all('div')[0]['class'][0]
    # class_name=doc.find('._uvp3p0 ._fhph4u div:first-child')
    items = doc('._uvp3p0 ._fhph4u .' + class_name).items()
    for item in items:
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                        '.' + item.attr('class'))))
        # ActionChains(browser).key_down(Keys.CONTROL).send_keys("w").key_up(Keys.CONTROL).perform()
        product = {
            'name': item.find('._17djt7om ').text(),
            'desc': item.find('._saba1yg').text(),
            'price': item.find('._ncmdki').text(),
            'cancel_policy': item.find('._l8zgil6').text()
        }
        print(product)
    # ._1rltvky
    global current_page
    if current_page < total_page:
        current_page += 1
        next_page = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'._b8vexar ._1rltvky')))
        next_page.click()
        time.sleep(3)
        get_product()
def main():
    total = search()
    # print(total)


if __name__ == '__main__':
    main()
# display.stop()