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
        self.course_credits = {}
        self.courses = []

    def parse_credits(self, response):
        # 6. Course_credits - integer / dictionary of key (level) and value (credit)
        self.course_credits[response.request.url] = response.css('.col-xs-9.col-md-9 ::text').get().strip()

    def parse(self, response):
        present_link = response.request.url
        course_level = response.css('.breadcrumb')  # for  4. Course_level - string
        course_level = course_level.css('a')[3]
        
        course_level , course_track = remove_tags(course_level.extract()).split(' in ', maxsplit=1)
        course_level = re.sub(r"Degree"," ",remove_tags(course_level))
        table = response.css('.field-item.even tbody')  # for parse 2,3,4,5,8
        university_title_full = (
            "Universitat Politechnica de Catalunya Barcelonatech.FIB Facultat d'Informatica de Barcelona."
        )
        course_credits_type = "ECTS"  # because in throughout Spain credits type is ECTS

        lines = table.css('tr')
        for line in lines:
            course_local_id = line.css('.acronym ::text').get()  # 2. Course_local_id - string
            course_title_full = line.css('.name ::text').get()  # 3. Course_title_full - string
            # 8. Course_link_descrip - string
            course_link_descrip = urljoin(present_link, line.css('.name a::attr(href)').get())
            yield response.follow(course_link_descrip, self.parse_credits)
            course_semester = line.css('.curs_obert ::text').get()  # 5. Course_semester - string
            if course_semester == "Q1, Q2":
                course_semester = "Spring, Fall"
            elif course_semester == "Q2":
                course_semester = "Spring"
            elif course_semester == "Q1":
                course_semester = "Fall"

            self.courses.append({
                'university_title_full': university_title_full,  # 1. University_title_full - string
                'course_local_id': course_local_id.strip(),  # 2. Course_local_id - string
                'course_title_full': course_title_full.strip(),  # 3. Course_title_full - string
                'course_level': course_level.strip(),  # 4. Course_level - string
                'course_track': course_track.strip(),
                'course_semester': course_semester,  # 5. Course_semester - string
                'course_credits_type': course_credits_type,  # 7. Course_credits_type
                'course_link_descrip': course_link_descrip,  # 8. Course_link_descrip - string
            })
