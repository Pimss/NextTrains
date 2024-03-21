# Next Trains web app
This web app allowed me to get in one single web page all the different trains to come and leave from the multiple stations in my city (Versailles) and on my way to work
It relies on Flask and jinja2 for templating. There is a lot of hard coded informations since I had to get each ids of lines and stop areas to query Navitia's API. Some of the trains had fixed time schedules, some did not. I had to deal with some disparities on Paris' train network and some spurious behaviors of the API (You damm C line, why you keep on changing terminus name?)
It fetches all the next train in the next 5 hours and displays it in a web page with the bare minimum of CSS and styling

## How to Use locally
* Get an API key on Navitia (it's free and not worth it)
* Get this code and add your key as an environnement variable: on linux ``` export API_KEY=<your_api_key>```
* Then run ```flask run```

## How to run it as an Azure Web app
Azure allows you to have one free web app thus you can use this opportunity to publish this online
* Subscribe to Azure on their web site
* Install Azure CLI
* In this folder run the following command ```az webapp up --runtime PYTHON:3.9 --sku F1 --logs --name <myapplicationname> --location westeurope``` you can change python's version or the location if you want
* Go to Azure's interface on the web, clic on App Services and on your newly created application
* In the parameters you can set the environnement variables: add ```API_KEY``` and put you api_key in the value. Congrats Microsoft has got your API key but at least you did not hard code it into your application
* It restarts and now you are ready to go


## About the application
I coded it for two people for now and the available links are ```/user1/going```, ```/user1/returning```,```/user2/going```, ```/user2/returning```
The information about the C line is erratic. Handling that complex data seems to give a hard time to Navitia, I wouldn't like to do their job.


## How to modify it for your needs
I used 2 files a lot: lines.json and stop_points.json that I pulled from Navitia's API. You need to find the good stop_area id and the good line id, this is not an easy task sometimes