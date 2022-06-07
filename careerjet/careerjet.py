import scrapy
import mysql
from mysql.connector import Error
from urllib.parse import unquote
import time
from timeit import default_timer as timer
from scrapy.crawler import CrawlerProcess

start = timer()
class ifexist():
    def ifexist(data):
        try:
            connection = mysql.connector.connect(host='db',                                               
                                                 database='crawlerdb',
                                                 user='root',
                                                 password='mypass123')
            sql_insert_query = "SELECT `job_url` FROM `store_all` where `job_url` like '%" + str(data) + "%'"
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


class spider_careerjet(scrapy.Spider):
    name = "careerjet"
    allowed_domains = ['www.careerjet.gr']
    start_urls = ['https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=1&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=2&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=3&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=4&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=5&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=6&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=7&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=8&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=9&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=10&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=11&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=12&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=13&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=14&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=15&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=16&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=17&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=18&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=19&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=20&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=21&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=22&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=23&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=24&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=25&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=26&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=27&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=28&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=29&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=30&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=31&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=32&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=33&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=34&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=35&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=36&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=37&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=38&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=39&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=40&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=41&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=42&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=43&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=44&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=45&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=46&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=47&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=48&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=49&sort=date',
                  'https://www.careerjet.gr/%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B7%CE%BD-%CE%B5%CE%BB%CE%BB%CE%B1%CE%B4%CE%B1-105779.html?p=50&sort=date']
    def __init__(self):
        # this here connect to database and q all url that have been crawled and store it into records.
        count_new = 0
        count_exist = 0
        self.count_new = count_new
        self.count_exist = count_exist
        try:
            self.connection = mysql.connector.connect(host='db',
                                                 database='crawlerdb',
                                                 user='root',
                                                 password='mypass123')
            cursor = self.connection.cursor(prepared=True)
            sql_select_Query = "SELECT job_url FROM store_all"
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql_select_Query)
            records = self.cursor.fetchall()  # this is dangerous should be replaced!!!!
            self.records = records
        except mysql.connector.Error as error:
            self.connection.rollback()
            print("Failed to connect {}".format(error))

    def parse(self, response):
        job_url = response.url
        job_url = unquote(job_url)
        isExists = response.xpath("//h2//a/@href").extract()
        for i in range(len(isExists)):
            url = 'https://www.careerjet.gr' + str(isExists[i])
            url = unquote(url)
            yield response.follow(url, callback=self.parser_next)

    def parser_next(self,response):
        job_url = response.url
        job_url = unquote(job_url)
        url_from_database = ifexist.ifexist(job_url)
        print(url_from_database)
        if len(url_from_database) > 1:
            print(url_from_database)

            job_html = response.body
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            try:
                self.cursor = self.connection.cursor(prepared=True)
                sql_insert_query = """ INSERT INTO 
                                                            `store_all`(
                                                             `job_url`,
                                                             `job_description`,
                                                             `Date`
                                                             )VALUES (%s,%s,%s)"""
                insert_tuple = (job_url, job_html, timestamp)
                self.cursor.execute(sql_insert_query, insert_tuple)
                self.connection.commit()
                # print("Record inserted successfully into table")
                self.count_new = self.count_new + 1
            except mysql.connector.Error as error:
                self.connection.rollback()
                print("Failed to insert into MySQL table {}".format(error))
            end = timer()
            print("Careerjet : Time cpu run:", end - start, ",", "New entries :", self.count_new, "& job url", job_url,
                  ",",
                  "Exist item's", self.count_exist)
        else:
            self.count_new = self.count_new + 1
            print("exist")
process = CrawlerProcess(settings={
    "FEEDS": {
        "items.json": {"format": "json"},
    },
})
process.crawl(spider_careerjet)
process.start()  # the script will block here until the crawling is finished