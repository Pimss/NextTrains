from datetime import timedelta
journeys={}
## Trajets aller William
journey={ "trip":"Versailles Chantiers - Montparnasse TER",
			  "color": "#000000",
			  "text_color":"white",
			  "logo":"https://upload.wikimedia.org/wikipedia/commons/e/e8/Logo-TER.png",
			  "stop_area":"IDFM:63880",
			  "line":"IDFM:C01744",
			  "route_names_check":lambda x: x =="Chartres - Gare Montparnasse",
			  "time_interval":timedelta(hours=5),
			  "known_journey_time":None,
			  "arrival_station":"Gare Montparnasse"
}
journeys[journey["trip"]]=journey


journey={ "trip":"Versailles Chantiers - Montparnasse N",
			  "color": "#00B297",
			  "text_color":"white",
			  "logo":"https://www.ratp.fr/sites/default/files/lines-assets/picto/sncf/picto_sncf_ligne-n.1634824971.svg",
			  "stop_area":"IDFM:63880",
			  "line":"IDFM:C01736",
			  "route_names_check":lambda x: x in["Mantes-la-Jolie - Gare Montparnasse","Dreux - Gare Montparnasse"],
			  "time_interval":timedelta(hours=5),
			  "known_journey_time":None,
			  "arrival_station":"Gare Montparnasse"
}

journeys[journey["trip"]]=journey

journey={ "trip":"Versailles Chantiers - La Défense",
			  "color": "#B6134C",
			  "text_color":"white",
			  "logo":"https://upload.wikimedia.org/wikipedia/commons/d/df/Paris_transit_icons_-_Train_U.svg",
			  "stop_area":"IDFM:63880",
			  "line":"IDFM:C01741",
			  "route_names_check":lambda x: x in["La Verrière - La Défense","Rambouillet - La Défense"],
			  "time_interval":timedelta(hours=5),
			  "known_journey_time":timedelta(minutes=22),
			  "arrival_station":None
}

journeys[journey["trip"]]=journey

journey={ "trip":"Versailles Rive Droite - La Défense",
			  "color": "#C4A4CC",
			  "text_color":"white",
			  "logo":"https://www.ratp.fr/sites/default/files/lines-assets/picto/sncf/picto_sncf_ligne-l.1634824971.svg",
			  "stop_area":"IDFM:64021",
			  "line":"IDFM:C01740",
			  "route_names_check":lambda x: x =="Versailles Rive Droite - Gare Saint-Lazare",
			  "time_interval":timedelta(hours=5),
			  "known_journey_time":timedelta(minutes=21),
			  "arrival_station":None
}

journeys[journey["trip"]]=journey

journey={ "trip":"Versailles Chantiers - Austerlitz",
			  "color": "#F3D311",
			  "text_color":"white",
			  "logo":"https://upload.wikimedia.org/wikipedia/fr/c/c1/Logo_RER_C.svg",
			  "stop_area":"IDFM:63880",
			  "line":"IDFM:C01727",
			  "route_names_check":lambda x: x in["Saint-Quentin en Yvelines - Montigny-le-Bretonneux - Dourdan","Saint-Quentin en Yvelines - Montigny-le-Bretonneux - Saint-Martin d'Étampes"],
			  "time_interval":timedelta(hours=5),
			  "known_journey_time":timedelta(minutes=40),
			  "arrival_station":None
}

journeys[journey["trip"]]=journey

journey={ "trip":"Versailles Chantiers - Massy",
			  "color": "#F3D311",
			  "text_color":"white",
			  "logo":"https://upload.wikimedia.org/wikipedia/fr/c/c1/Logo_RER_C.svg",
			  "stop_area":"IDFM:63880",
			  "line":"IDFM:C01727",
			  "route_names_check":lambda x: x =="Versailles Chantiers - Massy - Palaiseau",
			  "time_interval":timedelta(hours=5),
			  "known_journey_time":timedelta(minutes=20),
			  "arrival_station":None
}

journeys[journey["trip"]]=journey


journey={ "trip":"Versailles Château - Austerlitz",
			  "color": "#F3D311",
			  "text_color":"white",
			  "logo":"https://upload.wikimedia.org/wikipedia/fr/c/c1/Logo_RER_C.svg",
			  "stop_area":"IDFM:73721",
			  "line":"IDFM:C01727",
			  "route_names_check":lambda x: x =="Versailles Château Rive Gauche - Juvisy",
			  "time_interval":timedelta(hours=5),
			  "known_journey_time":timedelta(minutes=40),
			  "arrival_station":None
}

journeys[journey["trip"]]=journey

journey={ "trip":"Gare de Lyon - Montargis",
			  "color": "#B94E9A",
			  "text_color":"white",
			  "logo":"https://upload.wikimedia.org/wikipedia/commons/f/fb/Paris_transit_icons_-_Train_R.svg",
			  "stop_area":"IDFM:73626",
			  "line":"IDFM:C01731",
			  "route_names_check": lambda x: x =="Gare de Lyon - Montargis",
			  "time_interval":timedelta(hours=8),
			  "known_journey_time":None,
			  "arrival_station":"Montargis"
}

