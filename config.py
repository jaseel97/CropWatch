from decimal import Decimal

import json

def get_config():
    with open('config.json', 'r') as file:
        config = json.load(file)
    return config

# def get_config():
#     # images_folder = "/mnt/c/Users/jasee/OneDrive/Desktop/Studies/ASE/images"
#     config =  {}

#     config["image_directory"] = 'images' #"C:\\Users\\jasee\\OneDrive\\Desktop\\Studies\\ASE\\Group Project\\images"#"/mnt/c/Users/jasee/OneDrive/Desktop/Studies/ASE/images"
#     config["jwt_key"] = "awejhkf123wa9248adh839"

#     config["map_width"]  = Decimal(400)     # Width of the map image in pixels
#     config["map_height"] = Decimal(297)     # Height of the map image in pixels
#     config["min_lat"]    = Decimal(0)       # Minimum latitude of the map
#     config["max_lat"]    = Decimal(100)     # Maximum latitude of the map
#     config["min_lon"]    = Decimal(0)       # Minimum longitude of the map
#     config["max_lon"]    = Decimal(90)      # Maximum longitude of the map

#     return config