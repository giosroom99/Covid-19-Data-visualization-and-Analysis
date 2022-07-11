import requests
import json
import mysql.connector
import datetime
from datetime import date
import calendar
from secret import key
from mail import send_update
from logFile import Status_Report

today = datetime.datetime.today() # Get today time.



def driver():

    ###     ----Variables---

    
    real_time_url ="https://covid-api.mmediagroup.fr/v1/cases?country="
    countries = get_countries() # Get a list of countries.
    
    mydb =db_connect()  # Connect to DB
    print(mydb) # Print DB object

    realtime(real_time_url,mydb,countries,today) # This function collect real time data from API
    Status_Report("Finish"+today,"ALL Fectched")
    send_update("Finish"+today,"ALL Fectched")
    



def get_countries():
    
    url = "https://countriesnow.space/api/v0.1/countries"
    lit_of_countries = []
    try:
        response = requests.get(url)
        status = response.status_code
        reason = response.reason
        if(status ==200):
            data = response.text
            parse_json = json.loads(data)
            country_data = parse_json['data']
            for c in country_data:
                lit_of_countries.append(c['country'])
            lit_of_countries.append('US')
            print("United State have been added to the list")

            message="Countries Fetched"
            code ="Success"
            Status_Report(code,message)
            return lit_of_countries
        else:
            message="API request error: "+reason
            code ="Error "+status
            Status_Report(code,message)
            send_update(code,message)
            
        
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
        message="Connecion to DB was a success"
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


def realtime(real_time_url,mydb,countries,today):
    for country in  countries:
        response = requests.get(real_time_url+country)
        response = requests.get(url)
        status = response.status_code
        reason = response.reason
        data = response.text

        if(status ==200):
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
                    print("An error has occured in the database Insertion. \n Error: ",errdb)
                    code="Error DB Insert"
                    message=errdb
                    Status_Report(code,message)
                    send_update(code,message)
        else:
            message="API request error: "+reason
            code ="Error "+status
            Status_Report(code,message)
            send_update(code,message)

                

        except KeyError:
            print(KeyError,' for ',country)
            code="Error in country{0}".format(country)
            message=KeyError
            Status_Report(code,message)
           # send_update(code,message)
            


driver()
