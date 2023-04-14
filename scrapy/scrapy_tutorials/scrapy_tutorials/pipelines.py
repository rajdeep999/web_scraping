# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


import pymongo
class MongodbPipeline:
    collection_name = 'worldometer'
    def open_spider(self, spider):
        self.client = pymongo.MongoClient("Please add your db url")
        self.db = self.client['My_Database']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(item)
        return item


class SQLitedbPipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect('worldometer.db')
        self.c = self.connection.cursor()
        try:
            self.c.execute('''
                CREATE TABLE worldometer (
                country TEXT,
                year TEXT,
                population TEXT
                )
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.c.execute('''
         INSERT INTO worldometer (country,year,population) VALUES (?,?,?)
        ''', (
            item.get('country'),
            item.get('year'),
            item.get('population')
        ))
        self.connection.commit()
        return item
