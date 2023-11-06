from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import re

import time

# Set up the web driver with the path to your ChromeDriver executable
#driver = webdriver.Chrome("C:\\Users\\srava\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")
s= Service("C:/Users/srava/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service = s)
# Open LinkedIn
driver.get("https://www.linkedin.com")
time.sleep(5)
# Log in to your LinkedIn account (replace with your credentials)
email = "mahesh.americanit@gmail.com"
password = "9392614520@2023"

# Locate the email and password input fields by ID
email_input = driver.find_element(By.XPATH,"""/html/body/main/section[1]/div/div/form/div[1]/div[1]/div/div/input""")
email_input.send_keys(email)
password_input = driver.find_element(By.XPATH,"""/html/body/main/section[1]/div/div/form/div[1]/div[2]/div/div/input""")
password_input.send_keys(password)

# Submit the login form
sign_in = driver.find_element(By.XPATH,"/html/body/main/section[1]/div/div/form/div[2]/button")
sign_in.send_keys(Keys.ENTER)

def wait_for_element(xpath):
    wait = WebDriverWait(driver, 50)
    return wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
'''
# Use a while loop to keep checking for the element
while True:
    try:
        search = wait_for_element("/html/body/div[5]/header/div/div/div/div[1]/input")
        break  # Exit the loop if the element is found
    except:
        pass  # If the element is not found, continue waiting

# Interact with the element
search.send_keys("#opentowork")
search.send_keys(Keys.ENTER)
time.sleep(10)
people = driver.find_element(By.XPATH,"/html/body/div[5]/div[3]/div[2]/div/div[1]/div/div/div/section/ul/li[3]/button").click()
time.sleep(10)
see_all_results = driver.find_element(By.XPATH,"/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[3]/div/div[2]/a").click()
time.sleep(10)
'''
# Retrieve the page source
page_source = driver.page_source

# Pass the page source to BeautifulSoup
soup = BeautifulSoup(page_source, "lxml")

# Use BeautifulSoup to extract information from the page

# Navigate to the LinkedIn search page
driver.get("https://www.linkedin.com/search/results/people/?keywords=#opentowork")
#driver.get()


# Click on "See all results" button
see_all_results = driver.find_element(By.XPATH, "//a[@data-control-name='all_filters_click']")
see_all_results.click()
time.sleep(3)

# Extract profile URLs from the first 5 pages
profile_urls = []
for i in range(5):
    boxes = driver.find_elements(By.CLASS_NAME, "reusable-search__result-container")
    for box in boxes:
        profile_url = box.find_element(By.CSS_SELECTOR, "a.app-aware-link").get_attribute("href")
        profile_urls.append(profile_url)
    try:
        next_button = driver.find_element(By.XPATH, f"//button[@aria-label='Page {i+2}']")
        next_button.click()
        time.sleep(3)
    except:
        break

# Print the collected URLs
print(profile_urls)

'''    #next_button_tab = driver.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
    # If "Next" button exists, click it; otherwise, exit the loop
    if next_button_tab:
        next_button_tab.click()
        time.sleep(10)
    else:
        break  # Exit the loop when there's no "Next" button
'''







