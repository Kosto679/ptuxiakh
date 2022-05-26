import scrapy
import time
from urllib.parse import unquote
from timeit import default_timer as timer
start = timer()
import mysql
import mysql.connector 
from mysql.connector import Error
from scrapy.crawler import CrawlerProcess

class kariera(scrapy.Spider):
    print('Begin')
    name = "kariera"
    allowed_domains = ['www.kariera.gr']
    start_urls = [
        'https://www.kariera.gr/%CE%B8%CE%AD%CF%83%CE%B5%CE%B9%CF%82-%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%AF%CE%B1%CF%82?sort=date']
    conn = mysql.connector.connect(host="localhost",
                                   port="13306",
                                   user="root",
                                   database="crawlerdb",
                                   password="mypass123")
    cursor = conn.cursor()
    # initializing crawler variables
    def __init__(self):
        # this here connect to database and q all url that have been crawled and store it into records.
        count_new = 0
        count_exist = 0
        kariera_insert_count = 0
        self.count_new = count_new
        self.count_exist = count_exist
        self.sql = "SELECT job_url FROM store_all"
        self.kariera_insert_count= kariera_insert_count
        #self.records = self.database.kariera_list(self.sql)


        # Crawl each category list of job links
    def parse(self, response):
        print('Starting the parser')
        nextpage = []
        isExists = response.xpath("//a[@class='btn-arrow']").extract_first(default='not-found')
        # this part of the code checks if the arrow for next page exist if not exsist crawling only this page and goes to the next category
        if (isExists == 'not-found'):
            for job_url in response.xpath("//div[@class='job']//a[@class='job-title']/@href").extract():
                job_url = unquote(job_url)  # decoding url
                job_url_full = 'https://www.kariera.gr' + str(job_url)
                print(job_url_full)
                self.conn.cursor(prepared=True)
                self.cursor.execute('Select job_url from store_all where job_url like "' + str(job_url_full) + '"')
                select_query = self.cursor.fetchall()
                if len(select_query) == 0:
                    yield scrapy.Request(job_url_full, callback=self.parse_page)
                else:
                    self.count_exist = self.count_exist + 1
        else:
            nextpage = response.xpath("//div[@class='bloc clear center']//a[@class='btn-arrow']/@href").extract()
            isExists2 = response.xpath(
                "//div[@class='bloc clear center']//a[@class='btn-arrow']/i[@class='fa fa-chevron-right show-mobile']").extract_first(
                default='not-found')

            if (isExists2 != 'not-found'):
                url = 'https://www.kariera.gr' + str(nextpage[-1])
                url = unquote(url)

                next_page = response.urljoin(url)
                # If next_page have value
                for job_url in response.xpath("//div[@class='job']//a[@class='job-title']/@href").extract():
                    job_url_full = 'https://www.kariera.gr' + str(job_url)
                    job_url_full = unquote(job_url_full)
                    self.conn.cursor(prepared=True)
                    self.cursor.execute("Select job_url from store_all where job_url like '" + str(job_url_full) + "'")
                    select_query = self.cursor.fetchall()
                    if len(select_query) == 0:
                        yield scrapy.Request(job_url_full, callback=self.parse_page)
                    else:
                        self.count_exist = self.count_exist + 1

            if next_page:
                    request = scrapy.Request(url, callback=self.parse, dont_filter=True)
                    yield request

    def parse_page(self, response):
        print('Starting the parser_page')
        # this is the list with the job positions from the database
        job_url = response.url
        job_url = unquote(job_url)
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        job_html = response.body.decode(response.encoding)
        try:
                self.cursor = self.conn.cursor(prepared=True)
                sql_insert_query = """ INSERT INTO 
                                                            `store_all`(
                                                             `job_url`,
                                                             `job_description`,
                                                             `Date`
                                                             )VALUES (%s,%s,%s)"""
                insert_tuple = (job_url, job_html, timestamp)
                self.cursor.execute(sql_insert_query, insert_tuple)
                self.conn.commit()
                # print("Record inserted successfully into table")
                self.kariera_insert_count += 1
                end = timer()
                print("Kariera : Time cpu run:", end - start, ",", "New entries :", self.kariera_insert_count, "& job url", job_url, ",","Exist item's", self.count_exist)
        except mysql.connector.Error as error:
                self.connection.rollback()
                print("Failed to insert into MySQL table {}".format(error))
              
process = CrawlerProcess(settings={
    "FEEDS": {
        "items.json": {"format": "json"},
    },
})
process.crawl(kariera)
process.start()  # the script will block here until the crawling is finished