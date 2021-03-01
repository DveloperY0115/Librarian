# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import NotConfigured

import htmlmin
import json
from datetime import datetime
from .items import RawWebContent
from .db_manager import DatabaseManager


MEDIUMTEXT_MAX_LEN = 16777215


class HTMLPipeline:
    def process_item(self, item, spider):
        """
        Process HTTP response acquired from web servers.

        This pipeline does barely nothing, except compressing the HTML file to
        fit it into the database. If the document is too long, it will leave HTML field empty.

        Args:
            item: Scrapy item instance
            spider: Scrapy spider which uses this pipeline

        Returns: Scrapy item instance, but whose HTML data is compressed or None.

        """
        compressed_html = htmlmin.minify(item['html'])
        if len(compressed_html) > MEDIUMTEXT_MAX_LEN:
            # if the document is too long
            return None
        else:
            item['html'] = compressed_html
        return item


class DatabasePipeline:
    def __init__(self, db, user, passwd, host):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host
        self.db_manager = None

    def open_spider(self, spider):
        """
        Create connection to database(s) when a spider starts.

        Args:
            spider: Scrapy spider which uses this pipeline

        Returns: Nothing
        """
        self.db_manager = DatabaseManager(self.db, self.user, self.passwd, self.host)

    def close_spider(self, spider):
        """
        Close connection to database(s) when a spider stops.

        Args:
            spider: Scrapy spider which uses this pipeline

        Returns: Nothing
        """
        self.db_manager.close_connection()

    def process_item(self, item, spider):
        """
        Register the given item to the database(s) bound to the spider using this pipeline.

        Args:
            item: Scrapy item instance
            spider: Scrapy spider which uses this pipeline

        Returns: Scrapy item instance, or None if there was a problem
        """
        if item is not None:
            self.db_manager.register_item(item, 'pages', overwrite=False)
        return item

    @classmethod
    def from_crawler(cls, crawler):
        """
        Configure a pipeline using the settings held by a spider.

        Args:
            crawler: Scrapy crawler

        Returns: DatabasePipeline instance configured for the caller (crawler or spider)
        """
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
