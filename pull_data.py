
import requests
from datetime import datetime, timedelta
import json
import time
def extract_date(s):
    # s is a string in json format
    # Extract ['features'][0]['properties']['mdate'] from the JSON data
    data = json.loads(s)
    mdate = data['features'][0]['properties']['mdate']
    
    # Convert to datetime format
    dt_with_timezone = datetime.fromisoformat(mdate)
    
    # Convert to a naive datetime object (remove timezone information)
    dt_naive = dt_with_timezone.replace(tzinfo=None)
    
    return dt_naive




""" API SETTINGS """

DIRECTORY = "data/"

f = open("key.txt", "r")
data = open(DIRECTORY + "dataset.json", "w")
key = str(f.read()).strip()
print(key)
URL_KEY = "https://data.bordeaux-metropole.fr/geojson/features/CI_VCUB_P?key=" + key
year = 2022
month_start = 1
day_start = 1

month_end = 12
day_end = 31

station = 106  # station ident is a number

timeout_seconds = 30
max_retries = 10
timeout_count = 0
date_ignored = 0

# Set the initial date and time
current_date = datetime(year, month_end, day_end, 23, 59)

# Set the start date and time
start_date = datetime(year, month_start, day_start, 0, 0)


succes_count = 0
error_count = 0

start_time = time.time()

while current_date >= start_date and timeout_count < max_retries:
    current_date -= timedelta(minutes=1)

    # Format the date components
    new_date_day = current_date.day
    new_date_hour = current_date.hour
    new_date_month = current_date.month
    new_minute_str = str(current_date.minute).zfill(2)

    URL = URL_KEY + "&backintime=" + str(year) + "-" + str(new_date_month).zfill(2) + "-" + str(new_date_day).zfill(2) + "T" + str(new_date_hour).zfill(2) + ":" + new_minute_str + ":00&filter={\"ident\":" + str(station) + "}"


    # Make the request with a timeout
    try:
        response = requests.get(URL, timeout=timeout_seconds)
        response.raise_for_status()  # Raise an HTTPError for bad responses
    except requests.Timeout:
        # Handle timeout
        timeout_count += 1
        print("Timeout occurred. Retrying... (Retry count: {})".format(timeout_count))
        continue
    except requests.RequestException as e:
        # Handle other request exceptions
        error_count += 1
        print("Error during request. success: {}, error: {}".format(succes_count, error_count))
        print("Error message:", str(e))
        break

    # Reset the timeout count since the request was successful
    timeout_count = 0

    # Rest of the code remains unchanged...
    if response.status_code == 200:
        tmp_date = extract_date(str(response.content.decode('utf-8')))
        if (tmp_date <= current_date):
            data.write(str(response.content.decode('utf-8')))
            data.write("\n")
            current_date = tmp_date
        else:
            print("The date we got was not prior to the date we seeked. Reducing current date and retrying...")
            current_date -= timedelta(minutes=1)
        succes_count += 1
        print("Data retrieved successfully. Success: {}, Error: {}, Ignored: {}".format(succes_count, error_count, date_ignored))
    else:
        error_count += 1
        print("Error retrieving data. Success: {}, Error: {}, Ignored: {}".format(succes_count, error_count,date_ignored))
        print("Error message:", response.text)


print("--- %s seconds ---" % (time.time() - start_time))

