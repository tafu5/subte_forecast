import easygui
from mysql_connection import SQL_database_connection
from datetime import datetime

def selector() -> dict:

    """ Returns the input of the App by choosing the Line and stops 
        where the trip starts and ends """

    # Query to get line names and stop_id, 
    query = "SELECT a.stop_name, a.trip_id, a.stop_sequence, b.route_id FROM  (SELECT st.stop_name, s.trip_id, s.stop_sequence FROM subte.stop_times as s LEFT JOIN subte.stops_new as st on s.stop_id = st.stop_id WHERE (RIGHT(s.trip_id, 2) = '01')) AS a  LEFT JOIN subte.trips  AS b on a.trip_id = b.trip_id;"
    # Connect to the static database
    options = SQL_database_connection(query).drop_duplicates()
    # Get the line names
    line_options = options['route_id'].unique()

    # Line selector
    line_selection = easygui.choicebox("Select a Line: ",
                                        choices = line_options)

    if line_selection is not None:
        # Mask of line selection        
        stop_mask = options['route_id'] == str(line_selection)
        # Get stop names of the selected line
        stop_options = options[stop_mask]['stop_name'].unique()
        # Stop selector for the departure stop
        stop_from_selection = easygui.choicebox("From: ",
                                                choices = stop_options)
        # Delete the departure stop of the list
        stop_options_to = [c for c in stop_options if c != stop_from_selection]
        # Stop selector for the destination stop
        stop_to_selection = easygui.choicebox("To: ",
                                            choices = stop_options_to)
        
        # Get the sequence of the selected stops
        sequence_from_mask = (options['route_id'] == line_selection) & (options['stop_name'] == stop_from_selection)
        sequence_from = options[sequence_from_mask]['stop_sequence']

        sequence_to_mask = (options['route_id'] == line_selection) & (options['stop_name'] == stop_to_selection)
        sequence_to = options[sequence_to_mask]['stop_sequence']
        
        # Get trip_id
        trip_id = options[sequence_from_mask]['trip_id'].unique()[0]

        # Get the direction id of the service
        if int(sequence_from.unique()[0]) > int(sequence_to.unique()[0]):
            direction_id = '1'
        else:
            direction_id = '0'
        
        # Current day number
        n_day = datetime.now().day

        # Get the trip_number 
        if n_day == 6:
            trip_number = '2'
        elif n_day == 7:
            trip_number = '3' 
        else:
            trip_number = '1' 
        
        # Set the correct trip_id
        trip_id = trip_id[0] + direction_id + trip_number

        # Input values
        val = {'trip_id' : trip_id,
                'line' : line_selection,
                'stop_from' : stop_from_selection,
                'stop_to' : stop_to_selection}
    return val  

# Run the selector function to get the inputs    
values = selector()

