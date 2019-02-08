SearchCrawl

The techcrawl repository contains a scrapy webcrawler, a program to convert website links into a graph and view various graph metrics and a mongoDB database and collection to store webcrawler data. This collection allows the utilization
of search queries of the data. This can be used as a simple search engine. 

Has only been tested on Ubuntu 18.04

To start, just clone the repository and cd into the SearchCrawl/techcrawl/techcrawl/ directory where all of the files are located.
Then chmod 755 prereq.sh and ./prereq.sh.
Prereq.sh contains terminal commands to install the needed dependencies for the project to work.

Once everything has been installed, simply type ./run.sh.

This will initiate the crawler once you have specified an output file and the url to start from.
The crawler will grab links from the pages it encounters, and then crawl all of them for 
title of the page, base_url, body and of course links.

Once done you will be prompted to use the graph program or the index program. The graph program can
produce various graph metrics of the websites and links plus draw a simple visualization of the graph.
The index program will let you search the crawled data for the terms you supply. It will generate a score
for each page and then return the title and website url.

You dont have to use run.sh. You can run the programs on the command line.  


Some examples websites to try to see the difference in metrics:

https://www.theguardian.com/us/technology
https://www.slashdot.org
https://www.linuxinsider.com
