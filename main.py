# ---------------------------------- imports --------------------------------- #
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging

# local imports
from df import *
from browser_manager import Browser
from scraper import Scraper, ids
from mp import MP, MP_Site
from throttle import Throttle
from paths import current_folder, data_folder, logs_folder

# ------------------------------------- < ------------------------------------ #


# create log file
logging.basicConfig(
    filename=f"{logs_folder}/sejm.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
)


# scrape mp data function
def scrape_mp_data(mp_index, browser, throttle):

    # create MP_Site object, to get mp_info_site url
    url = MP_Site(mp_index).mp_info_site

    # use throttle module to wait before making a request
    throttle.wait()

    # check if server responds
    throttle.try_get_response(url, browser.driver)

    # get html from browser
    html = browser.driver.page_source

    # pass html to Scraper
    scraper = Scraper(html)

    # get political info data
    elected_date, party_list, constituency, no_of_votes, oath_date, club_name, parliamentary_experience = scraper.get_political_info()

    # get personal info data
    name, surname, birth_date, birth_place, education, school, profession = scraper.get_personal_info()

    # get email address
    email = scraper.get_email_address()

    # create MP object
    mp = MP(
        mp_index,
        name,
        surname,
        url,
        constituency,
        elected_date,
        party_list,
        no_of_votes,
        oath_date,
        parliamentary_experience,
        club_name,
        birth_date,
        education,
        school,
        profession,
        email
    )

    # return MP object
    return mp


def main():

    # create browser object
    browser = Browser()

    # create throttle object
    throttle = Throttle(2)

    # iterate over all MPs
    for i in ids:

        # load mps_df
        mps_df = load_df()

        # log
        logging.info(f"Scraping MP index: {i}")

        # check if MP index is already in the id column of the dataframe
        if check_if_id_exists(i, mps_df) == True:
            continue

        # scrape mp data
        mp = scrape_mp_data(i, browser, throttle)

        # append mp data to mps_df
        new_df = insert_mp_to_df(mp, mps_df)

        # save updated dataframe to csv
        save_df_to_csv(new_df)

    # quit browser
    browser.driver.quit()


if __name__ == "__main__":
    main()
