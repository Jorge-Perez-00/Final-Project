"""
Name: Jorge Perez
Email: jorge.perez59@myhunter.cuny.edu
Title: Exploring Criminal Activity in the Bronx Vs. New York City Overall
Resources: NYC OpenData (data.cityofnewyork.us), 
Python Documentation/Review Sources - geeksforgeeks.org, https://pandas.pydata.org/docs/, https://stackoverflow.com/
URL: https://jorge-perez-00.github.io/Intro-to-Data-Science-Final-Project/
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.api.types import CategoricalDtype


#READ DATASETS (NYC OPENDATA SETS)
NYPD_Complaints = pd.read_csv('NYPD_Complaint_Data_historic.csv',dtype = str)
NYPD_Calls_for_service = pd.read_csv('NYPD_Calls_for_Service__Historic_.csv',dtype = str)
NYPD_Arrests = pd.read_csv('NYPD_Arrests_Data__historic_.csv',dtype = str)
NYPD_Shootings_Indicents = pd.read_csv('NYPD_Shooting_Incident_Data__historic_.csv',dtype = str)


"""
This functions will iterate through the columns of each dataset and rename the columns that contain the Dates and Boroughs so that each dataset has the same columns names for both Dates and Boroughs for easy processing later on.
"""
def rename_columns(df):
    boro_columns = ["BORO_NM","BORO","ARREST_BORO"]
    date_columns = ["RPT_DT","INCIDENT_DATE","ARREST_DATE","OCCUR_DATE"]

    for column in boro_columns:
        if column in df.columns:
            df = df.rename(columns={column : "Borough"})

    for column in date_columns:
        if column in df.columns:
            df = df.rename(columns={column : "Date"})

    return df

"""
This function will drop all rows that contain empty values in both columns containing the Dates and Boroughs for each dataset
"""
def filter_dataframe(df):
    df.dropna(subset = ['Date'], inplace = True)
    df.dropna(subset = ['Borough'], inplace = True)

    return df


"""
RENAME COLUMNS
"""
NYPD_Complaints = rename_columns(NYPD_Complaints)
NYPD_Calls_for_service = rename_columns(NYPD_Calls_for_service)
NYPD_Arrests = rename_columns(NYPD_Arrests)
NYPD_Shootings_Indicents = rename_columns(NYPD_Shootings_Indicents)



"""
FILTER DATAFRAMES:
REMOVE ROWS WITH EMPTY VALUES ON THE "Date" OR "Borough" COLUMNS
"""
NYPD_Complaints_filtered = filter_dataframe(NYPD_Complaints)
NYPD_Calls_for_service_filtered = filter_dataframe(NYPD_Calls_for_service)
NYPD_Arrests_filtered = filter_dataframe(NYPD_Arrests)
NYPD_Shootings_Indicents_filtered = filter_dataframe(NYPD_Shootings_Indicents)


"""
This function will convert all the rows on the 'Date' column to datetime objects for easy processing later on. Then the dataframe will be sorted by dates and return a new dataframe with datetime objects on the 'Date' column
"""
def convertDates(df):
    data = df.copy()
    data["Date"] = pd.to_datetime(data["Date"])
    data =  data.sort_values(by="Date")

    return data



NYPD_Complaints_filtered = NYPD_Complaints_filtered.rename(columns={"LAW_CAT_CD":"Offense"})


"""
In this section the 'Date' and 'Borough' columns are filtered out of each dataframe.
These are the only columns we will need to compute the Yearly and Monthly counts
"""
NYPD_Complaints_filtered = NYPD_Complaints_filtered[["Date","Borough","Offense"]]
NYPD_Shootings_Indicents_filtered = NYPD_Shootings_Indicents_filtered[["Date","Borough"]]
NYPD_Arrests_filtered = NYPD_Arrests_filtered[["Date","Borough"]]
NYPD_Calls_for_service_filtered = NYPD_Calls_for_service_filtered[["Date","Borough"]]

"""
CONVERT DATES
"""
NYPD_Complaints_filtered = convertDates(NYPD_Complaints_filtered)
NYPD_Calls_for_service_filtered = convertDates(NYPD_Calls_for_service_filtered)
NYPD_Arrests_filtered = convertDates(NYPD_Arrests_filtered)
NYPD_Shootings_Indicents_filtered = convertDates(NYPD_Shootings_Indicents_filtered)




"""
This function will convert all the numerical months to their string equivalents
"""
def convertMonth(month):
    if  month == 1:
        return "January"
    elif month == 2:
        return "February"
    elif month == 3:
        return "March"
    elif month == 4:
        return "April"
    elif month == 5:
        return "May"
    elif month == 6:
        return "June"
    elif month == 7:
        return "July"
    elif month == 8:
        return "August"
    elif month == 9:
        return "September"
    elif month == 10:
        return "October"
    elif month == 11:
        return "November"
    elif month == 12:
        return "December"
    
"""
CUSTOM ORDER FOR SORTING THE "Month" COLUMN IN THE DATAFRAMES. This is used so that the Monthly plots showcase the correct monthly order. Without this the Monthly plots will plot the monthly data/counts in alphabetical order
"""
cat_month = CategoricalDtype(
    ['January', 'February', 'March', 'April','May','June','July','August','September','October','November',"December"], 
    ordered=True,
);




"""
In this processing section I used the pandas get_dummies() function to categorize the 'Borough' column by boroughs. I then create and add 2 columns contaning the year and month for each row in each dataframe. The 'Date' and 'Month' columns are used for later processing when 
we collect the total counts for each year and each month.
"""



"""
COMPLAINTS DATA PROCESSING
"""


NYPD_Complaints_filtered = pd.get_dummies(NYPD_Complaints_filtered,prefix="",prefix_sep="",columns=["Borough"])
NYPD_Complaints_filtered['Year'] = NYPD_Complaints_filtered['Date'].dt.year
NYPD_Complaints_filtered['Month'] = NYPD_Complaints_filtered['Date'].dt.month
NYPD_Complaints_filtered['Month'] = NYPD_Complaints_filtered['Month'].agg(convertMonth)
NYPD_Complaints_filtered['Month'] = NYPD_Complaints_filtered['Month'].astype(cat_month)


"""
CALLS FOR SERVICE DATA PROCESSING
"""
NYPD_Calls_for_service_filtered = pd.get_dummies(NYPD_Calls_for_service_filtered,prefix="",prefix_sep="",columns=["Borough"])
NYPD_Calls_for_service_filtered = NYPD_Calls_for_service_filtered.drop(columns=["(null)"],axis=1)
NYPD_Calls_for_service_filtered['Year'] = NYPD_Calls_for_service_filtered["Date"].dt.year
NYPD_Calls_for_service_filtered['Month'] = NYPD_Calls_for_service_filtered["Date"].dt.month
NYPD_Calls_for_service_filtered['Month'] = NYPD_Calls_for_service_filtered['Month'].agg(convertMonth)
NYPD_Calls_for_service_filtered['Month'] = NYPD_Calls_for_service_filtered['Month'].astype(cat_month)
print(NYPD_Calls_for_service_filtered)


"""
ARRESTS DATA PROCESSING
"""
NYPD_Arrests_filtered = pd.get_dummies(NYPD_Arrests_filtered,prefix="",prefix_sep="",columns=["Borough"])
NYPD_Arrests_filtered['Year'] = NYPD_Arrests_filtered['Date'].dt.year
NYPD_Arrests_filtered['Month'] = NYPD_Arrests_filtered["Date"].dt.month
NYPD_Arrests_filtered['Month'] = NYPD_Arrests_filtered['Month'].agg(convertMonth)
NYPD_Arrests_filtered['Month'] = NYPD_Arrests_filtered['Month'].astype(cat_month)


NYPD_Arrests_filtered = NYPD_Arrests_filtered.rename(columns={"B":"BRONX","K":"BROOKLYN","M":"MANHATTAN","Q":"QUEENS","S":"STATEN ISLAND"})



"""
SHOOTING INCIDENTS DATA PROCESSING
"""
NYPD_Shootings_Indicents_filtered = pd.get_dummies(NYPD_Shootings_Indicents_filtered,prefix="",prefix_sep="",columns=["Borough"])
NYPD_Shootings_Indicents_filtered['Year'] = NYPD_Shootings_Indicents_filtered['Date'].dt.year
NYPD_Shootings_Indicents_filtered['Month'] = NYPD_Shootings_Indicents_filtered['Date'].dt.month
NYPD_Shootings_Indicents_filtered['Month'] = NYPD_Shootings_Indicents_filtered['Month'].agg(convertMonth)
NYPD_Shootings_Indicents_filtered['Month'] = NYPD_Shootings_Indicents_filtered['Month'].astype(cat_month)




NYPD_Complaints_filtered = NYPD_Complaints_filtered.drop(columns=["Offense"],axis=1)









"""
VISUALIZATION: PLOTTING THE YEARLY AND MONTHLY PLOTS FOR EACH DATASET
"""


"""
COMPLAINTS
"""
complaints_by_year = NYPD_Complaints_filtered.groupby('Year').sum()
complaints_by_month = NYPD_Complaints_filtered.groupby(['Year','Month']).sum()

#YEAR
complaints_by_year.plot(figsize = (7,6),rot=45)
plt.title("Yearly NYPD Complaints in NYC by Borough (2006-2020)")
plt.xticks(complaints_by_year.index)
plt.xlabel("Years")
plt.ylabel("Number of NYPD Complaints")
plt.legend(bbox_to_anchor=(1.04,1),loc=2, borderaxespad=0)
plt.tight_layout()
plt.grid()
plt.savefig("NYPD Complaints (Yearly).png")


#MONTH
complaints_by_month.plot(figsize = (8,6),rot=45)
plt.title("Monthly NYPD Complaints in NYC by Borough (2006-2020)")
plt.xlabel("Months")
plt.ylabel("Number of NYPD Complaints")
plt.legend(bbox_to_anchor=(1.04,1),loc=2, borderaxespad=0)
plt.tight_layout()
plt.grid()
plt.savefig("NYPD Complaints (Monthly).png")


"""
CALLS FOR SERVICE DATA
"""
calls_by_year = NYPD_Calls_for_service_filtered.groupby('Year').sum()
calls_by_month = NYPD_Calls_for_service_filtered.groupby(['Year','Month']).sum()

#YEAR
calls_by_year.plot(figsize = (8,5),rot=45)
plt.title("Yearly Calls for Service in NYC by Borough (2018-2020)")
plt.xticks(calls_by_year.index)
plt.xlabel("Years")
plt.ylabel("Number of NYPD Calls for Service")
plt.legend(bbox_to_anchor=(1.04,1),loc=2, borderaxespad=0)
plt.tight_layout()
plt.grid()
plt.savefig("NYPD Calls for Service (Yearly).png")


#MONTH
calls_by_month.plot(figsize = (12,8),rot=45)
plt.title("Monthly Calls for Service in NYC by Borough (2018-2020)")
plt.xlabel("Months")
plt.ylabel("Number of NYPD Calls for Service")
plt.tight_layout()
plt.grid()
plt.savefig("NYPD Calls for Service (Monthly).png")




"""
ARREST DATA
"""
arrest_by_year = NYPD_Arrests_filtered.groupby('Year').sum()
arrests_by_month = NYPD_Arrests_filtered.groupby(['Year','Month']).sum()

#YEAR
arrest_by_year.plot(figsize = (8,5),rot=45)
plt.title("Yearly Arrests in NYC by Borough (2006-2020)")
plt.xticks(arrest_by_year.index)
plt.xlabel("Years")
plt.ylabel("Number of NYPD Arrests")
plt.legend(bbox_to_anchor=(1.04,1),loc=2, borderaxespad=0)
plt.tight_layout()
plt.grid()
plt.savefig("NYPD Arrests (Yearly).png")

#MONTH
arrests_by_month.plot(figsize = (14,8),rot=45)
plt.title("Monthly Arrests in NYC by Borough (2006-2020)")
plt.xlabel("Months")
plt.ylabel("Number of NYPD Arrests")
plt.tight_layout()
plt.grid()
plt.savefig("NYPD Arrests (Monthly).png")


"""
SHOOTING INCIDENTS
"""
shootings_by_year =  NYPD_Shootings_Indicents_filtered.groupby('Year').sum()
shootings_by_month =  NYPD_Shootings_Indicents_filtered.groupby(['Year','Month']).sum()

#YEAR
shootings_by_year.plot(figsize = (8,6),rot=45)
plt.title("Yearly Shooting Incidents in NYC by Borough (2006-2020)")
plt.xlabel("Years")
plt.xticks(shootings_by_year.index)
plt.yticks(range(0,900,50))
plt.ylabel("Number of Shooting Incidents")
plt.legend(bbox_to_anchor=(1.04,1),loc=2, borderaxespad=0)
plt.tight_layout()
plt.grid()
plt.savefig("Shooting Indicents (Yearly).png")

#MONTH
shootings_by_month.plot(figsize = (14,8),rot=45)
plt.title("Monthly Shooting Incidents in NYC by Borough (2006-2020)")
#plt.xticks(NYPD_Shootings_Indicents_filtered['Year'].unique())
plt.xlabel("Months")
plt.yticks(range(0,180,10))
plt.ylabel("Number of Shooting Incidents")
plt.tight_layout()
plt.grid()
plt.savefig("Shooting Indicents (Monthly).png")

















"""
YEARLY PREDICTIONS AND PREDICTIONS VISUALIZATIONS UP TO THE YEAR 2025
"""

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

"""
COMPLAINTS - PREDICTIONS/PLOTTING
"""
complaints = pd.DataFrame(complaints_by_year)
complaints['Date'] = complaints.index
complaints.index = range(0,len(complaints))


X = complaints[['Date']]
y = complaints[['BRONX','BROOKLYN','MANHATTAN','QUEENS','STATEN ISLAND']]

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=0)

model = LinearRegression()
model.fit(X_train,y_train)

X_predict = [[2021],[2022],[2023],[2024],[2025]]

y_predict = model.predict(X_predict)

complaints.index = complaints['Date']
complaints = complaints.drop(columns=['Date'],axis=1)

future_years = [2021,2022,2023,2024,2025]
complaints_predictions = pd.DataFrame(y_predict, index=future_years, columns=complaints.columns)

complaints = complaints.append(complaints_predictions)

#PLOTTING
complaints.plot(figsize = (8,6),rot=45)

plt.axvspan(2020,2025,color='blue',alpha=0.2)
plt.title("Future Yearly Predictions of NYPD Complaints in NYC by Borough (2006-2025)")
plt.xticks(complaints.index)
plt.xlabel("Years")
plt.ylabel("Number of NYPD Complaints")
plt.legend(bbox_to_anchor=(1.04,1),loc=2, borderaxespad=0)
plt.tight_layout()
plt.grid()
plt.savefig("NYPD Complaints - Predictions (Yearly).png")




"""
NYPD ARRESTS - PREDICTIONS/PLOTTING
"""
arrests = pd.DataFrame(arrest_by_year)
arrests['Date'] = arrest_by_year.index
arrests.index = range(0,len(arrests))

X = arrests[['Date']]
y = arrests[['BRONX','BROOKLYN','MANHATTAN','QUEENS','STATEN ISLAND']]

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=0)

model = LinearRegression()
model.fit(X_train,y_train)

X_predict = [[2021],[2022],[2023],[2024],[2025]]
y_predict = model.predict(X_predict)

arrests.index = arrests['Date']
arrests = arrests.drop(columns=['Date'],axis=1)

future_years = [2021,2022,2023,2024,2025]

arrests_predictions = pd.DataFrame(y_predict, index=future_years, columns=arrests.columns)

arrests = arrests.append(arrests_predictions)



#PLOTTING
arrests.plot(figsize = (8,6),rot=45)
plt.axvspan(2020,2025,color='blue',alpha=0.2)
plt.title("Future Yearly Predictions of Arrests in NYC by Borough (2006-2025)")
plt.xticks(arrests.index)
plt.xlabel("Years")
plt.ylabel("Number of NYPD Arrests")
plt.legend(bbox_to_anchor=(1.04,1),loc=2, borderaxespad=0)
plt.tight_layout()
plt.grid()
plt.savefig("NYPD Arrests - Predictions (Yearly).png")






"""
SHOOTING INCIDENTS - PREDICTIONS/PLOTTING
"""
shootings = pd.DataFrame(shootings_by_year)
shootings['Date'] = shootings_by_year.index
shootings.index = range(0,len(shootings))
print(shootings)

X = shootings[['Date']]
y = shootings[['BRONX','BROOKLYN','MANHATTAN','QUEENS','STATEN ISLAND']]


X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=0)


model = LinearRegression()
model.fit(X_train,y_train)




X_predict = [[2021],[2022],[2023],[2024],[2025]]
y_predict = model.predict(X_predict)


print(y_predict)

shootings.index = shootings['Date']
print(shootings)
shootings = shootings.drop(columns=['Date'],axis=1)
print(shootings)

future_years = [2021,2022,2023,2024,2025]
shooting_predictions = pd.DataFrame(y_predict, index=future_years, columns=shootings.columns)


print(shooting_predictions)

shootings = shootings.append(shooting_predictions)
print("PREDICTIONS:")
print(shootings)

#PLOTTING
shootings.plot(figsize = (8,6),rot=45)

plt.axvspan(2020,2025,color='blue',alpha=0.2)
plt.title("Future Yearly Predictions of Shooting Incidents in NYC by Borough (2006-2025)")
plt.xlabel("Years")
plt.xticks(shootings.index)
plt.yticks(range(0,900,50))
plt.ylabel("Number of Shooting Incidents")
plt.legend(bbox_to_anchor=(1.04,1),loc=2, borderaxespad=0)
plt.tight_layout()
plt.grid()
plt.savefig("Shooting Indicents - Predictions (Yearly).png")


plt.show()