
from scrapy.crawler import CrawlerProcess
import scrapy
import mysql
from mysql.connector import Error
from urllib.parse import unquote
from timeit import default_timer as timer

start = timer()
import time


class indeedgr(scrapy.Spider):
    name = "indeed"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'
    allowed_domains = ['gr.indeed.com']
    start_urls = ['https://gr.indeed.com/jobs?l=%CE%95%CE%BB%CE%BB%CE%AC%CE%B4%CE%B1&radius=100&ts=1565553176523&pts=1564835113484&rq=1&fromage=last&vjk=e8d2bf821e7322c1']

    # initializing crawler variables
    def __init__(self):
        # this here connect to database and q all url that have been crawled and store it into records.
        count_new = 0
        count_exist = 0
        self.count_new = count_new
        self.count_exist = count_exist
        self.runonce = 0
        self.i = 0

    # Crawl each category list of job links
    def parse(self, response):
        job_html = response.body
        #isExists = response.xpath("//div[@class='pagination']//a/@href").extract()
        isExists = response.xpath("//ul[@class='pagination-list']").extract()
        url = "https://gr.indeed.com"
        search = "/jobs?q=&l=Ελλάδα&radius=100&fromage=last&start="
        print(isExists)
        my_list = isExists[0]

        if self.i <= 40:
            self.i = self.i + 10
            url_fin = url + search + str(self.i)
            job_content = response.xpath("//a[@class='jcs-JobTitle']/@href").extract()
            for con in range(len(job_content)):
                urlnext = url + job_content[con]
                yield response.follow(urlnext, callback=self.parse_page)
            next_page = response.urljoin(url_fin)
            if next_page:
                request = scrapy.Request(url_fin, callback=self.parse, dont_filter=True)
                yield request
        else:
            try:
                url_fin = url + isExists[5]
                job_content = response.xpath("//a[@class='jcs-JobTitle']/@href").extract()
                for con in range(len(job_content)):
                    urlnext = url + job_content[con]
                    yield response.follow(urlnext, callback=self.parse_page)
                next_page = response.urljoin(url_fin)
                if next_page:
                    request = scrapy.Request(url_fin, callback=self.parse, dont_filter=True)
                    yield request
            except IndexError:
                pass

    def parse_page(self, response):
        # this is the list with the job positions from the database
        job_url = response.url
        job_url = unquote(job_url)
        job_html = response.body
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        try:
            connection = mysql.connector.connect(host='db',
                                                 database='crawlerdb',                                           
                                                 user='root',
                                                 password='mypass123')
            cursor = connection.cursor(prepared=True)
            c = connection.cursor()
            c.execute('SELECT job_url FROM store_all where job_url = "' + str(job_url) + '"')
           # c.execute("SELECT count(job_url) FROM store_all WHERE job_url LIKE %s ", ("%" + job_url + "%",))
            data = c.fetchall()
            if len(data) < 1:
                self.count_exist += 1
            else:
                try:
                    cursor = connection.cursor(prepared=True)
                    sql_insert_query = """ INSERT INTO 
                                                                                         `store_all`(
                                                                                          `job_url`,
                                                                                          `job_description`,
                                                                                          `Date`
                                                                                          )VALUES (%s,%s,%s)"""
                    insert_tuple = (job_url, job_html, timestamp)
                    result = cursor.execute(sql_insert_query, insert_tuple)
                    connection.commit()
                    # print("Record inserted successfully into table")
                    self.count_new = self.count_new + 1
                    end = timer()
                    print("Indeed: Time cpu run:", end - start, ",", "New entries :", self.count_new, "& job url",
                          job_url, ",", "Exist item's", self.count_exist, "pages crawled")
                except mysql.connector.Error as error:
                    connection.rollback()
                    print("Failed to insert into MySQL table {}".format(error))

        except mysql.connector.Error as error:
            connection.rollback()
            self.count_exist += 1
            print("Failed to insert into MySQL table {}".format(error))




process = CrawlerProcess(settings={
    "FEEDS": {
        "items.json": {"format": "json"},
    },
})
process.crawl(indeedgr)
process.start()  # the script will block here until the crawling is finished
