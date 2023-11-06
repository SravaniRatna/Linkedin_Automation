from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import pandas as pd
from datetime import datetime
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
    wait = WebDriverWait(driver, 30)
    return wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

max_retries = 3  # Set the maximum number of retries

# Use a while loop to keep checking for the element
while True:
    try:
        search = driver.find_element(By.XPATH, "/html/body/div[5]/header/div/div/div/div[1]/input")
        search.send_keys("#jobseeker.people")
        search.send_keys(Keys.ENTER)  # Send the Enter key to trigger the search
        time.sleep(10)
        break  # Exit the loop if the element is found
    except Exception as e:
        if max_retries <= 0:
            print(f"Max retries reached. Unable to find the search element. Exiting.")
            break
        print(f"Error: {str(e)} - Retrying...")
        time.sleep(20)  # Adjust the sleep time as needed
        max_retries -= 1

# Initialize a list to store the candidate names and LinkedIn URLs
candidate_names = []
profile_urls = []

#keywords = ["#opentowork", "#lookingforjob", "#jobseeker", "#jobseekers",
#            "#activelyseeking", "#jobhunt", "#jobsearch", "#lookingforwork",
#            "#resume", "#employmentseekers", "#hireme", "#availableforwork"]
# Interact with the element
''''
if max_retries >= 0:
    #for keyword in keywords:
    #search = driver.find_element(By.XPATH, "/html/body/div[5]/header/div/div/div/div[1]/input")
        search.send_keys("#lookingforjob")
        search.send_keys(Keys.ENTER)  # Send the Enter key to trigger the search
        time.sleep(10)
'''
    # Retry for the following elements
elements_to_retry = [
                "/html/body/div[4]/div[3]/div[2]/div/div[1]/div/div/div/section/ul/li/button",
#                "/html/body/div[5]/div[3]/div[2]/div/div[1]/div/div/div/section/ul/li[3]/button",
#                "/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[3]/div/div[2]/a"
                "/html/body/div[4]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/div[2]/a"
            ]

for xpath in elements_to_retry:
                try:
                    element = driver.find_element(By.XPATH, xpath)
                    element.click()
                    time.sleep(10)
                except Exception as e:
                    print(f"Error: {str(e)} - Retrying...")

    # Retrieve the page source
page_source = driver.page_source

    # Pass the page source to BeautifulSoup
soup = BeautifulSoup(page_source, "lxml")

    # Use BeautifulSoup to extract information from the page
boxes = soup.find_all("li", class_ = "reusable-search__result-container")



# Extract profile URLs from the current page
for box in boxes:
            profile_url = box.find("a", class_="app-aware-link")
            if profile_url:
                href = profile_url.get("href")
                profile_urls.append(href)

# After the loop, print the final number of collected URLs
print("Total URLs collected:", len(profile_urls))
'''
nps = soup.find_all("div", class_ = "artdeco-pagination artdeco-pagination--has-contro")
np = driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div[2]/div/div[1]/main/div/div/div[6]/div/div/button[2]")
np.click()
time.sleep(5)
'''
# Use Selenium to navigate to each profile URL
max_retries = 3  # Set the maximum number of retries

for url in profile_urls:
        for retry in range(max_retries):
            driver.get(url)
            time.sleep(10)  # Add sleep here if necessary

            try:
                    name = driver.find_element(By.XPATH, "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[1]/span[1]/a/h1")
                    candidate_names.append(name.text)
                    break  # Break the retry loop if successful
            except Exception as e:
                if retry < 2:
                    print(f"Error: {str(e)} - Retrying (Attempt {retry + 1})...")
                else:
                    print(f"Max retries reached for {url}. Skipping...")
                    candidate_names.append("None")

# Close the WebDriver when you're done
driver.quit()

# Define the current date and time
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

# Create a pandas DataFrame with the candidate names
df = pd.DataFrame({"Candidate Name": candidate_names, "Linkedin URL": profile_urls})

# Ask the user for the file name
file_name = input("Enter the file name (e.g., 'candidate_names.xlsx'): ")

# Add the current time to the file name
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
file_name_with_time = f"{file_name}_{current_time}.xlsx"

# Save the DataFrame to an Excel file with the user-specified file name
df.to_excel(file_name_with_time, index=False)