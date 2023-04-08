from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# https://www.youtube.com/watch?v=RvCBzhhydNk&t=1141s
from bs4 import BeautifulSoup

import numpy as np
from numpy import asarray
from numpy import savetxt

email = input("What is your LinkedIn email: ")
password = input("What is your LinkedIn passwords: ")

driver = webdriver.Chrome()

# https://stackoverflow.com/questions/48850974/selenium-scroll-to-end-of-page-in-dynamically-loading-webpage
def scroll_down(driver):
    # Calculate scroll height
    current_height = driver.execute_script("return document.body.scrollHeight")
    
    # Infinite loop
    while True:
        # Scroll down to the bottom of page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        # Click the show more button if there
        # if driver.find_element(By.XPATH, "//*[text()='Show more results']") is not None: -> This line of code will not work as .findelement always returns something. An empty array is not the same as None.
        if len(driver.find_elements(By.XPATH, "//*[text()='Show more results']")) > 0:
            driver.find_element(By.XPATH, "//*[text()='Show more results']").click()
            time.sleep(5)

        # Calculate new scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == current_height:
            break

        current_height = new_height


driver.get('https://www.linkedin.com')
driver.find_element(By.XPATH, '//input[@id="session_key"]').send_keys(email)
driver.find_element(By.XPATH, '//input[@id="session_password"]').send_keys(password)
driver.find_element(By.XPATH, '//button[@type="submit"]').click()
time.sleep(10)

driver.get('https://www.linkedin.com/mynetwork/invite-connect/connections/')
scroll_down(driver)
linkedinPage = BeautifulSoup(driver.page_source, 'html.parser')

driver.quit()

masterTable = [['Name', 'Occupation']]
linkedinCards = linkedinPage.find_all('li', class_="mn-connection-card artdeco-list")
for linkedinCard in linkedinCards:
    Names = linkedinCard.find('span', class_="mn-connection-card__name t-16 t-black t-bold")
    Occupations = linkedinCard.find('span', class_="mn-connection-card__occupation t-14 t-black--light t-normal")
    Table = [Names.text.strip(), Occupations.text.strip()]
    masterTable.append(Table)
print(masterTable)

# https://stackoverflow.com/questions/48230230/typeerror-mismatch-between-array-dtype-object-and-format-specifier-18e 
np.savetxt('LinkedIn_Connections_Webscraping_Table.tsv', masterTable, delimiter='\t', fmt='%s')