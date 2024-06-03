# ZILLOW DATA PROJECT
* This project's goal was to extract property info from zillow's website, store the information gathered, and place it into an interactive map that displays the information. Project also includes voter data for each county. Blue = DEM, Red = REP
* Project uses Folium, Pandas, geopy, and requests mainly.
* The project did get blocked by Zillow after an attempt was made. It was blocked due to many requests being made within a short time.
* Project makes a request to Zillow and reads in what was sent back and attempts to scrape all releveant information for the project (Address, Price, Sqft, Img, etc).
* Zillow has changed their html structure so the webscraper no longer works after April 2024. 
* Project includes a test case of what would have been collected when not blocked and was used during April 2024.
* Project makes use of a couple of datasets that hold information regarding county borders and the voter data of each county.
* Project uses PostgreSQL for the database.
* Project outputs a html file.
* Project was for Python Directed Studies under NMU.
