from flask import Flask, render_template_string, render_template, jsonify
from flask import json
from datetime import datetime
from urllib.request import urlopen, Request
import sqlite3

app = Flask(__name__) #com

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/commits/")
def commits_page():
    return render_template("commits.html")

@app.route('/extract-minutes/')
def extract_minutes():
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(req)
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    minutes_count = {}
    for commit in json_content:
        date_string = commit['commit']['author']['date']
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minute = date_object.minute
        minutes_count[minute] = minutes_count.get(minute, 0) + 1
    results = []
    for m in sorted(minutes_count.keys()):
        results.append({'minute': m, 'count': minutes_count[m]})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique1():
    return render_template("graphique.html")

@app.route("/contact/")
def mongraphique2():
    return render_template("contact.html")

@app.route("/histogramme/")
def mongraphique3():
    return render_template("histogramme.html")

if __name__ == "__main__":
    app.run(debug=True)
