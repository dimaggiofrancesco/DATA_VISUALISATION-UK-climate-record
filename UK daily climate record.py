
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that
# you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used
# for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d100/2f0bb04162655f0cba429b865292f31482e817e0b3ee9da0f40185d7.csv`.
# The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI)
# [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt)
# (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line
# graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between
# the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record
# high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for
# the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution.
# Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **None, None, United Kingdom**, and the stations the data comes from are shown on the map below.

# In[33]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
import numpy as np
import pylab


#df_temp - Opens file and make it easy to read
df_temp = pd.read_csv('Dataset.csv') #open the data file
df_temp['Temp']=df_temp['Data_Value']*0.1 #Creates a column with temperatures in °C
df_temp1 = df_temp.loc[df_temp['ID'] == 'UKM00003740'] #Select only one location
df_temp1 = df_temp1.sort_values(['Date','Element']) #Sorts the data by date 
#df_temp - Creates columns for Day and Month of the year
df_temp1['Date'] = pd.to_datetime(df_temp1['Date']) #Converts argument to datetime
df_temp1['Month'] = df_temp1['Date'].dt.strftime('%b')#Creates a column "Month" with the month taken by "Date"
df_temp1['Day'] = df_temp1['Date'].dt.day #Creates a column "Day" with the day taken by "Date"
df_temp1['Year'] = df_temp1['Date'].dt.year #Creates a column "Year" with the year taken by "Date"
df_temp1.set_index(['Month','Day']).sum(level=[0,1]).reset_index() #Creates 2 indexes "Month" and "Day"


#df graph_2015 - Creates df filtered for data in 2015
graph_2015max = df_temp1[(df_temp1['Year']==2015) & (df_temp['Element']=='TMAX')] #Creates a df where there are only the temperature with Element = TMAX
graph_2015min = df_temp1[(df_temp1['Year']==2015) & (df_temp['Element']=='TMIN')] #Creates a df where there are only the temperature with Element = TMIN
graph_2015 = pd.merge(graph_2015max, graph_2015min, how='outer', on=['Date']) #Merges the 2 creates dfs "graph_2015max" and "graph:2015min" on the column "Date"
graph_2015 = graph_2015[['Date', 'Temp_x','Temp_y']] #Selects only 3 columns from the df
graph_2015 = graph_2015.sort_values(['Date']) #Sorts the df by Date
graph_2015 = graph_2015.rename(index=str, columns={"Temp_x": "2015_Tmax", "Temp_y": "2015_Tmin"})
graph_2015 = graph_2015.reset_index() #Resets index
graph_2015.drop("index", 1, inplace = True) #Drops the old index

#df graph_2015 - Creates columns for Day and Month of the year
graph_2015['Date'] = pd.to_datetime(graph_2015['Date']) #Converts argument to datetime
graph_2015['Month'] = graph_2015['Date'].dt.strftime('%b')#Creates a column "Month" with the month taken by "Date"
graph_2015['Day'] = graph_2015['Date'].dt.day #Creates a column "Day" with the day taken by "Date"


#df graph - Creates df filtered for data from 2005 until 2014 (Exclude the only other different year "2015")
graph = df_temp1.where(df_temp1['Year']!=2015).groupby(['Month','Day']).Temp.agg(['min','max']) #Groups by Month and by Day
                                                            # (removing the year 2014) and select the Max and Min Value from the column "Temp"
graph = graph.reset_index() #Resets the index
sorter = ["Jan", "Feb", "Mar", "Apr", "May", "Jun","Jul","Aug","Sep","Oct","Nov","Dec"] #Creates a list of months to be used to sort the months in the "graph" df
sorterIndex = dict(zip(sorter,range(len(sorter)))) #Creates a dictionary with months and number
                                    # {'Aug': 7, 'Apr': 3, 'Oct': 9, 'Jun': 5, 'Dec': 11, 'Mar': 2, 'Nov': 10, 'Jul': 6, 'Feb': 1, 'Sep': 8, 'May': 4, 'Jan': 0}
