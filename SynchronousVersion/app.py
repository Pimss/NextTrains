import requests
from jinja2 import Template
from datetime import datetime,timedelta
from flask import Flask
import os

format_dt = '%Y%m%dT%H%M%S'
def translate_date(date_str):
	return datetime.strptime(date_str, format_dt).strftime("%H:%M")

# Getting the API key in the environnement variable (DON'T HARD CODE YOUR API KEY, EVER !)
headers= {"Authorization":os.getenv('API_KEY')}

with open("templates/template_m.html",'r') as file:
	html = file.read()

with open("templates/template_m_r.html",'r') as file:
	html_r = file.read()

with open("templates/template_w_r.html",'r') as file:
	html_w_r = file.read()

with open("templates/template_w.html",'r') as file:
	html_w = file.read()

def extract_link_journey(links):
	for link in links:
		if link["type"]=="vehicle_journey":
			return link
	return {}

app = Flask(__name__)

@app.route("/user1/going")
def index_w():
	next_ter=[]
	listed_dtm=[]
	# request to get TER train passing from Versailles Chantiers to Montparnasse
	response = requests.get("https://api.sncf.com/v1/coverage/fr-idf/stop_areas/stop_area:IDFM:63880/lines/line:IDFM:C01744/terminus_schedules",headers=headers)
	ini_time_for_now = datetime.now()
	for departure in response.json()["terminus_schedules"]:
		if departure["route"]["name"] == "Chartres - Gare Montparnasse":
			for dtm in departure["date_times"]:
				departure_time = datetime.strptime(dtm["date_time"], format_dt)
				if departure_time < ini_time_for_now + timedelta(hours=5):
					journey_id = extract_link_journey(dtm["links"])["id"]
					info_journey = requests.get("https://api.sncf.com/v1/coverage/fr-idf/vehicle_journeys/{}".format(journey_id),headers=headers).json()["vehicle_journeys"][0]
					for stop_time in info_journey["stop_times"]:
						if stop_time["stop_point"]["name"] == "Gare Montparnasse":
							arrivalTime= stop_time["arrival_time"][:2]+":"+stop_time["arrival_time"][2:4]
							next_ter.append({"departureTime":translate_date(dtm["date_time"]),"arrivalTime":arrivalTime})
							listed_dtm.append(departure_time)
							break
	if next_ter != []:
		next_ter = list(zip(*sorted(zip(next_ter,listed_dtm),key=lambda x: x[1])))[0]

	next_n=[]
	# request to get N line train from Versailles Chantiers to Montparnasse
	response = requests.get("https://api.sncf.com/v1/coverage/fr-idf/stop_areas/stop_area:IDFM:63880/lines/line:IDFM:C01736/terminus_schedules",headers=headers)
	ini_time_for_now = datetime.now()
	for departure in response.json()["terminus_schedules"]:
		if departure["route"]["name"] == "Mantes-la-Jolie - Gare Montparnasse":
			for dtm in departure["date_times"]:
				departure_time = datetime.strptime(dtm["date_time"], format_dt)
				if departure_time < ini_time_for_now + timedelta(hours=5):
					journey_id = extract_link_journey(dtm["links"])["id"]
					# Extracting each train arrival time since their journey can be either slow or fast
					info_journey = requests.get("https://api.sncf.com/v1/coverage/fr-idf/vehicle_journeys/{}".format(journey_id),headers=headers).json()["vehicle_journeys"][0]
					for stop_time in info_journey["stop_times"]:
						if stop_time["stop_point"]["name"] == "Gare Montparnasse":
							arrivalTime= stop_time["arrival_time"][:2]+":"+stop_time["arrival_time"][2:4]
							next_n.append({"departureTime":translate_date(dtm["date_time"]),"arrivalTime":arrivalTime})
							break
	next_train_u = []
	# request to get the U line train from Versailles Chantiers to La Defense
	response = requests.get("https://api.sncf.com/v1/coverage/fr-idf/stop_areas/stop_area:IDFM:63880/lines/line:IDFM:C01741/terminus_schedules",headers=headers)
	ini_time_for_now = datetime.now()
	for departure in response.json()["terminus_schedules"]:
		if departure["route"]["name"] == "La Verrière - La Défense":
			for dtm in departure["date_times"]:
				departure_time = datetime.strptime(dtm["date_time"], format_dt)
				if departure_time < ini_time_for_now + timedelta(hours=5):
					next_train_u.append({"departureTime":translate_date(dtm["date_time"]),"arrivalTime":(departure_time+timedelta(minutes=22)).strftime("%H:%M")})

	next_train_l=[]
	# request to get the U line train from Versailles Rive Droite to La Defense
	response = requests.get("https://api.sncf.com/v1/coverage/fr-idf/stop_areas/stop_area:IDFM:64021/lines/line:IDFM:C01740/terminus_schedules",headers=headers)
	ini_time_for_now = datetime.now()
	for departure in response.json()["terminus_schedules"]:
		if departure["route"]["name"] == "Versailles Rive Droite - Gare Saint-Lazare":
			for dtm in departure["date_times"]:
				departure_time = datetime.strptime(dtm["date_time"], format_dt)
				if departure_time < ini_time_for_now + timedelta(hours=5):
					next_train_l.append({"departureTime":translate_date(dtm["date_time"]),"arrivalTime":(departure_time+timedelta(minutes=21)).strftime("%H:%M")})

	# request to get the C line train from Versailles Chantiers to Austerlitz and from Versailles Chantiers to Massy
	# this API is subject to bugs with the namings of the routes
	response = requests.get("https://api.sncf.com/v1/coverage/fr-idf/stop_areas/stop_area:IDFM:63880/lines/line:IDFM:C01727/terminus_schedules",headers=headers)
	next_train_c_chantiers=[]
	next_train_c_massy=[]

	for departure in response.json()["terminus_schedules"]:
		if departure["route"]["name"] in ["Saint-Quentin en Yvelines - Montigny-le-Bretonneux - Dourdan","Saint-Quentin en Yvelines - Montigny-le-Bretonneux - Saint-Martin d'Étampes"]:
			for dtm in departure["date_times"]:
				departure_time = datetime.strptime(dtm["date_time"], format_dt)
				if departure_time < ini_time_for_now + timedelta(hours=5):
					next_train_c_chantiers.append({"departureTime":translate_date(dtm["date_time"]),"arrivalTime":(departure_time+timedelta(minutes=40)).strftime("%H:%M")})
		if departure["route"]["name"] == "Versailles Chantiers - Massy - Palaiseau":
			for dtm in departure["date_times"]:
				departure_time = datetime.strptime(dtm["date_time"], format_dt)
				if departure_time < ini_time_for_now + timedelta(hours=5):
					next_train_c_massy.append({"departureTime":translate_date(dtm["date_time"]),"arrivalTime":(departure_time+timedelta(minutes=20)).strftime("%H:%M")})

	# request to get the departures from Versailles Chateau to Austerlitz
	response = requests.get("https://api.sncf.com/v1/coverage/fr-idf/stop_areas/stop_area:IDFM:73721/lines/line:IDFM:C01727/terminus_schedules",headers=headers)
	next_train_c_chateau=[]
	for departure in response.json()["terminus_schedules"]:
		if departure["route"]["name"] == "Versailles Château Rive Gauche - Juvisy":
			for dtm in departure["date_times"]:
				departure_time = datetime.strptime(dtm["date_time"], format_dt)
				if departure_time < ini_time_for_now + timedelta(hours=5):
					next_train_c_chateau.append({"departureTime":translate_date(dtm["date_time"]),"arrivalTime":(departure_time+timedelta(minutes=40)).strftime("%H:%M")})

	temp = Template(html_w)
	return temp.render(trains_ter=next_ter,trains_n=next_n,trains_l=next_train_l,trains_c_chateau=next_train_c_chateau,trains_c_chantiers=next_train_c_chantiers,trains_u=next_train_u,trains_c_massy=next_train_c_massy)




