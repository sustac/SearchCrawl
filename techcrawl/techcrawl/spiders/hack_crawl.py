# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlparse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

x = 0

class HackCrawlSpider(scrapy.Spider):
    global stop
    name = 'hack_crawl'

    print("\n")
    url = input("Enter starting page(including https:// or http://): ")
    print("\n")
    
    start_urls = [url]

    def parse(self, response):
        global x
        links = []
        
        if response.xpath('//a/@href').extract() is not None:
            for link in response.xpath('//a/@href').extract():
                a = urlparse(link)
                link = "://".join([a.scheme, a.netloc])
                b = urlparse(response.url)
                b = "://".join([b.scheme, b.netloc])
                base_url = response.xpath('//title/text()').extract_first()
                if(link.startswith('https://') or link.startswith('http://')):
                    if (x < 15):
                        if(link not in links):
                            links.append(link)
                    yield {
                            'title' : base_url,
                            'url' : b,
                            'link': link
                        }
            x += 1
        
        else:
            pass
        
        for y in range(len(links)):
            next_page = links[y]
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)
        


