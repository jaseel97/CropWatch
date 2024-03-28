import pandas as pd
from gtts import gTTS
import os

# Function to detect spikes in temperature and moisture
def detect_issues(data, temp_threshold=2, moisture_threshold=0.05):
    issues = []

    # Loop through each zone
    for zone_id, zone_data in data.groupby('Zone Id'):
        # Check for high temperature
        temp_max = zone_data[zone_data['MetricName'] == 'Temp']['MetricValue'].max()
        if temp_max > 30:
            issues.append(f"Zone {zone_id} has high temperature: {temp_max:.2f}°C")

        # Check for high moisture
        moisture_max = zone_data[zone_data['MetricName'] == 'Moisture']['MetricValue'].max()
        if moisture_max > 0.70:
            issues.append(f"Zone {zone_id} has high moisture level: {moisture_max:.2f}")

        # Check for temperature spikes
        temp_values = zone_data[zone_data['MetricName'] == 'Temp']['MetricValue'].tolist()
        for i in range(1, len(temp_values) - 1):
            if abs(temp_values[i] - temp_values[i-1]) > temp_threshold and abs(temp_values[i] - temp_values[i+1]) > temp_threshold:
                issues.append(f"Zone {zone_id} has temperature spikes")

        # Check for moisture spikes
        moisture_values = zone_data[zone_data['MetricName'] == 'Moisture']['MetricValue'].tolist()
        for i in range(1, len(moisture_values) - 1):
            if abs(moisture_values[i] - moisture_values[i-1]) > moisture_threshold and abs(moisture_values[i] - moisture_values[i+1]) > moisture_threshold:
                issues.append(f"Zone {zone_id} has moisture spikes")

    return issues

# Read data from CSV file
data = pd.read_csv(r'/mnt/c/Users/jasee/OneDrive/Desktop/Studies/ASE/Group Project/API/data.csv')


# Sort the data by Zone Id
data = data.sort_values(by='Zone Id')

# Detect issues
issues = detect_issues(data)

# Convert issues to speech
text = ""
if issues:
    text += "Issues:\n"
    for issue in issues:
        text += f"{issue}\n"
else:
    text += "No issues detected.\n"

# Function to convert text to speech
def text_to_speech(text, filename):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    # os.system(f'start {filename}')

# Convert text to speech and save as MP3
text_to_speech(text, "output.mp3")
