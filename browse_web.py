from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
# On Raspberry pi
from selenium.webdriver.firefox.options import Options
from pyvirtualdisplay import Display
import os
from dotenv import load_dotenv

load_dotenv()
PATH_TO_FIREFOX_PROFILE = os.getenv('PATH_TO_FIREFOX_PROFILE')

def capture_daily():
    # On Raspberry Pi
    profile = webdriver.FirefoxProfile(PATH_TO_FIREFOX_PROFILE)
    display = Display(visible=0, size=(1024,768))
    display.start()
    service = webdriver.FirefoxService(executable_path='/usr/local/bin/geckodriver')
    options = Options()
    options.profile = profile
    driver = webdriver.Firefox(service=service, options=options)
    
    # Everywhere else
    #driver = webdriver.Firefox()
    
    try:
        driver.get("https://leetcode.com/problemset/")

        time.sleep(5)

        link = driver.find_element(By.CSS_SELECTOR, "a[href*='daily']")
        # print(link.get_attribute('href'))
        href_value = link.get_attribute('href')
        
        driver.get(href_value)
        driver.set_window_size(1200, 1500)
        # driver.maximize_window()
        time.sleep(5)
        element = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div[4]/div/div/div[4]/div/div[1]')
        element.screenshot('daily.png')
        time.sleep(5)
    except e:
        print("Error")
        print(e)
        
    driver.close()
    
    # On Raspberry Pi
    display.stop()
    
    return href_value
