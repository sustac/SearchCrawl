#!/bin/bash

while true
do
	echo -e "\n\nMake sure mongod is running in another terminal!!(sudo service mongod stop and then sudo mongod),\n"
	echo -e "Enter index to access mongoDB collection and run commands(need to run first to create collection/index!),\n"
	echo -e "Enter crawl to run web crawler and get data for mongodb collection,\n"
	echo -e "Enter graph for graph metric data,\n"
	read -p	"Enter quit to exit:  " answer

	case $answer in

		[crawl]* ) scrapy crawl hack_crawl
			   echo "--------------------------------------------------------------------------------------------------"
			   ;;

		[graph]* ) python3 makegraph.py
			   echo "--------------------------------------------------------------------------------------------------"
			   ;;
			
		[index]* ) python3 dbquery.py
			   echo "--------------------------------------------------------------------------------------------------"
			   ;;
	
		[quit]*  ) exit;;

		* ) echo -e "thats not an answer \n";;
	esac
done
	

