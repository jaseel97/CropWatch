from datetime import datetime, timedelta
import pandas as pd
from gtts import gTTS
import os

from config import get_config

config = get_config()

def get_recent_data():
    data = pd.read_csv(r'historic.csv')
    data = data.sort_values(by='ZoneId')
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])

    current_time = datetime.now()
    thirty_minutes_ago = current_time - timedelta(minutes=30)
    recent_data = data[data['Timestamp'] > thirty_minutes_ago]
    return recent_data

# Function to detect spikes in temperature and moisture
def detect_issues(data, temp_threshold=2, moisture_threshold=0.5):
    temp_spike = config["temperature_spike"]
    moisture_spike = config["moisture_spike"]

    current_datetime = datetime.now()
    current_date = current_datetime.date()
    current_time = current_datetime.time()
    formatted_datetime = f"{current_date.year}-{current_date.month:02}-{current_date.day:02} {current_time.hour:02}:{current_time.minute:02}:{current_time.second:02}"

    issues = []
    for zone_id, zone_data in data.groupby('ZoneId'):
        temp_max = zone_data[zone_data['MetricName'] == 'temperature']['MetricValue'].max()
        if temp_max > config["max_temperature"]:
            issues.append(f"Zone {zone_id} has high temperature: {temp_max:.2f} C")

        moisture_max = zone_data[zone_data['MetricName'] == 'moisture']['MetricValue'].max()
        if moisture_max > config["max_moisture"]:
            issues.append(f"Zone {zone_id} has high moisture level: {moisture_max:.2f}")

        temp_values = zone_data[zone_data['MetricName'] == 'temperature']['MetricValue'].tolist()
        for i in range(1, len(temp_values) - 1):
            if abs(temp_values[i] - temp_values[i-1]) > temp_spike and abs(temp_values[i] - temp_values[i+1]) > temp_spike:
                issues.append(f"Zone {zone_id} has a temperature spike")

        moisture_values = zone_data[zone_data['MetricName'] == 'moisture']['MetricValue'].tolist()
        for i in range(1, len(moisture_values) - 1):
            if abs(moisture_values[i] - moisture_values[i-1]) > moisture_spike and abs(moisture_values[i] - moisture_values[i+1]) > moisture_spike:
                issues.append(f"Zone {zone_id} has a moisture spike")

    distinct_warnings = {
        "Warnings":list(dict.fromkeys(issues)),
        "Timestamp":formatted_datetime
    }

    return distinct_warnings

def text_to_speech(text, filename):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    os.system(f'start {filename}')

def speak_issues():
    data = get_recent_data()
    issues = detect_issues(data)
    text = ""
    if issues:
        text += "Issues:\n"
        for issue in issues:
            text += f"{issue}\n"
            text_to_speech(text, "output.mp3")

def get_issues():
    data = get_recent_data()
    return detect_issues(data)
