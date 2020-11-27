#accepts sales records as "saleslog.csv"
#exports records ready to be uploaded to Google Ads and Facebook Ads as custom audiences as "fbadsaud.csv" and "goadsaud.csv"
#csv must be formatted with first row as column names 

import os
import pandas as pd
import numpy as np

#import sales records csv file as pandas dataframe
data = pd.read_csv('saleslog.csv')

#select relevant columns
fbframe = data[['SaleDate', 'FirstName', 'LastName', 'Email', 'EveningPhone', 'DayPhone', 'CellPhone', 'PostalCode', 'State', 'Revenue1', 'Revenue2', 'ProductID', 'SaleID']]

#add static columns
fbframe['Country'] = 'US'
fbframe['Event'] = 'Purchase'
fbframe['Currency'] = 'USD'

#combine value measures
fbframe['SaleValue'] = fbframe['Revenue1'] + fbframe['Revenue2']

#create new phone variables with formatting for Facebook
fbframe['Phone'] = '+1' + data['EveningPhone'].astype(str)
fbframe['Phone2'] = '+1' + data['DayPhone'].astype(str)
fbframe['Phone3'] = '+1' + data['CellPhone'].astype(str)

#drop values prior phone variables - new variabels created above
fbframe.drop(['EvePhone'], axis=1)
fbframe.drop(['DayPhone'], axis=1)
fbframe.drop(['CellPhone'], axis=1)
fbframe.drop(['EmailAlt'], axis=1)

#remove unnecessary columns
fbframe = fbframe[['SaleDate','FirstName', 'LastName', 'Email', 'PostalCode', 'Phone', 'Phone2', 'Phone3', 'Country', 'State', 'Event', 'SaleValue', 'Currency', 'ProductID', 'SaleID']]

#fill in blank or negative valued sales with '1' instead of 0 or less to prevent error / not being counted
fbframe.loc[(fbframe.SaleValue <= 0),'SaleValue']=1
fbframe.fillna(1, inplace=True)

#drop all columns google doesn't want
googframe = fbframe.drop(['State'], axis=1)
googframe = googframe.drop(['Phone2'], axis=1)
googframe = googframe.drop(['Phone3'], axis=1)
googframe = googframe.drop(['Email2'], axis=1)
googframe = googframe.drop(['Event'], axis=1)
googframe = googframe.drop(['SaleValue'], axis=1)
googframe = googframe.drop(['Currency'], axis=1)
googframe = googframe.drop(['ProductID'], axis=1)
googframe = googframe.drop(['SaleID'], axis=1)

#convert to string to make Facebook happy
fbframe['Phone'] = fbframe['Phone'].astype(str)
fbframe['Phone2'] = fbframe['Phone2'].astype(str)
fbframe['Phone3'] = fbframe['Phone3'].astype(str)

#export both dataframes as csv files 100% prepared for upload to each ad platform
fbframe.to_csv('fbsalelog.csv', index=False)
googframe.to_csv('googsalelog.csv', index=False)
