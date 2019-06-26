import json

class CataloniaPipeline(object):

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        finished_courses = []
        for course in spider.courses:
            try:
                #combine results to one set
                course['course_credits'] = spider.course_credits[course['course_link_descrip']]

                finished_courses.append({
                    'university_title_full': course['university_title_full'],  # 1. University_title_full - string
                    'course_local_id': course['course_local_id'],  # 2. Course_local_id - string
                    'course_title_full': course['course_title_full'],  # 3. Course_title_full - string
                    'course_level': course['course_level'],  # 4. Course_level - string
                    'course_semester': course['course_semester'],  # 5. Course_semester - string
                    'course_credits': spider.course_credits[course['course_link_descrip']],
                    'course_credits_type': course['course_credits_type'],  # 7. Course_credits_type
                    'course_link_descrip': course['course_link_descrip'],  # 8. Course_link_descrip - string
                    'course_track': course['course_track'],
                })
            except:
                pass
        # создадим словарь с нужным порядком ключей


        with open('dataset.json', 'w') as file: # save data to file
            json.dump(finished_courses, file)

    def process_item(self, item, spider):
        return item
