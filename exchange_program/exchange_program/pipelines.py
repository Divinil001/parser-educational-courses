
import csv

class CataloniaPipeline(object):

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        for course in spider.courses:
            try:
                course['course_credits'] = spider.course_credits[course['Course_link_descrip']]
            except:
                pass
        with open('dataset.csv', 'w') as file:
            fieldnames = ['university_title_full' , 'course_local_id', 'course_title_full','course_level', 'course_semester', 'course_credits' , 'course_credits_type', 'course_link_descrip' ]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for course in spider.courses:
                writer.writerow(course)

    def process_item(self, item, spider):
        return item
