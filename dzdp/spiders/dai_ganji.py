import scrapy
import dzdp.tool as tool

class DaiganjiSpiders(scrapy.Spider):
    name='dai_ganji'
    allowed_domains=["ganji.com"]
    start_urls=[]

    def parse(self, response):
        pass

