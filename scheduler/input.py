import sqlite3
from scheduler.constants import *
from scheduler.structures import *
from pexels_api import API
import json



DB_ADDRESS = "../Data/tws2.db"

def open247(day_results):
    for day in day_results:
        if day[3] == 1:
            return 0
    return 1

def get_attraction_list(requirement):
    types_string = ",".join(["'"+str(type_id)+"'" for type_id in requirement["types"]])
    query = f"""
    SELECT * FROM Attractions
    WHERE city_id = (SELECT id FROM Cities WHERE name = '{requirement["city"]}') 
    AND type_id IN (SELECT id FROM Types WHERE name IN ({types_string}))
    """
    conn = sqlite3.connect(DB_ADDRESS)
    cursor = conn.cursor()
    cursor.execute(query)
    attractions_results = cursor.fetchall()


    attractions = []
    for row in attractions_results:
        id, duration, rating, location, at_type,name = row[0],row[5],row[6],[row[8],row[9]],row[2],row[3]
        type_query = f"""
            SELECT name from Types
            WHERE id = {at_type}
        """
        cursor.execute(type_query)
        at_type = cursor.fetchall()[0][0]
        if id in requirement["exclude"]:
            continue
        if id in requirement["include"]:
            rating = MAX_RATING
        if id in requirement["duration"][0]:
            rating = MAX_RATING
            duration = requirement["duration"][1][requirement["duration"][0].index(id)]    
    
        time_query = f"""
            SELECT * FROM OperationHours
            WHERE attraction_id = {id}
        """     
        cursor.execute(time_query)
        day_results = cursor.fetchall()
        if len(day_results)==1:
            day_results = STD_TIMING
        if open247(day_results):
            day_results = ALL_TIMING
            
        timings=[]
        for i in range(0,7):
            timings.append(Timing(
                i,
                int(day_results[i][3]),
                int(day_results[i][4]) if day_results[i][4] is not None else -1,
                int(day_results[i][5]) if day_results[i][5] is not None else -1
            ))
        attractions.append(Attraction(id,duration,timings,rating,location,at_type,name))
    
    return(attractions)

def get_row(id):
    query = f"""
        SELECT * from Attractions WHERE id = {id}
    """
    conn = sqlite3.connect(DB_ADDRESS)
    cursor = conn.cursor()
    cursor.execute(query)
    attractions_results = cursor.fetchall()[0]
    # print(attractions_results)
    return attractions_results

def get_about(id):
    query = f"""
        SELECT about from Attractions WHERE id = {id}
    """
    conn = sqlite3.connect(DB_ADDRESS)
    cursor = conn.cursor()
    cursor.execute(query)
    attractions_results = cursor.fetchall()[0][0]
    # print(attractions_results)
    return attractions_results

def get_location(id):
    query = f"""
        SELECT lat,lng from Attractions WHERE id = {id}
    """
    conn = sqlite3.connect(DB_ADDRESS)
    cursor = conn.cursor()
    cursor.execute(query)
    attractions_results = cursor.fetchall()[0]
    # print(attractions_results)
    return attractions_results

# def get_photos(name,city):
#     # Type your Pexels API
#     PEXELS_API_KEY = 'ARe2hWfm1t82LI4DNHY5jIBokogficcSj5N5NLq82nE7Mxh6M0TExRP1'
#     # Create API object
#     api = API(PEXELS_API_KEY)
#     # Search five 'kitten' photos
#     api.search('Gateway of India,Mumbai', page=1, results_per_page=5)
#     # Get photo entries
#     photos = api.get_entries()

def get_photos(id):
    url_list = [
        "https://images.pexels.com/photos/1371168/pexels-photo-1371168.jpeg",
        "https://images.pexels.com/photos/2815093/pexels-photo-2815093.jpeg",
        "https://images.pexels.com/photos/6481558/pexels-photo-6481558.jpeg",
        "https://images.pexels.com/photos/13091771/pexels-photo-13091771.jpeg",
        "https://images.pexels.com/photos/6067512/pexels-photo-6067512.jpeg"
    ]
    return json.dumps(url_list)

def get_timing(id):
    query = f"""
        SELECT * from OperationHours WHERE attraction_id = {id}
    """
    conn = sqlite3.connect(DB_ADDRESS)
    cursor = conn.cursor()
    cursor.execute(query)
    attractions_results = cursor.fetchall()
    if len(attractions_results)==1:
        attractions_results = STD_TIMING
    if open247(attractions_results):
        attractions_results = ALL_TIMING

    timing_data = {}
    
    for index, day_result in enumerate(attractions_results):
        day_dict = {}
        
        day_dict['day'] = DAY_MAP[day_result[2]]  # Get the day name from the list
        day_dict['open'] = 'Open' if bool(day_result[3]) else 'Closed'  # Convert the 'open' value to a boolean
        if bool(day_result[3]):
            day_dict['opening_time'] = day_result[4][:2]+":"+day_result[4][2:]  # Get the opening time
            day_dict['closing_time'] = day_result[5][:2]+":"+day_result[4][2:]  # Get the closing time
        else:
            day_dict['opening_time'] = ""  # Get the opening time
            day_dict['closing_time'] = ""  # Get the closing time
        timing_data[index] = day_dict
    
    return json.dumps(timing_data)

def get_duration(id):
    query = f"""
        SELECT duration from Attractions WHERE id = {id}
    """
    conn = sqlite3.connect(DB_ADDRESS)
    cursor = conn.cursor()
    cursor.execute(query)
    attractions_results = cursor.fetchall()[0][0]
    return attractions_results