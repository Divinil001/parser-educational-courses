import json

class SeoulPipeline(object):

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):

        with open('dataset.json', 'w') as file: # save data to file
            json.dump(spider.courses, file)

    def process_item(self, item, spider):
        return item
