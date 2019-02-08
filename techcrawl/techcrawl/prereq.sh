sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install -y mongodb-org
sudo apt install python3-scrapy
sudo apt-get install python3-tk
pip3 install pymongo
pip3 install mongoengine
pip3 install numpy
pip3 install networkx
pip3 install matplotlib
chmod 755 run.sh
sudo mkdir /data
sudo mkdir /data/db
sudo chmod 755 /data
