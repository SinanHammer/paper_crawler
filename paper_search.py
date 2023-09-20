from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from configure import SEARCH_CONTENT, SEARCH_URL
import time


# driver.minimize_window()
# 打开知网登录页面
# driver.get('https://www.cnki.net/')

class PaperSearch(object):
    def __init__(self, driver):
        self.driver = driver
        self.url = SEARCH_URL
        self.s_content = SEARCH_CONTENT

    def search_type(self):
        # ---------------------**  切换查找的依据 **-------------------------------------------
        parent_element = self.driver.find_element(By.ID, "DBFieldBox")
        # 找到<span>元素并将其内容修改为"作者"
        span_element = parent_element.find_element(By.TAG_NAME, "span")
        self.driver.execute_script("arguments[0].textContent = '作者';", span_element)
        new_value = "作者"
        self.driver.execute_script("document.getElementById('txt_sug').value = arguments[0];", new_value)
        li_element = self.driver.find_element(By.XPATH, "//li[@value='AU']")
        li_element_default = self.driver.find_element(By.XPATH, "//li[@value='SU']")
        # 使用Selenium的方法来设置class属性为 "cur"
        self.driver.execute_script("arguments[0].setAttribute('class', '');", li_element_default)
        self.driver.execute_script("arguments[0].setAttribute('class', 'cur');", li_element)
        time.sleep(1)

    def search_content(self):
        # --------------------** 输入查找内容 **------------------------------------
        input_element = self.driver.find_element(By.ID, 'txt_SearchText')
        input_element.send_keys(self.s_content)
        # 点击进行查找
        input_element.send_keys(Keys.RETURN)

    def search_run(self):
        self.search_type()
        self.search_content()

    def page_over(self):
        self.driver.close()

    def driver_over(self):
        self.driver.quit()

# # 创建Firefox浏览器实例
# driver = webdriver.Firefox()
# a = PaperSearch(driver)
# a.search_run()
