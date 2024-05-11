from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Load the time periods data from JSON file
with open('schedule.json', 'r') as file:
    time_periods = json.load(file)

@app.route('/api/schedule')
def get_schedule():
    return {
        "schedule": time_periods
    }
    
# Get todays schedule route
@app.route('/api/today')
def get_todays_schedule():
    # Get the current day of the week
    import datetime
    today = datetime.datetime.today().strftime('%A')
    
    # Get the schedule for the current day
    todays_schedule = time_periods.get(today)
    
    return {
        "schedule": todays_schedule
    }

@app.route('/api/update-lecture/<int:id>', methods=['PUT'])
def update_lecture(id):
    global time_periods
    
    # Retrieve lecture data from request
    data = request.get_json()
    new_lecture = data.get('lecture')

    # Find the specific lecture item with the provided id
    for day_schedule in time_periods.values():
        for lecture in day_schedule:
            if lecture['id'] == id:
                lecture['lecture'] = new_lecture
                break
    
    # Save the updated time_periods back to the JSON file
    with open('schedule.json', 'w') as file:
        json.dump(time_periods, file, indent=4)
    
    return jsonify({'message': 'Lecture updated successfully'})

if __name__ == '__main__':
    app.run(debug=True)
