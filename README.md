# brucebase-scraper

# WARNING: I AM NOT REPONSIBLE FOR WHAT YOU USE THIS SCRAPER FOR
### This is my first web scraper and I don't how (if at all) it could affect the brucebase site

Python script to scrape setlists from Brucebase

Original concept by Superzann: [here](https://docs.google.com/spreadsheets/d/1ptVECBzRQs3AHBuDyJu19T0X7W04JLEv9soobJI0TU0/edit?usp=drivesdk)

Note: [Python](https://www.python.org/downloads/) needed to run this script, as well as the following modules
### Program will not run without these modules
  - requests (pip install requests)
  - BeautifulSoup (pip install BeautifulSoup4)

Current options:
  
  - Get setlist from a specified date (YYYY-MM-DD)
  - Get setlist from a specified month (YYYY-MM-DD)
  - Get setlist from a specified year (YYYY) <- I'm not sure how well this works with larger years
  
Repl test version: https://replit.com/@lilbud/Brucebase-Scraper?v=1
(Note: can't export, also only full date option)

In the file, you can set the export directory. By default it is set to your Documents folder, though this can be changed. It will still create a new folder in that directory, as well as subdirectories for Year and Month.

Depending on internet connection, larger requests could be slow
