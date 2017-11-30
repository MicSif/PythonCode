import scrapy
class GithubShiyanlou(scrapy.Spider):
	name='github-shiyanlou'
	@property
	def start_urls(self):
		url_first='https://github.com/shiyanlou?page={}&tab=repositories'
		return (url_first.format(i) for i in range(1,5))
	def parse(self,response):
		for each_repositorie in response.xpath('//li[@class="col-12 d-block width-full py-4 border-bottom public source"]'):
			yield {
			'name':each_repositorie.xpath('.//div[contains(@class,"mb-1")]/h3/a/text()').re_first('[^\d]{2}\s*(\w*)'),
			'update_time':each_repositorie.xpath('.//div[contains(@class,"mt-2")]/relative-time/@datetime').extract_first()
			}