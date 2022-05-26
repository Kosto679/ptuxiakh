import scrapy
import mysql
from mysql.connector import Error
from urllib.parse import unquote
from timeit import default_timer as timer
import requests
import json
from scrapy.crawler import CrawlerProcess

start = timer()
import time
class ajax():
    API_url= 'https://www.skywalker.gr/elGR/aggelia-ajax/euresi-aggelion-ergasias'
    scraped_stores = []

    def get_stores_info(self,page):
        headers = {'User-Agent': 'Mozilla/5.0'}
        data= {'perPage': '400','page':'1'}
        response = requests.post(self.API_url,headers=headers,data=data)
        #print(response.json())
        jsondata = json.loads(response.content.decode())
        #print(json.dumps(jsondata, indent = 4, sort_keys=True))
        linklist = []
        for i in range(0,400):
            link = 'https://www.skywalker.gr/elGR/aggelia/ergasias/'+str(json.dumps(jsondata["Items"][i]["Name"]).replace('"',''))+"/"+str(json.dumps(jsondata["Items"][i]["Id"]).replace('"',''))
            print(link)
            linklist.append(link)
        return  linklist

class ifexist():
    def ifexist(data):
        try:
            connection = mysql.connector.connect(host="localhost",
                                   port="13306",
                                   user="root",
                                   database="crawlerdb",
                                   password="mypass123")
            cursor = connection.cursor(prepared=True)
            
            sql_insert_query = "SELECT `job_url` FROM `store_all` where `job_url` = '" + str(data) + "'"
            cursor = connection.cursor()
            cursor.execute(sql_insert_query)
            result = cursor.fetchall()
            return result
            connection.commit()
        except mysql.connector.Error as error:
            connection.rollback()
            print("Failed to insert into MySQL table {}".format(error))



class spider_skywalker(scrapy.Spider):
    def __init__(self):
        # this here connect to database and q all url that have been crawled and store it into records.
        count_new = 0
        count_exist = 0
        self.count_new = count_new
        self.count_exist = count_exist
        try:
            self.connection = mysql.connector.connect(host="localhost",
                                   port="13306",
                                   user="root",
                                   database="crawlerdb",
                                   password="mypass123")
            self.cursor = self.connection.cursor(prepared=True)
            sql_select_Query = "SELECT job_url FROM store_all"
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql_select_Query)
            records = self.cursor.fetchall()  # this is dangerous should be replaced!!!!
            self.records = records
        except mysql.connector.Error as error:
            self.connection.rollback()
            print("Failed to connect {}".format(error))
    p = ajax()
    domain = ['https://www.skywalker.gr']
    linklist = p.get_stores_info(domain)
    name = "skywalker"
    allowed_domains = "www.skywalker.gr"
    start_urls = linklist

    # Crawl each category list of job links
    def parse(self, response):
        job_url = response.url
        job_url = unquote(job_url)
        url_from_database = ifexist.ifexist(job_url)
        if len(url_from_database) < 1:
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
            print("skywalker : Time cpu run:", end - start, ",", "New entries :", self.count_new, "& job url", job_url,
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
process.crawl(spider_skywalker)
process.start()  # the script will block here until the crawling is finished
