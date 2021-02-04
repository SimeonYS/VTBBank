import scrapy
from ..items import VtbbankItem
import re

pattern = r'(\r)?(\n)?(\t)?(\xa0)?'


class VtbspiderSpider(scrapy.Spider):
    name = 'vtbspider'
    allowed_domains = []
    start_urls = ['https://www.vtb.eu/en/news/']
    base_url = 'https://www.vtb.eu'

    def parse(self, response):
        articles = response.xpath('//div[@class="b-newsBlock__item"]')
        for article in articles:
            link = self.base_url + article.xpath('.//p/a/@href').get()

            yield scrapy.Request(link, callback = self.parse_article)

    def parse_article(self, response):
        date = response.xpath('//p[@class="e-date"]/text()').get().strip()
        title = response.xpath('//div[@class="b-newsOpened__title"]/h1[@class="e-promo e-promo--black"]/text()').get()
        content = ''.join(response.xpath('//div[@class="b-newsOpened__text"]//text()').getall())
        content = re.sub(pattern, '', content).strip()
        title = re.sub(pattern, '', title).strip()
        item = VtbbankItem()

        item['date'] = date
        item['title'] = title
        item['content'] = content

        yield item