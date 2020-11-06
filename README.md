# Surf's Up!

## Purpose
This project is to analyze weather data in Oahu, Hawaii from an SQLite database to try and get investors to invest in a surf board and ice cream shop called Surf's Up!.  The analysis will be used to show investors weather trends in Oahu so they can see how the weather will effect the success of the surfing and ice cream shop.  Specifically the investors want to see the following data:

 - Total precipitation each day for the latest year.
 - Number of stations collecting data.
 - Most active stations.
 - Low, High and Average temperatures for the most active station.
 - Histogram of temperature observations for the most active station.
 - Low, High and Average temperatures for given date ranges.
 
The investors also want to know if the shop would be sustainable year-round and have requested the following data:
 - Temperature stats for June in Oahu.
 - Temperature stats for December in Oahu.
 
## Resources
Data: hawaii.sqlite<br/>
Software: Python 3.8, Jupyter Notebook (anaconda3), VS Code, Flask

## Analysis
The analysis was completed in three main steps which are outlined below.

1. ***Prepare the Python toolkit*** - The first step in completing the analysis was to set up the tools, connect to the SQLite database and then create a session to link between Python and the database.  This was done by first importing the dependencies required for the analysis.
   ```py
   # Import dependencies
   from matplotlib import style
   style.use('fivethirtyeight')
   import matplotlib.pyplot as plt    
   import numpy as np
   import pandas as pd
   import datetime as dt
   ```   
   Next, the python SQL toolkit (SQLAlchemy) and Object Relational Mapper (ORM) were imported.
   ```py
   import sqlalchemy
   from sqlalchemy.ext.automap import automap_base
   from sqlalchemy.orm import Session
   from sqlalchemy import create_engine, func
   ```
   With all the necessary tools imported, the next step was to connect to the SQLite database, reflect an existing database into a new model and reflect the tables.  
   ```py
   # Connect to the SQLite database.
   engine = create_engine("sqlite:///hawaii.sqlite")
    
   # reflect an existing database into a new model
   Base = automap_base()

   # reflect the tables
   Base.prepare(engine, reflect=True)
   ```
   The database was then scanned to find all of the available classes and each class was saved as a reference.  
   ```py
   # We can view all of the classes that automap found
   Base.classes.keys()

   # Save references to each table
   Measurement = Base.classes.measurement
   Station = Base.classes.station
   ```
   The final step of before looking at the data was to create a session link from Python to the database.
   ```py
   # Create our session (link) from Python to the DB
   session = Session(engine)
   ```
   
