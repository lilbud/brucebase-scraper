# brucebase-scraper
Python script to scrape setlists from Brucebase

Note: [Python](https://www.python.org/downloads/) needed to run this script, as well as the following modules
  requests (pip install requests)
  BeautifulSoup (pip install BeautifulSoup4)
  
Program will not run without the above modules

Current options:
  Get setlist from a specified date (YYYY-MM-DD)
  Get setlist from a specified month (YYYY-MM-DD)
  Get setlist from a specified year (YYYY) <- I'm not sure how well this works with larger years
  
Repl test version: https://replit.com/@lilbud/Brucebase-Scraper?v=1
(Note: can't export, also only full date option)

In the file, you can set the export directory. By default it is set to your Documents folder, though this can be changed. It will still create a new folder in that directory, as well as subdirectories for Year and Month.

Depending on internet connection, larger requests could be slow
