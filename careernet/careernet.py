import scrapy
import re
import mysql.connector
import time
from scrapy.crawler import CrawlerProcess
class CarrernetSpider(scrapy.Spider):
    name = 'carrernet'
    page_number = 1
    start_urls = ['https://www.careernet.gr/aggelies']
    # mysql connection
    conn = mysql.connector.connect(host="db",                                  
                                   user="root",
                                   database="crawlerdb",
                                   password="mypass123")
    cursor = conn.cursor()

    def remove_html_tags(text):
        """Remove html tags from a string"""
        p = re.compile(r'<.*?>')
        data = p.sub('', text)
        data = data.strip()
        return data

    def parse(self, response):
        # find job path
        all_the_jobs = response.xpath('//article')
        # parse all jobs
        for job in all_the_jobs:
            job_url = job.xpath('.//header/a/@href').extract_first()
            if '/aggelia/' not in job_url:
                job_url = '/aggelia/' + job_url
            job_url_final = 'https://www.careernet.gr' + str(job_url)
            self.conn.cursor(prepared=True)
            self.cursor.execute("Select job_url from store_all where job_url like '"+str(job_url_final)+"'")
            select_query = self.cursor.fetchall()
            if len(select_query)  == 0:
                yield scrapy.Request(job_url_final, callback=self.parse_job)
        # go to next page
        next_page = 'https://www.careernet.gr/aggelies?page=' + str(CarrernetSpider.page_number)
        if CarrernetSpider.page_number <= 64:
            CarrernetSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)

    def parse_job(self, response):
        # parse information from job url
        title = response.xpath('//h1[@class="col-lg-11 col-md-11 col-sm-11 col-xs-12 aggelia-title"]').extract()
        job_url = response.url
        job_html = response.body.decode(response.encoding)
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        print(timestamp)
        print('Url:', job_url)
        title = CarrernetSpider.remove_html_tags(title[0])
        print('Title:', title)
        job_html = str(job_html)
        # mysql connection
        try:
            self.conn.cursor(prepared=True)
            sql_insert_query = """INSERT INTO
                                                    `store_all`(
                                                    `job_url`,
                                                    `job_description`,
                                                    `Date`
                                                    )VALUES (%s,%s,%s)"""
            insert_tuple = (job_url, job_html, timestamp)
            self.cursor.execute(sql_insert_query, insert_tuple)
            self.conn.commit()
        except mysql.connector.Error as error:
            self.conn.rollback()
            print("Failed to insert into MySQL table{}".format(error))



process = CrawlerProcess(settings={
    "FEEDS": {
        "items.json": {"format": "json"},
    },
})
process.crawl(CarrernetSpider)
process.start() # the script will block here until the crawling is finished
# C:\Users\spyrntou\AppData\Local\Programs\Python\Python38\Scripts\scrapy crawl skywalker    terminal run
