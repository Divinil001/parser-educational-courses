import csv

class CataloniaPipeline(object):

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        for course in spider.courses:
            try:
                course['credits'] = spider.credits[course['link']]
            except:
                pass
        with open('dataset.csv', 'w') as file:
            fieldnames = ['university_title' , 'id', 'name','course_level', 'semester', 'credits' , 'credits_type', 'link' ]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for course in spider.courses:
                writer.writerow(course)

    def process_item(self, item, spider):
        return item
