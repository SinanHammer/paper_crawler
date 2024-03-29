from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
from configure import headers, READ_TEXT, DOWLOAD, DETAILS
from bs4 import BeautifulSoup
from paper_search import PaperSearch
import pandas as pd
import requests
import random
import sys


class PaperInformation(PaperSearch):
    def __init__(self, driver):
        super(PaperInformation, self).__init__(driver)
        self.paper_table = None  # 查找到的页面的文献的总信息
        self.paper_count_sum = None  # 查找到的文献总条数
        self.page_count_num = ""  # 查找到页面的次序
        # self.origin_windows = self.driver.current_window_handle  # 获取原始窗口
        self.page_href = []  # 获取所有文献的链接
        self.new_window = None # 获取新窗口
        self.all_windows = None  # 获取所有窗口
        self.details = DETAILS[1]  # 判断是否对文献进行详细查取
        self.read_txt = READ_TEXT[1]  # 判断是否从txt文本获取文献链接
        self.download = DOWLOAD[0]  # 判断是否需要下载文献
        self.number = 0
        self.paper_table_xlsx = pd.DataFrame(columns=["序号", "题名", "作者", "来源", "发表时间", "数据库", "被引","下载"])  # 构建文献表的DataFrame
        self.paper_infor_xlsx = pd.DataFrame(columns=["序号", "题名", "作者", "机构", "关键词", "基金资助", "发表期刊", "发表日期", "级别", "摘要"])  # 构建单篇文章的数据信息

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
            tbody_element = self.driver.find_element(By.TAG_NAME, "tbody")
            # 获取tbody内的所有tr元素
            odd_elements = tbody_element.find_elements(By.TAG_NAME, "tr")
            self.paper_table = odd_elements
            # 遍历每个 odd 元素并获取其文本内容
            for odd_element in self.paper_table:
                self.paper_table_save(odd_element)
                self.paper_href_save(odd_element)

                # odd_content = odd_element.text
                # print("---"*20)
                # print(odd_content)
                # print(type(odd_content))
            self.paper_table_xlsx.to_excel("信息汇总.xlsx")

            print(self.page_href)

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

    def paper_href_save(self, odd_element):
        paper_each = odd_element.find_element(By.CLASS_NAME, "name")
        link_paper = paper_each.find_element(By.TAG_NAME, "a")
        link_ = link_paper.get_attribute("href")
        print(f"已获取到 **--《 {paper_each.text} 》--** 链接:", link_)
        # paper_each.click()
        self.page_href.append(link_)
        with open("链接.txt", 'a') as file:
            file.write(link_ + '\n')

        # # 设置等待时间上限
        # self.all_windows = self.driver.window_handles
        # print(self.all_windows)
        # # self.new_window = [window for window in self.all_windows if window != self.driver.current_window_handle]
        # self.new_window = self.all_windows[-1]
        # self.driver.switch_to.window(self.new_window)

    def paper_infor_save(self):
        if self.read_txt:
            with open("链接.txt", 'r') as file:
                self.page_href = file.readlines()
                print(self.page_href)
        for i in self.page_href:
            time.sleep(random.uniform(0, 1))
            if self.read_txt == False:
                self.page_over()
            if self.number % 2 == 0:
                self.driver = webdriver.Firefox()
            else:
                self.driver = webdriver.Edge()
            self.driver.get(i)
            # self.driver.minimize_window()
            wait = WebDriverWait(self.driver, 15)
            try:
                # 使用等待机制，等待页面加载完成
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
                paper_con = {}
                paper_title = self.driver.find_element(By.CLASS_NAME, "brief")
                paper_con["序号"] = self.number + 1
                paper_con["题名"] = paper_title.find_element(By.TAG_NAME, "h1").text
                paper_con["作者"] = paper_title.find_element(By.CLASS_NAME, "author").text

                fund_elements = self.driver.find_elements(By.CSS_SELECTOR, "a.author")
                if fund_elements:
                    # 提取第一个元素的文本内容
                    paper_con["机构"] = fund_elements[0].text
                else:
                    paper_con["机构"] = "-"

                fund_elements = self.driver.find_elements(By.CSS_SELECTOR, "p.keywords")
                if fund_elements:
                    # 提取第一个元素的文本内容
                    paper_con["关键词"] = fund_elements[0].text
                else:
                    paper_con["关键词"] = "-"

                fund_elements = self.driver.find_elements(By.CSS_SELECTOR, "p.funds")
                # 检查是否找到了基金资助元素
                if fund_elements:
                    # 提取第一个元素的文本内容
                    paper_con["基金资助"] = fund_elements[0].text.strip()
                else:
                    # 未找到基金资助元素
                    paper_con["基金资助"] = "-"

                if len(self.driver.find_elements(By.CSS_SELECTOR, "div.top-tip span a")) == 2:
                    paper_con["发表期刊"] = self.driver.find_elements(By.CSS_SELECTOR, "div.top-tip span a")[0].text
                    paper_con["发表日期"] = self.driver.find_elements(By.CSS_SELECTOR, "div.top-tip span a")[1].text
                else:
                    paper_con["发表期刊"] = self.driver.find_element(By.CSS_SELECTOR, "div.top-tip span a").text
                    paper_con["发表日期"] = "-"
                paper_con["级别"] = str([i.text for i in self.driver.find_elements(By.CSS_SELECTOR, "div.top-tip a.type")])

                fund_elements = self.driver.find_elements(By.NAME, "ChDivSummary")
                if fund_elements:
                    # 提取第一个元素的文本内容
                    paper_con["摘要"] = fund_elements[0].text
                else:
                    paper_con["摘要"] = "-"
                # print(pd.DataFrame(paper_con, index=[0]))
                if self.download:
                    down = self.driver.find_element(By.CSS_SELECTOR, "li.btn-dlpdf")
                    self.paper_dowload(down)

                # paper_con['专辑'] = self.driver.find_element(By.XPATH, "//span[text()='专辑:']/following-sibling::p").text
                # paper_con['专题'] = self.driver.find_element(By.XPATH, "//span[text()='专题:']/following-sibling::p").text
                # paper_con['分类号'] = self.driver.find_element(By.XPATH, "//span[text()='分类号:']/following-sibling::p").text
                # print(paper_con)
                self.number = self.number + 1
                self.paper_infor_xlsx = pd.concat([self.paper_infor_xlsx, pd.DataFrame(paper_con, index=[0])], ignore_index=True)
                paper_con.clear()
                self.driver_over()

            except TimeoutException:
                print("等待超时! 未找到符合条件的元素!")
                self.number = self.number + 1

    def paper_dowload(self, down):
        down.click()
        time.sleep(1)

    def paper_information_run(self):
        if self.read_txt:
            self.driver_over()
            self.paper_infor_save()
            self.paper_infor_xlsx.to_excel("详细信息汇总表.xlsx")
            sys.exit()
            # self.paper_infor_save_requests()
        else:
            self.driver.minimize_window()
            self.driver.get(self.url)
            self.search_run()
            self.get_paper_table()
            if self.details:
                self.paper_infor_save()
                self.paper_infor_xlsx.to_excel("详细信息汇总表.xlsx")
                sys.exit()
            else:
                sys.exit()

    # # 由于CNKI具有反爬机制,该处代码不能生效
    # def paper_infor_save_requests(self):
    #     if self.read_txt:
    #         with open ("链接.txt", 'r') as file:
    #             self.page_href = file.readlines()
    #             print(self.page_href)
    #         for i in self.page_href:
    #             time.sleep(random.uniform(0, 1))
    #             k = self.number % 2
    #             self.number = self.number + 1
    #             print(i)
    #             req = requests.post(i, headers=headers[k])
    #             response = req.text
    #             req.close()
    #             print("*" * 100)
    #             # print(response)
    #             soup = BeautifulSoup(response, 'lxml')
    #             titles = soup.find_all("h1")
    #             for title in titles:
    #                 print(title)



if __name__ == "__main__":
    # 创建Firefox浏览器实例
    driver = webdriver.Firefox()
    a = PaperInformation(driver)
    a.paper_information_run()

