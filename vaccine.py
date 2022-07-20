import requests
import json
from mail import send_update
from logFile import Status_Report


def vaccine_data(country):
    vaccine_base_url ='https://covid-api.mmediagroup.fr/v1/vaccines?country='
    # Initialize list
    vacine_data_set=[]
    response = requests.get(vaccine_base_url+country)
    status = response.status_code
    reason = response.reason
    if(status ==200):
        try:
            data = response.text
            parse_json = json.loads(data)
            all = parse_json["All"]


            administered = all["administered"]
            people_vaccinated = all["people_vaccinated"]
            people_partially_vaccinated = all["people_partially_vaccinated"]
            country = all["country"]
            Continent = all["continent"]
            print("Continent: {0}, Contry: {1}, administered: {2}, people_vaccinated: {3}, people_partially_vaccinated: {4}".format(Continent,country,administered,people_vaccinated,people_partially_vaccinated))

            #Return Vaccine Dataset
            vacine_data_set.append(administered)
            vacine_data_set.append(people_vaccinated)
            vacine_data_set.append(people_partially_vaccinated)
            print("Vaccine Datat added and Fecthed #########################################")
            return vacine_data_set

        except KeyError:
            print(KeyError,' for ',country)
            code="Error in country{0}".format(country)
            message=KeyError
            Status_Report(code,message)

            # Reutrn Default value if nothing found
            vacine_data_set.append(0)
            vacine_data_set.append(0)
            vacine_data_set.append(0)

            return vacine_data_set

    else:
        message="API request error: "+reason
        code ="Error "+status
        Status_Report(code,message)
        send_update(code,message)

        # Reutrn Default value if nothing found
        vacine_data_set.append(0)
        vacine_data_set.append(0)
        vacine_data_set.append(0)
        return vacine_data_set

