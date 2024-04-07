import pandas as pd
import numpy as np
import time
import pymongo

from datetime import datetime, timedelta
from input import values
from mysql_connection import SQL_database_connection


# Function to calculate the arrival and departure times including the current delay
def update_times(df: pd.DataFrame) -> pd.DataFrame:

    """ Returns the DF with the real arrival and departure times """
    
    real_arrival_time = list()
    real_departure_time = list()

    for i in np.arange(0, len(df), 1):
        if i == 0: 
            arrival_time = df['arrival_time'].iloc[0]
            departure_time = df['departure_time'].iloc[0]
        else:
            arrival_time = real_departure_time[i-1] + df['delta_times'].iloc[i]
            departure_time = arrival_time + df['stop_duration'].iloc[i]

        real_arrival_time.append(arrival_time)
        real_departure_time.append(departure_time)

    
    df['arrival_time'] = real_arrival_time
    df['departure_time'] = real_departure_time
    
    return df


# Function to calculate times between stop stations
def train_delta_time(df: pd.DataFrame, arrival_col: str, departure_col: str) -> list:

    """ Returns a list with the delta times between the train stations """

    # Number of stations 
    length = len(df)
    # delta_times contains the time diff between stations. The first variations is null
    delta_times = list([np.nan])
    
    for i in np.arange(0, length-1, 1):
        delta_times.append((df[arrival_col].iloc[i+1] - df[departure_col].iloc[i]))
    
    return delta_times


def get_trips(collection: pymongo.collection.Collection) -> pd.DataFrame:

    """ Returns important fields for the trip of the chosen line """

    # Current time
    current_time = int(time.time())
    # window_size is 1 hour in timestamp
    window_size = 60 * 30
    # initial_time is 1 hour before the current_time
    initial_time = current_time - window_size
    
    # Get trips
    trips = collection.aggregate([
        { '$unwind': "$Entity" },
        { '$unwind': "$Entity.Linea.Estaciones" },
        { '$match': {"Entity.Linea.Trip_Id": values['trip_id'],
                    "Header.timestamp": {"$gte": initial_time, "$lte": current_time}}},
        {
            '$project': {
                "stop_name": "$Entity.Linea.Estaciones.stop_name",
                "arrival_time": "$Entity.Linea.Estaciones.arrival.time",
                "arrival_delay": "$Entity.Linea.Estaciones.arrival.delay",
                "departure_time": "$Entity.Linea.Estaciones.departure.time",
                "trip_id": "$Entity.Linea.Trip_Id",
                "stop_id": "$Entity.Linea.Estaciones.stop_id",
                "_id": 1}
        }
    ])

    # Convert the dictionary to DataFrame
    trips = pd.DataFrame(trips)
    
    # Convert arrival and departure timestamp to datetime
    trips['arrival_time'] = trips.apply(lambda x: datetime.fromtimestamp(x['arrival_time']), axis = 1)
    trips['departure_time'] = trips.apply(lambda x: datetime.fromtimestamp(x['departure_time']), axis = 1)

    return trips


def merge_and_process(trip: pd.DataFrame, stop_station_times: pd.DataFrame) -> pd.DataFrame:

    """ Returns the expected stop times given the current trip time and the scheduled
        stop times """

    # Merge the current data trip with the stop_station_times
    trip_merged = trip.merge(
        stop_station_times[['delta_times', 'stop_id']], 
        on ='stop_id')
    
    # Number of stations for the selected line
    number_stations = len(trip_merged)

    # reassign the stop_id to sequential values starting from 0
    trip_merged = trip_merged.assign(stop_id = range(number_stations))
    
    # Calculate the duration for each stop station
    trip_merged['stop_duration'] = trip_merged['departure_time'] - trip_merged['arrival_time']
    
    # Update arrival and departure stop times
    trip_merged = update_times(trip_merged)

    return trip_merged


def filter_stops(trip_merged: pd.DataFrame) -> pd.DataFrame:

    """ Returns the expected time of the arrival to the train stop where begins the trip
        and the expected arrival time of the train stop where the trip ends """
    
    # Stop Dictionary: Contains stop names and stop IDs
    dictionary_stop = dict(zip(trip_merged['stop_name'], trip_merged['stop_id']))

    # Stop ID where the trip starts
    stop_from_id = dictionary_stop.get(values['stop_from'])

    # Stop ID where the trip ends
    stop_to_id = dictionary_stop.get(values['stop_to'])
    

    # Mask of the selected trip
    trip_mask = (trip_merged['stop_id'] == stop_from_id) | (trip_merged['stop_id'] == stop_to_id)

    # Data trip selected
    trip_filtered = trip_merged[trip_mask]

    return trip_filtered


def scheduled_train(last_result, trip_id : str):
    """ Returns scheduled trains after the last running service """
    
    # List to save the scheduled services
    scheduled_results = list()

    # Get the headway seconds for services
    sql_query = f"SELECT start_time, end_time, headway_secs FROM subte.frequencies WHERE trip_id = '{trip_id}';"
    headway_sec_data = SQL_database_connection(sql_query)
    headway_sec_data = pd.DataFrame(headway_sec_data)

    # Convert the 'start_time' and 'end_time' in seconds
    headway_sec_data['start_time'] = headway_sec_data['start_time'].apply(lambda x: x.total_seconds())
    headway_sec_data['end_time'] = headway_sec_data['end_time'].apply(lambda x: x.total_seconds())
    
    # Create a loop to save 5 results
    for i in range(5):
        
        # Get the start time of the last running service
        train_start = last_result[2]
        train_start_time = train_start.time()

        # Convert the 'train_start' in seconds
        train_start_time_seconds = timedelta(hours = train_start_time.hour,
                                             minutes = train_start_time.minute, 
                                             seconds = train_start_time.second).seconds
        
        # Mask 
        mask = (headway_sec_data['start_time'] < train_start_time_seconds) & (train_start_time_seconds < headway_sec_data['end_time'])

        # get the headway_sec for services where its trip_id ends in '2' or '3' 
        if (trip_id[-1] == '2') | (trip_id[-1] == '3'):
            headway_sec = int(headway_sec_data['headway_secs'].values[0])
        
        # Apply mask for services where trip_id ends in '1' to get the headway_sec
        else:
            headway_sec = headway_sec_data[mask]['headway_secs']
            headway_sec = int(headway_sec.values[0])
                
        ## Schedule times
        # Scheduled Time of the stop station where the trip starts
        from_time = last_result[0] + timedelta(seconds = headway_sec)
        # Scheduled time of the stop station where the trip ends
        to_time = last_result[1] + timedelta(seconds = headway_sec)
        # Scheduled time of the service
        train_start = train_start + timedelta(seconds =  headway_sec)

        # Save times in a list
        last_result = [from_time, to_time, train_start]

        # Add results to the 'scheduled_results' list 
        scheduled_results.append(last_result)
    
    return scheduled_results






        



