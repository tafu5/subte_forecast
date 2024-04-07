import requests

def API_request(url: str) -> dict:
    
    """ Returns the JSON if the request is succefully """

    # Make a request to the API
    response_gtfs_forecast = requests.get(url)

    # If the request was successful
    if response_gtfs_forecast.status_code == 200:
        
        print("Successful API request")
        
        # Store the response data in gtfs_forecast_table
        gtfs_forecast_table = response_gtfs_forecast.json()    

    else:
        
        # Display an error message if the request was not successful
        print("Error making API request:", response_gtfs_forecast.status_code)
    
    return gtfs_forecast_table
