""" SAMPLE
In this file you can find sample data which could be used
into the TrafficFlowMod class in model.py file
"""

# Graph represented by directed dictionary
# In order: first ("5", "7"), second ("5", "9"), third ("6", "7")...
graph = [
    ("5", ["7", "9"]),
    ("6", ["7", "8"]),
    ("7", ["8", "10"]),
    ("8", ["11", "12"]),
    ("9", ["10", "16"]),
    ("10", ["11", "13"]),
    ("11", ["14"]),
    ("12", ["15"]),
    ("13", ["14", "16"]),
    ("14", ["15", "17"]),
    ("15", []),
    ("16", ["17"]),
    ("17", [])
]

# Capacity of each link (Conjugated to Graph with order)
# Here all the 19 links have the same capacity
capacity = [3600] * 19

# Free travel time of each link (Conjugated to Graph with order)
free_time = [
    10, 10, 
    10, 14.1,
    10, 10,
    10, 14.1,
    10, 22.4,
    10, 10,
    10,
    10,
    10, 10,
    10, 10,
    10
]

# Origin-destination pairs
origins = ["5", "6"]
destinations = ["15", "17"]
# Generated ordered OD pairs: 
# first ("5", "15"), second ("5", "17"), third ("6", "15")...


# Demand between each OD pair (Conjugated to the Cartesian 
# product of Origins and destinations with order)
demand = [6000, 6750, 7500, 5250]

