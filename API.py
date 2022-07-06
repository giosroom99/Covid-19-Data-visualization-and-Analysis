import requests
import json
import mysql.connector
import datetime
from datetime import date
import calendar




def driver():
    ###     ----Variables---

    today = datetime.datetime.today()
    base_url = "https://covid-api.mmediagroup.fr/v1/history?country="
    #url_     = "https://covid-api.mmediagroup.fr/v1/cases?country=Germany&status=deaths"
    real_time_url ="https://covid-api.mmediagroup.fr/v1/cases?country="
    # url = "https://covid-api.mmediagroup.fr/v1/history?country=Germany&status=deaths"

    # Get a list of countries.
    countries = get_countries()
    # Connect to DB
    mydb =db_connect()
    
    my_date = date.today()
    day =calendar.day_name[my_date.weekday()]

    get_historical(base_url,mydb,countries)
    
    realtime(real_time_url,mydb,countries,today)
    



def get_countries():
    
    url = "https://countriesnow.space/api/v0.1/countries"
    lit_of_countries = []
    try:
        response = requests.get(url)
        data = response.text
        parse_json = json.loads(data)
        country_data = parse_json['data']
        for c in country_data:
            lit_of_countries.append(c['country'])
        return lit_of_countries
    except: 
        print("An error has occured while trying to get country list.",e)
        return False


def db_connect():
    try:
        mydb = mysql.connector.connect(
            host='192.254.186.163',
            user='giosroom_pyGio',
            password='myFord#05',
            database="giosroom_outsideTest"
        )
        return mydb
    except mysql.connector.Error as err:
        print("An error has occured while trying to connect to database \n Error: ",err)
        return False

def get_historical(base_url,mydb,countries):
    
    for country in countries:
        responseD = requests.get(base_url + country + "&status=deaths")
        responseC = requests.get(base_url + country + "&status=confirmed")
        responseR = requests.get(base_url + country + "&status=recovered")

        dataD = responseD.text
        dataC = responseC.text
        dataR = responseR.text

        try:
            parse_jsonD = json.loads(dataD)
            parse_jsonC = json.loads(dataC)
            parse_jsonR = json.loads(dataR)

            allD = parse_jsonD["All"]
            allC = parse_jsonC["All"]
            allR = parse_jsonR["All"]

            population = allD["population"]
            Continent = allD["continent"]

            datesD = allD["dates"]
            datesC = allC["dates"]
            datesR = allR["dates"]

            for date in datesR:
                print(Continent, country, population, date, ": Deaths:", datesD[date], "Confirmed: ", datesC[date],
                    "Recovered: ", datesR[date])
                try:
                    sql = 'INSERT INTO covid_data (Last_updated,Continent, country,population, deaths, confirmed, recorvered) VALUES (%s,%s,%s,%s,%s,%s,%s)'
                    val=(date,Continent,country,population,datesD[date],datesC[date],datesR[date])

                    mycursor = mydb.cursor()
                    mycursor.execute(sql,val)
                    mydb.commit()

                    print(date, country, "Task completed, db.commit")

                except mysql.connector.Error as errdb:
                    print("An error has occured in the database connection. \n Error: ",errdb)
                    

        except KeyError:
            print(KeyError, ' for ', country)
            

def realtime(real_time_url,mydb,countries,today):
    for country in  countries:
        response = requests.get(real_time_url+country)
        data = response.text

        try:
            parse_json = json.loads(data)
            all = parse_json["All"]

            deaths = all["deaths"]
            confirmed = all["confirmed"]
            recovered = all["recovered"]
            population = all["population"]
            Continent = all["continent"]
            print("Date:{6}, Continent: {0}, Contry: {1}, Population: {2}, Confirmed: {3}, Deaths: {4}, Recovered: {5}".format(Continent,country,population,confirmed,recovered,deaths, today))
            try:
                sql = 'INSERT INTO covid_data (Last_updated,Continent, country,population, deaths, confirmed, recorvered) VALUES (%s,%s,%s,%s,%s,%s,%s)'
                val=(today,Continent,country,population,deaths,confirmed,recovered)
                mycursor = mydb.cursor()
                mycursor.execute(sql,val)
                mydb.commit()
                print(country, "Task completed, db.commit")
               
            except mysql.connector.Error as errdb:
                print("An error has occured in the database connection. \n Error: ",errdb)
                

        except KeyError:
            print(KeyError,' for ',country)
            
      


driver()