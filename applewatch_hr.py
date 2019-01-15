import xml.etree.ElementTree as ET
import csv
import sys
import pandas as pd
import os
import datetime

tree = ET.parse(".\\Dataset\\apple_health_export\\export.xml")
root = tree.getroot()
#print(root.tag)
#print(root.attrib)

path = './dataset_applewatch/'
sj_name = sys.argv[1]
start_time = sys.argv[2]
end_time = sys.argv[3]
exper_date = sys.argv[4]
print(sj_name)
path = path + sys.argv[1] + '_' + exper_date + '_t' + start_time + '_t' + end_time + '/'

# Trying to make directory if it's not exist
if not os.path.exists(os.path.dirname(path)):
    try:
        os.makedirs(os.path.dirname(path))
    except OSError as exc: #Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

hr_dict = {}
# open a file for writing

Heartrate_data = open("./Heartrate_Data.csv", 'w')

# create the csv writer object
count = 0
for each_record in root.findall("Record"):

    if each_record.get("type") == "HKQuantityTypeIdentifierHeartRate":
        hr = each_record.get("value")
        time = each_record.get("startDate")
        date, time, timezone = time.split(' ')
        hr_dict.setdefault("date", [])
        hr_dict.setdefault("time", [])
        hr_dict.setdefault("timezone", [])
        
        hr_dict.setdefault("hr", [])
        hr_dict['hr'].append(hr)
        hr_dict['date'].append(date)
        hr_dict['time'].append(datetime.datetime.strptime(time, "%H:%M:%S").time())
        hr_dict['timezone'].append(timezone)
        
        #print("Heart_rate = " + hr, end='')
        #print("Time : " + time)

        

applewatch_hr_df = pd.DataFrame.from_dict(hr_dict)
#print(applewatch_hr_df[applewatch_hr_df['date'] == exper_date])


applewatch_hr_df = applewatch_hr_df.loc[applewatch_hr_df['date'] == exper_date]
filename = sj_name + '_' + exper_date + '_t' + start_time + '_t' + end_time
#print(applewatch_hr_df.loc[applewatch_hr_df['time']
"""
print(applewatch_hr_df.loc[(applewatch_hr_df['time'] > datetime.datetime.strptime(start_time.replace('-', ':'), "%H:%M:%S").time()) &
                           (applewatch_hr_df['time'] < datetime.datetime.strptime(end_time.replace('-', ':'), "%H:%M:%S").time())])
"""
applewatch_hr_df = applewatch_hr_df.loc[(applewatch_hr_df['time'] > datetime.datetime.strptime(start_time.replace('-', ':'), "%H:%M:%S").time()) &
                           (applewatch_hr_df['time'] < datetime.datetime.strptime(end_time.replace('-', ':'), "%H:%M:%S").time())]

applewatch_hr_df.to_csv(path + filename + ".csv", index=False)
print(applewatch_hr_df.head(10))
