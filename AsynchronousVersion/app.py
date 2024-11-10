import aiohttp
from aiohttp import web
from jinja2 import Template
from datetime import datetime,timedelta
import os
import asyncio
from journey import journeys

format_dt = '%Y%m%dT%H%M%S'
def translate_date(date_str):
	return datetime.strptime(date_str, format_dt).strftime("%H:%M")

def extract_link_journey(links):
	for link in links:
		if link["type"]=="vehicle_journey":
			return link
	return {}

with open("templates/template.html",'r') as file:
	html_w = file.read()

async def extract_arrival_time(session,arrival_station,id_journey,departure_time):
	"""
	Function that loops on a journey to extract the exact arrival time
	"""
	response = await session.get(f"https://api.sncf.com/v1/coverage/fr-idf/vehicle_journeys/{id_journey}")
	info_journey = (await response.json())["vehicle_journeys"][0]
	for stop_time in info_journey["stop_times"]:
		if stop_time["stop_point"]["name"] == arrival_station:
			arrival_time = stop_time["arrival_time"][:2]+":"+stop_time["arrival_time"][2:4]
			next_train={"departureTime":departure_time,"arrivalTime":arrival_time}
			return next_train
	return {}




async def get_data_trains(session,stop_area,line,route_names_check,time_interval,arrival_station=None,known_journey_time=None):
	"""
	Function to extract all next trains given a stop area (of the start station)
	"""
	next_trains=[]
	listed_dtm=[]
	response = await session.get(f"https://api.sncf.com/v1/coverage/fr-idf/stop_areas/stop_area:{stop_area}/lines/line:{line}/terminus_schedules")
	ini_time_for_now = datetime.now()
	for departure in (await response.json())["terminus_schedules"]:
		if route_names_check(departure["route"]["name"]) or route_names_check is None:
			if known_journey_time is not None:
				for dtm in departure["date_times"]:
					departure_time = datetime.strptime(dtm["date_time"], format_dt)
					if departure_time < ini_time_for_now + time_interval:
						
						next_trains.append({"departureTime":departure_time.strftime("%H:%M"),"arrivalTime":(departure_time+known_journey_time).strftime("%H:%M")})
						listed_dtm.append(departure_time)
			else:
				zipped = [(dtm,extract_link_journey(dtm["links"])["id"])for dtm in departure["date_times"] if (datetime.strptime(dtm["date_time"], format_dt)< ini_time_for_now + time_interval)]
				if zipped !=[]:
					dtms,journey_ids = zip(*zipped)
					next_trains += await asyncio.gather(*[extract_arrival_time(session,arrival_station,id_journey,translate_date(dtm["date_time"]))for (id_journey,dtm) in zip(journey_ids,dtms)])
					listed_dtm += [datetime.strptime(dtm["date_time"], format_dt) for dtm in departure["date_times"]]	
					listed_dtm,next_trains = zip(*[(departure,train) for (departure,train) in zip(listed_dtm,next_trains) if train!={} and (departure< ini_time_for_now + time_interval)])
					listed_dtm,next_trains = list(listed_dtm),list(next_trains)
	if next_trains != []:
		next_trains = list(zip(*sorted(zip(next_trains,listed_dtm),key=lambda x: x[1])))[0]
	return next_trains


async def list_journeys(journey,session):
	stop_area=journey["stop_area"]
	line=journey["line"]
	route_names_check= journey["route_names_check"]
	time_interval=journey["time_interval"]
	known_journey_time = journey["known_journey_time"]
	arrival_station=journey["arrival_station"]
	trips =await get_data_trains(session,stop_area,line,route_names_check,time_interval,arrival_station=arrival_station,known_journey_time=known_journey_time)
	journey["journeys"]=trips
	return journey



