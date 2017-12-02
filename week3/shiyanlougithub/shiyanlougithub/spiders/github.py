# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub.items import GithubItem

class GithubSpider(scrapy.Spider):
    name = 'github'

    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_tmpl.format(i) for i in range(1, 5))

    def parse(self, response):
        for repository in response.css('li.public'):
            item = GithubItem({
                'name': repository.xpath('.//a[@itemprop="name codeRepository"]/text()').re_first("\n\s*(.*)"),
                'update_time': repository.xpath('.//relative-time/@datetime').extract_first() 
            })
            repository_url = 'https://github.com'+repository.xpath('.//div[contains(@class,"mb-1")]/h3/a/@href').extract_first()
            request = scrapy.Request(repository_url,callback=self.parse_branch)
            request.meta['item'] = item
            yield request

    def parse_branch(self,response):
        item = response.meta['item']
        item['commits'] = response.xpath('(//span[@class="num text-emphasized"])[1]/text()').extract_first()
        item['branches'] = response.xpath('(//span[@class="num text-emphasized"])[2]/text()').extract_first()
        item['releases'] = response.xpath('(//span[@class="num text-emphasized"])[3]/text()').extract_first()
        yield item
