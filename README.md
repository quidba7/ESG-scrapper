# ESG scrapper
Python scripts to scrap various websites and collect ESG data. Output are flat files
The source we use are as follows:
* refinitive ESG website
* news api
* CRSHub (under development)
* Sustainanalytics


## To Use:

### refinitive:
* Download the scripts in the "refinitiv_esg" folder and change folder variable to your own drive folder
* install dependencies in requirements.txt file
* Run esg_score.py
* I schedule using windows scheduler every 3 days

### Dependencies
* Beautifulsoup
* Selenium
* pandas / numpy

### news api
* Create an account with news api and replace my api-key in the url to send through API (Don't use mine, it is a free subscription anyway)
* run scrap_news.py

### Dependencies
* requests

