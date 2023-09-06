from geopy.distance import geodesic
from scheduler.constants import *

def time_between_locations(l1:list,l2:list):
    distance = geodesic(l1, l2).kilometers
    travel_time = distance / AVG_SPEED 
    return travel_time

def converted_attractions(attractions, day):

  converted_attractions = []

  for attraction in attractions:
    converted_attraction = {
          "id" : attraction.id,
          "opening_time": int(attraction.timings[day].st_time),
          "closing_time": int(attraction.timings[day].en_time),
          "duration": 60*attraction.duration,
          "location": attraction.location
      }
    if converted_attraction['closing_time'] < converted_attraction['opening_time']:
       converted_attraction['closing_time']+=2400
    converted_attractions.append(converted_attraction)

  return converted_attractions