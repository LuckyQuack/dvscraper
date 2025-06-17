# This scrapes the departure vision for rails on the njtransit website using Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import csv
import os

csv_file = "departures.csv"
open(csv_file, "w").close()
write_header = True

user_stations = input("Enter NJ Transit station names separated by commas: ").split(",")
user_stations = [station.strip() for station in user_stations if station.strip()]

options = webdriver.FirefoxOptions()
options.page_load_strategy = 'eager'
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)

# Function to check if the 'Get Real-Time Departures' Button is clickable because it's disabled until the form gets a valid input
def check_departure_button(driver):
    element = driver.find_element(By.XPATH, "//button[contains(text(), 'Get real-time departures')]")
    return element.is_enabled()

# Function to check if the dv list exists, because it doesn't initially exist
def check_departure_vision(driver):
    element = driver.find_element(By.CSS_SELECTOR, value=".mt-n4")
    return element

wait = WebDriverWait(driver, 5)

for user_station in user_stations:
    driver.get("https://www.njtransit.com/dv-to")
    driver.implicitly_wait(1.5)

    # Try inputting station into search
    try:
        station_name = driver.find_element(by=By.ID, value="dv-to-station")
        station_name.clear()
        station_name.send_keys(user_station)

        # Waiting until departure button is clickable before entering input
        wait.until(check_departure_button)
        station_name.send_keys(Keys.ENTER)

        # Wait until departure vision loads, if it doesn't then there's an error
        wait.until(check_departure_vision)
    except:
        print(f"No data available for {user_station}")
        continue

    # When the train list exists we can find it, and then find the inner list that contains the data we want
    train_list = driver.find_element(by=By.CSS_SELECTOR, value=".mt-n4")
    trains = train_list.find_elements(by=By.TAG_NAME, value="li")

    seen = set()
    data = []

    # Get and clean up data
    for item in trains:
        text = item.text.strip()
        if text and text not in seen:

            seen.add(text)

            # Split into lines and remove empty lines
            lines = [line.strip() for line in text.split("\n") if line.strip()]

            # Removing the 3rd element that's always "View Stops Caret Down"
            lines = [line for line in lines if line != "View Stops Caret Down"]

            # There is a possibility that status or track # can be missing so we have to deal with that
            if len(lines) >= 3:
                station = lines[0]
                train = lines[1]
                time = lines[2]

                # Default for status and track
                status = ""
                track = ""

                # Checking for 4th line and figuring out whether its status or track
                if len(lines) >= 4:
                    # If last line starts with "Track", it's track info
                    if lines[-1].startswith("Track"):
                        track = lines[-1]
                        if len(lines) >= 5:
                            status = lines[-2]  # Second to last is status
                    else:
                        status = lines[-1]  # Last is status

                data.append([user_station, station, train, time, status, track])
    print(data)

    # Save data to csv file
    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["Station", "Destination", "Train", "Time", "Status", "Track"])
            write_header = False  # only write header once
        writer.writerows(data)

driver.close()