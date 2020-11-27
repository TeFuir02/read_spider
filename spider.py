import requests,time
from lxml import etree
import pymysql
from collections import OrderedDict

class Spider_Crawl():
    '''
    数据获取
    '''

    def get_url(self,url):

        for i in range(3):
            header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
            r = requests.get(url,header)
            if r.status_code == 200:
                r.encoding = r.apparent_encoding
                return r.text
            time.sleep(0.5)

    def parse(self,html):
        # 提取、整理
        r = etree.HTML(html)
        # xpath进行匹配

        vote_name = r.xpath("//div[@class = 'novelslist']//li/a/text()")
        #print("小说名:",vote_name)

        vote_url = r.xpath("//div[@class = 'novelslist']//li/a/@href")
        #print("小说url:", vote_url)

        #变成字典的数据
        d = dict(zip(vote_name, vote_url))
        # print('寻找到的数据',d)

        return d

    def detail_parse(self,html):
        # 每一个小说详细章节的匹配 提取、整理
        r = etree.HTML(html)
        # xpath进行匹配

        vote_list_name = r.xpath("//div[@id='list']//dd/a/text()")
        vote_list_url = r.xpath("//div[@id='list']//dd/a/@href")
        # print("详细章节的名称：",vote_list_name)
        # print("详细章节的url：",vote_list_url)

        j = 0
        detail_d = OrderedDict()
        for i in vote_list_name:
            detail_d[i] = vote_list_url[j]
            j += 1
        # detail_d = dict(zip(vote_list_name, vote_list_url))
        return detail_d


    def read_parse(self,html):
        # 每一个小说详细章节的匹配 提取、整理
        r = etree.HTML(html)
        content = r.xpath("//div[@id='content']//text()")
        a = ""
        for i in content:
            a += i
        print(a)
        return a


    def new_book_parse(self,html,x):
        # 每一个小说详细章节的匹配 提取、整理
        r = etree.HTML(html)
        new_book_list = r.xpath(x)
        return new_book_list
