import scrapy
from exchange_program.exchange_program.items import ExchangeProgramItem
from urllib.parse import urljoin
#ref https://raw.githubusercontent.com/mGalarnyk/Python_Tutorials/master/Scrapy/fundrazr/fundrazr/spiders/fundrazr_scrape.py

UNIVERSITY_TITLE = "Harbour.Space University"
CREDIT_TYPE = "ECTS"
URL = 'https://harbour.space/computer-science?curriculum-Bachelor'


class HarbourSpaceSpider(scrapy.Spider):
    name = "hspace_cs_bach"
    start_urls = [URL]

    def parse(self, response):
        for href in response.css("//li[contains(@class, 'subjects__item')]"):
            url = urljoin("https:", href.extract())
            yield scrapy.Request(url, callback=self.parse_course)

    def parse_course(self, response):
        item = ExchangeProgramItem()
        item['university_title_full'] = UNIVERSITY_TITLE

        # TODO Better to use get() method instead of extract() since it is safer
        item['course_title_full'] = response.xpath("//div[contains(@class, 'subject__item__title')]"
                                              "/descendant::text()").get()

        item['course_semester'] = 'year X'

        item['course_credits'] = response.xpath("//div[contains(@class, 'subject__item__credits')]"
                                                "/span[contains(@class, 'subjects__item__credits__count')]"
                                                "/descendant::text()").get()

        item['course_credits_type'] = CREDIT_TYPE
        yield


