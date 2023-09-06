
class DaySet:
    def __init__(self,day,date,day_limit):
        self.day = day
        self.day_limit = day_limit
        self.date = date
        self.attractions = []

class Timing:
    def __init__(self,day,open,st_time,en_time):
        self.day = day
        self.open = open
        self.st_time = st_time
        self.en_time = en_time

class Attraction:
    def __init__(self,id:int,duration:int,timings:list,rating:float,location:list,at_type:int,name:str):
        self.id = id
        self.duration = duration
        self.rating = rating
        self.location = location
        self.type = at_type
        self.timings = timings
        self.name = name
    
    # Define comparison for less than
    def __lt__(self, other):
        return self.rating > other.rating
