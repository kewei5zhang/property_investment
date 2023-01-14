import time
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

if __name__ == '__main__':
    options = webdriver.ChromeOptions() 
    # options.add_argument("start-maximized")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument("user-data-dir=/Users/keweizhang/Library/Application Support/Google/Chrome/Profile 2")
    browser = uc.Chrome()

        # Navigate to Url
    browser.get("https://www.realestate.com.au/vic/east-melbourne-3002/")
    time.sleep(30)
    print(By.ID)
    print(By.CLASS_NAME)
    # house_buy_2bed_element = browser.find_element('id', 'house-price-data-buy-2-bedrooms').get_attribute("outerHTML")
    house_buy_2bed_element = browser.find_element('id', 'house-price-data-buy-2-bedrooms')

    market_insight_element = house_buy_2bed_element.find_element("class name", "MarketInsights__InsightsContainer-sc-63txnk-0.kumviP")
    market_insight_values = market_insight_element.find_elements("class name", "Text__Typography-sc-vzn7fr-0.CGQsq")
    market_insight_desc = market_insight_element.find_elements("class name", "Text__Typography-sc-vzn7fr-0.cwMhfp")
    print("values")
    insights=dict(zip([(lambda x: x.get_attribute("innerHTML").replace("<!-- -->",""))(x) for x in market_insight_desc],[(lambda x: x.get_attribute("innerHTML").replace("<!-- -->",""))(x) for x in market_insight_values]))
    print(insights)
    # for e in market_insight_values:
    #     print(e.get_attribute("innerHTML").replace("<!-- -->",""))
    # print("description")
    # for e in market_insight_desc:
    #     print(e.get_attribute("innerHTML").replace("<!-- -->",""))
    # print("values")
    # print(market_insight_element)
    # for e in market_insight_value_elements:
    #     print(e.text)
    
    # market_insight_desc_elements = house_buy_2bed_element.find_elements('class name', 'Text__Typography-sc-vzn7fr-0 cwMhfp')
    # print("description")
    # print(market_insight_desc_elements)
    # for e in market_insight_desc_elements:
    #     print(e.text)
    time.sleep(1000)

    # # html = house_buy_2bed_element.page_source
    # print(market_insight_elements)
    
    # def is_ready(browser):
    #     return browser.execute_script(r"""
    #         return document.readyState === 'complete'
    #     """)
    # WebDriverWait(driver, 30).until(is_ready)
    
    # # Scroll to bottom of the page to trigger JavaScript action
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # time.sleep(30)
    # # WebDriverWait(driver, 30).until(is_ready)
    # # print("sleep 10 sec")
    # # time.sleep(15)

    #     # Get all the elements available with tag name 'p'
    # house_buy_2bed_element = browser.find_element(By.ID, 'house-price-data-buy-all-bedrooms')
    # print(house_buy_2bed_element)
    # # market_insight_elements = house_buy_2bed_element.find_elements(By.CLASS_NAME,"Text__Typography-sc-vzn7fr-0 biEGMT")
    # market_insight_elements = house_buy_2bed_element.find_elements(By.TAG_NAME, "h3")

    # print(market_insight_elements)
    # # print(elements.text)
    # for e in market_insight_elements:
    #     print(e.get_attribute)
    #     # attrs = vars(e)
    #     # print(', '.join("%s: %s" % item for item in attrs.items()))
    #     # print(e._id)
    #     # print(e.text)
        
    # time.sleep(1000)
    
  