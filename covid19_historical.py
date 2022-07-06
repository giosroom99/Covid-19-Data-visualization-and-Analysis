import requests
import json
import mysql.connector
import datetime
from datetime import date
import calendar
from secret import key
from mail import send_update
from logFile import Status_Report



def driver():
    ###     ----Variables---
    base_url = "https://covid-api.mmediagroup.fr/v1/history?country="

    # Get a list of countries.
    countries = get_countries()
    # Connect to DB
    mydb =db_connect()
    get_historical(base_url,mydb,countries)
    
    
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

    except BaseException as error: 
        print("An error has occured while trying to get country list.",error)
        code =error
        message="An error has occured while trying to get country list."
        Status_Report(code,message)
        send_update(code,message)
        return False

def db_connect():
    try:
        mydb = mysql.connector.connect(
            host=key.get('HOST'),
            user=key.get('USER'),
            password=key.get('PASSWORD'),
            database=key.get('DATABASE')
        )
        code="Sucess"
        message="Database connected"
        Status_Report(code,message)
        send_update(code,message)
        return mydb
    except mysql.connector.Error as err:
        print("An error has occured while trying to connect to database \n Error: ",err)
        code="Error DB"
        message=err
        Status_Report(code,message)
        send_update(code,message)
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
                    print("An error has occured in the database Insertion. \n Error: ",errdb)
                    code="Error DB Insert"
                    message=errdb
                    Status_Report(code,message)
                    send_update(code,message)

        except KeyError:
            print(KeyError,' for ',country)
            code="Error in country{0}".format(country)
            message=KeyError
            Status_Report(code,message)
           # send_update(code,message)
            



driver()