graph['Month_Rank'] = graph['Month'].map(sorterIndex) #Creates a new column 'Month_Rank' with a number associated with the month
graph.sort_values(['Month_Rank', 'Day'], ascending = [True, True], inplace = True) #Sorts 'graph' df according to 'Month_Rank' and Day'
graph.drop('Month_Rank', 1, inplace = True) #Drops 'Month_Rank' column
graph = graph.reset_index() #Resets index
graph.drop("index", 1, inplace = True) #Drops the old index


#df2 - Creates a new df which included the merged dfs graph and graph_2015
df2 = pd.merge(graph, graph_2015, how='outer', on=['Month','Day']) #Merges the 2 creates dfs "graph_2015max" and "graph:2015min" on the column "Date"
df2 = df2.drop(59) #Drops the 29th of February using the index value of 59
df2 = df2.reset_index() #Resets index
df2.drop("index", 1, inplace = True) #Drops the old index
df2 = df2[['Date','Month','Day','min','max','2015_Tmin','2015_Tmax']] #Reorders the columns
df2['outmax']=df2['2015_Tmax'].where(df2['2015_Tmax']>df2['max']) #Creates a new column that shows only temperature
                                                                # where the Tmax in 2015 was higher than the other years
df2['outmin']=df2['2015_Tmin'].where(df2['2015_Tmin']<df2['min']) #Creates a new column that shows only temperature
                                                                # where the Tmin in 2015 was lower than the other years

#df2 - Plots line Tmin 2005-2014 and Tmax 2005-2014
plt.plot(df2.index.values,df2['min'], label = 'Tmin 2005-2014') #Plots the min values using a line
plt.plot(df2.index.values,df2['max'], label = 'Tmax 2005-2014') #Plots the max values using a line
plt.gca().fill_between(range(len(df2)), df2['min'], df2['max'], facecolor='blue', alpha=0.25) #Fills the area between the linear data and exponential data

#df2 - Scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015
plt.scatter(df2.index.values,df2['outmin'], c='blue', label = 'Record Tmin 2015') #Plots the min values using a line
plt.scatter(df2.index.values,df2['outmax'], c='red', label = 'Record Tmax 2015') #Plots the max values using a line

#Legend format
plt.legend(loc=2, frameon=False, fontsize =12)

#Tick format
fig = plt.figure(1) # Prepare the figure
plot = fig.add_subplot(111) # Defines a fake subplot that is in fact only the plot
plot.tick_params(axis='both', which='major', labelsize=12) #Changes the fontsize of minor ticks label

#Title format
plt.title('Daily climate records in United Kingdom', fontsize = 16, fontweight='bold')

#y and x-axis label format
plt.ylabel('Temperature /°C', fontsize = 14)
plt.xlabel('Month', fontsize = 14)
plt.gca().xaxis.set_label_coords(0.5,-0.1)


#Figure size
fig = plt.gcf()
fig.set_size_inches(12.5, 7)
pylab.xlim([0,365])

x_axis = df2.groupby(['Month']).size()
x_axis = x_axis.reset_index()
x_axis['Month_Rank'] = x_axis['Month'].map(sorterIndex) #Creates a new column 'Month_Rank' with a number associated with the month
x_axis.sort_values(['Month_Rank'], ascending = True, inplace = True) #Sorts 'graph' df according to 'Month_Rank' and Day'
x_axis.drop('Month_Rank', 1, inplace = True) #Drops 'Month_Rank' column
x_axis = x_axis.reset_index() #Resets index
x_axis.drop("index", 1, inplace = True) #Drops the old index
x_axis.rename(index=str, columns={0: "Days"}, inplace = True)

x_values = []
x=0
for i in x_axis['Days']:
    x = x+i
    x_values.append(x)


plt.xticks(x_values, sorter)
plt.gca().axes.get_xaxis().set_ticklabels([])

x=0
for i in x_values:
    plt.gca().text(i - 20, -13.7, sorter[x],fontsize=12)
    x = x+1


plt.show()







