# Refugee Data Scraper

Scrapes day-by-day immigration data from refugees of all countries to US counties starting from present and working back until 2002 (the start of the data collection).

http://ireports.wrapsnet.org/Interactive-Reporting/EnumType/Report?ItemPath=/rpt_WebArrivalsReports/MX%20-%20Arrivals%20by%20Destination%20and%20Nationality

All data from 10/1/2017 to 1/1/2002 (US date format) is included in the `extracted/` directory.

## Usage

```
python main.py
```

## Extracted files

The extracted CSV files can be found in `extracted/`.

## Next steps

* Clean up the CSV files (some rows repeat the header row)
* Parse data from the CSV files
* Make cool visualizations!
