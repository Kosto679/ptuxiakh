import scrapy
import scrapy.utils
from mysql.connector import Error
import time
import mysql
from timeit import default_timer as timer
start = timer()
from scrapy.crawler import CrawlerProcess
class ifexist():
    def ifexist(data):
        try:
            connection = mysql.connector.connect(host='snf-876565.vm.okeanos.grnet.gr',
                                                 database='crawlerdb',
                                                 user='root',
                                                 password='10dm1@b0320')
            cursor = connection.cursor(prepared=True)
            sql_insert_query = "SELECT job_url FROM `store_all` where `job_url` = '" + str(data) + "'"
            cursor = connection.cursor()
            cursor.execute(sql_insert_query)
            try:
                result = cursor.fetchall()
                connection.commit()
            except:
                pass
            return result
        except mysql.connector.Error as error:
            connection.rollback()
            print("Failed to insert into MySQL table {}".format(error))

class jooble(scrapy.Spider):
    name = "jooble"
    allowed_domains = ['gr.jooble.org/']
    start_urls = ['https://gr.jooble.org/SearchResult']


    def __init__(self):
        self.count =1
        self.count_new = 0
        self.count_exist =0
        try:
            self.connection = mysql.connector.connect(host="localhost",
                                   port="13306",
                                   user="root",
                                   database="crawlerdb",
                                   password="mypass123")
            sql_select_Query = "SELECT job_url FROM store_all"
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql_select_Query)
            records = self.cursor.fetchall()  # this is dangerous should be replaced!!!!
            self.records = records
        except mysql.connector.Error as error:
            self.connection.rollback()
            print("Failed to connect {}".format(error))
    def parse(self, response):
        all_the_jobs = response.xpath('//article[@class="_2caa5a _5d7c45"]//h2//a/@datahref').extract()
        for whatever in range(len(all_the_jobs)):
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}
            head, sep, tail = all_the_jobs[whatever].partition('?p=')
            time.sleep(3)
            res1 = any(head in sublist for sublist in self.records)
            if (res1 == True):
                self.count_exist = self.count_exist + 1
                print("url is already in the database")
            else:
                print("Not Found ,", head)
                yield scrapy.Request(head, callback=self.parse_job, dont_filter=True, headers=headers, cookies={'datadome': 'kMBtR9Kz1tt0sWhavR5y.ErER6xH4qnDyNR3GtS~oaAjdPHOrhyRcePNg~GFaXP5QoYW8XSjM6PbepCMFKLdtmFd-AkyJFyQp-LRuyzoIdeNH4jD6W0yLhLaepj3jtk'})

        try:
            if response.status == 200:
                next_page = 'https://gr.jooble.org/SearchResult?p=' + str(self.count)
                self.count += 1
                yield response.follow(next_page, callback=self.parse, dont_filter=True, headers=headers)
        except:
            pass

    def parse_job(self, response):
        time.sleep(2)

        # this is the list with the job positions from the database
        job_url = response.url
        #job_url = unquote(job_url)
        job_html = response.body
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        url_from_database = ifexist.ifexist(job_url)

        if len(url_from_database) < 1:
            try:
                sql_insert_query = """ INSERT INTO 
                                                                    `store_all`(
                                                                     `job_url`,
                                                                     `job_description`,
                                                                     `Date`
                                                                     )VALUES (%s,%s,%s)"""
                insert_tuple = (job_url, job_html, timestamp)
                self.cursor.execute(sql_insert_query, insert_tuple)
                self.connection.commit()
                self.count_new = self.count_new + 1
            except mysql.connector.Error as error:
                self.cursor.rollback()
                print("Failed to insert into MySQL table {}".format(error))
            end = timer()
            print("Jooble . Time cpu run:", end - start, ",", "New entries :", self.count_new, "& job url", job_url,
                  ",")

process = CrawlerProcess(settings={
    "FEEDS": {
        "items.json": {"format": "json"},
    },
})
process.crawl(jooble)
process.start()  # the script will block here until the crawling is finished

