# PaperCrawler
Input: a json file containing "paper title","author",...
Output: download all the public paper with corresponding titles in json file from Internet

Preparation: install pip, scrapy, ijson, redis-server.
how to install pip: 
     for mac user: change to desired folder, and enter command: curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py --> python3 get-pip.py
     for windows user: directly download get-pip.py from https://bootstrap.pypa.io/get-pip.py --> python3 get-pip.py

how to install all the libraries using pip3 command
	pip3 install -r requirements.txt

how to install redis-server:
	1. Go to the official website of redis https://redis.io/download, Select the stable version
	2. Unzip and Put it on/usr/local/
	3. cd /usr/local/redis-6.0.4/
	4. sudo make test
how to install scraoy:
     change to the desired folder --> pip install scrapy
     
How to use:
	 arguments:
	 	json: designated json file
	 	itr_from: from which paper in the json file start to download
	 	offset: how many papers are expected to be downloaded in this execution
	 	--nolog: with out system log information

	 Running command example:
     	cd PaperCrawler --> put your json file here -->  scrapy crawl paperCrawler -a json='/Users/anonymity/Desktop/COI/COI_Project/dblp.v12.json' -a itr_from=0 -a offset=50 --nolog

