# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import NotConfigured

import json
import pymysql
from datetime import datetime
from .items import Article


class LibrarianWikiPipeline:
    def process_item(self, item, spider):
        if isinstance(item, Article):
            date_str = item['last_updated']
            item['last_updated'] = process_last_updated(date_str)
            """
            texts = item['text']
            texts = [line for line in texts if line not in whitespace]
            item['text'] = ''.join(texts)
            """
        return item


class DatabasePipeline:
    def __init__(self, db, user, passwd, host):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host
        
    def open_spider(self, spider):
        self.conn = pymysql.connect(db=self.db,
                                    user=self.user, passwd=self.passwd,
                                    host=self.host,
                                    charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        sql = "INSERT INTO pages (title, url, content, last_updated) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql,
                            (
                                item.get("title"),
                                item.get("url"),
                                item.get("text"),
                                item.get("last_updated")
                            ))
        self.conn.commit()
        return item

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict('DB_SETTINGS')
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


"""
Helper functions for modifying data extracted from Wikipedia articles
"""


def process_last_updated(date_str):
    date_str = date_str.replace('This page was last edited on ', '')
    date_str = date_str.strip()
    date_str = datetime.strptime(date_str, '%d %B %Y, at %H:%M')
    date_str = date_str.strftime('%Y-%m-%d %H:%M:%S')
    return date_str
