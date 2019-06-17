import scrapy
from exchange_program.exchange_program.items import ExchangeProgramItem
#ref https://raw.githubusercontent.com/mGalarnyk/Python_Tutorials/master/Scrapy/fundrazr/fundrazr/spiders/fundrazr_scrape.py

UNIVERSITY_TITLE = "Harbour.Space University"
CREDIT_TYPE = "ECTS"
URL = 'https://harbour.space/computer-science?curriculum-Bachelor'


class HarbourSpaceSpider(scrapy.Spider):
    name = "hspace_cs_bach"
    start_urls = [URL]

    def parse(self, response):
        for href in response.css("//li[contains(@class, 'subjects__item')]"):
            # TODO Better to use urljoin() method from Scrapy
            url = "https:" + href.extract()
            yield scrapy.Request(url, callback=self.parse_course)

    def parse_course(self, response):
        item = ExchangeProgramItem()
        item['university_title'] = UNIVERSITY_TITLE

        # TODO Better to use get() method instead of extract() since it is safer
        item['course_title'] = response.xpath("//div[contains(@class, 'subject__item__title')]"
                                              "/descendant::text()").extract()[0].strip()

        item['semester'] = 'year X'

        item['course_credits'] = response.xpath("//div[contains(@class, 'subject__item__credits')]"
                                                "/span[contains(@class, 'subjects__item__credits__count')]"
                                                "/descendant::text()").extract()[0].strip()

        item['credits_type'] = CREDIT_TYPE
        yield


