# Subway Arrival App

## Goal
The goal of this project is to show the arrival time between two subway stations in Buenos Aires on Real Time.

## Collected data
This project uses forecast GTFS data, which is collected in real time from the Transport API of Buenos Aires and is stored in a MongoDB database.

The API also provides static GTFS data containing information about transit systems such the stop names, schedule arrival and departure times, service frequency, etc. This data is stored in a MySQL database. 

## Files
- **mongodb_connection.py:** Make the connection to the collection stored in MongoDB.
- **mysql_connection.py:** Make the connection to the tables stored in MySQL
- **subte_request.py:** Make the API request
- **data_ingestion.py:** Store the requested data in the MongoDB database
- **run_data_ingestion.py:** Repeat the data ingestion every 3 minutes between the operation service time (7:00 to 23:00)
- **input:** Window Selector to choose the line and the departure and destination station.
- **data_process.py:** Function to merge structured and unstructured data and process it.
- **main.py:** Is app core that processes the trip information, collect the data,calculates arrival times, and returns the final results
- **results.py:** Shows the results


## Usage
By selecting the subway line and the stations where the trip starts and ends, the app will show the next service time from the departure station and the expected arrival time to the destination. Also will show the time for the nexts running services and the scheduled services.

## Example

### Data Ingestion

The API is requested every 3 minutes:

![Data_ingestion](1_data_ingestion.png)

### App

There are 3 steps:
- Selection of the line:

![Data_ingestion](2_line.png)
- Selection of the departure station:

![Data_ingestion](3_from.png)
- Selection of the destination:

![Data_ingestion](4_to.png)