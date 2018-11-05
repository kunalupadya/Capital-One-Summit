import pandas as pd
import math
import operator
import data_analysis.data_to_html as dh
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import csv
import datetime

imgpat = "/Users/kunalupadya/python_projects/capitalonesummit/data/static/img/"
pat = "/Users/kunalupadya/python_projects/capitalonesummit/data/static/my_data/"

def calc_dist(lat1,long1,lat2,long2):
    '''Calculates distance between latitudes and longitudes using the haversine formula, returns distance in miles'''
    r = 6371 #radius of earth
    deltalat = math.radians(lat2-lat1)
    deltalong = math.radians(long2-long1)
    a = math.sin(deltalat/2) * math.sin(deltalat/2) + \
    math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
    math.sin(deltalong/2) * math.sin(deltalong/2)
    c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a))
    d = r*c #distance in km
    d = d * 0.621371
    return d
#load data
data = pd.read_csv('/Users/kunalupadya/python_projects/capitalonesummit/data_analysis/los-angeles-metro-bike-share-trip-data/metro-bike-share-trip-data.csv')

#cleaning data
bads = list(data.index[(data["Ending Station Latitude"]==0) | (data["Ending Station Longitude"]==0) | (data["Starting Station Latitude"]==0) | (data["Starting Station Longitude"]==0)])
nulls = list(data.index[(data["Ending Station Latitude"].isnull()) | (data["Ending Station Longitude"].isnull()) | (data["Starting Station Latitude"].isnull()) | (data["Starting Station Longitude"].isnull())])
bads = bads + nulls
data.drop(bads,axis=0, inplace=True)

#make fields datetime objects
data['Start Time'] = pd.to_datetime(data['Start Time'])
data['End Time'] = pd.to_datetime(data['End Time'])



speed = 0.0012587537086655816 #speed in miles per second, calculated by taking the distance and dividing by duration (in seconds) for all one way trips
#count the number of occurrences of each station to 
stationstartmap = {}
stationstopmap = {}
startmaplocs = {}
stopmaplocs = {}
dists = []
one_way_only = []
##average trip length
# print(data.head().to_string())
for index, row in data.iterrows():
    startstat = int(row['Starting Station ID'])
    stopstat = int(row['Ending Station ID'])
    lat1 = row['Starting Station Latitude']
    long1 = row['Starting Station Longitude']
    lat2 = row['Ending Station Latitude']
    long2 = row['Ending Station Longitude']
    if row['Trip Route Category']=='One Way':
        dist = calc_dist(lat1,long1, lat2, long2)
        one_way_only.append(dist)
        dists.append(dist)
    else:
        dist = speed*row['Duration']
        if dist<15:
            dists.append(dist)
    if startstat not in stationstartmap:
        stationstartmap[startstat] = 1
        startmaplocs[startstat] = (row['Starting Station Latitude'],row['Starting Station Longitude'])
    else:
        stationstartmap[startstat] += 1
    if stopstat not in stationstopmap:
        stationstopmap[stopstat] = 1
        stopmaplocs[stopstat] = (row['Ending Station Latitude'], row['Ending Station Longitude'])
    else:
        stationstopmap[stopstat] += 1

sorted_start = sorted(stationstartmap.items(), key=operator.itemgetter(1))
sorted_stop = sorted(stationstopmap.items(), key=operator.itemgetter(1))
sorted_start.reverse()
sorted_stop.reverse()

