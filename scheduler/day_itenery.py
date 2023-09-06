import itertools
from scheduler.util import time_between_locations
from scheduler.input import get_row
from scheduler.constants import *
from scheduler.util import converted_attractions

def add_time(t1,t2):
    h1,m1 = t1//100,t1%100
    m1+=t2
    h2,m2 = m1//60, m1%60

    return (h1+h2)*100+m2

def get_day_iternery(locations):
    # Initialize a list to store the feasible orders of the locations.
    feasible_orders = []

    # Iterate over all combinations of the locations.
    for order in itertools.permutations(locations):
        cur_time = add_time(order[0]['opening_time'] ,order[0]['duration'])
        order_schedule = [[order[0]['id'],order[0]['opening_time'],cur_time]]  # Store the current order's schedule

        for i in range(1, len(order)):
            travel_time = time_between_locations(order[i - 1]['location'], order[i]['location'])*60
            travel_time = (round(travel_time)//10)*10 +10
            cur_time = add_time(cur_time,travel_time)
            cur_time = max(order[i]['opening_time'], cur_time)
            exit_time = add_time(cur_time ,order[i]['duration'])

            if exit_time > order[i]['closing_time']:
                break

            # Append the id, start time, and end time to the order_schedule
            order_schedule.append([order[i]['id'], cur_time, exit_time])
            cur_time = exit_time

        if len(order_schedule)==len(order):
            feasible_orders.append(order_schedule)

    # If there are no feasible orders, return None.
    if not feasible_orders:
        return None
    else:
        best_idx = 0
        best_time = 100000
        for i in range(len(feasible_orders)):
            tot_time = feasible_orders[i][-1][2]-feasible_orders[i][0][1]
            if tot_time<=best_time:
                best_idx = i
                best_time = tot_time
        return feasible_orders[best_idx]
    
def day_responce(final_days):
    num_days = len(final_days)
    final_days.sort(key=lambda x: x.date)
    resp = {}
    for i in range(num_days):
        dayItr = final_days[i]
        attractions_order = get_day_iternery(converted_attractions(dayItr.attractions,dayItr.day))
        attractions = []
        for ele in attractions_order:
            id,st,en = ele
            row = get_row(id)
            name,type,rating = row[3],TYPE_MAP[row[2]],row[6]
            attractions.append({
                'id' : id,
                'name': name,
                'type': type,
                'rating': rating,
                'start_time': st,
                'end_time': en
            })
            
        
        resp[i] = {
            'date' : dayItr.date,
            'day' : DAY_MAP[dayItr.day],
            'attractions' : attractions
        }
    return resp


