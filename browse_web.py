from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

def capture_daily():
    driver = webdriver.Chrome()
    driver.get("https://leetcode.com/problemset/")

    time.sleep(5)

    link = driver.find_element(By.CSS_SELECTOR, "a[href*='daily']")
    # print(link.get_attribute('href'))

    driver.get(link.get_attribute('href'))
    driver.set_window_size(1200, 2500)
    # driver.maximize_window()
    time.sleep(5)
    element = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div[4]/div/div/div[4]/div/div[1]')
    element.screenshot('daily.png')
    time.sleep(5)
    driver.close()