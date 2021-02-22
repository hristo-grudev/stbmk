import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import StbmkItem
from itemloaders.processors import TakeFirst


class StbmkSpider(scrapy.Spider):
	name = 'stbmk'
	start_urls = ['https://www.stb.com.mk/novosti/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="card-body"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@aria-label="Next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)


	def parse_post(self, response):
		title = response.xpath('//div[@class="container-fluid content-product"]//h3/text()').get()
		description = response.xpath('//div[@class="p-0"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		try:
			date = re.findall(r'\d{1,2}.\s*\d{1,2}.\s*\d{4}', description)[0]
		except:
			date = ''

		item = ItemLoader(item=StbmkItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
