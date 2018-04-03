import scrapy
import re
import dzdp.POI as POI
from dzdp.items import DzdpItem,ContentItem
import  traceback
import dzdp.tool as tool
import urllib
import xlrd
from scrapy.http import Request

imgdir1='D:/photo/20171019/'
imgdir2='D:/photo/环境图片/'
imgdir3='D:/photo/商品/'

class DzdpSpider(scrapy.Spider):
    name = "20171019"
    allowed_domains = ["dianping.com"]
    web_success=[]
    web=[]
    #start_urls = []
    #with open('C:/Users/Administrator/Desktop/huanjing_20171030.txt', 'r', encoding='utf-8') as f:
    ##    for line in f:
    #        web_success.append(line.split('[}')[0].replace('\n',''))
    #print(set(web_success))
    #'''
    with open('C:/Users/Administrator/Desktop/20171103.txt', 'r', encoding='utf-8') as f:
        for line in f:
            #url = 'https://www.dianping.com/search/keyword/8/0_' + str(line.split('[}')[0])
            #id=line.split('[}')[1].replace('\n','')
            #url = 'http://www.dianping.com/shop/%s/photos/tag-菜' %str(id)
            if id not in web_success:
                web.append(line.replace('\n',''))
    #print(start_urls)
   # '''
    def start_requests(self):
        for i in self.web:
            id = i.split('[}')[1].replace('\n', '')
            url = 'http://www.dianping.com/shop/%s/photos/tag-菜' %str(id)
            id1=i.split('[}')[0].replace('\n', '')
            name = i.split('[}')[2].replace('\n', '')
            yield  Request(url=url,meta={"id": id1, "name": name},callback=self.parse1)

    def parse1(self, response):
        id1=response.meta['id']
        name=response.meta['name']
        id=response.url.split('/')[-3]
        img_regex = r'(.*?(?:.jpg|.png|.jpeg|.bmp|.svg|.swf)+)'
        #img = 'http://p0.meituan.net/xianfu/d9e9b64a2b6da97411444e5cb010f0be24576.jpg'
        #print(re.findall(img_regex, img.split('/')[-1]))
        imglist=[]
        try:
            for sel in response.xpath('//div[@class="picture-list"]/ul/li'):
                imglist.append(sel)

            for sel in imglist:
                imgurl=sel.xpath('div/a/img/@src').extract_first()
                goods = sel.xpath('div[@class="picture-info"]/div/h3/a/text()').extract_first()
                if goods==None:
                    continue
                #img=re.findall(img_regex,imgurl.split('/')[-1])[0]
                img='%s_photo_%d.jpg' %(name,imglist.index(sel))
                print(goods,imgurl)
                data = '%s[}%s[}%s[}%s[}%s' % (id1, id, name, goods,img)
                tool.GetImg(imgdir3, imgurl, img)
                with open('C:/Users/Administrator/Desktop/shangping_20171106.txt', 'a', encoding='utf-8') as f:
                    f.write(data)
                    f.write('\n')
        except:
              print(response.url)

        '''
        urlname=urllib.request.unquote(response.url.split('_')[1])#url编码转中文
        for sel in response.xpath('//*[@id="shop-all-list"]/ul/li[1]'):
            shopname=sel.xpath('div[@class="txt"]/div/a/@title').extract_first()
            url=sel.xpath('div[@class="txt"]/div/a/@href').extract_first()
            address=sel.xpath('div[@class="txt"]/*/span[@class="addr"]/text()').extract_first()
            data='%s[}%s[}%s[}%s' %(urlname,shopname,url,address)
            with open('C:/Users/Administrator/Desktop/daipaqu_0.txt', 'a', encoding='utf-8') as f:
                  f.write(data)
                  f.write('\n')
        '''


