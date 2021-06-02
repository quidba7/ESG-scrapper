# ESG scrapper
Python scripts to scrap various websites and collect ESG data. Output are flat files
The source we use are as follows:
* refinitiv ESG website
* news api
* CSRHub (under development)
* esg censible (under development)
* sustainanalytics (under development)


## Data sources:

### refinitiv:
* download the scripts in the "refinitiv_esg" folder and change folder variable to your own drive folder
* install dependencies in requirements.txt file
* run esg_score.py
* I schedule using windows scheduler every 3 days

    #### dependencies:
    * beautifulsoup
    * selenium
    * pandas / numpy

### news api
* create an account with news api and replace my api-key in the url to send through API (Don't use mine, it is a free subscription anyway)
* run scrap_news.py

    #### dependencies:
    * requests