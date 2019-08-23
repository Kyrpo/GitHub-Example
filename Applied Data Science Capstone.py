#!/usr/bin/env python
# coding: utf-8

# # Segmenting and Clustering Neighborhoods in Toronto

# #### I import all the modules necessary to scrap and process the data from the website

# In[132]:


import pandas as pd
import requests as rq
from bs4 import BeautifulSoup as bs


# #### Following the steps from youtube video on how to use the BeautifulSoup package

# In[133]:


Wiki_PC_Canada = rq.get('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M').text
Soup_wiki = bs(Wiki_PC_Canada,'lxml')
Table = Soup_wiki.find('table',{'class':'wikitable sortable'})


# #### Here I create something similar to a ".csv" using the separetor "tr" that I found from the website and substitute it with a ","

# In[144]:


Table1=""
for tr in Table.find_all('tr'):
    row1=""
    for tds in tr.find_all('td'):
        row1=row1+","+tds.text
    Table1=Table1+row1[1:]


# #### Here I convert it to a ".csv" file first and into a database after that

# In[150]:


file=open("toronto.csv","wb")
file.write(bytes(Table1,encoding="ascii",errors="ignore"))
df = pd.read_csv('toronto.csv',header=None)
df.columns=["Postalcode","Borough","Neighbourhood"]


# #### Droping the rows where "Borough" = "Not assigned"

# In[137]:


indexNames = df[ df['Borough'] =='Not assigned'].index
df.drop(indexNames , inplace=True)


# #### If a cell has a borough but a Not assigned neighborhood, then the neighborhood will be the same as the borough.

# In[138]:


df.loc[df['Neighbourhood'] =='Not assigned' , 'Neighbourhood'] = df['Borough']


# #### Two rows will be combined into one row with the neighborhoods separated with a comma if they have the same postalcode

# In[139]:


result = df.groupby(['Postalcode','Borough'], sort=False).agg( ', '.join)
DF_PC_Canada=result.reset_index()


# In[140]:


DF_PC_Canada.shape


# In[141]:


DF_PC_Canada

