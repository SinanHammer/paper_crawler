# 						Paper Crawler

---

**paper crawler** 是基于研究过程中搜集文献中数据的流程，实现给定**搜索类型**和**搜索内容**，能够自动获取文献相关信息并根据需要自主下载搜集整理文献的工具，目前主要以CNKI为实现对象完成基本操作，在其余文献数据平台也具有极好的可复现性，更加精细的功能目前仍在继续完善。

---

##### 主要文件说明

-congfigure.py             提供搜索的类型内容的配置方法

-paper_search.py        实现根据设定的内容搜索查找文献相关配置页面![image-20230921105252233](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20230921105252233.png)

-paper_information.py      实现提取页面文献主要信息，并保存在excel中；针对具体文献实现基于**爬取信息**或**链接文本**更加精细的信息采集和可选择的自动下载![image-20230921113750463](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20230921113750463.png)

![image-20230921110251185](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20230921110251185.png)

![image-20230921110316928](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20230921110316928.png)

![image-20230921111543357](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20230921111543357.png)

![image-20230921125642112](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20230921125642112.png)

