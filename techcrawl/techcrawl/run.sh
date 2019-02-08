#!/bin/bash


python3 dbquery.py

echo -e "\n--------------------------------------------------------------------------------------------------"
echo -e "\nThe first command will run the web crawler and dump the data to mongoDB collection and csv file for graph program.\n"

scrapy crawl hack_crawl

echo -e "\n--------------------------------------------------------------------------------------------------"
echo -e "\nIf you want to use the draw command in the graph program the number of nodes cant be to high
      or the image wont load, enter info in graph program to see how big the graph is. \n"

while true
do
	echo -e "Enter index to access mongoDB collection and run commands,\n"
	echo -e "Enter graph for graph metric data,\n"
	read -p	"Enter quit to exit:  " answer

	case $answer in

		[graph]* ) python3 makegraph.py
			   echo "---------------------------------------------------------------------------------------------"
	 		   break;;
			
		[index]* ) python3 dbquery.py
			   echo "----------------------------------------------------------------------------------------------"
			   break;;
	
		[quit]*  ) exit;;

		* ) echo -e "thats not an answer \n";;
	esac
done
	