journeys[journey["trip"]]=journey

## Trajets retour William
journey={ "trip":"Montparnasse - Versailles Chantiers TER",
			  "color": "#000000",
			  "text_color":"white",
			  "logo":"https://upload.wikimedia.org/wikipedia/commons/e/e8/Logo-TER.png",
			  "stop_area":"IDFM:71139",
			  "line":"IDFM:C01744",
			  "route_names_check":lambda x: x =="Gare Montparnasse - Chartres",
			  "time_interval":timedelta(hours=5),
			  "known_journey_time":None,
			  "arrival_station":"Versailles Chantiers"
}
journeys[journey["trip"]]=journey

journey={ "trip":"Montparnasse - Versailles Chantiers N",
			  "color": "#00B297",
			  "text_color":"white",
			  "logo":"https://www.ratp.fr/sites/default/files/lines-assets/picto/sncf/picto_sncf_ligne-n.1634824971.svg",
			  "stop_area":"IDFM:71139",
			  "line":"IDFM:C01736",
			  "route_names_check":lambda x: True,
			  "time_interval":timedelta(hours=5),
			  "known_journey_time":None,
			  "arrival_station":"Versailles Chantiers"
}

journeys[journey["trip"]]=journey

journey={ "trip":"Austerlitz - Versailles Chantiers",
			  "color": "#F3D311",
			  "text_color":"white",
			  "logo":"https://upload.wikimedia.org/wikipedia/fr/c/c1/Logo_RER_C.svg",
			  "stop_area":"IDFM:71135",
			  "line":"IDFM:C01727",
			  "route_names_check":lambda x: "- Saint-Quentin en Yvelines - Montigny-le-Bretonneux" in x,
			  "time_interval":timedelta(hours=5),
			  "known_journey_time":timedelta(minutes=41),
			  "arrival_station":None
}

journeys[journey["trip"]]=journey


journey={ "trip":"Austerlitz - Versailles Château",
			  "color": "#F3D311",
			  "text_color":"white",
			  "logo":"https://upload.wikimedia.org/wikipedia/fr/c/c1/Logo_RER_C.svg",
			  "stop_area":"IDFM:71135",
			  "line":"IDFM:C01727",
			  "route_names_check":lambda x: "- Versailles Château Rive Gauche" in x,
			  "time_interval":timedelta(hours=5),
			  "known_journey_time":timedelta(minutes=40),
			  "arrival_station":None
}

journeys[journey["trip"]]=journey

journey={ "trip":"Massy - Versailles Chantiers",
			  "color": "#F3D311",
			  "text_color":"white",
			  "logo":"https://upload.wikimedia.org/wikipedia/fr/c/c1/Logo_RER_C.svg",
			  "stop_area":"IDFM:63244",
			  "line":"IDFM:C01727",
			  "route_names_check":lambda x: x =="Massy - Palaiseau - Versailles Chantiers",
			  "time_interval":timedelta(hours=5),
			  "known_journey_time":timedelta(minutes=20),
			  "arrival_station":None
}

journeys[journey["trip"]]=journey

journey={ "trip":"La Défense - Versailles Chantiers",
			  "color": "#B6134C",
			  "text_color":"white",
			  "logo":"https://upload.wikimedia.org/wikipedia/commons/d/df/Paris_transit_icons_-_Train_U.svg",
			  "stop_area":"IDFM:71517",
			  "line":"IDFM:C01741",
			  "route_names_check":lambda x: x in ["La Défense - Rambouillet","La Défense - La Verrière"],
			  "time_interval":timedelta(hours=5),
			  "known_journey_time":timedelta(minutes=22),
			  "arrival_station":None
}

journeys[journey["trip"]]=journey

journey={ "trip":"La Défense - Versailles Rive Droite",
			  "color": "#C4A4CC",
			  "text_color":"white",
			  "logo":"https://www.ratp.fr/sites/default/files/lines-assets/picto/sncf/picto_sncf_ligne-l.1634824971.svg",
			  "stop_area":"IDFM:71517",
			  "line":"IDFM:C01740",
			  "route_names_check":lambda x: x =="Gare Saint-Lazare - Versailles Rive Droite",
			  "time_interval":timedelta(hours=5),
			  "known_journey_time":timedelta(minutes=21),
			  "arrival_station":None
}

journeys[journey["trip"]]=journey

journey={ "trip":"Montargis - Gare de Lyon",
			  "color": "#B94E9A",
			  "text_color":"white",
			  "logo":"https://upload.wikimedia.org/wikipedia/commons/f/fb/Paris_transit_icons_-_Train_R.svg",
			  "stop_area":"IDFM:411483",
			  "line":"IDFM:C01731",
			  "route_names_check": lambda x: x =="Montargis - Gare de Lyon",
			  "time_interval":timedelta(hours=8),
			  "known_journey_time":None,
			  "arrival_station":"Gare de Lyon"
}

journeys[journey["trip"]]=journey

