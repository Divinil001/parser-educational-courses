import json

class SapienzaPipeline(object):

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        finished_courses = []
        for course in spider.courses:
            for info in spider.addition_info:
                try:
                    #combine results to one set
                    if course['course_link_descrip'] == info['course_link_descrip']:
                        finished_courses.append({
                            'university_title_full': course['university_title_full'],
                            'course_local_id': info['course_local_id'],
                            'course_title_full': info['course_title_full'],
                            'course_level': course['course_level'],
                            'course_semester': info['course_semester'],
                            'course_credits': info['course_credits'],
                            'course_credits_type': course['course_credits_type'],
                            'course_link_descrip': course['course_link_descrip'],
                            'course_track': course['course_track'],
                        })
                except:
                    pass

        with open('dataset.json', 'w') as file: # save data to file
            json.dump(finished_courses, file)

    def process_item(self, item, spider):
        return item
