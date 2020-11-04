# Surf's Up!

## Purpose
This project is to analyze weather data in Oahu, Hawaii from an SQLite database to try and get investors to invest in a surf board and ice cream shop called Surf's Up!.  The analysis will be used to show investors weather trends in Oahu so they can see how the weather will effect the success of the surfing and ice cream shop.  Specifically the investors want to see the following data:

 - Precipitation data from Oahu weather stations for one year.
 - Number of stations collecting data.
 - Most active stations.
 - Low, High and Average temperatures for the most active station.
 - Histogram of temperature observations for the most active station.
 - Temperature data for June in Oahu.
 - Temperature data for December in Oahu.
 
## Resources
Data: hawaii.sqlite<br/>
Software: Python 3.8, Jupyter Notebook (anaconda3), VS Code, Flask

## Analysis


## Results
Provide a bulleted list with three major points from the two analysis deliverables. Use images as support where needed.
1. The average temperature in June (74.9°F) is 4° warmer than the average in December (71.0°F).  While there does appear to be a recorded drop in temperature for December,  it doesn't appear to be a large enough drop to deter people from surfing and eating ice cream.  Based on the average temperatures, it appears the shop could be sustainable year-round but to be more informed, a study would need to be done to determine the ideal surfing and ice cream eating temperatures for customers.
2. The high temperature in June (85°F) is 2° warmer than the high temperature in December (83°F).  The similarity in these values suggests that the weather doesn't change significantly in Oahu between June and December.  Again, based on the high temperatures, it appears the shop could be sustainable year-round.
3. The low temperature in June (64°F) is 8° warmer that the low temperature in December (56°F).  The low temperatures for December may be enough to deter customers from surfing or eating ice cream, but again, a second study would need to be done to determine the ideal surfing and ice cream eating temperatures for customers.  Also, although the low temperatures could be a cause for concern, the average temperature for December suggests that cold days below 60°F are rare.

## Summary
The results of the analysis show that Surf's Up! surf and ice cream shop could be a sustainable year-round business in Oahu in regards to temperature.  The data shows that Oahu in June has an average temperature of 75°F with a high of 85°F and a low of 64°F.  The temperature in December is slightly cooler with an average of 71°F, a high of 83°F and a low of 56°F.  Although the low for December is quite a bit colder than June, the average December temperature is only 4° cooler and still likely to be within ideal surfing and ice cream eating temperatures for customers.

To look a bit deeper into the sustainability of the shop year-round, a study could be done asking customers what temperatures they prefer for surfing and eating ice cream.  It would also be smart to compare the precipitation in June versus that in December.  Since people don't typically surf or eat ice cream as much if it's raining, precipitation could play an important part in the success of the shop as well.  The two additional queries for the low, high and average precipitation in June and the low, high and average precipitation in December are shown below.  

| June Precipitation | December Precipitation |
|---|---|
|![June_precip](Results/June_precip.png)|![December_precip](Results/December_precip.png)|

The tables show that the average precipitation is slightly higher in December (0.22") than in June (0.14") and that December had a higher maximum precipitation (6.42") than the max in June (4.43").  The additional rainfall may have a negative effect on sales and year-round sustainability.  Another query to better understand the rain patterns would be to look at how many days out of the each month had precipitation.  This could provide valuable information for how often sales could be impacted by rain.
