from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

new_release_url = 'https://www.audible.in/newreleases'
bestseller_url = 'https://www.audible.in/adblbestsellers'
path = 'driver/chromedriver.exe'
options = Options()  
options.headless = True
driver = webdriver.Chrome(path, options=options)
driver.get(bestseller_url)
# Wait time of 5 sec to let website load properly
time.sleep(5)

box = driver.find_elements(By.XPATH, "//li[contains(@class,'productListItem')]")

book_namer_li = []
author_name = []
narrator_name = []
rating_li = []
release_date_li = []

last_page = int(driver.find_elements(By.XPATH, "//a[contains(@class,'pageNumberElement ')]")[-1].text)
page_no = 1

while page_no <= last_page:
    box = driver.find_elements(By.XPATH, "//li[contains(@class,'productListItem')]")
    for book in box:
        book_namer_li.append(book.find_element(By.XPATH, ".//h3[contains(@class,'bc-heading')]/a").text)
        author_name.append(book.find_element(By.XPATH, ".//li[contains(@class,'authorLabel')]/span/a").text)
        narrator_name.append(book.find_element(By.XPATH, ".//li[contains(@class,'narratorLabel')]/span/a").text)
        release_date_li.append(book.find_element(By.XPATH, ".//li[contains(@class,'releaseDateLabel')]").text)
        rating_li.append(book.find_element(By.XPATH, ".//li[contains(@class,'ratingsLabel')]/span").text)
    page_no += 1
    nxt_button = driver.find_element(By.XPATH, "//span[contains(@class,'nextButton ')]")
    nxt_button.click()

df = pd.DataFrame({"Audible Book": book_namer_li, "Author Name": author_name, "Narrator Name": narrator_name,
                   "Rating": rating_li, "Release Date": release_date_li})
df['Release Date'] = df['Release Date'].str.replace("Release Date: ", "")
df.to_csv(r'data/audible_books.csv', index=False)

driver.quit()
