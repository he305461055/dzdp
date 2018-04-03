import scrapy
import re
from bs4 import BeautifulSoup

dirPath = 'C:/Users/Administrator/Desktop/DAIYUYING/zhilian/'
filename = 'zhilian.txt'
writefilename = 'zhilian_detail.txt'

class ZhiLianSpiders(scrapy.Spider):
    name = 'zhilian'
    allowed_domains=['http://company.zhaopin.com/']
    start_urls=[]
    '''
    with open('%s%s' % (dirPath, filename), 'r') as f:
        for line in f:
            if 'http://company.zhaopin.com/' in line.replace('\n', ''):
                 start_urls.append(line.replace('\n', ''))
    '''
    def parse(self, response):
        if response.status != 200:
            return None

        company_name=response.xpath('//div[@class="mainLeft"]/div/h1/text()').extract()[0].replace('\r','').replace('\n','').replace(' ','')

        try:
          company_size=response.xpath('.//tr[2]/td[2]/span/text()').extract()[0]
        except:
          company_size=''

        try:
          company_website=response.xpath('.//tr[3]/td[2]/span/a/text()').extract()[0]
        except:
          company_website=''

        company_industries=','.join(response.xpath('.//tr[4]/td[2]/span/text()').extract())

        company_address=response.xpath('.//tr[5]/td[2]/span/text()').extract()[0]

        soup= BeautifulSoup(response.body,"html.parser")
        company_info=''.join(re.findall("[\u4e00-\u9fa5_a-zA-Z0-9]|[\（\）\《\》\——\；\，\。\‘\’\“\”\<\>\！\《\》\【\】\*\&\……\￥\#\@\~]|[\^,.!`?+=\_\-:;\']",soup.find('div',class_='company-content').text))
        #company_info=''.join(response.xpath('//div[@class="company-content"]/text()').re(u"[\u4e00-\u9fa5_a-zA-Z0-9]|[\（\）\《\》\——\；\，\。\‘\’\“\”\<\>\！\《\》\【\】\*\&\……\￥\#\@\~]|[\^,.!`?+=\_\-:;\']"))

        regx=u'(\d{4}[\s\S]*成立|\d{1,3}年|[\s\S]{1,2}年)'
        company_year=re.findall(regx,company_info)

        data='%s[}%s[}%s[}%s[}%s[}%s[}%s' %(company_name,company_size,company_website,company_industries,company_address,company_year,company_info)

        with open('%s%s' % (dirPath, writefilename), 'a', encoding='utf-8') as f:
            f.write(data)
            f.write('\n')



