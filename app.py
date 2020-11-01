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
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/vi.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# Define the precipitation route.
@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
                        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Define the stations route.
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Define the observations route.
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
                    filter(Measurement.station == 'USC00519281').\
                    filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Define the statistics route.
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs),
    func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
                        filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
        
    
    results = session.query(*sel).\
                    filter(Measurement.date >= start).\
                    filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

