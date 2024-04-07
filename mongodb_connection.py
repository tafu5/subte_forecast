# Data ingestion using pymongo
import pymongo
from config import MONGODB_LINK

def NoSQL_database_conection() -> pymongo.collection.Collection:
    
    """ Returns the NoSQL database """

    # Connect to the server
    client = pymongo.MongoClient(MONGODB_LINK)

    # Select the database
    db = client['subte']

    # Select the collection
    collection = db['gtfs_forecast']

    return collection


def insert_doc(collection: pymongo.collection.Collection, gtfs_forecast_table: dict) -> str:

    # Getting the timestamp of the document to add
    doc_collected = collection.aggregate(
        [
            {"$project": {"timestamp": "$Header.timestamp",
                        "_id": 0}}
        ]
    )

    # get timestamp values
    doc_collected = [c.get('timestamp') for c in doc_collected]

    # Getting the timestamp of the document to add
    doc_to_add = gtfs_forecast_table["Header"]['timestamp']

    # Check if document is already in the database
    doc_check = doc_to_add in doc_collected

    # If is not in the database it will be added
    if not doc_check:
        # Data ingestion to the database in  MongoDB
        outcome = "Document added"
        collection.insert_one(gtfs_forecast_table)
    else:
        outcome = "Document already stored"

    return print(outcome)

