#!/usr/bin/env python
# coding: utf-8

# In[147]:



#accepts "SoldLogExport.csv"

import os
import pandas as pd
import numpy as np
import pandas as pd

data = pd.read_csv('SoldLogExport.csv')

data.columns

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

fbframe = fbframe[['SoldDate','FirstName', 'LastName', 'Email', 'Email2', 'PostalCode', 'Phone', 'Phone2', 'Phone3', 'Country', 'State', 'Event', 'Value', 'Currency', 'VehicleVIN', 'DealNumber']]

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

fbframe.to_csv('fbsoldlog.csv', index=False)
googframe.to_csv('googsoldlog7.csv', index=False)


# In[148]:



googframe = googframe.rename(columns={'FirstName':'First Name','LastName':'Last Name','PostalCode':'Zip'})

googframe['Phone'] = googframe['Phone'].str.rstrip('.0')


# In[149]:


googframe.to_csv('goog4.csv', index=False)


# In[150]:


googframe['a'], googframe['b'], googframe['c'] = map(googframe['Phone'].str.slice, [0, 3, 6], [1, 6, 9])


# In[151]:


googframe['Phone']


# In[152]:


googframe['B'] = googframe['Phone'].str[1:2]
googframe['C'] = googframe['Phone'].str[2:5]
googframe['D'] = googframe['Phone'].str[5:8]
googframe['E'] = googframe['Phone'].str[8:13]


# In[153]:


googframe['Phone'] = googframe['B'] + " " + "(" + googframe['C'] + ")" + " " + googframe['D'] + " " +  googframe['E']


# In[154]:


googframe = googframe[['First Name','Last Name','Phone','Email','Zip','Country']]


# In[157]:


googframe.to_csv("googaud.csv",index=False)


# In[158]:


fbframe2 = fbframe.rename(columns={'SoldDate':'event_time','FirstName':'fn','LastName':'ln','Email':'email','Email2':'email','Phone':'phone','Phone2':'phone','Phone3':'phone','Country':'country','State':'st','City':'ct','Event':'event_name','Value':'value','Currency':'currency','VehicleVIN':'item_number','DealNumber':'order_id','PostalCode':'zip'})
fbaud = fbframe2[['fn','ln','st','country','email','phone']]
fbframe2.to_csv('fbconversions.csv', index=False)


# In[ ]:
