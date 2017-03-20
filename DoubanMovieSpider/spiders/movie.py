# -*- coding: utf-8 -*-
import scrapy
from DoubanMovieSpider.items import DoubanmoviespiderItem


class MovieSpider(scrapy.Spider):
    name = "movie"
    allowed_domains = ["douban.com"]
    start_urls = ['https://movie.douban.com/top250/']
    url = 'https://movie.douban.com/top250'

    def parse(self, response):
        selector = scrapy.Selector(response)
        movies = selector.xpath('//div[@class="info"]')
        for movie in movies:
            item = DoubanmoviespiderItem()
            title = movie.xpath('div[@class="hd"]/a')
            fullTitle = title.xpath('string(.)').extract_first().replace('\n', '').replace(' ', '')
            info = movie.xpath('div[@class="bd"]/p/text()').extract_first().replace('\n', '').replace(' ', '')
            star = movie.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract_first()
            quote = movie.xpath('div[@class="bd"]/p[@class="quote"]/span/text()')
            if quote:
                quote = '"' + quote.extract_first() + '"'
            item['title'] = fullTitle
            item['info'] = info
            item['star'] = star
            item['quote'] = quote
            yield item
        next_page = selector.xpath('//span[@class="next"]/link/@href').extract_first()
        if next_page:
            yield scrapy.Request(self.url + next_page, callback=self.parse)
