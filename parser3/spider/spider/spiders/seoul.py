import scrapy
from urllib.parse import urljoin
from scrapy.utils.markup import remove_tags
import re

class SeoulSpider(scrapy.Spider):
    name = "seoul"
    start_urls = [
        'http://sugang.snu.ac.kr/sugang/cc/cc100.action?lang=eng&srchCptnCorsFg=C013300001&workType=S&pageNo=1&srchCond=1&srchOpenUpDeptCd=400&srchOpenDeptCd=4190&srchIsEngSbjt=Y&srchOpenSchyy=2019&srchOpenShtm=U000200001U000300001',
        'http://sugang.snu.ac.kr/sugang/cc/cc100.action?lang=eng&srchCptnCorsFg=C013300001&workType=S&pageNo=1&srchCond=1&srchOpenUpDeptCd=400&srchOpenDeptCd=4190&srchIsEngSbjt=Y&srchOpenSchyy=2019&srchOpenShtm=U000200002U000300001',
        'http://sugang.snu.ac.kr/sugang/cc/cc100.action?lang=eng&srchCptnCorsFg=C013300002&workType=S&pageNo=1&srchCond=1&srchOpenUpDeptCd=400&srchOpenDeptCd=4190&srchIsEngSbjt=Y&srchOpenSchyy=2019&srchOpenShtm=U000200001U000300001',
        'http://sugang.snu.ac.kr/sugang/cc/cc100.action?lang=eng&srchCptnCorsFg=C013300002&workType=S&pageNo=1&srchCond=1&srchOpenUpDeptCd=400&srchOpenDeptCd=4190&srchIsEngSbjt=Y&srchOpenSchyy=2019&srchOpenShtm=U000200002U000300001',
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.courses = []
    def parse_pages(self, response):
        university_title_full = "Seoul National University SNU"
        course_credits_type = "CSH"
        course_track = "None"

        table = response.css('.tbl_basic tbody tr')
        lines = table.css('td::text').getall()
        title = table.css('td a::text').getall()
        course_semester = ''

        # define semester
        if re.search("U000200001U000300001", response.request.url):
            course_semester = "Fall"
        elif re.search("U000200002U000300001", response.request.url):
            course_semester = "Spring"
        # scraped information from table
        i = 0
        level = [] ; credits = [] ; local_id = []
        for info in lines:
            if re.search("Bachelor", info) or re.search("Master's", info) :
                level.append(info)
            if re.search("\d\d\d\d.\d\d\d+", info) : 
                local_id.append(info)
            if re.search("\d-\d-\d", info) : #4-3-2
                important, garbage = info.split('-', maxsplit = 1)
                credits.append(important)
            i = i + 1
        print(level, credits ,local_id)
        for course_title_full , course_level , course_local_id , course_credits in zip(title , level , local_id , credits):
            self.courses.append({
                'university_title_full': university_title_full,
                'course_local_id': course_local_id,
                'course_title_full': course_title_full,
                'course_level': course_level,
                'course_semester': course_semester,
                'course_credits': course_credits,
                'course_credits_type': course_credits_type,
                'course_link_descrip': response.request.url,
                'course_track': course_track,
            })

    def parse(self, response):
        #parse all pages with table
        paging = response.css('.paging span a::text').getall()
        next_page = ''
        for page in paging:
            next_page = re.sub(r"pageNo=1" , "pageNo=" + page , response.request.url)
            yield response.follow(next_page, self.parse_pages)
