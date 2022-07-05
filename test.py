import requests
import json
import mysql.connector


def get_countries():
    url = "https://countriesnow.space/api/v0.1/countries"
    lit_of_countries = []
    response = requests.get(url)
    data = response.text
    parse_json = json.loads(data)
    country_data = parse_json['data']
    for c in country_data:
        lit_of_countries.append(c['country'])
    return lit_of_countries



mydb = mysql.connector.connect(
    host='',
    user='',
    password='',
    database=""
)



print(".....",mydb)

base_url = "https://covid-api.mmediagroup.fr/v1/history?country="
# url = "https://covid-api.mmediagroup.fr/v1/history?country=Germany&status=deaths"
countries = get_countries()

status = ['deaths', 'confirmed', 'recovered']


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

            sql = 'INSERT INTO new_table (Last_updated,Continent, country,population, deaths, confirmed, recorvered) VALUES (%s,%s,%s,%s,%s,%s,%s)'
            val=(date,Continent,country,population,datesD["2020-05-28"],datesC["2020-05-28"],datesR["2020-05-28"])

            mycursor = mydb.cursor()
            mycursor.execute(sql,val)

        mydb.commit()
        print("DoNE")

    except KeyError:
        print(KeyError, ' for ', country)