@app.route("/user1/returning")
def index_w_r():
	next_ter=[]
	response = requests.get("https://api.sncf.com/v1/coverage/fr-idf/stop_areas/stop_area:IDFM:71139/lines/line:IDFM:C01744/terminus_schedules",headers=headers)
	ini_time_for_now = datetime.now()
	for departure in response.json()["terminus_schedules"]:
		if departure["route"]["name"] == "Gare Montparnasse - Chartres":
			for dtm in departure["date_times"]:
				departure_time = datetime.strptime(dtm["date_time"], format_dt)
				if departure_time < ini_time_for_now + timedelta(hours=5):
					journey_id = extract_link_journey(dtm["links"])["id"]
					info_journey = requests.get("https://api.sncf.com/v1/coverage/fr-idf/vehicle_journeys/{}".format(journey_id),headers=headers).json()["vehicle_journeys"][0]
					for stop_time in info_journey["stop_times"]:
						if stop_time["stop_point"]["name"] == "Versailles Chantiers":
							arrivalTime= stop_time["arrival_time"][:2]+":"+stop_time["arrival_time"][2:4]
							next_ter.append({"departureTime":translate_date(dtm["date_time"]),"arrivalTime":arrivalTime})
							break
	next_n=[]
	listed_dtm=[]
	response = requests.get("https://api.sncf.com/v1/coverage/fr-idf/stop_areas/stop_area:IDFM:71139/lines/line:IDFM:C01736/terminus_schedules",headers=headers)
	ini_time_for_now = datetime.now()
	for departure in response.json()["terminus_schedules"]:

		for dtm in departure["date_times"]:
			departure_time = datetime.strptime(dtm["date_time"], format_dt)
			if departure_time < ini_time_for_now + timedelta(hours=5):
				journey_id = extract_link_journey(dtm["links"])["id"]
				info_journey = requests.get("https://api.sncf.com/v1/coverage/fr-idf/vehicle_journeys/{}".format(journey_id),headers=headers).json()["vehicle_journeys"][0]
				for stop_time in info_journey["stop_times"]:
					if stop_time["stop_point"]["name"] == "Versailles Chantiers":
						arrivalTime= stop_time["arrival_time"][:2]+":"+stop_time["arrival_time"][2:4]
						next_n.append({"departureTime":translate_date(dtm["date_time"]),"arrivalTime":arrivalTime})
						listed_dtm.append(departure_time)
						break
	if next_n != []:
		next_n = list(zip(*sorted(zip(next_n,listed_dtm),key=lambda x: x[1])))[0]

	next_train_c_chantiers=[]
	next_train_c_chateau=[]
	listed_dtm=[]
	response = requests.get("https://api.sncf.com/v1/coverage/fr-idf/stop_areas/stop_area:IDFM:71135/lines/line:IDFM:C01727/terminus_schedules",headers=headers)

	
	for departure in response.json()["terminus_schedules"]:
		if "- Saint-Quentin en Yvelines - Montigny-le-Bretonneux" in departure["route"]["name"]:
			for dtm in departure["date_times"]:
				departure_time = datetime.strptime(dtm["date_time"], format_dt)
				if departure_time < ini_time_for_now + timedelta(hours=5):
					next_train_c_chantiers.append({"departureTime":translate_date(dtm["date_time"]),"arrivalTime":(departure_time+timedelta(minutes=41)).strftime("%H:%M")})
					
		if "- Versailles Château Rive Gauche" in departure["route"]["name"]:
			for dtm in departure["date_times"]:
				departure_time = datetime.strptime(dtm["date_time"], format_dt)
				if departure_time < ini_time_for_now + timedelta(hours=5):
					listed_dtm.append(departure_time)
					next_train_c_chateau.append({"departureTime":translate_date(dtm["date_time"]),"arrivalTime":(departure_time+timedelta(minutes=41)).strftime("%H:%M")})
	if next_train_c_chateau != []:
		next_train_c_chateau = list(zip(*sorted(zip(next_train_c_chateau,listed_dtm),key=lambda x: x[1])))[0]
	next_train_c_massy=[]
	response = requests.get("https://api.sncf.com/v1/coverage/fr-idf/stop_areas/stop_area:IDFM:63244/lines/line:IDFM:C01727/terminus_schedules",headers=headers)

	
	for departure in response.json()["terminus_schedules"]:
		if departure["route"]["name"] == "Massy - Palaiseau - Versailles Chantiers":
			for dtm in departure["date_times"]:
				departure_time = datetime.strptime(dtm["date_time"], format_dt)
				if departure_time < ini_time_for_now + timedelta(hours=5):
					next_train_c_massy.append({"departureTime":translate_date(dtm["date_time"]),"arrivalTime":(departure_time+timedelta(minutes=20)).strftime("%H:%M")})
		

	next_train_u = []
	response = requests.get("https://api.sncf.com/v1/coverage/fr-idf/stop_areas/stop_area:IDFM:71517/lines/line:IDFM:C01741/terminus_schedules",headers=headers)
	ini_time_for_now = datetime.now()
	for departure in response.json()["terminus_schedules"]:
		if departure["route"]["name"] == "La Défense - Rambouillet":
			for dtm in departure["date_times"]:
				departure_time = datetime.strptime(dtm["date_time"], format_dt)
				if departure_time < ini_time_for_now + timedelta(hours=5):
					next_train_u.append({"departureTime":translate_date(dtm["date_time"]),"arrivalTime":(departure_time+timedelta(minutes=22)).strftime("%H:%M")})

	next_train_l=[]
	response = requests.get("https://api.sncf.com/v1/coverage/fr-idf/stop_areas/stop_area:IDFM:71517/lines/line:IDFM:C01740/terminus_schedules",headers=headers)
	ini_time_for_now = datetime.now()
	for departure in response.json()["terminus_schedules"]:
		if departure["route"]["name"] == "Gare Saint-Lazare - Versailles Rive Droite":
			for dtm in departure["date_times"]:
				departure_time = datetime.strptime(dtm["date_time"], format_dt)
				if departure_time < ini_time_for_now + timedelta(hours=5):
					next_train_l.append({"departureTime":translate_date(dtm["date_time"]),"arrivalTime":(departure_time+timedelta(minutes=21)).strftime("%H:%M")})

	temp = Template(html_w_r)
	return temp.render(trains_ter=next_ter,trains_n=next_n,trains_l=next_train_l,trains_c_chateau=next_train_c_chateau,trains_c_chantiers=next_train_c_chantiers,trains_u=next_train_u,trains_c_massy=next_train_c_massy)



