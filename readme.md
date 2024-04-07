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
<img width="841" alt="1_data_ingestion" src="https://github.com/tafu5/subte_forecast/assets/55017296/662bcfec-93ef-41ab-8195-c8908547e7ba">


### App

There are 3 steps:
- Selection of the line:

<img width="558" alt="2_line" src="https://github.com/tafu5/subte_forecast/assets/55017296/568c8ae6-078c-4646-9021-61a4764cc5ff">

- Selection of the departure station:

<img width="547" alt="3_from" src="https://github.com/tafu5/subte_forecast/assets/55017296/128fef30-fbc9-4b1f-bbbb-5e89dfab9682">


- Selection of the destination:

<img width="546" alt="4_to" src="https://github.com/tafu5/subte_forecast/assets/55017296/67aa6aec-1de4-424a-a560-e6669bf9b2e4">

#### Results:
<img width="847" alt="5_results" src="https://github.com/tafu5/subte_forecast/assets/55017296/0e6c5bbd-f743-41f2-858a-a132aa3e88c2">


