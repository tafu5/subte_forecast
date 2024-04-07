from sqlalchemy import create_engine, text
import pandas as pd
from config import MYSQL_LINK

def SQL_database_connection(query: str) -> pd.DataFrame:
    
    """ Returns the query as a DataFrame"""

    # Connection to the database in MySQL
    engine = create_engine(MYSQL_LINK)
    # Run the query
    stop_station_times = pd.DataFrame(engine.connect().execute(text(query)).fetchall())

    return stop_station_times

