import json

class CataloniaPipeline(object):

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        for course in spider.courses:
            try:

                #combine results to one set
                course['course_credits'] = spider.course_credits[course['course_link_descrip']]
            except:
                pass

        with open('dataset.json', 'w') as file: # save data to file
            json.dump(spider.courses, file)

    def process_item(self, item, spider):
        return item
