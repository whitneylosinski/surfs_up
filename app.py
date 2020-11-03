# Import dependencies
import datetime as dt
import numpy as np 
import pandas as pd

# Import SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import Flask dependencies
from flask import Flask, jsonify

# Connect to the SQLite database file
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database into the class
Base = automap_base()

# Reflect the tables into the class
Base.prepare(engine, reflect=True)

# Save the references to each table.
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create the session (link) from Python to the Database.
session = Session(engine)

#Define Flask application
app = Flask(__name__)

# Define the welcome route.
@app.route("/")
def welcome():
    return(
    '''
    Welcome to Surf's Up!: Hawai'i Climate Analysis API!<br/>
    -------------------------------------------------------------------------------------------------------<br/>
    Available Routes:<br/>
    <pre class="tab">/api/v1.0/stations          (List of weather observation stations.)</pre>
    <pre class="tab">/api/v1.0/precipitation     (Precipitation data for the previous year.)</pre>
    <pre class="tab">/api/v1.0/tobs              (Temperature data from station USC00519281 for the previous year.)</pre>
    -------------------------------------------------------------------------------------------------------<br/>
    Date Searches (yyyy-mm-dd):<br/>
    <pre class="tab">/api/v1.0/temp/start        (Low, High & Average temp for each day after a specified date.)</pre>
    <pre class="tab">/api/v1.0/temp/start/end    (Low, High & Average temp for each day in a given date range.)</pre>
    -------------------------------------------------------------------------------------------------------<br/>
    Data available from 2010-01-01 to 2017-08-23
    ''')

# Define the stations route.
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.name, Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations)

# Define the precipitation route.
@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp, Measurement.station).\
                        filter(Measurement.date >= prev_year).order_by(Measurement.date).all()
    precipData = []
    for precip in precipitation:
        precipDict = {precip.date: precip.prcp, "Station": precip.station}
        precipData.append(precipDict)
    return jsonify(precipData)

# Define the observations route.
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs).\
                    filter(Measurement.station == 'USC00519281').\
                    filter(Measurement.date >= prev_year).order_by(Measurement.date).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

# Define the statistics route.
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs),
    func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
                        filter(Measurement.date >= start).group_by(Measurement.date).all()
        #temps = list(np.ravel(results))
        temps=[]
        for result in results:
            date_dict = {}
            date_dict["Date"] = result[0]
            date_dict["Low Temp"] = result[1]
            date_dict["Avg Temp"] = result[2]
            date_dict["High Temp"] = result[3]
            temps.append(date_dict)
        return jsonify(temps)

        
    
    results = session.query(*sel).\
                    filter(Measurement.date >= start).\
                    filter(Measurement.date <= end).group_by(Measurement.date).all()
    #temps = list(np.ravel(results))
    temps=[]
    for result in results:
        date_dict = {}
        date_dict["Date"] = result[0]
        date_dict["Low Temp"] = result[1]
        date_dict["Avg Temp"] = result[2]
        date_dict["High Temp"] = result[3]
        temps.append(date_dict)
    return jsonify(temps)

