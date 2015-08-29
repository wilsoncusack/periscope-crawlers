# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#!/usr/bin/python
import psycopg2
#import os

from scrapy.exceptions import DropItem

class CrawlersPipeline(object):

	# def open_spider(self, spider):
	# 	# can call get env database_url for this?
	# 	conn = psycopg2.connect("postgres://dildnnrtxzwbhd:0_PSHQh5konS1dKcY8CIyCplBK@ec2-54-235-80-55.compute-1.amazonaws.com:5432/d6h2dosmoqipg1")
	# 	cursor = conn.cursor()

	# called when program starts
	# sets up db connection
	# could use open_spider, but they used init in one of their examples
	def __init__(self):
		#self.conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
		self.conn = psycopg2.connect("postgres://dildnnrtxzwbhd:0_PSHQh5konS1dKcY8CIyCplBK@ec2-54-235-80-55.compute-1.amazonaws.com:5432/d6h2dosmoqipg1")
		self.cursor = self.conn.cursor()


	# called on every item that is processed
	# if the article isn't already in the db, it adds it
	# otherwise, it drops the item
	def process_item(self, item, spider):
		# conn = psycopg2.connect("postgres://dildnnrtxzwbhd:0_PSHQh5konS1dKcY8CIyCplBK@ec2-54-235-80-55.compute-1.amazonaws.com:5432/d6h2dosmoqipg1")
		# cursor = conn.cursor()
		self.cursor.execute("SELECT COUNT(*) FROM articles WHERE title = %s AND author = %s AND publication = %s", 
			(item['title'], item['author'], item['publication'],))
		# grab the first thing from the SQL query
		count = self.cursor.fetchone()[0]
		if count > 0:
			raise DropItem("Dropping article, already in database")
		else:
			#note, dateadded will default to current date, datewritten need to be configured with item['date']
			SQL = "INSERT INTO articles (title, link, author, body, publication, political_score, pos_neg_score, publication_description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)" 
			data = (item['title'], item['link'], item['author'], item['body'], 
				item['publication'], item['politicalScore'], item['posNegScore'], item['description'],)
			self.cursor.execute(SQL, data)
	    	return item

	# called when the spider is closed
	# terminates db connection and commits changes
	def close_spider(self, spider):
		self.conn.commit()
		self.cursor.close()