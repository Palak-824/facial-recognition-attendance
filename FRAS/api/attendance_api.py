from flask import Flask, jsonify, request
import os
import pandas as pd
from threading import Thread
from werkzeug.serving import make_server

app = Flask(__name__)

# Your existing API routes here
@app.route("/")
def home():
    return "Flask API running"

# Store the server object globally
class FlaskServer:
    def __init__(self, app):
        self.server = make_server('127.0.0.1', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def start(self):
        self.thread = Thread(target=self.server.serve_forever)
        self.thread.start()

    def shutdown(self):
        self.server.shutdown()
        self.thread.join()

flask_server = FlaskServer(app)

@app.route('/get-attendance', methods=['GET'])
def get_attendance():
    # Get the date parameter from the URL
    selected_date = request.args.get('date')
    
    if not selected_date:
        return jsonify({"error": "Date not provided"}), 400

    # Construct the file name based on the date
    file_name = f"attendance\\attendance_{selected_date}.csv"
    
    if os.path.exists(file_name):
        # Read the CSV file using pandas
        df = pd.read_csv(file_name, usecols=['Id', 'Name'])
        
        # Convert the dataframe to a dictionary format
        data = df.to_dict(orient="records")
        
        return jsonify(data)
    else:
        return jsonify({"error": f"Attendance file for {selected_date} not found"}), 404