with open(pat+'startstat.csv', mode='w') as statfile:
    writeme = csv.writer(statfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writeme.writerow(['Station', 'Occurrence', 'Latitude', 'Longitude'])
    for key, value in stationstartmap.items():
        temp = startmaplocs[key]
        writeme.writerow([key, value, temp[0],temp[1]])

with open(pat+'stopstat.csv', mode='w') as statfile:
    writeme = csv.writer(statfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writeme.writerow(['Station', 'Occurrence', 'Latitude', 'Longitude'])
    for key, value in stationstopmap.items():
        temp = stopmaplocs[key]
        writeme.writerow([key, value, temp[0],temp[1]])



#get summary statistics for data
# one way
print('one way')
distframe = pd.Series(one_way_only)
print(distframe.describe())

print('all')
distframe = pd.Series(dists)
print(distframe.describe())

dist_distribution = plt.figure()
ax=dist_distribution.add_subplot(111)
sns.distplot(dists, bins= 100)
ax.set_xlim(left=0,right = 5)
# ax.Axes.set_xlim(right=8)
plt.xlabel('Distance (miles)')
plt.ylabel('Density')
plt.title('Density of Distance Travelled per Bike Ride')
plt.savefig(imgpat+'distance_distribution.png')
plt.show()


dist_distribution = plt.figure()
ax=dist_distribution.add_subplot(111)
sns.distplot(one_way_only, bins= 100)
ax.set_xlim(left=0,right = 5)
# ax.Axes.set_xlim(right=8)
plt.xlabel('Distance (miles)')
plt.ylabel('Density')
plt.title('Density of Distance Travelled per Bike Ride')
plt.savefig(imgpat+'distance_distribution_one_way.png')
plt.show()


# data.between_time('0:15', '0:45')

## creates data tables
starttable = dh.tuplev(sorted_start) #start data, returned as an html table
endtable = dh.tuplev(sorted_stop) #stop data, returned as an html table
with open(pat + "starttable.txt", "w") as text_file:
    text_file.write(starttable)
with open(pat + "endtable.txt", "w") as text_file:
    text_file.write(endtable)

# print()
# print(sorted_start)
# print(sorted_stop)
# clean_data =


## used to calculate the number of users per year
weekind = data['Start Time'][0].weekofyear
weeks = []
commuters = []
numriders = []
numflexers = []
numwalk = []
nummonthlies = []
while weekind !=14:
    weekdf = data.loc[data['Start Time'].dt.weekofyear == weekind, :].reset_index(drop=True)
    weeks.append(weekdf['Start Time'][0])
    weeklycommuters = 0
    commutersset = {}
    numriders.append(len(weekdf))
    flexers = weekdf[weekdf['Passholder Type']=='Flex Pass']
    numflexers.append(len(flexers))
    monthlies = weekdf[weekdf['Passholder Type'] == 'Monthly Pass']
    nummonthlies.append(len(monthlies))
    walkers = weekdf[weekdf['Passholder Type'] == 'Walk-up']
    numwalk.append(len(walkers))
    for k in range(7):
            day1 = weekdf['Start Time'][0].dayofyear + k
            dayones = weekdf.loc[weekdf['Start Time'].dt.dayofyear== day1,:].reset_index(drop=True)
            # day2 = weekdf['Start Time'][0].dayofyear + j
            # daytwos = weekdf.loc[weekdf['Start Time'].dt.dayofyear == day2, :].reset_index(drop=True)
            for index, row in dayones.iterrows():
                stid = row['Starting Station ID']
                enid = row['Ending Station ID']
                time1 = row['Start Time'].hour
                time2 = row['End Time'].hour
                # comp = daytwos.loc[(daytwos['Starting Station ID'] == stid) & (daytwos['Ending Station ID'] == enid) & ((daytwos['Start Time'].dt.hour == time1) | (daytwos['End Time'].dt.hour == time2)), ['Starting Station ID', 'Ending Station ID', 'Start Time', 'End Time']]
                # if len(comp) != 0: # indicates that there is an entry in another day at the same time going from the same starting location to the ending location
                strrep = str(row['Starting Station ID']) + str(row['Ending Station ID']) + str(row['Start Time'].hour)+str(row['End Time'].hour)
                if strrep not in commutersset:
                        # weeklycommuters +=1
                    commutersset[strrep] = 1
                else:
                    commutersset[strrep] += 1
                    if commutersset[strrep] == 3:
                        weeklycommuters +=1
                    if commutersset[strrep] == 4:
                        commutersset[strrep] = 1

    commuters.append(weeklycommuters)
    weekind +=1
    weekind = weekind % 53
    if weekind ==0:
        weekind +=1
    print(commuters)
    print(weekind)

commute = plt.figure()
ax = commute.add_subplot(111)
plt.plot(weeks, commuters, 'bo-')
plt.xlabel('Month')
plt.title('Number of Commuters using Bike Sharing Service by week')
plt.ylabel('Number of Commuters')
distframe = pd.Series(commuters)
print(distframe.describe())
myFmt = mdates.DateFormatter('%b')
ax.xaxis.set_major_formatter(myFmt)
plt.setp(plt.gca().xaxis.get_majorticklabels(),'rotation', 45)
plt.gcf().subplots_adjust(bottom=0.2)
plt.savefig(imgpat + 'commuters_over_time4.png')
plt.show()

numrides = plt.figure()
ax = numrides.add_subplot(111)
plt.plot(weeks, numriders, 'bo-')
plt.xlabel('Month')
plt.title('Number of People using Bike Sharing Service by week')
plt.ylabel('Number of Riders')
distframe = pd.Series(numriders)
print(distframe.describe())
myFmt = mdates.DateFormatter('%b')
ax.xaxis.set_major_formatter(myFmt)
plt.setp(plt.gca().xaxis.get_majorticklabels(),'rotation', 45)
plt.gcf().subplots_adjust(bottom=0.2)
plt.savefig(imgpat + 'numriders.png')
plt.show()


percflex = []
percmonth = []
percwalk = []
for k in range(len(nummonthlies)):
    percflex.append(numflexers[k]/numriders[k])
    percmonth.append(nummonthlies[k] / numriders[k])
    percwalk.append(numwalk[k] / numriders[k])

flexmonth = plt.figure()
print(percflex)
print(percmonth)
print(percwalk)
ax = flexmonth.add_subplot(111)
plt.plot(weeks, percflex, 'bo-', label='Percentage of Flex Pass Users')
plt.plot(weeks, percmonth, 'ro-', label='Percentage of Monthly Pass Users')
plt.plot(weeks, percwalk, 'go-', label='Percentage of Walk-up Pass Users')
plt.legend()
plt.xlabel('Month')
plt.title('Change in Pass Types Used Over Time')
plt.ylabel('Percentage of passes')
distframe = pd.Series(numriders)
print(distframe.describe())
myFmt = mdates.DateFormatter('%b')
ax.xaxis.set_major_formatter(myFmt)
plt.setp(plt.gca().xaxis.get_majorticklabels(),'rotation', 45)
plt.gcf().subplots_adjust(bottom=0.2)
plt.savefig(imgpat + 'pass_type.png')
plt.show()

print(numriders)
print(numflexers)
print(nummonthlies)



# same thing except with times
timeind = 0
times = []
numriders = []
x = [datetime.datetime(2018,10,31,0,0) + datetime.timedelta(hours=i) for i in range(24)]
while timeind !=24:
    weekdf = data.loc[data['Start Time'].dt.hour == timeind, :].reset_index(drop=True)
    numriders.append(len(weekdf))
    # for k in range(7):
    #         day1 = weekdf['Start Time'][0].dayofyear + k
    #         dayones = weekdf.loc[weekdf['Start Time'].dt.dayofyear== day1,:].reset_index(drop=True)
    #         # day2 = weekdf['Start Time'][0].dayofyear + j
    #         # daytwos = weekdf.loc[weekdf['Start Time'].dt.dayofyear == day2, :].reset_index(drop=True)
    #         for index, row in dayones.iterrows():
    #             stid = row['Starting Station ID']
    #             enid = row['Ending Station ID']
    #             time1 = row['Start Time'].hour
    #             time2 = row['End Time'].hour
    #             # comp = daytwos.loc[(daytwos['Starting Station ID'] == stid) & (daytwos['Ending Station ID'] == enid) & ((daytwos['Start Time'].dt.hour == time1) | (daytwos['End Time'].dt.hour == time2)), ['Starting Station ID', 'Ending Station ID', 'Start Time', 'End Time']]
    #             # if len(comp) != 0: # indicates that there is an entry in another day at the same time going from the same starting location to the ending location
    #             strrep = str(row['Starting Station ID']) + str(row['Ending Station ID']) + str(row['Start Time'].hour)+str(row['End Time'].hour)
    #             if strrep not in commutersset:
    #                     # weeklycommuters +=1
    #                 commutersset[strrep] = 1
    #             else:
    #                 commutersset[strrep] += 1
    #                 if commutersset[strrep] == 3:
    #                     weeklycommuters +=1
    #                 if commutersset[strrep] == 4:
    #                     commutersset[strrep] = 1
    timeind +=1
    # timeind = timeind % 25
    # print(commuters)
    print(timeind)
times = plt.figure()
ax = times.add_subplot(111)
plt.plot(x,numriders)
plt.xlabel('Hour (in military time)')
plt.title('Number of Rides at Times in the Day')
plt.ylabel('Number of Rides')
myFmt = mdates.DateFormatter('%H')
ax.xaxis.set_major_formatter(myFmt)
plt.setp(plt.gca().xaxis.get_majorticklabels(),'rotation', 45)
plt.gcf().subplots_adjust(bottom=0.2)
plt.savefig(imgpat + 'hours.png')
plt.show()