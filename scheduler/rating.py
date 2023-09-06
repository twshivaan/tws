from scheduler.structures import *
from scheduler.constants import *
from scheduler.util import *
from scheduler.day_itenery import get_day_iternery

def get_timing(day_set:DaySet, attraction:Attraction):
    if len(day_set.attractions) == 0:
        return 0
    
    best_time = float("inf")
    for selected_attraction in day_set.attractions:
        travel_time = time_between_locations(selected_attraction.location, attraction.location)
        best_time = min(best_time,travel_time)
    return best_time

def average_rating(attractions:list):
    total_rating = 0
    total_duration = 0
    for attraction in attractions:
        total_rating += attraction.rating
        total_duration += attraction.duration
    return total_rating/total_duration

def get_effective_rating(day_set:DaySet, attraction:Attraction,time_penelty_factor:float):
    effective_timing = max(get_timing(day_set,attraction) - LENIENT_TIMING,0)
    effective_rating = attraction.rating - effective_timing*time_penelty_factor
    return effective_rating

def get_rating_matrix(day_sets:list,attractions:list): 
    AVG_RATING = average_rating(attractions)
    rating = []
    for i in range(len(day_sets)):
        for j in range(len(attractions)):
                cur_day = day_sets[i].day
                new_day_set = day_sets[i].attractions + [attractions[j]]
                if ( attractions[j].timings[cur_day].open == 0 or #attraction closed on that day
                    get_day_iternery(converted_attractions(new_day_set,cur_day))==None): #Not possible
                    rating.append([i,j,0])
                else:
                    effective_rating = get_effective_rating(day_sets[i],attractions[j],AVG_RATING)
                    rating.append([i,j,effective_rating])
    rating.sort(key=lambda x: x[2])
    return rating

def match_attraction_day(day_sets:list,attractions:list):
    rating_matrix = get_rating_matrix(day_sets,attractions)
    return rating_matrix[-1]



