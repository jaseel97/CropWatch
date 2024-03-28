import os
from flask import Flask, jsonify, send_file
from PIL import Image
from repo import create_connection
from service import calculate_crop_percentage
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
db_conn = create_connection()

def get_coordinates(conn):
    print("in service")
    cursor = db_conn.cursor()
    rows = cursor.execute('''
        SELECT l.employee_id, l.x, l.y
        FROM location l
        JOIN (
            SELECT employee_id, MAX(created_at) AS latest_created_at
            FROM location
            GROUP BY employee_id
        ) latest_loc
        ON 
            l.employee_id = latest_loc.employee_id
            AND l.created_at = latest_loc.latest_created_at
    ''')
    print(rows)

def analyze_image(image_path):
    try:
        crop_percentages = calculate_crop_percentage(image_path)
        return {'image': os.path.basename(image_path), 'crop_percentages': crop_percentages}
    except Exception as e:
        return {'image': os.path.basename(image_path), 'error': str(e)}

@app.route('/coordinates', methods=['GET'])
def get_coordinates_route():
    coordinates = get_coordinates(db_conn)
    print("controller : ",coordinates)
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
            image_paths = [os.path.join(images_folder, filename) for filename in os.listdir(images_folder)
                            if filename.endswith('.jpeg') or filename.endswith('.png')]
            # Collect results for each image analysis
            for result in executor.map(analyze_image, image_paths):
                results.append(result)

        response = jsonify(results)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_image/<filename>', methods=['GET'])
def get_image_route(filename):
    images_folder = "/mnt/c/Users/jasee/OneDrive/Desktop/Studies/ASE/images"
    image_path = os.path.join(images_folder, filename)
    return send_file(image_path, mimetype='image/jpeg')  # Assuming JPG images

if __name__ == '__main__':
    app.run(debug=True)
