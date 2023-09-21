# 爬虫相关设置
headers = [{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0"},
           {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31"}
           # {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"},
           # {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31"}
           ]


# 查找内容相关设置
SEARCH_CONTENT = "武汉大学"
SEARCH_URL = "https://www.cnki.net/"
READ_TEXT = [False, True]
DOWLOAD = [False, True]
DETAILS = [False, True]
# 可选择范围  主题 篇关摘 关键词 篇名 全文 作者 第一作者 通讯作者 作者单位 基金 摘要 小标题 参考文献 分类号 文献来源 DOI
TYPE = "作者单位"
Type = {'主题': 'SU','篇关摘': 'TKA', '关键词': 'KY', '篇名': 'TI', '全文': 'FT', '作者': 'AU', '第一作者': 'FI', '通讯作者': 'RP',\
        '作者单位': 'AF', '基金': 'FU', '摘要': 'AB', '小标题': 'CO', '参考文献': 'RF', '分类号': 'CLC', '文献来源': 'LY', 'DOI': 'DOI' }

