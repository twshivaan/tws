import heapq
from datetime import datetime,timedelta
from scheduler.constants import *
from scheduler.structures import *
from scheduler.input import get_attraction_list
from scheduler.rating import match_attraction_day
from scheduler.day_itenery import day_responce
from scheduler.util import converted_attractions


def setup(request):
    # format_string = '%a, %d %b %Y %H:%M:%S GMT'
    # request['st_date'] = datetime.strptime(request['st_date'], format_string).strftime('%Y-%m-%d').date()
    # request['en_date'] = datetime.strptime(request['en_date'], format_string).strftime('%Y-%m-%d').date()
    request['st_date'] = datetime.strptime(request['st_date'], "%Y-%m-%d").date()
    request['en_date'] = datetime.strptime(request['en_date'], "%Y-%m-%d").date()

    num_types = len(request['types'])
    num_days,start_day =  (request['en_date'] - request['st_date']).days+1, request['st_date'].weekday()
    daySets = []
    curDate,curDay = request['st_date'],start_day
    for i in range(num_days):
        new_day = DaySet(curDay,curDate,DAY_LIMIT)
        daySets.append(new_day)

        curDate += timedelta(days=1)
        curDay = curDate.weekday()
    
    type_heaps = {}
    for types in request['types']:
        type_heaps[types] = []
    
    attractions = get_attraction_list(request)

    for attraction in attractions:
        # print(attraction.__dict__)
        type_heaps[attraction.type].append(attraction)
    
    for types in request['types']:
        heapq.heapify(type_heaps[types])

    typeSets = []

    for types in request['types']:
        typeSets.append(heapq.heappop(type_heaps[types]))
    
    return daySets,typeSets,type_heaps


def location_itenery(request):
    daySets,typeSets,type_heaps = setup(request)
    # print(len(daySets),len(typeSets))

    final_days= []
    
    while(len(daySets)!=0 and len(typeSets)!=0):
        day_idx, type_idx,_  = match_attraction_day(daySets,typeSets)
        daySets[day_idx].attractions.append(typeSets[type_idx])

        if len(daySets[day_idx].attractions) == daySets[day_idx].day_limit:
            final_days.append(daySets[day_idx])
            daySets.pop(day_idx)
        
        for i in range(len(typeSets)):
            typeSets[i].rating += TYPE_INCLUSION_FACTOR
        
        if len(type_heaps[typeSets[type_idx].type])!=0:
            typeSets[type_idx] = heapq.heappop(type_heaps[typeSets[type_idx].type])
        else:
            typeSets.pop(type_idx)
    
    # for ele in final_days:
    #     print(ele.day,ele.date,converted_attractions(ele.attractions,ele.day))
    
    return day_responce(final_days)



    
    
    
# request = {
#     'city': 'Mumbai', 
#     'st_date': '2023-08-10', 
#     'en_date': '2023-08-10', 
#     'types': [
#         'Nature & Outdoor',
#         'Historical & Cultural',
#         'Food & Drinks',
#         'Shopping & Markets',
#         'Transportation & Infrastructure',
#         'Relaxation & Wellness',
#         'Religious',
#         'Amusement & Entertainment'
#     ], 
#     'exclude': [918,], 
#     'include': [], 
#     'duration': [[], []]
# }
# print(location_itenery(request))