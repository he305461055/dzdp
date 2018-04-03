import scrapy
import dzdp.tool as tool
import os
import re
import dzdp.POI as POI
from scrapy.http import Request
import time
from bs4 import BeautifulSoup
import json
from scrapy.selector import Selector
import html.parser
from selenium import webdriver
import json

class DzdpSpiders(scrapy.Spider):

    if tool.channel_name == 'MEITUAN':
        channel_type = 1
    elif tool.channel_name == 'DZDP':
        channel_type = 2
    file_name='dzdp_food_detail'
    name='dzdp_shopping'
    allowed_domains=["dianping.com"]
    web_success = []
    start_urls=[]
    if not os.path.exists(r'%s%s.txt' %(tool.data_dir,tool.successfilename)):
        with open('%s%s.txt' %(tool.data_dir,tool.successfilename),'w',encoding='utf-8'):
            pass
    with open('%s%s.txt' %(tool.data_dir,tool.successfilename), 'r',encoding='utf-8') as f:
        for line in f:
            web_success.append(line.replace('\n', ''))

    '''
    for i in range(0,19):
        file = '%s%s_%d.txt' % (tool.data_dir,file_name, i)
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                #url = 'http://www.dianping.com/shop/' + str(line.split('[}')[0])
                url='http://www.dianping.com/ajax/json/shopDynamic/allReview?shopId=%s&cityId=8&categoryURLName=food&power=5&cityEnName=chengdu&shopType=10' %str(line.split('[}')[0])
                #if url not in web_success:
                start_urls.append(url)
    '''
    def parse(self, response):
        pass
        '''
        id=response.url.split('&')[0].split('=')[-1]
        mydata = re.findall('\"summarys\":(.*?),\"dishTagStrList\"', response.body_as_unicode())[0]
        for myjson in json.loads(mydata):
            type=myjson['summaryType']
            flag=myjson['summaryName']
            string=myjson['summaryString']
            count=myjson['summaryCount']
            data='%s[}%s[}%s[}%s[}%s' %(id,flag,type,string,count)
            tool.GetFile('shop_mark',data,3,10000)
        '''
        '''
        id=response.url.split('/')[-2]
        page=int(response.url.split('=')[-1])
        max_page=response.xpath('//*[@id="top"]/div[4]/div[2]/div/div[1]/div/ul/li[1]/span/em/text()').extract_first().replace('(','').replace(')','')
        for sele in response.xpath('//div[@class="comment-list"]/ul/li'):
            user_name=sele.xpath('div/p[@class="name"]/a/text()').extract_first()
            user_star=sele.xpath('div/p[@class="contribution"]/span/@class').extract_first().split('-')[-1]
            content_star=sele.xpath('div[@class="content"]/div[@class="user-info"]/span/@class').extract_first().split('-')[-1].replace('\n','')
            content_sorce=','.join(sele.xpath('div//div[@class="comment-rst"]/span/text()').extract()).replace('\n','')
            content=''.join(sele.xpath('div//div[@class="comment-txt"]/div/text()').re(u"[\u4e00-\u9fa5_a-zA-Z0-9]|[\（\）\《\》\——\；\，\。\‘\’\“\”\<\>\！\《\》\【\】\*\&\……\￥\#\@\~]|[\^,.!`?+=\_\-:;\']"))
            data='%s[}%s[}%s[}%s[}%s[}%s' %(id,user_name,user_star,content_star,content_sorce,content)
            #tool.GetFile('newcontent', data, 3, 10000)
        #tool.GetFile('success', response.url, 3, 100000)
        if page*20<int(max_page):
            follow_url='http://www.dianping.com/shop/22584878/review_all?pageno=%d' %(page+1)
            yield Request(url=follow_url,callback=self.parse)
        '''
    def parse1(self, response):
        flag=0 #用来判断页面的类型，有些商场的页面跟普通的页面是一样的
        img_regex = r'(.*?(?:.jpg|.png|.jpeg|.bmp|.svg|.swf)+)'#图片正则

        if response.status!=200:
            print('%s======response拿值失败,状态：%s'%(response.url,response.status))
            print('########################################################')
            return None

        shop_type = '>'.join(response.xpath('//*[@id="body"]/div[2]/div[1]/a/text()').extract()).replace('\n', '').replace( ' ', '')  # 店铺类型
        if not shop_type.strip():#shop_type=='':
            shop_type = '>'.join(response.xpath('//*[@id="top"]/div[6]/div[1]/a/text()').extract()).replace('\n', '').replace(' ', '')  # 店铺类型
            flag = 1

        print(shop_type)
        if (tool.type not in shop_type):
            print('%s=====不是\"%s\"该类型退出' %(response.url,tool.type))
            print('########################################################')
            return None

        shop_id = response.url.split('/')[-1]  # 店铺ID

        if flag==1:
          shop_name = response.xpath('//*[@id="top"]/div[6]/div[1]/span/text()').extract()[0]  # 店铺名称
        else:
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

        if coordinate==' ':
            pattern1 = re.compile('shopGlat: "(.*?)"', re.S)  # 获取坐标
            pattern2 = re.compile('shopGlng:"(.*?)"', re.S)  # 获取坐标
            try:
              coordinate ='%s %s' %(re.findall(pattern1, str(response.body))[0],re.findall(pattern2, str(response.body))[0])
            except:
              coordinate = ' '

        if flag==1:
            shop_sorce_list = response.xpath('//*[@id="market-detail"]/div/p')
            shop_stars = shop_sorce_list[-3].xpath('span[2]/@class').extract()[0].split()[1] # 商铺星级

            mean_price = shop_sorce_list[-2].xpath('text()').extract()[1].replace('\n','').replace( ' ', '')  # 人均

            shop_sorce = ' '.join(shop_sorce_list[-3].xpath('span/text()').extract()) # 商铺评分

            shop_address = response.xpath('//*[@id="market-detail"]/p[1]/text()').extract()[0].replace('\n','').replace( ' ', '')  # 商铺地址

            try:
                shop_phone = shop_sorce_list[0].xpath('text()').extract().replace(' ','').strip() # 商铺电话
            except:
                shop_phone = ' '

            try:
                shop_time = ' '.join(response.xpath('//*[@id="market-detail"]/p[2]/text()').extract()).replace('\n', '').replace(' ', '').replace('\xa0', '')  # 商铺营业时间
            except:
                shop_time = ' '

        else:
            shop_sorce_list = response.xpath('//div[@class="brief-info"]/span')
            shop_stars = shop_sorce_list[0].xpath('@class').extract()[0].split(' ')[-1]  # get('class')[1]  # 商铺星级

            mean_price = shop_sorce_list[2].xpath('text()').extract()[0]  # 人均
            if '人均' not in mean_price and '消费' not in mean_price:
                mean_price = shop_sorce_list[1].xpath('text()').extract()[0]  # 人均

            if len(shop_sorce_list) > 3:
                shop_sorce = '%s %s %s' % (
                shop_sorce_list[-3].xpath('text()').extract()[0], shop_sorce_list[-2].xpath('text()').extract()[0],
                shop_sorce_list[-1].xpath('text()').extract()[0])  # 商铺评分
            else:
                shop_sorce = ' '

            shop_address = response.xpath('//span[@itemprop="street-address"]/text()').extract()[0].replace('\n','').replace(' ', '')  # 商铺地址

            try:
                shop_phone = ' '.join(response.xpath('//p[@class="expand-info tel"]/span/text()').extract().replace(' ','').strip())  # 商铺电话
            except:
                shop_phone = ' '

            try:
                shop_time = ' '.join(response.xpath('//p[@class="info info-indent"]/span/text()').extract()).replace( '\n', '').replace(' ', '').replace('\xa0', '')  # 商铺营业时间
                if '别名' in shop_time:
                    shop_time = ' '.join( response.xpath('//p[@class="info info-indent"][2]/span/text()').extract()).replace('\n','').replace(' ', '')  # 商铺营业时间
            except:
                shop_time = ' '

        shop_park = ''

        shop_phone1=''

        shop_charge=''

        shop_service=''

        shop_info=''

        create_time=''

        pay_play=''

        comment_list=response.xpath('//div[@class="content"]/span/a/text()').extract() # 点评
        if len(comment_list)>0:
           comment = ','.join(comment_list)
        else:
           comment=' '

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
        shop_phone, shop_phone1, shop_charge, mean_price, shop_time, shop_service, shop_info, self.channel_type, create_time, pay_play, shop_park, comment, shop_type)

        shop_attached = '%s[}%s[}%s[}%s[}%s[}%s[}%s' % (shop_id, business_licence,original_business_licence, beverage_license,original_beverage_license, ' ', ' ')
        #print(shop_detail_info)
        tool.GetFile(tool.detailfilename, shop_detail_info,3, 5000)
        #'''
        # 下载图片
        try:
            if shop_img_adress != ' ' and 'http:' in original_shop_img_adress:
                tool.GetImg(tool.img_dir,original_shop_img_adress, shop_img_adress)
        except Exception as e:
            print(e)
            print(original_shop_img_adress)
            print('无法下载请检查路径')
            return None

        try:
            if business_licence != ' ' and 'http:' in original_business_licence:
                tool.GetImg(tool.yyzz_img_dir,original_business_licence, business_licence.split('/')[-1].split('?')[0])
        except Exception as e:
            print(e)
            print(original_business_licence)
            print('无法下载请检查路径')
            return None

        try:
            if beverage_license != ' ' and 'http:' in original_beverage_license:
                tool.GetImg(tool.yyzz_img_dir,original_beverage_license, beverage_license.split('/')[-1].split('?')[0])
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
        with open('%s%s.txt' % (tool.data_dir, tool.successfilename), 'a') as f:
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

        user_comment_url='http://www.dianping.com/ajax/json/shopfood/wizard/reviewAllFPAjax?shopId=%s&cityId=%s&power=5' %(str(shop_id),str(tool.city_id))
        yield Request(user_comment_url,callback=self.UserComment)


    def UserComment(self,response):
        shop_id=response.url.split('?')[-1].split('&')[0].split('=')[-1]
        data=response.body.decode('utf-8')
        data=json.loads(data)['msg']['reviewAreaFPHtml']
        for sel in Selector(text=data).xpath('//ul[@class="comment-list J-list"]/li'):#Selector(text=data).xpath('//li'):
            try:
                user_name = sel.xpath('p/a[@class="name"]/text()').extract()[0]  # 用户名称

                content_sorce = sel.xpath('div/p[@class="shop-info"]/span')
                content_stars = content_sorce[0].xpath('@class').extract()[0].split()[-1]  # 评分星级

                content_sorce = ' '.join(content_sorce.xpath('text()').extract())  # 用户评分

                user_content = ''.join(sel.xpath('*//p[@class="desc J-desc"]/text()').extract())
                if len(user_content) < 1:
                    user_content = ''.join(sel.xpath('*//p[@class="desc"]/text()').extract())

                content = '%s[}%s[}%s[}%s[}%s[}%d{]' % (shop_id, user_name, content_stars, content_sorce, user_content, self.channel_type)
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