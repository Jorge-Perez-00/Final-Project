# Overview
As a long time resident of the Bronx I’ve known that the Bronx was considered a dangerous place for a long time and for that reason I wanted to explore whether or not the Bronx should still be considered one of the top dangerous boroughs of New York City. For this project I used 4 datasets from the official NYC OpenData website and applied data science techniques through the Python programming language and extracted the information and knowledge that accurately showcases the patterns of criminal activity in New York City. The Python tools that I used to explore the datasets were Pandas, Numpy, Matplotlib, and Sklearn.                                       




# Data

### NYPD Complaints Dataset
The first dataset that I explored was the NYPD Complaints Historic dataset. This dataset contained all valid felony, misdemeanor, and violation crimes reported to the New York City Police Department from 2006 up to 2020 and has been last updated in 2021. The dataset consisted of several columns like both the x and y coordinates of the complaint, the description of the complaint, the exact date occurrence of the complaint, the borough where the complaint took place, and many more. For my project I only used the columns containing the date of occurrence and the boroughs where the complaints took place. With the help of the Python programming language, I extracted both the yearly and monthly complaints reported to NYPD between 2006-2020 and created plots that showcases both the yearly and monthly patterns of complaints in all boroughs of New York City.


![Yearly](docs/assets/NYPD Complaints (Yearly).png)
![Monthly](docs/assets/NYPD Complaints (Monthly).png)

### NYPD Calls for Service
The second dataset that I used to explore the criminal activity patterns of New York City is the NYPD Calls for Service Historic dataset. This dataset contains the millions of calls made to the New York Police Department between 2018-2020. Just like the NYPD complaints dataset, this dataset also contained the location coordinates of each service call, the dates, the boroughs, and much more. For this dataset I also only used the dates and recorded borough of each service call to compute and extract the yearly and monthly service calls between 2018-2020 for all 5 boroughs of New York City.
