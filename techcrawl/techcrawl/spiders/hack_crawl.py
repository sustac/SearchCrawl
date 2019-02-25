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
    seed_urls = []
    

    #### Enter seed page and the output file to write links to, needed for makegraph and to calculate pagerank. Enter crawl depth.
    print("\n")
    url = ''
    while url != 'done':
        url = input("Enter initial starting page(s)(including https:// or http://)(enter done to stop): ")
        if url == 'done':
            url = 'done'
            print('\n')
        else:
            seed_urls.append(url)
        print("\n")
    
    files = [f for f in os.listdir(os.curdir) if os.path.isfile(f)]
    files = [f for f in files if f.endswith('.csv')]
    print('These are the csv files in current directory: ')
    [print(f) for f in files]
    print('\n')
    
    file_csv = input("Enter csv output file name(use existing or create one): ")
    print("\n")
    depth = input("Enter crawl depth: ")
    depth = int(depth)
    print("\n")
    
    start_urls = seed_urls

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
                    
                    #limit crawl and only add link once
                    if (x < depth):
                        if(link not in links):
                            links.append(link)
                    
                    #will only write url to collection once
                    if(response.url not in url_list):
                        url_list.append(response.url)
                        header = response.xpath('//h1/text()').extract()
                        header += response.xpath('//h2/text()').extract()
                        header += response.xpath('//h3/text()').extract()
                        item = TechcrawlItem()
                        item['title'] = response.xpath('//title/text()').extract_first()
                        item['url'] = response.url
                        item['body'] = response.xpath('//p/text()').extract()
                        item['headers'] = header
                        item['domain'] = url
                        item['pagerank'] = 0.0
                        item['score_added'] = int(0)
                        item['have_added'] = int(0)
                        yield item
                    
                    # doing best to stop duplicates in csv file
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
                  
        #links to follow in crawl
        for y in range(len(links)):
            next_page = links[y]
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)
        


