from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import warnings
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select


warnings.filterwarnings('ignore')

url = 'https://www.adamchoi.co.uk/overs/detailed'
path = 'driver/chromedriver.exe'
options = Options()
options.headless = True
driver = webdriver.Chrome(path, options=options)
driver.get(url)
# Wait time of 5 sec to let website load properly
time.sleep(5)

# select dropdown box
select = Select(driver.find_element("xpath", "//select[@id='country']"))
# Change country as per requirement
select.select_by_visible_text('Spain')


all_matches = driver.find_element("xpath", "//label[@analytics-event='All matches']")
all_matches.click()

# declaring list to store scrape data
date_li = []
home_team_li = []
score_li = []
away_team_li = []

# scraping all tr data
tr_data = driver.find_elements("xpath", "//tr")

# looping through all rows and store td in respective lists
for row in tr_data:
    date_li.append(row.find_elements(By.TAG_NAME, "td")[0].text)
    home_team_li.append(row.find_elements(By.TAG_NAME, "td")[1].text)
    score_li.append(str(row.find_elements(By.TAG_NAME, "td")[2].text))
    away_team_li.append(row.find_elements(By.TAG_NAME, "td")[3].text)

# clsoing the browser
driver.quit()

# Storing the scrape data in dataframe and subsequently in csv file
df = pd.DataFrame({"Date": date_li, "Home team": home_team_li, "Score": score_li, "Away team": away_team_li})
df.to_csv("data/scorecard.csv", index=False)
