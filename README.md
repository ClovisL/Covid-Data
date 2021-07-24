# Covid-19 Data By Country
## Interactive Dashboard

An interactive website that takes the latest Covid data for 209 countries, using JSON files from https://github.com/owid/covid-19-data/tree/master/public/data.

An SQL database is created that imports the JSON files.
An HTML file under the /map folder opens a browser window that displays a heatmap for Covid data.


## How to use
From a terminal window (such as GitBash), the Flask app file must first be run using > python app.py

On a browser window, enter http://127.0.0.1:5000/

From either the dropdown list or the bubble map on the site, select a country to get the data and charts updated for that selection.

## Data shown on webpage
**For the selected country, the following info is diplayed:**

An info box with the most recent data for number of cases, deaths, vaccinations, and population.

A gauge showing what percentage of the population has been vaccinated.

A line graph showing 2 lines, one for cases and one for deaths, accross all months from the start of the data set to the end.

An info box and pie chart for variants of the virus.
