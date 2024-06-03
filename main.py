#   Smith River
#   Directed Studies Python
#   Creates a map of the USA showing which county voted for which party. Uses the data stored from Zillow requests in postgreSQL database to create markers of each property and their location.
import folium
import requests
import pandas as pd
import time
import geopandas as gpd
from zillowDB import getTableInfo

def usaMap():   #Sets the map to middle of the USA
    print("setting map to USA\n")
    mapOfUSA = folium.Map(location = (38, -102), zoom_start=5)
    return mapOfUSA

def fixFipID(df):   #Fixes the data table's way of establishing state codes.
    for k,v in df["features"].items():
        if len(v['id']) < 5:
            v['id'] = '0' + v['id']

def fixVoterMap(df):    
    test = getVoterData()

    for item in df['features']:
        item.update({'id':list(state_codes.keys())[list(state_codes.values()).index(item['id'][0:2])]})
        item.update({'party':"bad"}) #Shows parties that weren't identitifed
        
        for i in list(enumerate(test)): 
            if test[i[0]]['state'] == item['id'] and test[i[0]]['county']==item['properties']['name']:
                item.update({'party':test[i[0]]['party']})

def editGeoData(geoData):   #Controls the methods that will be translating all data requested.
    print("adding voter data per county\n")
    df = pd.DataFrame.from_dict(geoData)
    fixFipID(df)
    fixVoterMap(df)
    return df['features']

def fixCountyNames(row):    #Data table had incorrect spelling and identification of counties that would cause invalid data.
    row['county'] = row['county'].replace('LaSalle County','La Salle')
    row['county'] = row['county'].replace(' County','')
    row['county'] = row['county'].replace(' Parish','')
    row['county'] = row['county'].replace(' Cty Townships','')
    row['county'] = row['county'].replace(' Cty Townshps','')
    row['county'] = row['county'].replace('ED 10','North Slope')
    row['county'] = row['county'].replace('ED 11','Northwest Arctic')
    row['county'] = row['county'].replace('ED 12','Yukon-Koyukuk')
    row['county'] = row['county'].replace('ED 13','Nome')
    row['county'] = row['county'].replace('ED 14','Fairbanks North Star')   #Everything below is simply a trial and error for what each ED # is which county in alaska. Just brute force it.
    row['county'] = row['county'].replace('ED 15','')   
    row['county'] = row['county'].replace('ED 16','')
    row['county'] = row['county'].replace('ED 17','')
    row['county'] = row['county'].replace('ED 18','')
    row['county'] = row['county'].replace('ED 19','')
    row['county'] = row['county'].replace('ED 20','')
    row['county'] = row['county'].replace('ED 21','')
    row['county'] = row['county'].replace('ED 22','')
    row['county'] = row['county'].replace('ED 23','')
    row['county'] = row['county'].replace('ED 24','')
    row['county'] = row['county'].replace('ED 25','')
    row['county'] = row['county'].replace('ED 26','')
    row['county'] = row['county'].replace('ED 27','')
    row['county'] = row['county'].replace('ED 28','')
    row['county'] = row['county'].replace('ED 29','')
    row['county'] = row['county'].replace('ED 30','')
    row['county'] = row['county'].replace('ED 31','')
    row['county'] = row['county'].replace('ED 32','')
    row['county'] = row['county'].replace('ED 33','')
    row['county'] = row['county'].replace('ED 34','')
    row['county'] = row['county'].replace('ED 35','')
    row['county'] = row['county'].replace('ED 36','')
    row['county'] = row['county'].replace('ED 37','')
    row['county'] = row['county'].replace('ED 38','')
    row['county'] = row['county'].replace('ED 39','')
    row['county'] = row['county'].replace('ED 40','')
    return row

def getVoterData():     #gets the voter data info for each county from a downloaded data table. Change file path to your current one.
    print("Retrieving voter data by county\n")
    ls = []
    elections = pd.read_csv(r"C:\Users\RS\Downloads\president_county_candidate.csv",usecols=['state','county','party','won'])
    countyWon = elections[elections['won']==True]

    for index,row in countyWon.iterrows():
         row = row.to_dict()
         row = fixCountyNames(row)
         ls.append(row)
    return ls

def getGeoData(url):    #gets the data needed for creating the counties on the folium map
    print("Requesting GeoData Info...\n")
    geoData = requests.get(url).json()
    editGeoData(geoData)

    return geoData

def getColor(feat):     #Sets the color of each county for what they voted for
    if feat['party'] == 'DEM':
        return 'blue'
    if feat['party'] == 'REP':
        return 'red'
    return 'blue'       #This could be set to a different color for invalids but this should not happen if the data sets were worded properly.

def markerInfo():   #gets the info for the 5 test states
    info = []
    subList = ['mi','oh','in','il','wi']
    for state in subList:
        info.append(getTableInfo(state))
    return info
  