2. ***Exploring the data*** - With the toolkit set up, the tables loaded and the database connected to Python, the data could now be queried to find the required deliverables.  The first deliverable was to find the total precipititation for each day for the latest year.  To do this, the variable `prev_year` was set to the last date in the database minus 365 days.  The data was then queried to see the date and precipitation data from the Measurement class, filtered by only the dates greater than or equal to the `prev_year` variable.  Adding `.all()` to the query, extracted the results and put them into a list.  The list was then saved to a dataframe with the index set to the `'date'` column.  The dataframe was sorted by the index, putting the list in chronological order.  The data was plotted using Matplotlib and then the statistics were shown using `df.describe()`.  See the code and the resulting plot and statistics below.
   ```py
   # Design a query to retrieve the last 12 months of precipitation data and plot the results. 
   #Starting from the last data point in the database. 
   prev_year = dt.date(2017, 8, 23)

   # Calculate the date one year from the last date in data set.
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

   # Perform a query to retrieve the data and precipitation scores
   results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >=prev_year).all()

   # Save the query results as a Pandas DataFrame and set the index to the date column
   df = pd.DataFrame(results, columns=['date', 'precipitation'])
   df.set_index(df['date'], inplace=True)

   # Sort the dataframe by date
   df = df.sort_index()
   print(df)

   # Use Pandas Plotting with Matplotlib to plot the data
   df.plot(title='Total Precitpitation per Day')
   plt.xticks(rotation=90)
   ```
   | Precipitation Plot | Precipitation Stats |
   |:--:|:--:|
   |![precip_plot](Results/Precip_plot.png)|![precipitation data](Results/Precip_data.png)|
   
   The next deliverable was to find the number of stations collecting data for the provided database.  This was done by querying the Station class for station data and using the `func.count` SQLAlchemy function to count each data point retreived.  Again, `.all()` was added to extract the data points and add them to a list.  The following script shows the query.  Running it showed that there were 9 active stations.
   ```py 
   # How many stations are available in this dataset?
   session.query(func.count(Station.station)).all()
   ```
   
   The third deliverable was to detemine which station was the most active.  This was done by writing a query to look at the Measurement class for the station and return both the station and the count of each time the station recorded data.  The query was then grouped by each station and ordered in descending order by the count.  The data was extracted to a list using `.all()`.  The query and results are shown below.
   ```py  
   # What are the most active stations?
   # List the stations and the counts in descending order.
   session.query(Measurement.station, func.count(Measurement.station)).\
                 group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
   ```
   ![active_stations](Results/active_stations.png)
   
   The fourth deliverable was to find the lowest temperature recorded, highest temperature recorded and the average temperature at the most active station.  This was done using the `func.min`, `func.max`, and `func.avg` SQLAlchemy functions.  The query was written to return the minimum, maximum and average temperature observation (tobs) from the Measurement class and filter the data for only the 'USC00419281' station, which was found to be the most active.  The results of the query below give the output [(54.0, 85.0, 71.66378066378067)] with the first number being the low, the second the high and the third the average temperature.
   ```py
   # Using the station id from the previous query, calculate the lowest temperature recorded, 
   # highest temperature recorded, and average temperature most active station?
   session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
              filter(Measurement.station == 'USC00519281').all()
   ```
   
   The fifth deliverable was to print a histogram of all the temperatures recorded at the most active station for the past twelve months.  This was done by querying the temperature observations (tobs) from the Measurement class and filtering by the station and `prev_year` variable that was defined earlier in the first deliverable.  The results were extracted into a list using `.all()`, saved to a Pandas DateFrame and then plotted into a histogram as shown below.
   ```py
   # Choose the station with the highest number of temperature observations.
   # Query the last 12 months of temperature observation data for this station and plot the results as a histogram
   results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= prev_year).all()
   df = pd.DataFrame(results, columns=['tobs'])
   df.plot.hist(bins=12)
   plt.title("Temperaure observations")
   plt.tight_layout()
   ```
   ![Temps_histogram](Results/Temps_histogram.png)
   
   The sixth deliverable was to find the lowest temperature recorded, highest temperature recorded and the average temperature for any given date range.  This was done by writing a function that took in the arguments `start_date` and `end_date` and ran a query to find the necessary data.  The query used the `func.min`, `func.max`, and `func.avg` SQLAlchemy functions and returned the low temperature, average temperature and high temperature filtered by the start and end dates provided.  See the query script below.
   ```py
   # Write a function called `calc_temps` that will accept start date and end date in the format '%Y-%m-%d' 
   # and return the minimum, average, and maximum temperatures for that range of dates
   def calc_temps(start_date, end_date):
       return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),
           func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
   print(calc_temps('2017-06-01', '2017-06-30'))
   ```
   
