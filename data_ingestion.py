from subte_request import API_request
from mongodb_connection import NoSQL_database_conection, insert_doc
from config import API_REQUEST_LINK
import time

# Make the API request
gtfs_forecast_table = API_request(API_REQUEST_LINK)

# Connection to the NoSQL database in MongoDB
collection = NoSQL_database_conection()

current_time = int(time.time())
# window_size is 1 hour in timestamp
window_size = 60 * 30
# initial_time is 1 hour before the current_time
initial_time = current_time - window_size

# Delete old documents
collection.delete_many({"Header.timestamp": {"$lt": initial_time}})

# Make the data ingest
insert_doc(collection, gtfs_forecast_table)

