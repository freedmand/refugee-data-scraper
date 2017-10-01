# Refugee Data Scraper

Scrapes day-by-day immigration data from refugees of all countries to US counties starting from present and working back until 2002 (the start of the data collection).

http://ireports.wrapsnet.org/Interactive-Reporting/EnumType/Report?ItemPath=/rpt_WebArrivalsReports/MX%20-%20Arrivals%20by%20Destination%20and%20Nationality

## Usage

```
python main.py
```

## Extracted files

The extracted CSV files can be found in `extracted/`.

## Limitations

A few of the extracted CSV files contain an error page in HTML. The dates corresponding to these CSV files need to be rescraped.

## Next steps

* Clean up the CSV files (some rows repeat the header row)
* Parse data from the CSV files
* Continue scraping until 1/1/2002 (the start)
* Rescrape CSV files that contain errors
* Make cool visualizations!