async def init_app():
	app = web.Application()
	headers= {"Authorization":str(os.getenv('API_KEY'))}

	routes = web.RouteTableDef()
	@routes.get('/albert/going')
	async def albert_going(request):
		async with aiohttp.ClientSession(headers=headers) as session:
			selected_journeys = [ journeys["Versailles Rive Droite - Saint-Cloud"],
								  journeys["Versailles Chantiers - Saint-Cloud"],
								  journeys["Versailles Chantiers - Javel"],
								  journeys["Versailles Château - Javel"]
			]
			journeys_with_time = await asyncio.gather(*[list_journeys(journey,session) for journey in selected_journeys])
			temp = Template(html_w)
		return aiohttp.web.Response(text=temp.render(trips=journeys_with_time),content_type='text/html')

	@routes.get('/albert/returning')
	async def albert_returning(request):
		async with aiohttp.ClientSession(headers=headers) as session:
			selected_journeys = [ journeys["Saint-Cloud - Versailles Rive Droite"],
								  journeys["Saint-Cloud - Versailles Chantiers"],
								  journeys["Javel - Versailles Chantiers"],
								  journeys["Javel - Versailles Château"],
			]
			journeys_with_time = await asyncio.gather(*[list_journeys(journey,session) for journey in selected_journeys])
			temp = Template(html_w)
		return aiohttp.web.Response(text=temp.render(trips=journeys_with_time),content_type='text/html')

	@routes.get('/ubert/going')
	async def ubert_going(request):
		async with aiohttp.ClientSession(headers=headers) as session:
			selected_journeys = [ journeys["Versailles Chantiers - Montparnasse TER"],
								  journeys["Versailles Chantiers - Montparnasse N"],
								  journeys["Versailles Rive Droite - La Défense"],
								  journeys["Versailles Chantiers - La Défense"],
								  journeys["Versailles Chantiers - Austerlitz"],
								  journeys["Versailles Château - Austerlitz"],
								  journeys["Versailles Chantiers - Massy"]
								  # journeys["Gare de Lyon - Montargis"]
			]
			journeys_with_time = await asyncio.gather(*[list_journeys(journey,session) for journey in selected_journeys])
			temp = Template(html_w)
		return aiohttp.web.Response(text=temp.render(trips=journeys_with_time),content_type='text/html')

	@routes.get('/ubert/returning')
	async def ubert_returning(request):
		async with aiohttp.ClientSession(headers=headers) as session:
			selected_journeys = [ journeys["Montparnasse - Versailles Chantiers TER"],
								  journeys["Montparnasse - Versailles Chantiers N"],
								  journeys["La Défense - Versailles Rive Droite"],
								  journeys["La Défense - Versailles Chantiers"],
								  journeys["Austerlitz - Versailles Chantiers"],
								  journeys["Austerlitz - Versailles Château"],
								  journeys["Massy - Versailles Chantiers"]
								  # journeys["Montargis - Gare de Lyon"]
			]
			journeys_with_time = await asyncio.gather(*[list_journeys(journey,session) for journey in selected_journeys])
			temp = Template(html_w)
		return aiohttp.web.Response(text=temp.render(trips=journeys_with_time),content_type='text/html')


	@routes.get('/frederich/going')
	async def frederich_going(request):
		async with aiohttp.ClientSession(headers=headers) as session:
			selected_journeys = [ journeys["Versailles Chantiers - Montparnasse TER"],
								  journeys["Versailles Chantiers - Montparnasse N"],
								  journeys["Versailles Rive Droite - La Défense"],
								  journeys["Versailles Chantiers - La Défense"],
								  journeys["Versailles Chantiers - Austerlitz"],
								  journeys["Versailles Château - Austerlitz"],
								  journeys["Versailles Chantiers - Massy"],
								  journeys["Gare de Lyon - Montargis"]
			]
			journeys_with_time = await asyncio.gather(*[list_journeys(journey,session) for journey in selected_journeys])
			temp = Template(html_w)
		return aiohttp.web.Response(text=temp.render(trips=journeys_with_time),content_type='text/html')

	@routes.get('/frederich/returning')
	async def frederich_returning(request):
		async with aiohttp.ClientSession(headers=headers) as session:
			selected_journeys = [ journeys["Montparnasse - Versailles Chantiers TER"],
								  journeys["Montparnasse - Versailles Chantiers N"],
								  journeys["La Défense - Versailles Rive Droite"],
								  journeys["La Défense - Versailles Chantiers"],
								  journeys["Austerlitz - Versailles Chantiers"],
								  journeys["Austerlitz - Versailles Château"],
								  journeys["Massy - Versailles Chantiers"],
								  journeys["Montargis - Gare de Lyon"]
			]
			journeys_with_time = await asyncio.gather(*[list_journeys(journey,session) for journey in selected_journeys])
			temp = Template(html_w)
		return aiohttp.web.Response(text=temp.render(trips=journeys_with_time),content_type='text/html')

	app.add_routes(routes)
	return app


# app=init_app()
# web.run_app(app,host="0.0.0.0")

	