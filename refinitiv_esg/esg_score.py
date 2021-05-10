from bs4 import BeautifulSoup
import requests

import pandas as pd
from pandas import Series,DataFrame


import csv
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import Series,DataFrame
import urllib
import pickle

# now we want to collect email addresses
# Add javascript with selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime

from bs4 import BeautifulSoup
import requests
import pandas as pd
from urllib.request import Request, urlopen
import re


# function to extract the scores from the webpage
def extract_scores(content):
    temp_dict = {}

    # first we look for main esg score
    ele = content.find("h3", {"class": "Heading Heading--m"})

    print(ele.text.split(":")[1].strip())
    temp_dict["main_score"] = ele.text.split(":")[1].strip()

    # then we look for sub esg scores
    env = content.find_all("div", {"class": "Grid-item"})

    # loop through all divs
    for el in env:
        # loop through all div table items
        table_ele = el.find_all("div", {"class": "table-item"})

        for sub_note in table_ele:
            # get names of the sub category
            name = sub_note.find("div", {"class": "table-align-left"})

            # get score of the sub category
            val = sub_note.find("div", {"class": "table-align-right"})
            temp_dict[name.text] = val.text
            print((name.text, val.text))

    # now pick ranking on industry
    rank = content.find("h4", {"class": "Heading Heading--xl"})
    temp_dict["industry_rank"] = rank.text
    print(rank.text)

    # now pick description
    descr = content.find("p", {"class": "Standfirst"})
    temp_dict["descr"] = descr.text
    print(descr.text)

    return pd.DataFrame(temp_dict, index=[0])

# main run
def run_selenium_srap(df, esg_main_df, folder):

    with open(f"{folder}\\refinitiv_esg\\ind.pkl", 'rb') as f:
        last_ind = pickle.load(f)

    # case where we pick last index, we initialize at zero
    if last_ind>=df.shape[0]-1:
        last_ind=0

    # first we will loop every hour 87 companies to avoid exceed limit from refinitive
    for j in range(last_ind, int(df.shape[0] / 87) + 1):
        for ind in range(j * 87, (j + 1) * 87):

            # we make sur we don't go over dataframe number of rows
            if ind < df.shape[0]:
                # now we loop through company names
                # Now clear selection
                #     button = driver.find_element_by_xpath('//button[@class="SearchInput-clearButton"]')
                #     button.click()
                #     time.sleep(3)

                # Now insert company name
                e = driver.find_element_by_xpath('//input[@id="searchInput-1"]')
                e.send_keys(df.loc[ind, "company"])
                time.sleep(3)

                # We click on the enter
                button = driver.find_element_by_xpath('//button[@class="SearchInput-searchButton"]')
                button.click()
                time.sleep(3)

                # We can collect ESG score
                cc_html = driver.page_source
                content = BeautifulSoup(cc_html, 'html.parser')

                # We can collect ESG score
                company_df = extract_scores(content)

                # we append to main dataframe
                esg_main_df  = pd.concat([esg_main_df, company_df], axis=0)

                # Now clear selection
                button = driver.find_element_by_xpath('//button[@class="SearchInput-clearButton"]')
                button.click()
                time.sleep(3)
                print("{} company".format(str(ind)))

                # we save every 10 companies
                if ind % 10 == 0:
                    # save the 10 companies
                    save_csv(esg_main_df)

                    # redefine the dataframe as empty
                    esg_main_df = pd.DataFrame([], columns=['Environment', 'Emissions', 'Resource Use', 'Innovation',
                                                            'Social', 'Human Rights', 'Product Responsibility', 'Workforce',
                                                            'Community', 'Governance', 'Management', 'Shareholders', 'CSR Strategy',
                                                            'industry_rank', 'descr', 'main_score'])

                with open(f"{folder}\\refinitiv_esg\\ind.pkl", 'wb') as f:
                    pickle.dump(ind, f)

        # we wait an hour to be able to collect again
        time.sleep(60 * 61)

    # after we looped over all companies, we re-load temp.csv file and define as final df
    esg_main_df = pd.read_csv(f"{folder}\\refinitiv_esg\\temp.csv")

    esg_main_df["Val_date"] = datetime.now()
    esg_main_df.to_csv(f"{folder}\\refinitiv_esg\\esg_score_{datetime.now():%Y-%m-%d %H-%M-%S%z}.csv", index=False)
    with open(f"{folder}\\refinitiv_esg\\ind.pkl", 'wb') as f:
        pickle.dump(0, f)

    # now we save temp as empty csv
    temp = pd.DataFrame(columns=["Environment", "Emissions", "Resource Use", "Innovation", "Social", "Human Rights"
        , "Product Responsibility","Workforce","Community","Governance","Management","Shareholders","CSR Strategy","industry_rank"
        ,"descr","main_score"])

    temp.to_csv(f"{folder}\\refinitiv_esg\\temp.csv", index=False)

def save_csv(df):
    """
    We save in excel
    :return:
    """
    temp = pd.read_csv(r"C:\Users\Administrator\PycharmProjects\myscrapper\refinitiv_esg\temp.csv")

    # we merge with dataframe
    df = pd.concat([df, temp], axis=0)

    # we save again as csv
    df.to_csv(r"C:\Users\Administrator\PycharmProjects\myscrapper\refinitiv_esg\temp.csv", index=False)

if __name__ == "__main__":

    # read the csv file with company names
    folder = "C:\\Users\\Administrator\\PycharmProjects\\myscrapper"
    df = pd.read_csv(f"{folder}\\refinitiv_esg\\companies.csv")

    # start by collecting driver chrome
    driver = webdriver.Chrome(f"{folder}\\chromedriver\\chromedriver.exe")
    driver.get("https://www.refinitiv.com/en/sustainable-finance/esg-scores")
    time.sleep(10)

    # start by clicking on cookies
    button = driver.find_element_by_xpath('//button[@id="onetrust-accept-btn-handler"]')
    button.click()
    time.sleep(3)

    # ESG final dataframe
    esg_main_df = pd.DataFrame([], columns=['Environment', 'Emissions', 'Resource Use', 'Innovation', 'Social',
                                            'Human Rights', 'Product Responsibility', 'Workforce', 'Community',
                                            'Governance', 'Management', 'Shareholders', 'CSR Strategy',
                                            'industry_rank', 'descr', 'main_score'])

    # run selenium scrap on current page
    run_selenium_srap(df, esg_main_df, folder)







