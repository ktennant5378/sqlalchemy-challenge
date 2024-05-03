# Import the dependencies.
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, select

from flask import Flask, jsonify
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement_table = Base.classes.measurement
station_table = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app .route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date one year from the last date in data set.
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    # Perform a query to retrieve the data and precipitation scores
    recent_year_query = session.query(measurement_table.date, measurement_table.prcp).filter(measurement_table.date >= year_ago).all()

    # Convert the query results to a dictionary using date as the key and prcp as the value
    prcp_data = []
    for date, prcp in recent_year_query:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    return jsonify(session.query(station_table.station).all())

@app.route("/api/v1.0/tobs")
def tobs():
    # Calculate the date one year from the last date in data set.
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Query the last 12 months of temperature observation data for this station and plot the results as a histogram
    year_temps_q = select(measurement_table.tobs).filter(measurement_table.station == 'USC00519281').where(measurement_table.date >= year_ago)
    top_station_temps_df = pd.read_sql(year_temps_q, conn)

    return jsonify(top_station_temps_df.to_dict())

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    start_date_query = session.query(func.min(measurement_table.tobs), func.avg(measurement_table.tobs), func.max(measurement_table.tobs)).filter(measurement_table.date >= start).all()

    return jsonify(start_date_query)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    start_end_date_query = session.query(func.min(measurement_table.tobs), func.avg(measurement_table.tobs), func.max(measurement_table.tobs)).filter(measurement_table.date >= start).filter(measurement_table.date <= end).all()

    return jsonify(start_end_date_query)


if __name__ == '__main__':
    app.run(debug=True)

