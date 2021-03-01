# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import NotConfigured

import json
from datetime import datetime
from .items import RawWebContent
from .db_manager import DatabaseManager


class Pipeline:
    def process_item(self, item, spider):

        return item


class DatabasePipeline:
    def __init__(self, db, user, passwd, host):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host
        self.db_manager = None

    def open_spider(self, spider):
        self.db_manager = DatabaseManager(self.db, self.user, self.passwd, self.host)

    def close_spider(self, spider):
        self.db_manager.close_connection()

    def process_item(self, item, spider):
        self.db_manager.register_item(item, 'pages', overwrite=False)
        return item

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict('WIKI_ARTICLE_DB_SETTINGS')
        if not db_settings:
            raise NotConfigured
        db = db_settings['db']
        user = db_settings['user']
        passwd = db_settings['passwd']
        host = db_settings['host']
        return cls(db, user, passwd, host)


class JsonWriterPipeline:
    def open_spider(self, spider):
        filename = 'items-{}'.format(spider.name) + '{}.jl'.format(datetime.now())
        self.file = open(filename, 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item