## Trajets aller Marion

journey={ "trip":"Versailles Rive Droite - Saint-Cloud",
			  "color": "#C4A4CC",
			  "text_color":"white",
			  "logo":"https://www.ratp.fr/sites/default/files/lines-assets/picto/sncf/picto_sncf_ligne-l.1634824971.svg",
			  "stop_area":"IDFM:64021",
			  "line":"IDFM:C01740",
			  "route_names_check":lambda x: x =="Versailles Rive Droite - Gare Saint-Lazare",
			  "time_interval":timedelta(hours=5),
			  "known_journey_time":timedelta(minutes=14),
			  "arrival_station":None
}

journeys[journey["trip"]]=journey

journey={ "trip":"Versailles Chantiers - Javel",
			  "color": "#F3D311",
			  "text_color":"white",
			  "logo":"https://upload.wikimedia.org/wikipedia/fr/c/c1/Logo_RER_C.svg",
			  "stop_area":"IDFM:63880",
			  "line":"IDFM:C01727",
			  "route_names_check":lambda x: "- Saint-Quentin en Yvelines - Montigny-le-Bretonneux" in x,
			  "time_interval":timedelta(hours=5),
			  "known_journey_time":timedelta(minutes=23),
			  "arrival_station":None
}

journeys[journey["trip"]]=journey

journey={ "trip":"Versailles Château - Javel",
			  "color": "#F3D311",
			  "text_color":"white",
			  "logo":"https://upload.wikimedia.org/wikipedia/fr/c/c1/Logo_RER_C.svg",
			  "stop_area":"IDFM:73721",
			  "line":"IDFM:C01727",
			  "route_names_check":lambda x: "Versailles Château Rive Gauche -" in x,
			  "time_interval":timedelta(hours=5),
			  "known_journey_time":timedelta(minutes=24),
			  "arrival_station":None
}

journeys[journey["trip"]]=journey

journey={ "trip":"Versailles Chantiers - Saint-Cloud",
			  "color": "#B6134C",
			  "text_color":"white",
			  "logo":"https://upload.wikimedia.org/wikipedia/commons/d/df/Paris_transit_icons_-_Train_U.svg",
			  "stop_area":"IDFM:63880",
			  "line":"IDFM:C01741",
			  "route_names_check":lambda x: x in ["La Verrière - La Défense","Rambouillet - La Défense"],
			  "time_interval":timedelta(hours=5),
			  "known_journey_time":timedelta(minutes=13),
			  "arrival_station":None
}

journeys[journey["trip"]]=journey

## Trajets retour Marion

journey={ "trip":"Saint-Cloud - Versailles Rive Droite",
			  "color": "#C4A4CC",
			  "text_color":"white",
			  "logo":"https://www.ratp.fr/sites/default/files/lines-assets/picto/sncf/picto_sncf_ligne-l.1634824971.svg",
			  "stop_area":"IDFM:73749",
			  "line":"IDFM:C01740",
			  "route_names_check":lambda x: x =="Gare Saint-Lazare - Versailles Rive Droite",
			  "time_interval":timedelta(hours=5),
			  "known_journey_time":timedelta(minutes=14),
			  "arrival_station":None
}

journeys[journey["trip"]]=journey


journey={ "trip":"Javel - Versailles Chantiers",
			  "color": "#F3D311",
			  "text_color":"white",
			  "logo":"https://upload.wikimedia.org/wikipedia/fr/c/c1/Logo_RER_C.svg",
			  "stop_area":"IDFM:71150",
			  "line":"IDFM:C01727",
			  "route_names_check":lambda x: "- Saint-Quentin en Yvelines - Montigny-le-Bretonneux" in x,
			  "time_interval":timedelta(hours=5),
			  "known_journey_time":timedelta(minutes=23),
			  "arrival_station":None
}

journeys[journey["trip"]]=journey


journey={ "trip":"Javel - Versailles Château",
			  "color": "#F3D311",
			  "text_color":"white",
			  "logo":"https://upload.wikimedia.org/wikipedia/fr/c/c1/Logo_RER_C.svg",
			  "stop_area":"IDFM:71150",
			  "line":"IDFM:C01727",
			  "route_names_check":lambda x: "- Versailles Château Rive Gauche" in x,
			  "time_interval":timedelta(hours=5),
			  "known_journey_time":timedelta(minutes=24),
			  "arrival_station":None
}

journeys[journey["trip"]]=journey

journey={ "trip":"Saint-Cloud - Versailles Chantiers",
			  "color": "#B6134C",
			  "text_color":"white",
			  "logo":"https://upload.wikimedia.org/wikipedia/commons/d/df/Paris_transit_icons_-_Train_U.svg",
			  "stop_area":"IDFM:73749",
			  "line":"IDFM:C01741",
			  "route_names_check":lambda x: x in ["La Défense - Rambouillet","La Défense - La Verrière"],
			  "time_interval":timedelta(hours=5),
			  "known_journey_time":timedelta(minutes=13),
			  "arrival_station":None
}

journeys[journey["trip"]]=journey