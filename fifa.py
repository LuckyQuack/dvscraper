# Script to scrape the fifa club world cup njtransit page
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import csv

options = webdriver.FirefoxOptions()
options.page_load_strategy = 'eager'
driver = webdriver.Firefox(options=options)

driver.get("https://www.njtransit.com/fifa")

driver.implicitly_wait(1.5)

# Find the table holding fifa club world cup schedule
fifa_schedule = driver.find_element(by=By.TAG_NAME, value="tbody")
rows = fifa_schedule.find_elements(by=By.TAG_NAME, value="tr")

data = []

# Data to collect: event, date, 1st train, stadium open time, match time, type
# Data is scraped out in weird format that needs to get cleaned up
for r in rows[1:]:
    print(r.text)
    item = r.text.strip()
    lines = [line.strip() for line in item.strip().split("\n") if line.strip()]
    i = 0
    while i < len(lines):
        title_line = lines[i]
        time1 = lines[i + 1]
        time2 = lines[i + 2]
        time3 = lines[i + 3]

        if "TRAIN" in time3:
            time3, type_ = time3.replace("TRAIN", "").strip(), "TRAIN"
        else:
            time3, type_ = time3, ""

        # Extract the last two words as the date (e.g., "June 17", "July 5")
        *event_parts, month, day = title_line.split()
        event = " ".join(event_parts)
        date = f"{month} {day}"

        data.append([event, date, time1, time2, time3, type_])
        i += 4

# Save to csv
with open("matches.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Event", "Date", "1st train", "Stadium open time", "Match", "Type"])
    writer.writerows(data)

driver.close()