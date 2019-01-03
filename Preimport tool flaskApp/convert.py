import pandas as pd
import numpy as np
import csv
import requests

def converter(filename):
    df  = pd.read_csv(filename, skiprows = 8, delimiter = '\t', encoding = 'latin-1')
    df.rename(columns = {'#':'partySize', 'St':'status'}, inplace = True)
    df['Phone'] = df['Phone'].apply(lambda x: str(x).replace('.',''))

    # remove special characters from names
    import string as stg # capwords: capitalize only first letter
    df['Last Name'] = df['Last Name'].dropna().apply(lambda x: stg.capwords(x))

    df['visitDate'] = ''

    df['printedDate'] = ''

    df['shift'] = ''

    heading0 = [ind for ind, row in df.iterrows() if row['Time']=='Time']
    heading1 = [ind for ind, row in df.iterrows() if row['Time']=='Printed']
    heading2 = [ind for ind, row in df.iterrows() if row['Time']=='Date:']

    df = df.drop(heading0)

    visitDates = []
    shifts = []

    for ind, val in enumerate(heading2[:15]):
        visitDate = df.loc[val,'partySize']
        shift = df.loc[val,'Last Name']
        visitDates.append(visitDate)
        printedDate = df.loc[val-1,'partySize']
        valNext = heading2[ind+1]
        valEnd = [item for item in df.index if item >= val and item < valNext][-1]  # finding last index value of this subtable
        df.loc[val:valEnd, 'visitDate'] = visitDate
        df.loc[val:valEnd, 'printedDate'] = printedDate
        df.loc[val:valEnd, 'shift'] = shift
        # print(val, valEnd, visitDate, printedDate, shift)

    dfTotals = pd.DataFrame(index = visitDates, columns = ['shift','totalCovers'])
    dfTotals.index.name = 'visitDate'
    for ind, val in enumerate(heading2[:15]):
        visitDate = df.loc[val, 'visitDate']
        dfTotals.loc[visitDate, 'shift'] = df.loc[val, 'Last Name']
        dfTotals.loc[visitDate, 'totalCovers'] = df.loc[val, 'status']

    df.drop(heading1+heading2, inplace = True)

    dfr = pd.DataFrame(columns = ['date_booked', 'time_slot', 'num_seats', 'table_seated_at',
                                   'last_name', 'first_name', 'status', 'phone_numbers',
                                   'visit_notes'])


    dfr['date_booked'] = df['Made']
    dfr['time_slot'] = df['Time']
    dfr['num_seats'] = df['partySize']
    dfr['table_seated_at'] = df['Tbl']
    dfr['last_name'] = df['Last Name']
    dfr['first_name'] = df['First Name']
    dfr['status'] = df['status']
    dfr['phone_numbers'] = df['Phone']
    dfr['visit_notes'] = df['Notes/Codes']

    # Some formatting fixes

    dfr['visit_notes'] = dfr['visit_notes'].str.replace("\(OpenTable", "OpenTable")
    dfr['visit_notes'] = dfr['visit_notes'].str.replace("VIP\)", "VIP; ")
    dfr['visit_notes'] = dfr['visit_notes'].str.replace("Web Reservation", "")
    return dfr
