# Capital-One-Summit
Repository for website for Capital One Summit

Includes the programs created for data analysis, as well as the django/heroku app that defines the structure of the website for data visualization.


Guide to Project:

This project was created using Django and hosted using Heroku. I performed all data analysis using pandas, using matplotlib, seaborn, and tableau for data visualization.

I began by loading the data file and cleaning it, removing any rows that had null station IDs. I then performed my analysis on the data (analysis.py, found in data_analysis). I used tableau to plot stations geographically to visualize the most popular stations, but everything else was displayed using matplotlib and seaborn.
