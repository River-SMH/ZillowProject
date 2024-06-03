#   Smith River
#   Directed Studies Python
#   Handles the creation and storage of tables and its data.
import time
import psycopg2

def makeConnection(): #Establishes the connection to the postgreSQL database
    connect = psycopg2.connect(host="localhost",dbname="postgres",user="postgres",password="123",port=5432)
    cur = connect.cursor()
    return(cur,connect)

def  closeConnection(cur,connect): #Closes out the connection to avoid data leaks.
    cur.close()
    connect.close()

def createTable(aState):    #Creates a table of the state if it doesn't already exist
    cur,connect = makeConnection()
    cur.execute("""CREATE TABLE IF NOT EXISTS {}_properties (
                address VARCHAR(255),
                pricing VARCHAR(255),
                lat VARCHAR(255),
                long VARCHAR(255),
                beds VARCHAR(255),
                baths VARCHAR(255),
                sqft VARCHAR(255),
                party VARCHAR(255),
                link VARCHAR(255),
                image VARCHAR(255)
                )
            """.format(aState))
    connect.commit()
    closeConnection(cur,connect)
    
def addToTable(aState,data):    #Appends the property info for each state
    cur,connect = makeConnection()
    cur.execute("""INSERT INTO {}_properties (address,pricing,lat,long,beds,baths,sqft,link,image) SELECT
                '{}','{}','{}','{}','{}','{}','{}','{}','{}' WHERE NOT EXISTS(SELECT 1 FROM {}_properties WHERE address='{}');
            """.format(aState,data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],aState,data[0]))   
    connect.commit()
    closeConnection(cur,connect)

def updateParty(aState,party):  #Updates the party tab in the postgreSQL database referencing the data table retrieved from main.
    cur,connect = makeConnection()
    cur.execute("""INSERT INTO {}_properties (party) VALUES {}""".format(aState,party))
    connect.commit()
    closeConnection(cur,connect)
    

def getTableInfo(aState):   #Returns table information
    cur,connect = makeConnection()
    aList =[]
    time.sleep(1)
    cur.execute("""SELECT * FROM {}_properties;""".format(aState))
    for i in cur.fetchall():
        aList.append(i)
    closeConnection(cur,connect)
    return aList
