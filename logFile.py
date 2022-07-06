import datetime
from datetime import date
import calendar


def Status_Report(code,message):
    todayTime = datetime.datetime.today() # Get today time.
    today = date.today()



    # dd/mm/YY
    d = today.strftime("%d-%m-%Y")

    try:
        f = open("LogFiles/Status_Report_"+str(d)+".txt", "a")
        f.write("Status Report : "+str(todayTime)+"\nCode: {0} Message: {1}\n\n".format(code,message))

        f.close()
    except BaseException as error:
        print("An error has occured \n Error: {0} time: {1}".format(error,todayTime) )

