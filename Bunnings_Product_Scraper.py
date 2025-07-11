# -*- coding: utf-8 -*-
import os
import csv
import sys
import time
import platform
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from runCount_config import check_run_count

# Only run if run count is less than the number of days specified in the config
check_run_count()


# -------------------------------
# SETUP SELENIUM DRIVER
# -------------------------------

# Configure Chrome to run in headless mode 
chrome_options = Options()
#chrome_options.add_argument("--headless=new")  
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--remote-debugging-port=9222")

# Initialise the Chrome WebDriver
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10) # Explicit wait object

# Open Bunnings website
driver.get("https://www.bunnings.com.au/")
print("Opened Bunnings")
time.sleep(3) # Wait for site scripts and dynamic content to load


# ----------------------------------
# DEFINE SCRAPE PARAMETERS
# ----------------------------------

# Detect OS to use correct keyboard shortcut for clearing search box
is_mac = platform.system() == "Darwin"

# Search terms to run through
search_terms = ["hammer", "drill", "saw"]

# Timestamp to tag each result
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Store all product data from all searches
product_data = []


# -------------------------
# SEARCH AND SCRAPE 
# -------------------------

for query in search_terms:
    try:
        # Locate the search box and click it
        search_box = driver.find_element(By.ID, "custom-css-outlined-input")
        # Force-click the search box using JavaScript to bypass issues with overlapping elements 
        # (e.g. banners or popups)
        driver.execute_script("arguments[0].click();", search_box)
        # Short delay to allow any page animations or transitions to finish before typing
        time.sleep(1)

        # Clear the search box using keyboard shortcuts
        if is_mac:
            search_box.send_keys(Keys.COMMAND, "a")
        else:
            search_box.send_keys(Keys.CONTROL, "a")
        search_box.send_keys(Keys.BACKSPACE)
        time.sleep(1)

        # Enter search term and submit
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        print(f"Searching for: {query}")

        # Wait for product titles to appear on page
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-locator^="search-product-tile-title"]')))
        # Wait an additional 2 seconds to allow the rest of the dynamic content to fully render
        time.sleep(2)

        # Grab product tile elements (limit to top 10)
        product_containers = driver.find_elements(By.CSS_SELECTOR, '[data-locator^="search-product-tile-index-"]')

        for container in product_containers[:10]:
            try:
                # Extract Title
                title_elem = container.find_element(By.CSS_SELECTOR, '[data-locator^="search-product-tile-title"]')
                title = title_elem.text.strip()

                # Extract Link
                link_elem = container.find_element(By.CSS_SELECTOR, 'a[data-locator^="image-rating-"]')
                link = link_elem.get_attribute("href")

                # Extract Price
                price_elem = container.find_elements(By.CSS_SELECTOR, '[data-locator^="search-product-tile-price"]')
                if price_elem:
                    full_price_text = price_elem[0].text.strip().replace("\n", "")
                    price = full_price_text if full_price_text else "N/A"
                else:
                    price = "N/A"

                # Print and save scraped product info
                print(f"{title} | {price} | {link}")
                product_data.append([timestamp, query, title, price, link])
            except Exception as e:
                print("Error extracting product:", e)

    except Exception as e:
        print("Could not search:", e)

# -------------------------------
# SAVE SCRAPED DATA TO CSV
# -------------------------------

file_exists = os.path.isfile("bunnings_scrape.csv")

# Append results to CSV (create header if file doesn't exist)
with open("bunnings_scrape.csv", "a", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(["Timestamp", "SearchTerm", "Title", "Price", "URL"])
    writer.writerows(product_data)

print("Data appended to bunnings_scrape.csv")

# Close the browser
driver.quit()