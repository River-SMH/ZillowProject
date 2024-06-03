#   Smith River
#   Directed Studies Python
#   Handles the requests and web scrapes the information needed for the database. Has a test case at the bottom due to an issue of being blocked by the website and them changing their request layout.
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import zipcodes
from zillowDB import createTable, addToTable

headers = {                 #Headers for request
    'authority': 'www.zillow.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'sec-ch-ua': '"Not A(Brand";v="99", "Opera GX";v="107", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0',
}

def getLatLong(address):   #Gets the lat and long of the address to place on the map
    try:
        geoloc = Nominatim(user_agent="Geopy Library")
        l = geoloc.geocode(address)

        return(l.latitude,l.longitude)
    except:
        print("{} is not in Nominatim".format(address))
        return(None)
    
def dataCollected(properties,propImg):      #Extracts the info retrieved from the request. This was working on a version of zillow April 2024.
    l=list()
    obj = {}
    for x in range(0,len(properties)): 
                try:    
                    b = properties[x].find("a",{"class":"StyledPropertyCardDataArea-c11n-8-100-7__sc-10i1r6-0 izzuNb property-card-link"}).text
                    obj["address"] = b
                except:
                    obj['address'] = None

                try:             
                    obj["pricing"] = properties[x].find("div",{"class":"StyledPropertyCardDataArea-c11n-8-100-7__sc-10i1r6-0 imqyAK"}).text
                except:
                    obj["pricing"] = None

                try:
                    cord = getLatLong(properties[x].find("a",{"class":"StyledPropertyCardDataArea-c11n-8-100-7__sc-10i1r6-0 izzuNb property-card-link"}).text)
                    obj["lat"] = cord[0]
                    obj["long"] = cord[1]
                except:
                    obj["lat"] = None
                    obj["long"] = None        
                    
                try:
                    obj["beds"] = properties[x].find('li').text
                except:
                    obj["size"] = None

                try:
                    obj["baths"] = properties[x].find('li').find_next('li').text
                except:
                    obj["size"] = None

                try:
                    obj["sqft"] = properties[x].find('li').find_next('li').find_next('li').text
                except:
                    obj["size"] = None

                try:
                    obj["link"] = propImg[x].find('a')['href']
                except:
                    obj["link"] = None
                
                try: 
                    obj["img"] = propImg[x].find('source')['srcset']
                except:
                    obj["img"] = None

                l.append(obj)
                obj={}
    return l

def insertData(data,page):
    for aProp in range(len(data)):
        l = list()
        for k,v in data[aProp].items():
            l.append(v)
        print(l)
        addToTable(page,l)

def getPage():      #originally designed to grab every state's first page results prior to being blocked by zillow.

    l = list()
    ll = map(lambda x:x.lower(),["AK", "AL"])#, "AR", "AZ", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "IA",
        # "ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN", "MO",
        # "MS", "MT", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK",
        # "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI",
        # "WV", "WY","DC","AS", "MP", "PR", "VI"])
    url = 'https://www.zillow.com/homes/for_sale/{}/1_p/'

    for page in ll:             #makes a request with each state
        createTable(page)
        print(url.format(page))
        request = requests.get(url.format(page),headers = headers).text
        time.sleep(60)                                                  #60 second wait time to avoid being blocked by zillow.
        soup = BeautifulSoup(request,'html.parser')
        print(soup)
        properties = soup.find_all("div",{"class":"StyledPropertyCardDataWrapper-c11n-8-100-7__sc-hfbvv9-0 bmhhEb property-card-data"})
        propImg = soup.find_all("div",{"class":"StyledPropertyCardPhotoWrapper-c11n-8-100-7__sc-1gbptz1-0 dEJjQu"})
        data = dataCollected(properties,propImg)
        insertData(data,page)


#getPage()
#####################TEST CODE BELOW##################

def stateProperty(): #Test 5 previous listings from zillow.
    states = ['mi','oh','in','il','wi']
    for i in states:
        createTable(i)
    listings = [['3167 Sandpoint Dr, Brighton, MI 48114','$315,000','42.556600','-83.745120','3','2','1,366','https://www.zillow.com/homedetails/3167-Sandpoint-Dr-Brighton-MI-48114/23929751_zpid/','https://photos.zillowstatic.com/fp/68c9fd8d0bf85335a8ef65adf0fccd2d-cc_ft_960.webp'],
                ['1232 Willow Bend Dr, Medina, OH 44256','$489,900','41.114400','-81.832370','4','5','3,587','https://www.zillow.com/homedetails/1232-Willow-Bend-Dr-Medina-OH-44256/34901777_zpid/','https://photos.zillowstatic.com/fp/c8824d4c1ffa1c6897f52cb46f68e39c-sc_1920_1280.webp'],
                ['9680 E Rio Grande Ave, Terre Haute, IN 47805','$379,900','39.564710','-87.267640','4','3','2,958','https://www.zillow.com/homedetails/9680-E-Rio-Grande-Ave-Terre-Haute-IN-47805/77142960_zpid/','https://photos.zillowstatic.com/fp/aae88176a84db8230870f267c47a3184-cc_ft_960.webp'],
                ['759 Taras Dr, Davis, IL 61019','$269,000','42.442950','-89.402780','3','3','3,128','https://www.zillow.com/homedetails/759-Taras-Dr-Davis-IL-61019/122360030_zpid/','https://photos.zillowstatic.com/fp/83339c0e86ab6a3e3db966053f813d33-cc_ft_960.webp'],
                ['1919 Bridgeview Dr, Neenah, WI 54956','$345,000','44.227240','-88.483350','4','3','2,036','https://www.zillow.com/homedetails/1919-Bridgeview-Dr-Neenah-WI-54956/40599555_zpid/','https://photos.zillowstatic.com/fp/ce96a7b54253c7669d4b707ef39541c0-cc_ft_960.webp']]
    for i in listings:
        print(i[0][-8:-6])
        addToTable(i[0][-8:-6],i)
    time.sleep(5)

stateProperty()

