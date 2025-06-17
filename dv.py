from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Firefox()

driver.get("https://www.njtransit.com/dv-to")

driver.implicitly_wait(1.5)

# Find and click cookies button
cookie_button = driver.find_element(by=By.CSS_SELECTOR, value = "button.btn.btn-secondary")
cookie_button.click()

# Find where to input station name and send the name of station you want
# Possible idea is to automate input of stations to get the dv data for multiple stations, maybe can use the list of stations that show
station_name = driver.find_element(by=By.ID, value="dv-to-station")
station_name.send_keys("Newark Penn Station")

# function to check if the 'Get Real-Time Departures' Button is clickable because it's disabled until the form gets a valid input
def check_departure_button(driver):
    element = driver.find_element(By.XPATH, "//button[contains(text(), 'Get real-time departures')]")
    return element.is_enabled()

wait = WebDriverWait(driver, 10)
wait.until(check_departure_button)

# Pressing enter to submit form works better than clicking button for some reason
station_name.send_keys(Keys.ENTER)

# TODO
# Scrape the dv info to get next train info
# Data to collect: train name, arrival time, train status "All Aboard, In 13 min, etc.", Track #, destination

# function to check if the dv list exists, because it doesn't initially exist
def check_departure_vision(driver):
    element = driver.find_element(By.CSS_SELECTOR, value=".mt-n4")
    return element

wait = WebDriverWait(driver, 10)
wait.until(check_departure_vision)

train_list = driver.find_element(by=By.CSS_SELECTOR, value=".mt-n4")
trains = train_list.find_elements(by=By.TAG_NAME, value="li")
for item in trains:
    print(item.text)

# For debugging: This is for creating an error so the browser doesn't close down
message = driver.find_element(by=By.ID, value="message")
text = message.text

driver.quit()