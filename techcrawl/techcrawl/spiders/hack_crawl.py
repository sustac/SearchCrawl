import scrapy
import csv
import re
import os
from urllib.parse import urlparse
from techcrawl.items import TechcrawlItem
from scrapy.linkextractors import LinkExtractor
#from scrapy.spiders import CrawlSpider, Rule

x = 0
file_csv = ''
depth = 0
duplicate = []

class HackCrawlSpider(scrapy.Spider):
    global stop
    global file_csv
    global depth
    name = 'hack_crawl'

    #### Enter seed page and the output file to write links to, needed for makegraph and to calculate pagerank. Enter crawl depth.
    print("\n")
    url = input("Enter starting page(including https:// or http://): ")
    print("\n")
    
    files = [f for f in os.listdir(os.curdir) if os.path.isfile(f)]
    print('These are the csv files in current directory: ')
    [print(f) for f in files if f.endswith('.csv')]
    print('\n')

    file_csv = input("Enter csv output file name: ")
    print("\n")
    depth = input("Enter crawl depth(1-20): ")
    depth = int(depth)
    print("\n")
    
    start_urls = [url]

    def parse(self, response):
        global x
        global file_csv
        global duplicate
        links = []
        webdata = []
        url_list = []
        

        if response.xpath('//a/@href').extract() is not None:
            for link in response.xpath('//a/@href').extract():
                a = urlparse(link)
                link = "://".join([a.scheme, a.netloc])
                b = urlparse(response.url)
                url = "://".join([b.scheme, b.netloc])
                url = re.sub('https://', '', url)
                url = re.sub('http://', '', url)
                url = re.sub('www.', '', url)
                if(link.startswith('https://') or link.startswith('http://')):
                    if (x < depth):
                        if(link not in links):
                            links.append(link)
                    if(response.url not in url_list):
                        url_list.append(response.url)
                        item = TechcrawlItem()
                        item['title'] = response.xpath('//title/text()').extract_first()
                        item['url'] = response.url
                        item['body'] = response.xpath('//p/text()').extract()
                        item['domain'] = url
                        item['pagerank'] = 0.0
                        item['score_added'] = int(0)
                        yield item
                    stopdupe = link + url
                    if(stopdupe not in duplicate):
                        duplicate.append(stopdupe)
                        webdata.append(url)
                        webdata.append(link)


                        with open(file_csv, 'a') as outfile:
                            wr = csv.writer(outfile, quoting=csv.QUOTE_ALL)
                            wr.writerow(webdata)

                        webdata = []
                                
            x += 1
        
        else:
            pass
                  
        for y in range(len(links)):
            next_page = links[y]
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)
        


