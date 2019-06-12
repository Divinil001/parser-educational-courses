import scrapy
#from urllib.parse import urljoin
from scrapy.utils.markup import remove_tags

class CataloniaSpider(scrapy.Spider):
    name = "catalonia"
    start_urls = [
        'https://www.fib.upc.edu/en/mobility/incoming/how-apply',
    ]

    def get_courses(self, ul , next , links, semester):

        # разделители
        d1 = "'s degree in"
        d2 = '-'
        d3 = ' '
        d4 = 'Exchange period ('

        semester =  remove_tags(semester.extract()).split(d4)
        #e = semester.sub(d4,'',semester)
        courses = []

        i = 0
        for x , y , z  in zip( ul.css('li'), next.css('li'), links):
            degree, rest = remove_tags(x.extract()).split(d1)
            name, id = rest.split(d2)

            buffer, credits = remove_tags(y.extract()).split(d2)
            credits = credits.strip()
            credits_num, credits_type = credits.split(d3)

            #1. University_title_full - string
            university_title = "Universitat Politechnica de Catalunya Barcelonatech.FIB Facultat d'Informatica de Barcelona."

            courses.append({
                'university_title' : university_title, # 1. University_title_full - string
                'id': id.strip(), # 2. Course_local_id - string
                'name': name.strip(), # 3. Course_title_full - string
                'degree': degree.strip(), # 4. Course_level - string
                'semester': semester, # 5. Course_semester - string
                'credits_num' : credits_num.strip(), # 6.Course_credits - integer
                'credits_type' : credits_type.strip(),# 7. Course_credits_type
                'links' : links[i], #8. Course_link_descrip - string
            })
            i = i+1

        return courses

    def parse(self, response): # 4 пункт парсинга
        alerts = response.css('.alert')
        ul = alerts[3].css('ul ul')[0] # для парсинга 2,3,4 пунктов
        next = alerts[3].css('ul ul')[2] # для парсинга 6, 7 пунктов

        links = next.css('a::attr(href)').extract() #
        semester = alerts[1].css('ul li')[2] # для 8 пункта

        courses = self.get_courses(ul , next , links, semester)
        print(courses)
        #print(links)

        #print([remove_tags(x) for x in semester.getall()])

        #print(urls.getall()
