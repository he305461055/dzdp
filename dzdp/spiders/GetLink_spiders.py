import scrapy
import re
from dzdp.items import DzdpItem,ContentItem
import dzdp.tool as tool
import math
import os

dirPath='C:/Users/Administrator/Desktop/DAIYUYING/zhilian/'
filename='zhilian.txt'

class GetLinkSpider(scrapy.Spider):
    name = 'getlink'
    allowed_domains = ["zhaopin.com"]
    start_urls = []
    page=math.ceil(2184/60)+1
    '''
    for i in range(1,page):
         #url='http://sou.zhaopin.com/jobs/searchresult.ashx?in=210500%3B160400%3B160000%3B160500%3B160200%3B300100%3B160100%3B160600&jl=%E5%8C%97%E4%BA%AC&kw=o2o&p=' + str(i)
         url='http://sou.zhaopin.com/jobs/searchresult.ashx?in=210500%3B160400%3B160000%3B160500%3B160200%3B300100%3B160100%3B160600&jl=%E4%B8%8A%E6%B5%B7%2B%E5%B9%BF%E5%B7%9E%2B%E6%B7%B1%E5%9C%B3%2B%E6%88%90%E9%83%BD&kw=o2o&p='+str(i)
         start_urls.append(url)
    '''

    def parse(self, response):
        linklist=[]
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
        if not os.path.isfile('%s%s' %(dirPath,filename)):
            open('%s%s' % (dirPath, filename), 'w').close()

        links=response.xpath('//tr[1]/td[3]/a/@href').extract()
        print(len(links))
        for link in links:
            with open('%s%s' %(dirPath,filename), 'r') as f:
                for line in f:
                    linklist.append(line.replace('\n', ''))
            if link not in linklist:
                with open('%s%s' %(dirPath,filename),'a',encoding='utf-8') as f:
                     f.write(link)
                     f.write('\n')
