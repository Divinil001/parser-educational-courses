import scrapy


class LjubljanaSpider(scrapy.Spider):
    name = 'ljubljana'
    allowed_domains = ['fri.uni-lj.si']
    start_urls = ['https://fri.uni-lj.si/en/incoming-students']

    def parse(self, response):
        courses = response.xpath('//div[@class="body-page-rows"]/table/tbody/tr')[0]
        data = [x for x in courses.xpath("//td//text()").getall() if x != '\r\n\t\t\t']
        for x in range(len(data)):
            data[x] = data[x].replace("\xa0", " ")
        print(len(data))
        index = 0
       
        course_level = None

        
        while index < len(data):
            if data[index] == ' Code' or data[index] == 'Code':
                if data[(index)+1] != "Course":
                    course_level = data[(index)+1]
                index += 1
            course = dict()
            course['University_title_full'] = 'University of Ljubljana'
            course['Course_local_id'] = data[index]
            course['Course_title_full'] = data[(index)+1]
            course['Course_level'] = course_level
            course['Course_semester'] = data[(index)+2]
            course['Course_credits'] = data[(index)+3]
            course['Course_credits_type'] = 'ECTS'
            # TODO Add link to the course itself
            # Response: there's no link
            index += 6
            yield course
