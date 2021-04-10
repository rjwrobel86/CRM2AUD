#!/usr/bin/env python
# coding: utf-8

#accepts "SoldLogExport.csv"
#outputs audiences for google and facebook, as well as offline conversions for facebook

import os
import pandas as pd
import numpy as np
import pandas as pd

data = pd.read_csv('SoldLogExport.csv')

fbframe = data[['SoldDate', 'FirstName', 'LastName', 'Email', 'EmailAlt', 'EvePhone', 'DayPhone', 'CellPhone', 'PostalCode', 'State', 'FrontGross', 'BackGross', 'SoldNote', 'VehicleVIN', 'DealNumber']]

fbframe['Country'] = 'US'
fbframe['Event'] = 'Purchase'
fbframe['Currency'] = 'USD'
fbframe['Value'] = fbframe['FrontGross'] + fbframe['BackGross']
fbframe['Phone'] = '+1' + data['EvePhone'].astype(str)
fbframe['Phone2'] = '+1' + data['DayPhone'].astype(str)
fbframe['Phone3'] = '+1' + data['CellPhone'].astype(str)
fbframe['Email2'] = data['EmailAlt']

fbframe.drop(['EvePhone'], axis=1)
fbframe.drop(['DayPhone'], axis=1)
fbframe.drop(['CellPhone'], axis=1)
fbframe.drop(['EmailAlt'], axis=1)

fbframe.loc[(fbframe.Value <= 0),'Value']=1
fbframe.fillna(1, inplace=True)

googframe = fbframe.drop(['State'], axis=1)
googframe = googframe.drop(['Phone2'], axis=1)
googframe = googframe.drop(['Phone3'], axis=1)
googframe = googframe.drop(['Email2'], axis=1)
googframe = googframe.drop(['Event'], axis=1)
googframe = googframe.drop(['Value'], axis=1)
googframe = googframe.drop(['Currency'], axis=1)
googframe = googframe.drop(['VehicleVIN'], axis=1)
googframe = googframe.drop(['DealNumber'], axis=1)
googframe = googframe.drop(['SoldDate'], axis=1)

fbframe['Phone'] = fbframe['Phone'].astype(str)
fbframe['Phone2'] = fbframe['Phone2'].astype(str)
fbframe['Phone3'] = fbframe['Phone3'].astype(str)

fbframe['Phone'] = fbframe['Phone'].str.rstrip('.0')
fbframe['Phone2'] = fbframe['Phone2'].str.rstrip('.0')
fbframe['Phone3'] = fbframe['Phone3'].str.rstrip('.0')

fbframe2 = fbframe.rename(columns={'SoldDate':'event_time','FirstName':'fn','LastName':'ln','Email':'email','Email2':'email','Phone':'phone','Phone2':'phone','Phone3':'phone','Country':'country','State':'st','City':'ct','Event':'event_name','Value':'value','Currency':'currency','VehicleVIN':'item_number','DealNumber':'order_id','PostalCode':'zip'})
googframe = googframe.rename(columns={'FirstName':'First Name','LastName':'Last Name','PostalCode':'Zip','EvePhone':'Phone','Email':'Email'})

googframe['Country'] = 'US'

fbaud = fbframe2[['fn','ln','st','country','email','phone']]
goog2 = googframe[['First Name','Last Name','Email','Zip','Country','Phone']]

fbframe2.to_csv('fbconversions.csv', index=False)
#goog2.to_csv('googaud.csv', index=False)
fbaud.to_csv('fbaud.csv', index=False)

goog2 = goog2[['First Name','Last Name','Email','Zip','Country','Phone2']]
goog2 = goog2.rename(columns={'Phone2':'Phone'})

goog2.to_csv('googaud.csv', index=False)
