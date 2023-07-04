from os import times
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup


def click_first_date(calendar):
    current_week = calendar.find_element(By.CSS_SELECTOR, "[aria-label='selected day']")
    current_week.click()

def click_last_date(calendar):
    weeks = calendar.find_elements(By.CLASS_NAME, "datepickerSaturday")
    print('AVER: ', weeks)
    last_day = weeks[-1]
    last_day.click()


def filter_dates(): ## MODIFY WHERE IT CLICKS from current week, 3 months, end of month after 3 clicks on arrow
    calendar_button = driver.find_element(By.ID, 'widgetFieldDateRange')
    calendar_button.click()
    calendar_table = driver.find_element(By.CLASS_NAME, 'datepickerViewDays')
    calendar_row = calendar_table.find_element(By.CLASS_NAME, 'datepickerDays')
    click_first_date(calendar_row)
    next_arrow = driver.find_element(By.CLASS_NAME, 'datePickerNextArrow')
    next_arrow.click()
    next_arrow.click()
    next_arrow.click()

    calendar_table = driver.find_element(By.CLASS_NAME, 'datepickerViewDays')
    calendar_row = calendar_table.find_element(By.CLASS_NAME, 'datepickerDays')
    click_last_date(calendar_row)
    time.sleep(2)
    apply_button = driver.find_element(By.ID, 'datePickerApplyButton')
    apply_button.click()

def uncheck_everything(list): # THIS CAN BE DONE BY PRESSING THE BUTTON "CLEAR" INSTEAD OF UNCHECKING EACH INDIVIDUAL COUNTRY
    checkboxes = list.find_element(By.ID, 'clearAllCountry')
    checkboxes.click()
    

def filter_countries():
    filter_button = driver.find_element(By.ID, 'filterStateAnchor')
    filter_button.click()

    time.sleep(2)

    country_list = driver.find_element(By.ID, 'ecoFilterBoxCountry')
    uncheck_everything(country_list)

    # Read the Excel file and filter countries based on the 'Condition' column
    df = pd.read_excel('markets_in_scope.xlsx')
    filtered_countries = df.loc[df['Is it in scope? (5%)'] == True, 'Market']
    print('These are the markets', filtered_countries)
    for country_name in filtered_countries:
        try:
            li_element = country_list.find_element(By.XPATH, f'//li//label[contains(., "{country_name}")]')
            li_element.click()
        except NoSuchElementException:
            print(f"Element not found for country: {country_name}. Skipping...")
            continue  # Skip to the next iteration

    importance_button = driver.find_element(By.ID, 'importance3')
    importance_button.click()

    apply_filters = driver.find_element(By.ID, 'ecSubmitButton')
    apply_filters.click()


# Set up Chrome driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Navigate to the website
driver.get('https://econcal.forexprostools.com/?features=datepicker,timezone,country_importance,filters&calType=week')
time.sleep(3)
filter_dates()
time.sleep(3)
filter_countries()
time.sleep(3)
events_list = driver.find_element(By.ID, 'ecEventsTable')

# Assuming you have the HTML content stored in a variable called 'html_content'
soup = BeautifulSoup(events_list.get_attribute('innerHTML'), 'html.parser')

# Find all the day sections
day_sections = soup.find_all('section', class_='day-section')

# Initialize lists to store the extracted data
dates = []
countries = []
events = []

# Iterate over each day section
for day_section in day_sections:
    # Extract the date from the header
    date_header = day_section.find('header', class_='article dateRow')
    print(date_header)
    # Check if the header exists
    if date_header is not None:
        date = date_header.find('h2', class_='theDay').text.strip()
        
        # Extract the event information from each list item
        event_items = day_section.find_all('li')
        for event_item in event_items:
            country = event_item.find('div', class_='left flagCur').span['title']
            event = event_item.find('div', class_='left event').text.strip()
            
            # Append the data to the respective lists
            dates.append(date)
            countries.append(country)
            events.append(event)

print(date, countries, events)
data = {'Date': dates, 'Country': countries, 'Event': events}
df = pd.DataFrame(data)
# Export the DataFrame to an Excel file
df.to_excel('filtered_countries.xlsx', index=False)