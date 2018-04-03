import scrapy
import re
import dzdp.POI as POI
from dzdp.items import DzdpItem,ContentItem
import  traceback
import dzdp.tool as tool
from scrapy.http import Request

class DzdpSpider(scrapy.Spider):
    name = "dzdp_food1111111"
    allowed_domains = ["dianping.com"]
    web_success=[]
    start_urls = []
    #with open('C:/Users/Administrator/Desktop/daipaqu_1.txt', 'r',encoding='utf-8') as f:
    #    for line in f:
    #        start_urls.append(line.split('[}')[1].replace('\n', ''))
    '''
    with open('C:/Users/Administrator/Desktop/DZDP_BASIC/dzdp_success_list.txt', 'r') as f:
        for line in f:
            web_success.append(line.replace('\n', ''))
    for i in range(0, 51):
        file = '%s%s_%d.txt' % (tool.data_dir,tool.addressfilename, i)
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                url = 'http://www.dianping.com' + str(line.split('[}')[0])
                if url not in web_success:
                    start_urls.append('http://www.dianping.com%s' %line.split('[}')[0])
    print(len(start_urls))
    '''

    def parse(self, response):
       # yield Request(url='http://www.dianping.com/shop/9977885',callback=self.parse1)
       pass

    def parse1(self, response):
        print(response.body)
        img_regex = r'(.*?(?:.jpg|.png|.jpeg|.bmp|.svg|.swf)+)'#图片正则
        print(response.body)
        if response.status!=200:
            print(response.url)
            print('response拿值失败')
            print(response.status)
            print('########################################################')
            return None
        #print(response.url)

        shop_id = response.url.split('/')[-1]  # 店铺ID

        shop_name = response.xpath('//*[@id="body"]/div[2]/div[1]/span/text()').extract()[0]# 店铺名称

        try:
            original_shop_img_adress = response.xpath('//img[@itemprop="photo"]/@src').extract()[0]# 原始商铺图片地址
            shop_img_adress = re.findall(img_regex,original_shop_img_adress)[0].split('/')[-1]  # 商铺图片
        except:
            shop_img_adress = ' '

        pattern = re.compile('poi: "(.*?)"', re.S)  # 获取坐标
        try:
            poi = re.findall(pattern, str(response.body))[0]
            coordinate= str(POI.decode(poi))
        except:
            coordinate=' '

        shop_sorce_list = response.xpath('//div[@class="brief-info"]/span')
        shop_stars = shop_sorce_list[0].xpath('@class').extract()[0].split(' ')[-1]#get('class')[1]  # 商铺星级

        try:
          mean_price = shop_sorce_list[2].xpath('text()').extract()[0]  # 人均
          if '人均' not in mean_price:
              mean_price = shop_sorce_list[1].xpath('text()').extract()[0]  # 人均
        except:
          mean_price = shop_sorce_list[1].xpath('text()').extract()[0]  # 人均

        if len(shop_sorce_list) > 3:
            shop_sorce = '%s %s %s' % (shop_sorce_list[-3].xpath('text()').extract()[0], shop_sorce_list[-2].xpath('text()').extract()[0], shop_sorce_list[-1].xpath('text()').extract()[0])  # 商铺评分
        else:
            shop_sorce = ' '

        shop_address = response.xpath('//span[@itemprop="street-address"]/text()').extract()[0].replace('\n','').replace(' ', '')  # 商铺地址

        try:
            shop_phone=' '.join(response.xpath('//p[@class="expand-info tel"]/span/text()').extract()) # 商铺电话
        except:
            shop_phone = ' '

        shop_phone1=''

        shop_charge=''

        try:
            shop_time = ' '.join(response.xpath('//p[@class="info info-indent"]/span/text()').extract()).replace('\n','').replace(' ','') # 商铺营业时间
        except:
            shop_time = ' '

        shop_service=''

        shop_info=''

        if tool.channel_name == 'MEITUAN':
            channel_type = 1
        elif tool.channel_name == 'DZDP':
            channel_type = 2

        create_time=''

        pay_play=''

        shop_park=''

        comment_list=response.xpath('//div[@class="content"]/span/a/text()').extract() # 点评
        if len(comment_list)>0:
           comment = ','.join(comment_list)
        else:
           comment=' '

        shop_type = '>'.join(response.xpath('//*[@id="body"]/div[2]/div[1]/a/text()').extract()).replace('\n', '').replace(' ', '')  # 店铺类型

        #regex = re.compile("licensePics:(.*?),]",re.S)
        #regex = r"licensePics:\[\\'(.*?)\\',\]"

        regex = r"licensePics:\[\\'(.*?)\\',\]"

        business_list = re.findall(regex,str(response.body))
        if len(business_list)>0:
          business_list = business_list[0].split(',')

        if len(business_list)>0:
            original_business_licence=business_list[0].replace('\\','').replace("'",'')
            temp_business_licence=re.findall(img_regex,original_business_licence.split('/')[-1].split('?')[0])
            if len(temp_business_licence)==0:
                business_licence = '%s.jpg' % (original_business_licence.split('/')[-1].split('?')[0])
            else:
                business_licence = temp_business_licence[0]

        else:
            original_business_licence=' '
            business_licence=' '

        if len(business_list)>1:
            original_beverage_license=business_list[1].replace('\\','').replace("'",'')
            temp_beverage_license=re.findall(img_regex,original_beverage_license.split('/')[-1].split('?')[0])
            if len(temp_beverage_license)==0:
                beverage_license='%s.jpg' %(original_beverage_license.split('/')[-1].split('?')[0])
            else:
                beverage_license=temp_beverage_license[0]
        else:
            original_beverage_license=' '
            beverage_license=' '

        shop_detail_info = '%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%d[}%s[}%s[}%s[}%s[}%s' % (
        shop_id, shop_name, shop_img_adress, coordinate, shop_stars, shop_sorce, shop_address,
        shop_phone, shop_phone1, shop_charge, mean_price, shop_time, shop_service, shop_info, channel_type, create_time, pay_play, shop_park, comment, shop_type)

        shop_attached = '%s[}%s[}%s[}%s[}%s[}%s[}%s' % (shop_id, business_licence,original_business_licence, beverage_license,original_beverage_license, ' ', ' ')

        for sel in response.xpath('//ul[@class="comment-list J-list"]/li'):
              try:
                  user_name = sel.xpath('p/a[@class="name"]/text()').extract()[0] # 用户名称

                  content_sorce = sel.xpath('div/p[@class="shop-info"]/span')
                  content_stars = content_sorce[0].xpath('@class').extract()[0].split()[-1] # 评分星级
                  content_sorce = ' '.join(content_sorce.xpath('text()').extract())  # 用户评分

                  user_content = ''.join(sel.xpath('*//p[@class="desc J-desc"]/text()').extract())
                  if len(user_content)<1:
                      user_content = ''.join(sel.xpath('*//p[@class="desc"]/text()').extract())

                  content = '%s[}%s[}%s[}%s[}%s[}%d{]' % (shop_id, user_name, content_stars, content_sorce, user_content, channel_type)
              except:
                  continue
              tool.GetFile(tool.contentfilename, content,3, 5000)
              '''
              content_item = ContentItem()
              content_item['shop_id'] = shop_id
              content_item['user_name'] = user_name
              content_item['content_stars'] = content_stars
              content_item['content_sorce'] = content_sorce
              content_item['user_content'] = user_content
              content_item['channel_type'] = channel_type
              yield content_item
            '''


        tool.GetFile(tool.detailfilename, shop_detail_info,3, 5000)
        #'''
        # 下载图片
        try:
            if shop_img_adress != ' ' and 'http:' in original_shop_img_adress:
                tool.GetImg(original_shop_img_adress, shop_img_adress)
        except Exception as e:
            print(e)
            print(original_shop_img_adress)
            print('无法下载请检查路径')
            return None

        try:
            if business_licence != ' ' and 'http:' in original_business_licence:
                tool.GetImg(original_business_licence, business_licence.split('/')[-1].split('?')[0])
        except Exception as e:
            print(e)
            print(original_business_licence)
            print('无法下载请检查路径')
            return None

        try:
            if beverage_license != ' ' and 'http:' in original_beverage_license:
                tool.GetImg(original_beverage_license, beverage_license.split('/')[-1].split('?')[0])
        except Exception as e:
            print(e)
            print(original_beverage_license)
            print('无法下载请检查路径')
            return None


        # 写入商铺资质
        if (beverage_license != ' ' or business_licence != ' '):
            tool.GetFile('intelligence', shop_attached,3, 5000)
        #'''
        print('成功')
        with open('%s%s.txt' %(tool.data_dir,tool.successfilename), 'a') as f:
            f.write(response.url)
            f.write('\n')

        '''
        item = DzdpItem()
        item['shop_id'] = shop_id
        item['shop_id'] = shop_id
        item['shop_name'] = shop_name
        item['shop_img_address'] = shop_img_adress.split('/')[-1]
        item['shop_poi'] = coordinate
        item['shop_stars'] = shop_stars
        item['shop_sorce'] = shop_sorce
        item['shop_address'] = shop_address
        item['shop_phone'] = shop_phone
        item['shop_phone1'] = shop_phone1
        item['shop_charge'] = shop_charge
        item['mean_price'] = mean_price
        item['shop_time'] = shop_time
        item['shop_service'] = shop_service
        item['shop_info'] = shop_info
        item['channel_type'] = channel_type
        item['create_time'] = create_time
        item['pay_play'] = pay_play
        item['shop_park'] = shop_park
        item['comment'] = comment
        item['shop_type'] = shop_type
        yield item
        '''
