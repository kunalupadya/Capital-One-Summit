import pandas as pd
import operator

#load data
data = pd.read_csv('/Users/kunalupadya/python_projects/capitalonesummit/data_analysis/los-angeles-metro-bike-share-trip-data/metro-bike-share-trip-data.csv')

#cleaning data
bads = list(data.index[(data["Ending Station Latitude"]==0) | (data["Ending Station Longitude"]==0) | (data["Starting Station Latitude"]==0) | (data["Starting Station Longitude"]==0)])
nulls = list(data.index[(data["Ending Station Latitude"].isnull()) | (data["Ending Station Longitude"].isnull()) | (data["Starting Station Latitude"].isnull()) | (data["Starting Station Longitude"].isnull())])
bads = bads + nulls
data.drop(bads,axis=0, inplace=True)

#count the number of occurrences of each station to 
stationstartmap = {}
stationstopmap = {}
print(data.head().to_string())
for index, row in data.iterrows():
    startstat = int(row['Starting Station ID'])
    stopstat = int(row['Ending Station ID'])
    if startstat not in stationstartmap:
        stationstartmap[startstat] = 1
    else:
        stationstartmap[startstat] += 1
    if stopstat not in stationstopmap:
        stationstopmap[stopstat] = 1
    else:
        stationstopmap[stopstat] += 1
sorted_start = sorted(stationstartmap.items(), key=operator.itemgetter(1))
sorted_stop = sorted(stationstopmap.items(), key=operator.itemgetter(1))
sorted_start.reverse()
sorted_stop.reverse()


print(sorted_start)
print(sorted_stop)
# clean_data =
