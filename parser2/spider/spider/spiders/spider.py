import scrapy
from urllib.parse import urljoin
from scrapy.utils.markup import remove_tags
import re

class SapienzaSpider(scrapy.Spider):
    name = "sapienza"
    start_urls = [
        'https://corsidilaurea.uniroma1.it/en',
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.courses = []
        self.addition_info = []

    def parse_next(self, response): # for credits, id, title, semester
        table = response.css('tbody')
        course_ssd = table.css('.insegnamento-ssd::text').getall() # need for choose correct lines
        title = table.css('.insegnamento-title::text').getall() # after we need strip it to id and title_full
        credits_number =  table.css('.insegnamento-crediti::text').getall()
        semesters = table.css('.insegnamento-semestre::text').getall()

        # choose correct data
        for credits , semester , course_title, ssd in zip(credits_number, semesters , title , course_ssd ):
            if ssd != '\n        ' and credits != '\n        ':
                if re.search(r' - ',course_title):
                    id , title_full = course_title.split(' - ', maxsplit = 1)
                    if re.search(r'First semester',semester):
                        semester = 'Fall'
                    elif re.search(r'Second semester',semester):
                        semester = 'Spring'
                    elif re.search(r'Go to group ',semester):
                        semester = 'None'

                    self.addition_info.append({
                        'course_local_id': id.strip(),
                        'course_title_full': title_full.strip(),
                        'course_semester': semester,
                        'course_credits': credits.strip() ,
                        'course_link_descrip' : response.request.url,
                    })

    def parse(self, response):
        university_title_full = "Sapienza University of Rome"
        course_credits_type = "CFU"

        table = response.css('.views-table.cols-5.table.table-0.table-0.table-0.table-0 tbody')
        next_link = table.css('.views-field.views-field-title-field a::attr(href)').getall()
        track = table.css('.views-field.views-field-title-field a::text').getall()
        for x in track:
            track.remove('\r\n')

        level = table.css('.views-field.views-field-field-tipologia-corso::text').getall()
        faculty = table.css('.views-field.views-field-field-facolta::text').getall()

        for fac , course_level , course_track , link in zip(faculty , level , track , next_link):
            if re.search("Informatics and Statistics", fac) or re.search("Information Engineering", fac):
                course_link_descrip = re.sub(r"home","cds",link)
                yield response.follow(course_link_descrip, self.parse_next)
                self.courses.append({
                    'university_title_full' : university_title_full,
                    'course_level': course_level.strip(),
                    'course_credits_type' : course_credits_type,
                    'course_link_descrip' : course_link_descrip,
                    'course_track': course_track.strip(),
                })
