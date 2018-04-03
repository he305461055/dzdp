import scrapy
import re
from dzdp.items import DzdpItem,ContentItem
import dzdp.tool as tool

class DdaiyuyingSpider(scrapy.Spider):
    name = "daiyuying"
    allowed_domains = ["siilu.com"]
    '''
    start_urls = ['http://www.siilu.com/service/9049.html']

    file = '%s%s_%d.txt' % (tool.data_dir, tool.daiadressfilename, 0)
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            #url = 'http://www.dianping.com' + str(line.split('[}')[0])
            start_urls.append(line.split('[}')[0])
    '''
    def parse(self, response):
        if response.status != 200:
            print(response.url)
            print('response拿值失败')
            print(response.status)
            print('########################################################')
            return None

        if '.html' in response.url:

            id=response.xpath('//p[@class="sev_into"]/a/@href').extract()[0].split('/')[-1]

            try:
              name=response.xpath('//div[@class="sev_list"]/dl[1]/dd/h2/text()').extract()[0]
            except:
              name = response.xpath('//*[@id="surl"]/strong/text()').extract()[0]

            table=response.xpath('//*[@id="showfwxq"]/div/div/table/tr/td')
            try:
              hangye_classify=','.join(table[1].xpath('a/text()').extract())
              #','.join(response.xpath('.//tr[1]/td[2]/a/text()').extract())
            except:
              hangye_classify=''

            try:
              pingtai_classify=','.join(table[3].xpath('a/text()').extract())
            except:
              pingtai_classify=' '

            try:
                success=','.join(response.xpath('//*[@id="showcgal"]/div/dl/dd/a/img/@alt').extract())
            except:
                success=' '

            type=response.xpath('//*[@id="wrap"]/ul/li/a[last()-1]/text()').extract()[0]

            create_time=response.xpath('//div[@class="sev_list"]/dl[last()]/dd/text()').extract()[0]

            mark=','.join(response.xpath('//div[@class="label_con"]/a/text()').extract())

            try:
              price = response.xpath('//*[@id="show_price"]/text()').extract()[0]
            except:
              regx1='{"price1":"(.*?)",'
              price = re.findall(regx1,str(response.body))[0]

            info=''.join(response.xpath('//div[@class="clearfix"]/dl/dd/text()').re(u"[\u4e00-\u9fa5_a-zA-Z0-9]|[\（\）\《\》\——\；\，\。\‘\’\“\”\<\>\！\《\》\【\】\*\&\……\￥\#\@\~]|[\^,.!`?+=\_\-:;\']"))

            regx=r"\d{1,10}人"
            sum=re.findall(regx,info)
            if len(sum)>0:
                people=sum[0]
            else:
                people=' '

            data='%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}' %(id,name,type,create_time,mark,people,price,hangye_classify,pingtai_classify,success,info)

            #tool.GetFile(tool.daifilename1, data, 1, 5000)

        else:
            id = response.url.split('/')[-1]

            web_address=response.xpath('/html/body/div[2]/div[1]/div[2]/p[1]/text()').extract()[0]

            address=response.xpath('/html/body/div[2]/div[1]/div[2]/p[2]/text()').extract()[0]

            phone=response.xpath('/html/body/div[2]/div[1]/div[2]/div[1]/p[1]/text()').extract()[0]

            email=response.xpath('/html/body/div[2]/div[1]/div[2]/div[1]/p[2]/text()').extract()[0]

            data = '%s[}%s[}%s[}%s[}%s' % (id, web_address,address,phone,email)

            tool.GetFile(tool.daifilename2, data, 1, 5000)