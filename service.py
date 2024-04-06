from datetime import datetime
import logging
import os
import sqlite3
from flask import Flask, jsonify
from PIL import Image
from flask import send_file
from matplotlib import pyplot as plt
import matplotlib
from config import get_config
from repo import create_connection
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

# app = Flask(__name__)
# db_conn = create_connection()

def classify_crop_condition(pixel):
    r, g, b = pixel
    red_range = [(200, 0, 0), (255, 150, 150)]
    yellow_range = [(255, 255, 0), (255, 255, 150)]
    green_range = [(0, 128, 0), (150, 255, 150)]

    if red_range[0][0] <= r <= red_range[1][0]:
        return "Healthy Crops"
    elif yellow_range[0][1] <= g <= yellow_range[1][1]:
        return "Dried Crops"
    elif green_range[0][1] <= g <= green_range[1][1]:
        return "Healthy Crops"
    else:
        return "Barren Land"

def calculate_crop_percentage(image_path):
    image = Image.open(image_path)
    rgb_image = image.convert('RGB')
    width, height = rgb_image.size

    crop_counters = Counter()
    for pixel in rgb_image.getdata():
        crop_condition = classify_crop_condition(pixel)
        crop_counters[crop_condition] += 1

    total_pixels = width * height
    crop_percentages = {condition: round((count / total_pixels) * 100,2) for condition, count in crop_counters.items()}
    return {'image': os.path.basename(image_path), 'crop_percentages': crop_percentages}

def get_zones(conn):
    try:
        resp = []
        cursor = conn.cursor()
        cursor.execute('SELECT distinct zone_id FROM zone_metrics')
        trackers = cursor.fetchall()  # Fetch all rows
        for tracker in trackers:
            resp.append(tracker[0])
        return resp
    except sqlite3.Error as e:
        print("Error fetching trackers:", e)
        return []

def get_historic_data(conn, start_date, end_date, cadence, zone_id):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    cadence_format = ""
    if cadence == "hour":
        cadence_format = '%Y-%m-%d %H'
    elif cadence == "day":
        cadence_format = '%Y-%m-%d'
    elif cadence == "week":
        cadence_format = '%Y-%W'
    else:
        cadence_format = '%Y-%m'
    cursor = conn.cursor()
    query = f'''
    SELECT
        strftime('{cadence_format}',created_at) as cadence_start,
	    metric_name,
        min(metric_value) as minimum,
	    avg(metric_value) as average,
        max(metric_value) as maximum
    FROM zone_metrics
    WHERE zone_id = ?
        AND created_at BETWEEN ? AND ?
    GROUP BY zone_id, metric_name,cadence_start;
    '''
    cursor.execute(query, (zone_id,start_date,end_date))
    data = {"temperature":{"avg":[],"min":[],"max":[]},"moisture":{"avg":[],"min":[],"max":[]}}
    for row in cursor:
        label = ""
        metric_name = row[1]
        if cadence == 'hour':
            label = str(row[0])
        else:
            label = row[0]

        data[metric_name]["min"].append([label,row[2]])
        data[metric_name]["avg"].append([label,row[3]])
        data[metric_name]["max"].append([label,row[4]])
    return data