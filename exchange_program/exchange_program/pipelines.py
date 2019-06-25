<<<<<<< HEAD
import json
=======

import csv
>>>>>>> 1517fcca455d0ce84c5f207c45aae27c7ed3cb1d

class CataloniaPipeline(object):

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        for course in spider.courses:
            try:
<<<<<<< HEAD
                #combine results to one set
                course['course_credits'] = spider.course_credits[course['course_link_descrip']]
            except:
                pass

        with open('dataset.json', 'w') as file: # save data to file
            json.dump(spider.courses, file)
=======
                course['course_credits'] = spider.course_credits[course['Course_link_descrip']]
            except:
                pass
        with open('dataset.csv', 'w') as file:
            fieldnames = ['university_title_full' , 'course_local_id', 'course_title_full','course_level', 'course_semester', 'course_credits' , 'course_credits_type', 'course_link_descrip' ]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for course in spider.courses:
                writer.writerow(course)
>>>>>>> 1517fcca455d0ce84c5f207c45aae27c7ed3cb1d

    def process_item(self, item, spider):
        return item
