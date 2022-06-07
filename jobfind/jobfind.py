import scrapy
import mysql
from mysql.connector import Error
from timeit import default_timer as timer
from scrapy.crawler import CrawlerProcess

start = timer()
import time


class jobfind(scrapy.Spider):
    name = "jobfind"
    allowed_domains = ['www.jobfind.gr']
    start_urls = ['https://www.jobfind.gr/JobAds/all/']

    # initializing crawler variables
    def __init__(self):
        # this here connect to database and q all url that have been crawled and store it into records.
        count_new = 0
        count_exist = 0
        self.count_new = count_new
        self.count_exist = count_exist
        try:
            self.connection = mysql.connector.connect(host="db",
                                   user="root",
                                   database="crawlerdb",
                                   password="mypass123")
            sql_select_Query = "SELECT job_url FROM store_all "
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql_select_Query)
            records = self.cursor.fetchall()
            self.records = records
        except mysql.connector.Error as error:
            #self.connection.rollback()
            print("Failed to connect {}".format(error))

    # Crawl each category list of job links
    def parse(self, response):
        nextpage = []
        test = []
        next_page = response.xpath("//a[@class='btn btn-default gtnext']/@href").extract()
        total_pages = response.xpath("//a[@class='btn btn-default gtlast']/@href").extract()
        total_pages = total_pages[0]
        total_page_number=total_pages[-3:]
        # this part of the code checks if the arrow for next page exist if not exsist crawling only this page and goes to the next category
        # If next_page have value
        for i in range(1,int(total_page_number)):
            print("round" , i)
            url = 'https://www.jobfind.gr/JobAds/all/?pageid=' + str(i)
            #  url = unquote(url)
           # print("this is the next web page" , url)
            next_page = response.urljoin(url)
            for job_url in response.xpath("//div[@class='col-sm-8']//div[@class='titleph']//h3[@class='title']//a/@href").extract():
                job_url_full = 'https://www.jobfind.gr' + str(job_url)
                print(job_url_full)
                res1 = any(job_url_full in sublist for sublist in self.records)
                if (res1 == True):
                    self.count_exist = self.count_exist + 1
                    print("url is already in the database")
                else:
                    print("Not Found ,", job_url_full)
                    yield response.follow(job_url_full, callback=self.parse_page)

    def parse_page(self, response):
        # this is the list with the job positions from the database
        job_url = response.url
        #  job_url = unquote(job_url)
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
            result = self.cursor.execute(sql_insert_query, insert_tuple)
            self.connection.commit()
            # print("Record inserted successfully into table")
            self.count_new = self.count_new + 1
        except mysql.connector.Error as error:
            self.connection.rollback()
            print("Failed to insert into MySQL table {}".format(error))
        end = timer()
        print("JobFind . Time cpu run:", end - start, ",", "New entries :", self.count_new, "& job url", job_url, ",",
              "Exist item's", self.count_exist)
process = CrawlerProcess(settings={
    "FEEDS": {
        "items.json": {"format": "json"},
    },
})
process.crawl(jobfind)
process.start()  # the script will block here until the crawling is finished