@app.route("/user2/going")
def index():

	next_train_l=[]
	response = requests.get("https://api.sncf.com/v1/coverage/fr-idf/stop_areas/stop_area:IDFM:64021/lines/line:IDFM:C01740/terminus_schedules",headers=headers)
	ini_time_for_now = datetime.now()
	for departure in response.json()["terminus_schedules"]:
		if departure["route"]["name"] == "Versailles Rive Droite - Gare Saint-Lazare":
			for dtm in departure["date_times"]:
				departure_time = datetime.strptime(dtm["date_time"], format_dt)
				if departure_time < ini_time_for_now + timedelta(hours=5):
					next_train_l.append({"departureTime":translate_date(dtm["date_time"]),"arrivalTime":(departure_time+timedelta(minutes=14)).strftime("%H:%M")})

	response = requests.get("https://api.sncf.com/v1/coverage/fr-idf/stop_areas/stop_area:IDFM:63880/lines/line:IDFM:C01727/terminus_schedules",headers=headers)
	next_train_c_chantiers=[]

	for departure in response.json()["terminus_schedules"]:
		if "- Saint-Quentin en Yvelines - Montigny-le-Bretonneux" in departure["route"]["name"]:
			for dtm in departure["date_times"]:
				departure_time = datetime.strptime(dtm["date_time"], format_dt)
				if departure_time < ini_time_for_now + timedelta(hours=5):
					next_train_c_chantiers.append({"departureTime":translate_date(dtm["date_time"]),"arrivalTime":(departure_time+timedelta(minutes=23)).strftime("%H:%M")})

	response = requests.get("https://api.sncf.com/v1/coverage/fr-idf/stop_areas/stop_area:IDFM:73721/lines/line:IDFM:C01727/terminus_schedules",headers=headers)
	next_train_c_chateau=[]
	for departure in response.json()["terminus_schedules"]:
		if departure["route"]["name"] == "Versailles Château Rive Gauche - Juvisy":
			for dtm in departure["date_times"]:
				departure_time = datetime.strptime(dtm["date_time"], format_dt)
				if departure_time < ini_time_for_now + timedelta(hours=5):
					next_train_c_chateau.append({"departureTime":translate_date(dtm["date_time"]),"arrivalTime":(departure_time+timedelta(minutes=24)).strftime("%H:%M")})


	
	next_train_u = []
	response = requests.get("https://api.sncf.com/v1/coverage/fr-idf/stop_areas/stop_area:IDFM:63880/lines/line:IDFM:C01741/terminus_schedules",headers=headers)
	ini_time_for_now = datetime.now()
	for departure in response.json()["terminus_schedules"]:
		if departure["route"]["name"] == "La Verrière - La Défense":
			for dtm in departure["date_times"]:
				departure_time = datetime.strptime(dtm["date_time"], format_dt)
				if departure_time < ini_time_for_now + timedelta(hours=5):
					next_train_u.append({"departureTime":translate_date(dtm["date_time"]),"arrivalTime":(departure_time+timedelta(minutes=13)).strftime("%H:%M")})
	temp = Template(html)
	return temp.render(trains_l=next_train_l,trains_c_chateau=next_train_c_chateau,trains_c_chantiers=next_train_c_chantiers,trains_u=next_train_u)

