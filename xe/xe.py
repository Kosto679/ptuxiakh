import scrapy
import mysql.connector
import time
from array import array
from scrapy.crawler import CrawlerProcess


class ifexist():
    def ifexist(data):
        try:
            connection = mysql.connector.connect(host='db',
                                                 database='crawlerdb',
                                                 user='root',
                                                 password='mypass123')
            cursor = connection.cursor(prepared=True)
            sql_insert_query = "SELECT job_url FROM `store_all` where `job_url` = '" + str(data) + "'"
            cursor = connection.cursor()
            cursor.execute(sql_insert_query)
            try:
                result = cursor.fetchall()
            except:
                pass
            return result
            connection.commit()
        except mysql.connector.Error as error:
            connection.rollback()
            print("Failed to insert into MySQL table {}".format(error))
class xe(scrapy.Spider):
    name = 'xe'
    page_number = 1
    start_urls = ['https://www.xe.gr/jobs/results']
    # mysql connection


    def __init__(self):
        self.count_new = 0
        self.exist = 0
        try:
            self.connection = mysql.connector.connect(host='db',
                                                      database='crawlerdb',
                                                      user='root',
                                                      password='mypass123')
            self.cursor = self.connection.cursor()

        except mysql.connector.Error as error:
            self.connection.rollback()
            print("Failed to connect {}".format(error))
    def parse(self, response):
        # find job path
        domain = 'https://www.xe.gr'
        page_posts= response.xpath("//div[@class='result-list-narrow-item-wrapper']//a/@href").extract()
        get_next_page = response.xpath("//li[@class='pagination-next']//a/@href").extract_first()
        for i in range(len(page_posts)):
            yield response.follow(page_posts[i], callback=self.parse_job)
        if len(get_next_page) is not None:
            yield response.follow(get_next_page, callback=self.parse)

    def parse_job(self, response):
        # parse information from job url
        # title = response.xpath('//span[@id="js_jobTitle"]/text()').extract_first()
        job_url = response.url
        job_html = response.body.decode(response.encoding)
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        job_html = str(job_html)
        url_from_database = ifexist.ifexist(job_url)
        if len(url_from_database) < 1:
            # mysql connection
            try:
                sql_insert_query = """INSERT INTO
                                                                       `store_all`(
                                                                       `job_url`,
                                                                       `job_description`,
                                                                       `Date`
                                                                       )VALUES (%s,%s,%s)"""
                insert_tuple = (job_url, job_html, timestamp)
                self.cursor.execute(sql_insert_query, insert_tuple)
                self.connection.commit()
                self.count_new = self.count_new + 1
                print("xe, New entries :", self.count_new, "& job url", job_url)
            except mysql.connector.Error as error:
                self.cursor.rollback()
                print("Failed to insert into MySQL table{}".format(error))
        else:
            self.exist = self.exist + 1

process = CrawlerProcess(settings={
    "FEEDS": {
        "items.json": {"format": "json"},
    },
})
process.crawl(xe) 
process.start() 