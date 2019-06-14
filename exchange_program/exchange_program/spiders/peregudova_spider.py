import scrapy
from urllib.parse import urljoin
from scrapy.utils.markup import remove_tags
import re

class CataloniaSpider(scrapy.Spider):
    name = "catalonia"
    start_urls = [
        'https://www.fib.upc.edu/en/studies/bachelors-degrees/bachelor-degree-informatics-engineering/curriculum/syllabus',
        'https://www.fib.upc.edu/en/studies/masters/master-informatics-engineering/curriculum/syllabus',
        'https://www.fib.upc.edu/en/studies/masters/master-innovation-and-research-informatics/curriculum/syllabus',
        'https://www.fib.upc.edu/en/studies/masters/master-artificial-intelligence/curriculum/syllabus',
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.credits = {}
        self.courses = []

    def parse_credits(self , response):
        self.credits[response.request.url] = response.css('.col-xs-9.col-md-9 ::text').get().strip()

    def parse(self, response):
        present_link = response.request.url
        course_level = response.css('.breadcrumb') # for  4. Course_level - string
        course_level = course_level.css('a')[3]
        course_level = re.sub(r" Degree in ",", ",remove_tags(course_level.extract()))
        course_level = re.sub(r" in ",", ",remove_tags(course_level))
        table = response.css('.field-item.even tbody') # for parse 2,3,4,5,8

        university_title = "Universitat Politechnica de Catalunya Barcelonatech.FIB Facultat d'Informatica de Barcelona."
        credits_type = "ECTS" # because in throughout Spain credits type is ECTS

        lines = table.css('tr')
        for line in lines:
            id = line.css('.acronym ::text').get()  # 2. Course_local_id - string
            name = line.css('.name ::text').get() # 3. Course_title_full - string
            link = urljoin(present_link , line.css('.name a::attr(href)').get()) #8. Course_link_descrip - string
            yield response.follow(link, self.parse_credits)
            semester = line.css('.curs_obert ::text').get() # 5. Course_semester - string
            if semester == "Q1, Q2":
                semester = "Spring, Fall"
            elif semester == "Q2":
                semester = "Spring"
            elif semester == "Q1":
                semester = "Fall"

            self.courses.append({
                'university_title' : university_title, # 1. University_title_full - string
                'id': id.strip(), # 2. Course_local_id - string
                'name': name.strip(), # 3. Course_title_full - string
                'course_level': course_level.strip(), # 4. Course_level - string
                'semester': semester, # 5. Course_semester - string
                'credits_type' : credits_type,# 7. Course_credits_type
                'link' : link, #8. Course_link_descrip - string
            })