@app.route("/user2/returning")
def index_r():

	
	next_train_l=[]
	response = requests.get("https://api.sncf.com/v1/coverage/fr-idf/stop_areas/stop_area:IDFM:73749/lines/line:IDFM:C01740/terminus_schedules",headers=headers)
	ini_time_for_now = datetime.now()
	for departure in response.json()["terminus_schedules"]:
		if departure["route"]["name"] == "Gare Saint-Lazare - Versailles Rive Droite":
			for dtm in departure["date_times"]:
				departure_time = datetime.strptime(dtm["date_time"], format_dt)
				if departure_time < ini_time_for_now + timedelta(hours=5):
					next_train_l.append({"departureTime":translate_date(dtm["date_time"]),"arrivalTime":(departure_time+timedelta(minutes=14)).strftime("%H:%M")})

	response = requests.get("https://api.sncf.com/v1/coverage/fr-idf/stop_areas/stop_area:IDFM:71150/lines/line:IDFM:C01727/terminus_schedules",headers=headers)


	next_train_c_chantiers=[]
	next_train_c_chateau=[]

	for departure in response.json()["terminus_schedules"]:
		if departure["route"]["name"] == "Dourdan - Saint-Quentin en Yvelines - Montigny-le-Bretonneux":
			for dtm in departure["date_times"]:
				departure_time = datetime.strptime(dtm["date_time"], format_dt)
				if departure_time < ini_time_for_now + timedelta(hours=5):
					next_train_c_chantiers.append({"departureTime":translate_date(dtm["date_time"]),"arrivalTime":(departure_time+timedelta(minutes=23)).strftime("%H:%M")})
		if "- Versailles Château Rive Gauche" in departure["route"]["name"]:
			for dtm in departure["date_times"]:
				departure_time = datetime.strptime(dtm["date_time"], format_dt)
				if departure_time < ini_time_for_now + timedelta(hours=5):
					next_train_c_chateau.append({"departureTime":translate_date(dtm["date_time"]),"arrivalTime":(departure_time+timedelta(minutes=24)).strftime("%H:%M")})

	next_train_u = []
	response = requests.get("https://api.sncf.com/v1/coverage/fr-idf/stop_areas/stop_area:IDFM:73749/lines/line:IDFM:C01741/terminus_schedules",headers=headers)
	ini_time_for_now = datetime.now()
	for departure in response.json()["terminus_schedules"]:
		if departure["route"]["name"] == "La Défense - Rambouillet":
			for dtm in departure["date_times"]:
				departure_time = datetime.strptime(dtm["date_time"], format_dt)
				if departure_time < ini_time_for_now + timedelta(hours=5):
					next_train_u.append({"departureTime":translate_date(dtm["date_time"]),"arrivalTime":(departure_time+timedelta(minutes=13)).strftime("%H:%M")})


	temp = Template(html_r)
	return temp.render(trains_l=next_train_l,trains_c_chateau=next_train_c_chateau,trains_c_chantiers=next_train_c_chantiers,trains_u=next_train_u)

if __name__ == '__main__':
   app.run()