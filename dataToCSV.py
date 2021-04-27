import pandas as pd

# file variables
dateFormatSource = '%d.%m.%Y'
dateFormatUS = '%m/%d/%Y'
year = '2021'
file_export_name = 'prayer_time_'+year+'.csv'
file_import_name = 'data.csv'
file_import_sep = ' '


#import data.csv
df = pd.read_csv(file_import_name, sep=file_import_sep, dtype=str)

# get prayer name
prayers_name = df.columns[1:]

# add year to date column
prefix = '.'+year
for i in range(len(df['date'])):
    df['date'][i] = df['date'][i]+prefix

# delete not existence day 29/02 from the year
df = df.drop(df.loc[df['date'] == '29.02'+prefix].index)

# changing data type of date column
df['date'] = pd.to_datetime(df['date'], format=dateFormatSource)

# constructing ical format
subject = []
date = []
time = []

for day in df['date'].dt.strftime(dateFormatUS):
    prayers_time = df.loc[df['date'].dt.strftime(dateFormatUS) == day]
    for sholat in prayers_name:
        subject.append(sholat)
        date.append(day)
        time.append(prayers_time[sholat].values[0])

# compound all collected data into a lsit
data = {
    'Subject': subject,
    'Start Date': date,
    'Start Time': time,
    'End Date': date,
    'End Time': time,
    'All Day': ['FALSE' for i in range(len(date))],
    'Description': ['' for i in range(len(date))],
    'Location': ['Berlin' for i in range(len(date))],
    'UID': ['' for i in range(len(date))]
}


# export data into a csv file
prayers_time_DataFrame = pd.DataFrame(data=data)
prayers_time_DataFrame.to_csv(file_export_name, sep=',', index=False)
