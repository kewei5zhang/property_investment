import time
import json
import csv
import logging
import sys
import ssl; ssl._create_default_https_context = ssl._create_stdlib_context
import undetected_chromedriver as uc

from typing import Literal, get_args
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

_STATES = Literal['act','nsw','nt','qld','sa','tas','vic','wa']
_PROPERTY_TYPES = Literal['house','unit']
_BUY_OR_RENT = Literal['buy','rent']
_BEDROOMS = Literal['all','2','3','4']

BASE_URL = "https://www.realestate.com.au"
PRICE_CONTAINER_CLASS = "indexstyles__PriceContainer-sc-10e5b9w-2.gqfeob"
MARKET_INSIGHT_CONTAINER_CLASS = "MarketInsights__InsightsContainer-sc-63txnk-0.kumviP"
MARKET_INSIGHT_VALUE_ELEMENT_CLASS = "Text__Typography-sc-vzn7fr-0.CGQsq"
DESC_ELEMENT_CLASS = "Text__Typography-sc-vzn7fr-0.cwMhfp"
PRICE_VALUE_ELEMENT_CLASS = "Text__Typography-sc-vzn7fr-0.iNyqSz"
PAGE_LOAD_TIMEOUT = 15

OUTPUT_FOLDER = "data"
 
logging.basicConfig(format='%(process)d-%(levelname)s-%(message)s', stream=sys.stdout, level=logging.INFO)
 
class Suburb:
    def __init__(self, name: str, state: _STATES, postcode: str):
        assert state in get_args(_STATES), f"'{state}' is invalid - valid options are {get_args(_STATES)}"
        self.name = name
        self.state = state
        self.postcode = postcode
    
    def __str__(self):
        return f'Suburb {self.name} in {self.state} state, post code {self.postcode}'
    
    def get_url(self):
        # https://www.realestate.com.au/vic/doncaster-east-3109
        url = "{base_url}/{state}/{suburb}-{postcode}/".format(base_url=BASE_URL, state = self.state, suburb = self.name, postcode = self.postcode)
        return url
    
    def get_element_id(self, property_type: _PROPERTY_TYPES, buy_or_rent: _BUY_OR_RENT, bedrooms: _BEDROOMS):
        elementId = f"{property_type}-price-data-{buy_or_rent}-{bedrooms}-bedrooms"
        return elementId
    
    def get_metadata(self, property_type: _PROPERTY_TYPES, buy_or_rent: _BUY_OR_RENT, bedrooms: _BEDROOMS):
        metadata = {
            'suburb': self.name,
            'state': self.state,
            'postcode': self.postcode,
            'property_type': property_type,
            'buy_or_rent': buy_or_rent,
            'bedrooms': bedrooms
        }
        return metadata
    
    def get_market_insight(self, property_type: _PROPERTY_TYPES, buy_or_rent: _BUY_OR_RENT, bedrooms: _BEDROOMS):
        assert property_type in get_args(_PROPERTY_TYPES), f"'{property_type}' is invalid - valid options are {get_args(_PROPERTY_TYPES)}"
        assert buy_or_rent in get_args(_BUY_OR_RENT), f"'{buy_or_rent}' is invalid - valid options are {get_args(_BUY_OR_RENT)}"
        assert bedrooms in get_args(_BEDROOMS), f"'{bedrooms}' is invalid - valid options are {get_args(_BEDROOMS)}"

        logging.info(f' 🔗 URL:{self.get_url()}')
        options = uc.ChromeOptions()
        # options.add_argument("--headless")
        browser = uc.Chrome(options)
        browser.get(self.get_url())
        # Wait the page to load
        logging.info(f' 🌀 Page Loading...')
        time.sleep(PAGE_LOAD_TIMEOUT)
        
        # Locate market insights
        try:
            metadata = self.get_metadata(property_type, buy_or_rent, bedrooms)
            element = browser.find_element('id', self.get_element_id(property_type, buy_or_rent, bedrooms))
            market_insight_container = element.find_element('class name', MARKET_INSIGHT_CONTAINER_CLASS)
            price_container = element.find_element('class name', PRICE_CONTAINER_CLASS)
            market_insight_values = market_insight_container.find_elements('class name', MARKET_INSIGHT_VALUE_ELEMENT_CLASS)
            market_insight_description = market_insight_container.find_elements('class name', DESC_ELEMENT_CLASS)
            price_value = price_container.find_element('class name', PRICE_VALUE_ELEMENT_CLASS)
            price_description = price_container.find_element('class name', DESC_ELEMENT_CLASS)

            market_insight = dict(zip([(lambda x: x.get_attribute("innerHTML").replace("<!-- -->","").replace(" ","_"))(x) for x in market_insight_description],[(lambda x: x.get_attribute("innerHTML").replace("<!-- -->",""))(x) for x in market_insight_values]))
            price = {price_description.get_attribute("innerHTML").replace("<!-- -->","").replace(" ","_") : price_value.get_attribute("innerHTML").replace("<!-- -->","")}
            logging.info(f' Browser Closed')
            browser.close()
        except Exception as e:
            logging.info(f' ❌ Something Went Wrong...')
            logging.info(f'{e}')
            browser.close()
            logging.info(f' Browser Closed')
        return metadata | market_insight | price 

def main(source_file: str, state: _STATES, property_type: _PROPERTY_TYPES, buy_or_rent: _BUY_OR_RENT, bedrooms: _BEDROOMS):
    with open(source_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        output_filename = f'{OUTPUT_FOLDER}/stats_{property_type}_{buy_or_rent}_{bedrooms}.csv'
        # This skips the first row of the CSV file.
        next(csv_reader)
        for idx, row in enumerate(csv_reader):
            try:
                suburb = Suburb(row[1].lower().replace(' ','-'), state, row[0])
                property_insight = suburb.get_market_insight(property_type,buy_or_rent,bedrooms)
                with open(output_filename, 'a') as stats_output:
                    csvwriter = csv.writer(stats_output)
                    if idx == 0:
                        csvwriter.writerow(property_insight.keys())
                    csvwriter.writerow(property_insight.values())
                print(json.dumps(property_insight))
                logging.info(f' ✅ Json dumped!')
            except Exception as e:
                logging.info(f'{e}')
                pass

if __name__ == "__main__":
    source_file = "VIC_postcode.csv"
    main(source_file, "vic", "house", "buy", "all")
        
    # doncaster_east = Suburb("thomastown","vic","3074")
    # property_insight = doncaster_east.get_market_insight("house","buy","2")
    # # print(json.dumps(property_insight))
    # print(property_insight.keys())
    # print(property_insight.values())
    