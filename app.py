from flask import Flask, render_template, request
import xml.etree.ElementTree as ET

app = Flask(__name__)

tree = ET.parse('data/data.xml')
root = tree.getroot()

districts = {}
for district in root.findall('district'):
    district_name = district.find('name').text
    chef_lieu = district.find('chefLieu').text

    districts[district_name] = chef_lieu
    if len(districts) == 10:
        break

regions = list(districts.keys())
chefs_lieux = list(districts.values())

number = 0


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/quiz', methods=['GET', 'POST'])  # url_for('quiz', number='1')
def quiz():
    global number
    return render_template('quiz.html', number=1, ask_value=regions[number], response=chefs_lieux[number])


@app.route('/add', methods=['POST'])
def add_response():
    global number
    number += 1
    response = chefs_lieux[number - 1]
    if response == request.form["response"]:
        class_css = "bg-success"
    else:
        class_css = "bg-danger"

    class_css += " text-white py-1 text-center mb-1"
    return f"<div class=\"{class_css}\"><h5>Quelle est le chef lieu de la region du {regions[number - 1]} ? Réponse : {request.form['response']} <h5></div>"
