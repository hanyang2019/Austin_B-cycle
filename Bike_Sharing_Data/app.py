import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from collections import OrderedDict
from sqlalchemy.pool import QueuePool

app = Flask(__name__)

#################################################
# Database Setup
#################################################
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/b_cycle.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
trip_date = Base.classes.new_bike_data
Trip=Base.classes.filtered_trip
Location=Base.classes.Austin_B_Cycle_Kiosk_Locations
Data_pie = Base.classes.df_pie_all

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

#################################################
# John (Bar Chart Data)
#################################################


@app.route("/Day")
def day():

    # Use Pandas to perform the sql query
    
    trip_query=db.session.query(trip_date).statement
    df=pd.read_sql_query(trip_query,db.session.bind)
    
    dayslist = df['day_of_week'].value_counts(dropna=False).keys().tolist()
    dayscountlist = df['day_of_week'].value_counts(dropna=False).tolist()
    days_dict = dict(zip(dayslist, dayscountlist))
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    days_dict = OrderedDict(sorted(days_dict.items(),key =lambda x:days.index(x[0])))
    newdaylist = list(days_dict.keys())
    newdaycount = list(days_dict.values())

    trace = {
        "x": newdaylist,
        "y": newdaycount,
        "type": "scatter",
        "fill": "tozeroy",
    }
    return jsonify(trace)

@app.route("/All")
def all():
    # Use Pandas to perform the sql query
    trip_query=db.session.query(trip_date).statement
    df=pd.read_sql_query(trip_query,db.session.bind)
    dates = df['Checkout Date'].value_counts(dropna=False).keys().tolist()
    datescount = df['Checkout Date'].value_counts(dropna=False).tolist()
    
    trace = {
        "x": dates,
        "y": datescount,
        "type": "bar",
        "fill": "tozeroy",
    }
    return jsonify(trace)

@app.route("/Month")
def month():
    # Use Pandas to perform the sql query
    trip_query=db.session.query(trip_date).statement
    df=pd.read_sql_query(trip_query,db.session.bind)
    monthslist = df['month'].value_counts(dropna=False).keys().tolist()
    monthcount = df['month'].value_counts(dropna=False).tolist()
    months_dict = dict(zip(monthslist, monthcount))
    months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    months_dict = OrderedDict(sorted(months_dict.items(),key =lambda x:months.index(x[0])))
    newmonthlist = list(months_dict.keys())
    newmonthcount = list(months_dict.values())
    print(newmonthlist)
    print(newmonthcount)

    trace = {
        "x": newmonthlist,
        "y": newmonthcount,
        "type": "scatter",
        "fill": "tozeroy",
    }
    return jsonify(trace)



@app.route("/options")
def options():
    options = ["All", "Month", "Day"]

    return jsonify(options)

#################################################
# Han (Heatmap Data)
#################################################


@app.route("/data")
def getdata():
    trip_query=db.session.query(Trip).statement
    df=pd.read_sql_query(trip_query,db.session.bind)

    def process(df, year):
        df1=df[df["Year"]==year]
        checkout=df1["Checkout Kiosk ID"].value_counts()
        Return=df1["Return Kiosk ID"].value_counts()
        c_df=pd.DataFrame({"c_count":checkout})
        r_df=pd.DataFrame({"r_count":Return})
        c_df.reset_index(drop=False,inplace=True)
        r_df.reset_index(drop=False,inplace=True)
        merge=pd.merge(c_df,r_df,on="index",how="outer")
        merge["Year"]=year
        merge["Count"]=merge["c_count"]+merge["r_count"]
        df2=merge[["index","Count","Year"]]
        df2=df2.rename(columns={"index":"kiosk_id"})
        df2.sort_values(["kiosk_id"],inplace=True)
        df2.reset_index(drop=True,inplace=True)
        return df2

    df_14=process(df,2014)
    df_15=process(df,2015)
    df_16=process(df,2016)
    df_all=pd.concat([df_14,df_15,df_16])
    df_all.reset_index(drop=True,inplace=True)

    location_query=db.session.query(Location).statement
    kiosk_df=pd.read_sql_query(location_query,db.session.bind)
    kiosk_df=kiosk_df[["Kiosk ID", "Latitude","Longitude","Kiosk Name"]]
    data_df=pd.merge(df_all,kiosk_df,left_on="kiosk_id",right_on="Kiosk ID")
    final_data=data_df[["Kiosk ID","Count","Year","Latitude","Longitude", "Kiosk Name"]]
    data_json=final_data.to_json(orient="records")
    return data_json

#################################################
# Monica (Pie Chart Data)
#################################################
@app.route("/names")
def names():
    """Return a list of columns"""
    stmt = db.session.query(Data_pie).statement
    df = pd.read_sql_query(stmt, db.session.bind)
    # df['column name'].values.tolist()
    year_list = df["Year"].unique()
    year_list_unique = year_list.tolist()
    return jsonify(year_list_unique)

@app.route("/samples/<year>")
def samples(year):
    stmt = db.session.query(Data_pie).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    selected_year = year

    year_data = df.loc[df["Year"] == int(selected_year),:]

    year_data_json = {
        "Membership": year_data["Membership"].tolist(),
        "Counts": year_data["Counts"].tolist(),
    }

    return jsonify(year_data_json)

if __name__ == "__main__":
    app.run()