3. **Explore year-round sustainability** - The third and final step of the analysis was to explore temperature data for the months of June and December in Oahu to determine if the surf and ice cream shop business chould be sustainable year-round.  To find the June temperatures, a query was written to return the date and temperature observations (tobs) data from the Measurement class.  The month value of the date data was then extracted from the full date and the data returned from the query was filtered to only the dates with month equal to 6.  The data was then extracted to a list using `.all()`, saved into a Pandas DataFrame with the index set to the date column, and sorted by the index.  To display the temperature statistics for the month of June, `df.describe()` was used.  See the June query below.
   ```py
   # Write a query that filters the Measurement table to retrieve the temperatures for the month of June.
   June_temps = session.query(Measurement.date, Measurement.tobs).filter(extract('month', Measurement.date)==6).all()
     
   # Create a DataFrame from the list of temperatures for the month of June. 
   df = pd.DataFrame(June_temps, columns=['date', 'temperature'])
   df.set_index(df['date'], inplace=True)
   df = df.sort_index()
   
   # Calculate and print out the summary statistics for the June temperature DataFrame.
   df.describe()
   ```
   
   The query was then written again in the exact same way, but instead of setting the month equal to 6, the data was filtered to only the dates with month equal to 12.  See the December query below.
   ```py
   # Write a query that filters the Measurement table to retrieve the temperatures for the month of December.
   December_temps = session.query(Measurement.date, Measurement.tobs).filter(extract('month', Measurement.date)==12).all()
     
   # Create a DataFrame from the list of temperatures for the month of December. 
   df = pd.DataFrame(December_temps, columns=['date', 'temperature'])
   df.set_index(df['date'], inplace=True)
   df = df.sort_index()
   
   # Calculate and print out the summary statistics for the Decemeber temperature DataFrame.
   df.describe()
   ```   
   
## Results
The June and December temperature query results are shown below along with an explanation of three key differences between the data for each month.

   | June Temperatures | December Temperatures |
   |:--:|:--:|
   |![June_temps](Results/June_temps.png)|![December_temps](Results/December_temps.png)|

 1. **Average Temperature** - The average temperature in June (74.9°F) is 4° warmer than the average in December (71.0°F).  While there does appear to be a recorded drop in temperature for December,  it doesn't appear to be a large enough drop to deter people from surfing and eating ice cream.  Based on the average temperatures, it appears the shop could be sustainable year-round but to be more informed, a study would need to be done to determine the ideal surfing and ice cream eating temperatures for customers.
 
 2. **High Temperature** - The high temperature in June (85°F) is 2° warmer than the high temperature in December (83°F).  The similarity in these values suggests that the weather doesn't change significantly in Oahu between June and December.  Again, based on the high temperatures, it appears the shop could be sustainable year-round.
 
 3. **Low Temperature** - The low temperature in June (64°F) is 8° warmer that the low temperature in December (56°F).  The low temperatures for December may be enough to deter customers from surfing or eating ice cream, but again, a second study would need to be done to determine the ideal surfing and ice cream eating temperatures for customers.  Also, although the low temperatures could be a cause for concern, the average temperature for December suggests that cold days below 60°F are less common.

## Summary
The results of the analysis show that Surf's Up! surf and ice cream shop could be a sustainable year-round business in Oahu in regards to temperature.  Although the low for December is quite a bit colder than June, the average December temperature is only 4° cooler and still likely to be within ideal surfing and ice cream eating temperatures for customers.

To look a bit deeper into the sustainability of the shop year-round, a study could be done asking customers what temperatures they prefer for surfing and eating ice cream.  It would also be smart to compare the precipitation in June versus that in December.  Since people don't typically surf or eat ice cream as much if it's raining, precipitation could play an important part in the success of the shop as well.  The two additional queries for the low, high and average precipitation in June and the low, high and average precipitation in December are shown below.  

   | June Precipitation | December Precipitation |
   |:--:|:--:|
   |![June_precip](Results/June_precip.png)|![December_precip](Results/December_precip.png)|

The tables show that the average precipitation is slightly higher in December (0.22") than in June (0.14") and that December had a higher maximum precipitation (6.42") than the max in June (4.43").  The additional rainfall may have a negative effect on sales and year-round sustainability.  Another query to better understand the rain patterns would be to look at how many days out of each month had precipitation.  This could provide valuable information for how often sales could be impacted by rain.
