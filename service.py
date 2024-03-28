import os
from flask import Flask, jsonify
from PIL import Image
from flask import send_file
from repo import create_connection
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
db_conn = create_connection()

def get_coordinates(conn):
    coordinates = {}
    cursor = conn.cursor()
    cursor.execute('''
    WITH RecentLocations AS (
    SELECT 
        employee_id,
        x,
        y,
        created_at,
        ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY created_at DESC) AS rn
    FROM location
    )
    SELECT employee_id,x,y
    FROM RecentLocations
    WHERE rn = 1;
    ''')

    for row in cursor:
        coordinates[row[0]] = {"x":row[1],"y":row[2]}

    return coordinates

def classify_crop_condition(pixel):
    r, g, b = pixel
    red_range = [(200, 0, 0), (255, 150, 150)]
    yellow_range = [(255, 255, 0), (255, 255, 150)]
    green_range = [(0, 128, 0), (150, 255, 150)]

    if red_range[0][0] <= r <= red_range[1][0]:
        return "Dead Crops"
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
    crop_percentages = {condition: (count / total_pixels) * 100 for condition, count in crop_counters.items()}
    return {'image': os.path.basename(image_path), 'crop_percentages': crop_percentages}


@app.route('/coordinates', methods=['GET'])
def get_coordinates_route():
    coordinates = get_coordinates(db_conn)
    response = jsonify(coordinates)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/analyze_images', methods=['GET'])
def analyze_images_route():
    try:
        images_folder = "/mnt/c/Users/jasee/OneDrive/Desktop/Studies/ASE/images"
        results = []

        # Concurrently analyze images using ThreadPoolExecutor
        with ThreadPoolExecutor() as executor:
            image_paths = [os.path.join(images_folder, filename) for filename in os.listdir(images_folder) if filename.endswith('.jpg') or filename.endswith('.jpeg')]
            print(image_paths)
            # Collect results for each image analysis
            for result in executor.map(calculate_crop_percentage, image_paths):
                results.append(result)
        print(results)
        response = jsonify(results)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_image/<filename>', methods=['GET'])
def get_image_route(filename):
    images_folder = "/mnt/c/Users/jasee/OneDrive/Desktop/Studies/ASE/images"
    image_path = os.path.join(images_folder, filename)
    return send_file(image_path, mimetype='image/jpg')  # Assuming JPG images

if __name__ == '__main__':
    app.run(debug=True)
