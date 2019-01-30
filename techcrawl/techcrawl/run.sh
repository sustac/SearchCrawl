#!/bin/bash

echo -e "\nthe first command will run the web crawler and dump the data into a json file \n"

echo -e "the 2 other programs will use the json file to access the data. \n"


read -p "Enter the name of the output file from crawl(has to be .json): " output


scrapy crawl hack_crawl -o $output 

echo -e "\nIf you want to use the draw command in the graph program the number of nodes cant be to high"
echo -e  "or the image wont load, enter info in graph program to see how big the graph is. \n"

while true
do
	echo -e "Enter graph to see graph metrics on crawl data"
	echo -e "enter index to search for terms in data"
	read -p "enter quit to exit:  " answer
	echo -e "\n"

	case $answer in

		[graph]* ) python3 makegraph.py;;
			  
			
		[index]* ) python3 invertedindex.py;;
			 
	
		[quit]*  ) exit;;

		* ) echo -e "thats not an answer \n";;
	esac
done
	

