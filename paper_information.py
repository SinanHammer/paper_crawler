from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time

from paper_search import PaperSearch
import pandas as pd


class PaperInformation(PaperSearch):
    def __init__(self, driver):
        super(PaperInformation, self).__init__(driver)
        self.paper_table = None  # 查找到的页面的文献的总信息
        self.paper_count_sum = None  # 查找到的文献总条数
        self.page_count_num = ""  # 查找到页面的次序
        self.origin_windows = self.driver.current_window_handle  # 获取原始窗口
        self.page_href = None
        self.new_window = None # 获取新窗口
        self.all_windows = None  # 获取所有窗口
        self.paper_table_xlsx = pd.DataFrame(columns=["序号", "题名", "作者", "来源", "发表时间", "数据库", "被引","下载"])  # 构建文献表的DataFrame
        self.paper_infor_xlsx = pd.DataFrame(columns=["题名", "作者", "机构", "关键词", "基金资助", "专辑", "专题", "分类号", "发表期刊", "发表日期", "级别", "摘要"])  # 构建单篇文章的数据信息


    def get_paper_table(self):
        # 设置等待时间上限，单位为秒
        wait = WebDriverWait(self.driver, 30)

        try:
            # 使用等待机制，等待页面加载完成
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "seq")))
            # 执行下面的程序
            count_paper = self.driver.find_element(By.CLASS_NAME, "pagerTitleCell")
            self.paper_count_sum = count_paper.find_element(By.TAG_NAME, 'em')
            self.page_count_num = self.driver.find_element(By.CLASS_NAME, "countPageMark").text
            print(count_paper.text)
            tbody_element =self.driver.find_element(By.TAG_NAME, "tbody")
            # 获取tbody内的所有tr元素
            odd_elements = tbody_element.find_elements(By.TAG_NAME, "tr")
            self.paper_table = odd_elements
            # 遍历每个 odd 元素并获取其文本内容
            for odd_element in self.paper_table:
                self.paper_table_save(odd_element)
                self.paper_infor_save(odd_element)
                self.paper_dowload(odd_element)
                # odd_content = odd_element.text
                # print("---"*20)
                # print(odd_content)
                # print(type(odd_content))
            self.paper_table_xlsx.to_excel("信息汇总.xlsx")

        except TimeoutException:
            print("等待超时! 未找到符合条件的元素!")

        # except Exception as e:
        #     print(e)


    def paper_table_save(self, odd_element):
        content = {}
        content['序号'] = int(odd_element.find_element(By.CLASS_NAME, "seq").text)
        content["题名"] = odd_element.find_element(By.CLASS_NAME, "name").text
        content["作者"] = odd_element.find_element(By.CLASS_NAME, "author").text
        content['来源'] = odd_element.find_element(By.CLASS_NAME, "source").text
        content['发表时间'] = odd_element.find_element(By.CLASS_NAME, "date").text
        content['数据库'] = odd_element.find_element(By.CLASS_NAME, "data").text
        content["被引"] = odd_element.find_element(By.CLASS_NAME, "quote").text
        content['下载'] = odd_element.find_element(By.CLASS_NAME, "download").text
        self.paper_table_xlsx = pd.concat([self.paper_table_xlsx, pd.DataFrame(content, index=[0])], ignore_index=True)


    def paper_infor_save(self, odd_element):
        paper_each = odd_element.find_element(By.CLASS_NAME, "name")
        link_paper = paper_each.find_element(By.TAG_NAME, "a")
        link_ = link_paper.get_attribute("href")
        print(f"已获取到 **--《 {paper_each.text} 》--** 链接:", link_)
        paper_each.click()
        time.sleep(2)
        # # 设置等待时间上限，单位为秒
        # self.all_windows = self.driver.window_handles
        # print(self.all_windows)
        # # self.new_window = [window for window in self.all_windows if window != self.driver.current_window_handle]
        # self.new_window = self.all_windows[-1]
        # self.driver.switch_to.window(self.new_window)
        # wait = WebDriverWait(self.driver, 15)
        # try:
        #     # 使用等待机制，等待页面加载完成
        #     wait.until(EC.presence_of_element_located((By.XPATH, "//h3[@class='author']")))
        #     paper_con = {}
        #     paper_title = self.driver.find_element(By.CLASS_NAME, "brief")
        #     paper_con['题名'] = paper_title.find_element(By.TAG_NAME, "h1").text
        #     paper_con['作者机构'] = paper_title.find_element(By.XPATH, "//h3[@class='author']")
        #     # paper_con['作者'] = paper_title.find_element(By.ID, "authorpart").text
        #     # paper_con['机构'] = paper_title.find_element(By.XPATH, "//a[contains(@class, 'author') and contains(@target, '_blank')]").text
        #     print(paper_con)
        #     self.driver.switch_to.window(self.origin_windows)
        #
        # except TimeoutException:
        #     print("等待超时! 未找到符合条件的元素!")


    def paper_dowload(self, odd_element):
        pass

    def paper_information_run(self):
        self.search_run()
        self.get_paper_table()


# 创建Firefox浏览器实例
driver = webdriver.Firefox()
a = PaperInformation(driver)
a.paper_information_run()