# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from .items import Article
from datetime import datetime
from string import whitespace


class LibrarianWikiPipeline:
    def process_item(self, item, spider):
        if isinstance(item, Article):
            date_str = item['last_updated']
            date_str = date_str.replace('This page was last edited on ', '')
            date_str = date_str.strip()
            date_str = datetime.strptime(date_str, '%d %B %Y, at %H:%M')
            date_str = date_str.strftime('%Y-%m-%d %H:%M:%S')
            item['last_updated'] = date_str

            texts = item['text']
            texts = [line for line in texts if line not in whitespace]
            item['text'] = ''.join(texts)

        return item