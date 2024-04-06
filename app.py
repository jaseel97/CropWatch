import json
import logging
import os
from flask import Flask, jsonify, render_template, request, send_file
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from config import get_config
from issue_service import get_issues
from repo import create_connection, create_sqlite_connection
from service import calculate_crop_percentage, get_historic_data, get_zones
from concurrent.futures import ThreadPoolExecutor
from tracker_service import create_tracker, delete_tracker, get_coordinates, get_trackers
from psycopg2.extras import LoggingConnection

logging.basicConfig(level=logging.DEBUG)
config = get_config()

db_conn = create_sqlite_connection()

app = Flask(__name__)
cors = CORS(app)
app.config['JWT_SECRET_KEY'] = config['jwt_key']
jwt = JWTManager(app)

@app.route('/get_image/<filename>', methods=['GET'])
def get_image_route(filename):
    image_path = os.path.join(config["image_directory"], filename)
    return send_file(image_path, mimetype='image/jpg')

@app.route('/analyze_images', methods=['GET'])
def analyze_images_route():
    try:
        images_folder = config["image_directory"]
        results = []
        with ThreadPoolExecutor() as executor:
            image_paths = [os.path.join(images_folder, filename) for filename in os.listdir(images_folder) if filename.endswith('.jpg') or filename.endswith('.jpeg')]
            for result in executor.map(calculate_crop_percentage, image_paths):
                results.append(result)
        response = jsonify(results)
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/coordinates', methods=['GET'])
# @jwt_required()
def get_coordinates_route():
    coordinates = get_coordinates(db_conn)
    response = jsonify(coordinates)
    return response

@app.route('/historic', methods=['GET'])
# @jwt_required()
def get_coordinates_by_window():
    start_date = request.args.get('startDate')#"2024-03-01"
    end_date   = request.args.get('endDate')#"2024-03-31"
    cadence    = request.args.get('cadence')#"hour"
    zone       = request.args.get('zone')#"1"

    data = get_historic_data(db_conn, start_date, end_date, cadence, zone)
    response = jsonify(data)
    return response

@app.route('/issues', methods=['GET'])
# @jwt_required()
def get_issues_route():
    data = get_issues()
    response = jsonify(data)
    return response


@app.route('/trackers', methods=['GET','POST','DELETE'])
# @jwt_required()
@cross_origin()
def trackers_route():
    res = []
    if request.method == 'GET':
        res = get_trackers(db_conn)
    elif request.method == 'POST':
        data = request.get_json(force=True)
        res = create_tracker(db_conn,int(data['id']),data['employee'])
    elif request.method == 'DELETE':
        tracker_id = request.args.get('id', type=int)
        res = delete_tracker(db_conn,tracker_id)

    if res == False:
        return jsonify({'error': "something went wrong"}), 500

    response = jsonify(res)
    return response

@app.route('/zones',methods=['GET'])
def zones():
    res = get_zones(db_conn)
    return jsonify(res)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    users = {
    'user1': 'password1',
    'user2': 'password2'
    }

    if username in users and users[username] == password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

@app.route('/config',methods=['POST','GET'])
def update_config():
    global config
    if request.method == 'POST':
        new_config = request.get_json(force=True)
        config["max_temperature"] = new_config["max_temperature"]
        config["min_temperature"] = new_config["min_temperature"]
        config["max_moisture"] = new_config["max_moisture"]
        config["min_moisture"] = new_config["min_moisture"]
        with open("config.json", "w") as json_file:
            json.dump(config, json_file)
        config = get_config()
        return jsonify(True)
    else:
        return jsonify({
            "max_temperature":config['max_temperature'],
            "min_temperature":config['min_temperature'],
            "max_moisture":config['max_moisture'],
            "min_moisture":config['min_moisture']
        })


# Logout endpoint (not really necessary for JWT)
@app.route('/logout', methods=['POST'])
def logout():
    return jsonify({"message": "Successfully logged out"}), 200

@app.route("/")
@app.route("/menu.html")
def index():
   return render_template("menu.html")

@app.route("/crophealth.html")
def crop_health():
   return render_template("crophealth.html")

@app.route("/historicaldata.html")
def historical_data():
   return render_template("historicaldata.html")

@app.route("/trackerid.html")
def tracker_id():
   return render_template("trackerid.html")

@app.route("/settings.html")
def settings():
   return render_template("settings.html")

if __name__ == '__main__':
    config = get_config()
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
