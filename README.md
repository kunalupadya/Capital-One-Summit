# Capital-One-Summit
Repository for website for Capital One Summit

Includes the programs created for data analysis, as well as the django/heroku app that defines the structure of the website for data visualization.


Guide to Project:

This project was created using Django and hosted using Heroku. I performed all data analysis using pandas, using matplotlib, seaborn, and tableau for data visualization.

I began by loading the data file and cleaning it, removing any rows that had null station IDs. I then performed my analysis on the data (analysis.py, found in data_analysis). I used tableau to plot stations geographically to visualize the most popular stations, but everything else was displayed using matplotlib and seaborn. 

Some of the more interesting challenges I faced were:
1. Calculating distance - I ended up using the law of Haversines to calculate distance from start station to end station, but this was only applicable to one-way trips. For round trips, I had to extrapolate distance from duration of each trip, which may have been inaccurate.

2. Displaying station visits - I wanted to display the data using a table that did not take up too much space, so I learned how to use an interactive table plugin from Datatables.net to create a searchable, expandable, paginated table that uses jquery.

3. Displaying station locations - I wanted a way to display station locations on a map that accurately showed where in Los Angeles each station was, while also showing the number of uses each station had. In order to do this effectively, I opted to use Tableau. In doing this, I was able to create a geographically accurate map that plotted stations with their usage indicated by size and color of the marker.

My code is structured in Django convention, where the directory "data" contains all the app information (models, views, url patterns) while the directory "capitalonesummit" contains django settings and deployment settings. As mentioned before, the "data_analysis" directory holds the python file which I created to perform all analysis.
