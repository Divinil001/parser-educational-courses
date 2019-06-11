# -*- coding: utf-8 -*-
import math
import scrapy
from bs4 import BeautifulSoup


class MetuSpider(scrapy.Spider):
    name = 'metu'
    allowed_domains = ['catalog.metu.edu.tr']
    start_urls = ['https://catalog.metu.edu.tr/prog_courses.php?prog=901',
                  'https://catalog.metu.edu.tr/prog_courses.php?prog=910',
                  'https://catalog.metu.edu.tr/prog_courses.php?prog=903',
                  'https://catalog.metu.edu.tr/prog_courses.php?prog=905',
                  'https://catalog.metu.edu.tr/prog_courses.php?prog=571']

    def parse(self, response):
        for href in response.css('div table tr td.short_course a').xpath('@href').getall():
            yield response.follow(href, self.parse_course)

    def parse_course(self, response):
        results = dict()

        results['University_title_full'] = 'Middle East Technical University'

        results['Course_local_id'] = BeautifulSoup(
            ''.join(response.css('table.course tr')[0].css('td')[1].getall())
        ).get_text()

        results['Course_title_full'] = response.css('div.field-body h2::text').get()

        results['Course_level'] = BeautifulSoup(
            ''.join(response.css('table.course tr')[5].css('td')[1].getall())
        ).get_text()

        results['Course_semester'] = BeautifulSoup(
            ''.join(response.css('table.course tr')[7].css('td')[1].getall())
        ).get_text()

        results['Course_credits'] = math.floor(
            float(
                BeautifulSoup(
                    ''.join(response.css('table.course tr')[2].css('td')[1].getall())
                ).get_text()
            )
        )

        results['Course_credits_type'] = 'ECTS'

        results['Course_link_descrip'] = response.url

        yield results
