from flask import Flask, render_template ,request, jsonify,redirect,session,make_response
import sqlite3
import json
from scheduler.location_itenery import location_itenery
# from scheduler.input import get_about,get_location
import scheduler.input as getInput

DB_ADDRESS = "tws2.db"

icon_map = {
    'Nature & Outdoor': "fa-tree",
    'Historical & Cultural': "fa-landmark",
    'Food & Drinks': "fa-martini-glass",
    'Shopping & Markets': "fa-store",
    'Transportation & Infrastructure': "fa-train",
    'Relaxation & Wellness': "fa-spa",
    'Religious': "fa-yin-yang",
    'Amusement & Entertainment': "fa-ticket",
}

app = Flask(__name__)
app.secret_key = "very_secure_and_secret_key_shhhhh"

def get_city_list():
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_ADDRESS)
    cursor = conn.cursor()

    # Fetch data from the database
    cursor.execute('SELECT * FROM Cities')
    data = cursor.fetchall()

    # Close the database connection
    conn.close()

    return data 

def get_city_idx(name):
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_ADDRESS)
    cursor = conn.cursor()

    query = f"""
        SELECT id FROM Cities WHERE name= '{name}'
    """
    # Fetch data from the database
    cursor.execute(query)
    data = cursor.fetchall()

    # Close the database connection
    conn.close()

    return data[0][0] 

def get_attraction_types(city):
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_ADDRESS)
    cursor = conn.cursor()

    query = f"""SELECT DISTINCT t.name
            FROM Attractions a
            INNER JOIN Types t ON a.type_id = t.id
            WHERE a.city_id = {city};
            """
    # Fetch data from the database
    cursor.execute(query)
    data = cursor.fetchall()
    attraction_types_list = []
    for d in data:
        attraction_types_list.append(d[0])
    return attraction_types_list

# Inline conversion using lambda
format_time = lambda tt: str(tt).zfill(4)[:2] + ":" + str(tt).zfill(4)[2:]

@app.route('/',methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.form["data"]
        session["data"] = data
        response = make_response('OK', 200)
        return response
    cities = get_city_list()
    return render_template('index.html', cities=cities)

@app.route('/select_attractions/')
def select_attractions():
    data = json.loads(session.get("data"))
    selected_city = data['city']
    start_date = data['startDate']
    end_date = data['endDate']
    city_name = get_city_list()[int(selected_city)][1]
    attraction_types = get_attraction_types(selected_city)
    print(data)
    return render_template(
        'attractions.html', 
        city_name=city_name, attraction_types=attraction_types, icon_map=icon_map,
        start_date=start_date, end_date=end_date)

@app.route('/itenery', methods=['GET','POST'])
def itenery():
    if request.method == "POST":
        request_data = request.json  # This will parse the JSON data from the request body
        session["request_data"] = request_data
        response = make_response('OK', 200)
        return response
    request_data = session.get("request_data")
    print('GET',request_data)
    print()
    response_data = location_itenery(request_data.copy())
    print('POST',response_data)
    attraction_types = get_attraction_types(get_city_idx(request_data['city']))
    return render_template('itenery.html',city_name =request_data['city'],
                           response_data=response_data,format_time=format_time,icon_map=icon_map,
                           getInput=getInput,request_data=request_data,attraction_types=attraction_types)

if __name__ == '__main__':
    app.run(debug=True)

