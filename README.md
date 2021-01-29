# PaperCrawler
Input: a json file containing "paper title","author",...
Output: download all the public paper with corresponding titles in json file from Internet

Preparation: install pip and scrapy.
how to install pip: 
     for mac user: change to desired folder, and enter command: curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py --> python3 get-pip.py
     for windows user: directly download get-pip.py from https://bootstrap.pypa.io/get-pip.py --> python3 get-pip.py
how to install scraoy:
     change to the desired folder --> pip install scrapy
     
How to use:
     cd PaperCrawler --> put your json file here -->  scrapy crawl paperCrawler --nolog

