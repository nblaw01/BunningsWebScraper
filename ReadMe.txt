BUNNINGS WEB SCRAPER
--------------------

This Python script automates product searches on the Bunnings Australia website using Selenium. 
It performs searches based on predefined keywords, scrapes key product info (title, price, and URL), 
and appends the results to a local CSV file.

FEATURES
--------
- Optional headless Chrome browser automation
- Run limit using a configurable counter (run_count.txt) to use in conjunction with cron automation
- Customisable list of search terms
- Scrapes product title, price, and URL (top 10 results per search)
- Appends results to: bunnings_scrape.csv
- Works on macOS and Windows (adjusts keyboard shortcuts accordingly)

USAGE

1. Install Python 3 and pip if not already installed.
2. Install dependencies:
   pip install selenium
3. Download ChromeDriver:
4. Run the script:
   python bunnings_scraper.py

   This will launch Chrome, perform searches, and save the results in 'bunnings_scrape.csv'.

RUN COUNT MANAGEMENT
--------------------
To ensure it only runs for a month in con junction with automation I set up using cron, the script 
limits how many times it can be run using a run count file (run_count.txt).
If the count reaches MAX_RUNS (default: 31), the script will exit.

This is managed in 'runCount_config.py'.

You can reset  or remove the count by deleting or editing 'run_count.txt'.

CONFIGURATION
-------------
You can modify the following:

- MAX_RUNS (in runCount_config.py): Sets how many runs are allowed before stopping
- search_terms (in bunnings_scraper.py): List of keywords to search (e.g., ["hammer", "drill"])
- To run in headless mode, uncomment the chrome_options.add_argument("--headless") line

OUTPUT
------
The script saves data to:
bunnings_scrape.csv

Each row includes:
- Timestamp
- Search term
- Product title
- Price
- Product URL

FOLDER STRUCTURE
----------------
Bunnings WebScraper/
├── runCount_config.py        # Run limit logic
├── run_count.txt             # Tracks usage count
├── bunnings_scraper.py       # Main script
├── bunnings_scrape.csv       # Output data (created on first run)

KNOWN ISSUES
------------
- Dynamic site elements may sometimes fail to load.
- If the site blocks automation, reduce run frequency or try a different user agent.

AUTHOR
------
Nick Lawler