def makeMap():      #Applies all data retrieved and translated to the map
    print("Making Map Borders\n")
    mapUSA = usaMap()
    countyData = getGeoData(countyJson)

    folium.GeoJson(countyData,      #Changes the way the borders work in the map and counties.
                   name="test",
                   style_function=lambda x:{   
                                            'color': 'black',
                                            'fillColor': getColor(x),
                                            'fillOpacity': 0.3
                                            }).add_to(mapUSA)                                    
    markers = markerInfo()          
    for i in range(len(markers)):       #Creates the markers on the map
        print(markers[i][0][2],markers[i][0][3])
        folium.Marker(location =[markers[i][0][2],markers[i][0][3]], popup=folium.Popup("""
                                                                                        <img src="{}"
                                                                                        <img style="width:100%; height:100%;">
                                                                                        <h2>
                                                                                        {}
                                                                                        </h2>
                                                                                        <h4>
                                                                                        Price:{}
                                                                                        </h4>
                                                                                        <h4>
                                                                                        Beds:{}
                                                                                        </h4>
                                                                                        <h4>
                                                                                        Baths:{}
                                                                                        </h4>
                                                                                        <h4>
                                                                                        Sqft:{}
                                                                                        </h4>
                                                                                        <h5> <a href="{}">Listing </a> </h5>
                                                                                        """.format(markers[i][0][9], markers[i][0][0], markers[i][0][1], markers[i][0][4], markers[i][0][5], markers[i][0][6], markers[i][0][8]),max_width=500)).add_to(mapUSA) 

    mapUSA.save('USAcountyMap.html')    #pushes the changes to the map file

state_codes = {     #used to help translate data set.
    'Washington': '53', 'Delaware': '10', 'District of Columbia': '11', 'Wisconsin': '55', 'West Virginia': '54', 'Hawaii': '15',
    'Florida': '12', 'Wyoming': '56', 'Puerto Rico': '72', 'New Jersey': '34', 'New Mexico': '35', 'Texas': '48',
    'Louisiana': '22', 'North Carolina': '37', 'North Dakota': '38', 'Nebraska': '31', 'Tennessee': '47', 'New York': '36',
    'Pennsylvania': '42', 'Alaska': '02', 'Nevada': '32', 'New Hampshire': '33', 'Virginia': '51', 'Colorado': '08',
    'California': '06', 'Alabama': '01', 'Arkansas': '05', 'Vermont': '50', 'Illinois': '17', 'Georgia': '13',
    'Indiana': '18', 'Iowa': '19', 'Massachusetts': '25', 'Arizona': '04', 'Idaho': '16', 'Connecticut': '09',
    'Maine': '23', 'Maryland': '24', 'Oklahoma': '40', 'Ohio': '39', 'Utah': '49', 'Missouri': '29',
    'Minnesota': '27', 'Michigan': '26', 'Rhode Island': '44', 'Kansas': '20', 'Montana': '30', 'Mississippi': '28',
    'South Carolina': '45', 'Kentucky': '21', 'Oregon': '41', 'South Dakota': '46'
}

us_state_to_abbrev = {  #used to help translate data set
    "Alabama": "AL","Alaska": "AK","Arizona": "AZ","Arkansas": "AR",
    "California": "CA","Colorado": "CO","Connecticut": "CT","Delaware": "DE","Florida": "FL","Georgia": "GA","Hawaii": "HI","Idaho": "ID",
    "Illinois": "IL","Indiana": "IN","Iowa": "IA","Kansas": "KS","Kentucky": "KY","Louisiana": "LA","Maine": "ME","Maryland": "MD","Massachusetts": "MA",
    "Michigan": "MI","Minnesota": "MN","Mississippi": "MS","Missouri": "MO","Montana": "MT","Nebraska": "NE","Nevada": "NV","New Hampshire": "NH",
    "New Jersey": "NJ","New Mexico": "NM","New York": "NY","North Carolina": "NC","North Dakota": "ND","Ohio": "OH","Oklahoma": "OK","Oregon": "OR",
    "Pennsylvania": "PA","Rhode Island": "RI","South Carolina": "SC","South Dakota": "SD","Tennessee": "TN","Texas": "TX","Utah": "UT","Vermont": "VT",
    "Virginia": "VA","Washington": "WA","West Virginia": "WV","Wisconsin": "WI","Wyoming": "WY","District of Columbia": "DC","American Samoa": "AS",
    "Northern Mariana Islands": "MP","Puerto Rico": "PR","United States Minor Outlying Islands": "UM","U.S. Virgin Islands": "VI",
}

countyJson = "https://raw.githubusercontent.com/python-visualization/folium/main/tests/us-counties.json"
makeMap()
