from mysql_connection import SQL_database_connection
from mongodb_connection import NoSQL_database_conection
from input import values
from data_process import train_delta_time, merge_and_process, get_trips, filter_stops, scheduled_train


def main_run() -> list:
    # Query SQL
    sql_query = f"SELECT stop_id, arrival_time as arrival_time_real, departure_time as departure_time_real FROM stop_times WHERE trip_id ='{values['trip_id']}'"

    # Get the stop station times 
    stop_station_times = SQL_database_connection(sql_query)

    # Add duration between stop stations 
    stop_station_times['delta_times'] = train_delta_time(stop_station_times,
                                                        'arrival_time_real',
                                                        'departure_time_real')

    # Get the connection to the database that contains past trips
    collection = NoSQL_database_conection()

    # Get the trips of the selected line
    trips = get_trips(collection)    

    
    # Results will contains the expected arrival times to the selected stop stations
    results = list()
    
    for _id in trips['_id'].unique():
        
        # Mask to get the current trip
        mask_trip = trips['_id'] == _id

        # Get the current trip among the total trips 
        current_trip = trips[mask_trip].copy().reset_index(drop = True)

        # Data processing
        trip_merged = merge_and_process(current_trip, stop_station_times)
        
        # Data filtering
        trip_filtered = filter_stops(trip_merged)

        # Get arrival times to the stop stations
        trip_arrival_times = trip_filtered['arrival_time']
        
        # Add the start time of the service
        trip_arrival_times_datetime = [time.to_pydatetime() for time in trip_arrival_times] + [current_trip['arrival_time'].iloc[0].to_pydatetime()]
        
        # Save results to the 'trip_arrival_times_datetime' list
        results.append(trip_arrival_times_datetime)
        
    # Remove duplicated results
    unique_results = set(map(tuple, results))
    
    # Sort results 
    unique_results = sorted(unique_results, 
                            key = lambda x: x[0])
    
    # Add Scheduled services
    scheduled_reults = scheduled_train(unique_results[-1], values['trip_id'])
    
    # Concat the running services with the scheduled ones
    total_results = unique_results + scheduled_reults
    
    # Numeber of running services
    total_running_trains = len(unique_results)
    
    return total_results, total_running_trains


