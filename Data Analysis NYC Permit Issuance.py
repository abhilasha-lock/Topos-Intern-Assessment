#!/usr/bin/env python
# coding: utf-8

# In[13]:


# Import libraries
from __future__ import division
import pandas as pd
import seaborn as sns
import geopandas
import matplotlib.pyplot as plt
from geopandas import GeoDataFrame


# In[2]:


data=pd.read_csv('DOB_Permit_Issuance.csv',low_memory=False)


# In[3]:


data.head(5)


# In[4]:


#How many building permits are issued in NYC each year till 2018?
data = data[data['Permit Status']=='ISSUED']
data['Issuance Date'] = pd.to_datetime(data['Issuance Date'],format='%m/%d/%Y %H:%M:%S %p') #format date to perform datetime functions
data=data[data['Issuance Date'].dt.year != 2019]
data['Issuance Date'].dt.year.value_counts() #counting values by year using datetime function


# In[5]:


#Plotting the data

data['Issuance Date'].dt.year.value_counts().sort_index().plot(kind='bar') #sorting index so data is in order by year

plt.title('Building Permits Issued per Year', size=14)
plt.xlabel('Year', size=12)
plt.ylabel('Count', size=12)
plt.ylim(0,200000)
plt.show()


# In[6]:


#Which type of permits are most common?

data['Permit Type'].value_counts().sort_values(ascending=False)


# In[7]:


#Mapping permit type with the full form to make it more readable

data['Permit Type'] = data['Permit Type'].map({'EW': 'Equipment Work', 'PL': 'Plumbing',
                                            'EQ': 'Construction Equipment', 'AL': 'Alteration',
                                            'NB': 'New Building','SG': 'Sign', 'DM': 'Demolition', 'FO': 'Foundation',
                                            })


#Plotting the data
fig = plt.figure(figsize=(14,7))

data['Permit Type'].value_counts().plot(kind='bar')
plt.title('Permits Issued by Type', size=14)
plt.xlabel('Permit Type',size=12)
plt.ylabel('Count', size=12)
plt.xticks(rotation='horizontal')

plt.show()



# In[8]:


# Where the most building permits issued between 1989-2018?

data['BOROUGH'].value_counts() 


# In[9]:


#Plotting the above data

#Plotting the data
data['BOROUGH'].value_counts().plot(kind='bar')

plt.title('Building Permits Issued by Borough', size=14)
plt.ylabel('Count', size=12)
plt.xticks(rotation='horizontal')
plt.show()


# In[10]:


#What percentage of borough permits are for residential projects?

boroughs = ['BROOKLYN', 'MANHATTAN', 'QUEENS', 'STATEN ISLAND', 'BRONX'] #list of borough names to pass to for loop

for i in boroughs:
    """
    this for loop returns the percentage of residential permits
    within each borough

    count the number of residential permits then divide by the
    total number of borough permits
    """
    print('\n' + i)
    print(data[data['BOROUGH'] == i]['Residential'].value_counts() / len(data[data['BOROUGH'] == i]))


# In[11]:


#How many permits have been issued by zip code?

#Since zipcode for NYC begin with 10000, removed the erroneous data

data = data[data['Zip Code'] >= 10000]  #returns only zip codes that are > or = to 10000

print('Permits by zip code \n')
print(data['Zip Code'].value_counts().sort_index().head(5))  #counting the number of permits by zipcode then sorting them
print('\n')
print('5 zip codes with most permits issued:')
data['Zip Code'].value_counts().sort_values(ascending=False).head(5) #five zip codes with most permits issued


# In[15]:


#Reading data from NYC Zip Code Boundaries Shapefile

zip_codes = GeoDataFrame.from_file('ZIP_CODE_040114/ZIP_CODE_040114.shp') #read in shape file
zip_codes['zip_code'] = zip_codes['ZIPCODE'].astype(int) #converting zipcode column to integer data type
data['Zip Code'] = data['Zip Code'].astype(int) #converting zipcode column in Permit Issuance data to integer data type


# In[16]:


#Count the number of occurrences for each zip code in the data frame, 
#then converting the data series to a data frame for merging.

counts = data['Zip Code'].value_counts()
counts = counts.to_frame(name='count')
counts = counts.reset_index()


# In[22]:


#Merge the number of occurences for each zip code, with the corresponding zip code polygon

counts = GeoDataFrame(counts.merge(zip_codes, how='left', left_on='index', right_on='zip_code'))

#Dropping all NaNs in the geometry column.

counts = counts.dropna() #drop null values

#Plotting the data
fig, ax = plt.subplots(figsize = (8,8))

counts.plot(column='count', cmap='Blues',alpha=1,linewidth=0.1, ax=ax)

plt.title('Building Permits by Zipcode', size=20)
plt.axis('off')
plt.show()


# In[ ]:




