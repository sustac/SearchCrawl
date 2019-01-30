SearchCrawl

The techcrawl repository contains a scrapy webcrawler, a program to convert website links into a graph and view various graph metrics and a simple in-memory inverted index to search for terms.

Has only been tested on Ubuntu 18.04

To start, just clone the repository and cd into the SearchCrawl/techcrawl/techcrawl/ directory where all of the files are located.
Then chmod 755 prereq.sh and ./prereq.sh.
Prereq.sh contains terminal commands to install the needed dependencies for the project to work.

Once everything has been installed, simply type ./run.sh.

This will initiate the crawler once you have specified an output file and the url to start from.
The crawler will grab links from the first 15 pages it encounters, and then crawl all of them for 
title of the page, base_url and of course links. I have set it to 15 just to limit the run time of
the crawler.

Once done you will be prompted to use the graph program or the index program. The graph program can
produce various graph metrics of the websites and links plus draw a simple visualization of the graph.
The index program will let you search for whatever terms you like and will return all results. You can
also get the frequency of whatever term you supply. 


Some examples websites to try to see the difference in metrics:

https://www.theguardian.com/us/technology
https://www.slashdot.org
https://www.linuxinsider.com
