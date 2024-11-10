# Next Trains web app
This web app allowed me to get in one single web page all the different trains to come and leave from the multiple stations in my city (Versailles) and on my way to work
It relies on Flask and jinja2 for templating. There is a lot of hard coded informations since I had to get each ids of lines and stop areas to query Navitia's API. Some of the trains had fixed time schedules, some did not. I had to deal with some disparities on Paris' train network and some spurious behaviors of the API (You damm C line, why you keep on changing terminus name?)
It fetches all the next train in the next 5 hours and displays it in a web page with the bare minimum of CSS and styling

We implemented a synchronous and a asynchronous version

## Requirements
* Get an API key on Navitia (It used to be free however it no longer is... you missed it)


## The Synchronous version
It uses the default package for python web services: Flask and thus requires less work

### How to run locally

* Install the python requirements: ```pip install requirements.txt```
* Add your Navitia key as an environnement variable: on linux ``` export API_KEY=<your_api_key>```
* Then run ```flask run```


### How to run it as an Azure Web app
Azure allows you to have one free web app thus you can use this opportunity to publish this online
* Subscribe to Azure on their web site
* Install Azure CLI
* In this folder run the following command ```az webapp up --runtime PYTHON:3.12 --sku F1 --logs --name <myapplicationname> --location westeurope``` you can change python's version or the location if you want
* Go to Azure's interface on the web, clic on App Services and on your newly created application
* In the parameters you can set the environnement variables: add ```API_KEY``` and put you api_key in the value. Congrats Microsoft has got your API key but at least you did not hard code it into your application
* It restarts and now you are ready to go


### About the application
I coded it for two people for now and the available links are ```/user1/going```, ```/user1/returning```,```/user2/going```, ```/user2/returning```
The information about the C line is erratic. Handling that complex data seems to give a hard time to Navitia, I wouldn't like to do their job.




## The Asynchronous version

Small update of the app that runs faster with less html templates and more clarity in the app. It relies on aiohttp to run asynchronously: since the app is making many requests to Navitia's API it is better to run the code asynchronously to allow running code while watting for external server to respond

### How to run locally

* Install the python requirements: ```pip install requirements.txt```
* Add your Navitia key as an environnement variable: on linux ``` export API_KEY=<your_api_key>```
* Then run ```gunicorn --bind 0.0.0.0 --worker-class aiohttp.worker.GunicornWebWorker --timeout 600 app:init_app```


### How to run it as an Azure Web app
Azure allows you to have one free web app thus you can use this opportunity to publish this online
* Subscribe to Azure on their web site
* Install Azure CLI
* In this folder run the following command ```az webapp up --runtime PYTHON:3.12 --sku F1 --logs --name <myapplicationname> --location westeurope --startup-file start_command``` you can change python's version or the location if you want
* Go to Azure's interface on the web, clic on App Services and on your newly created application
* In the parameters you can set the environnement variables: add ```API_KEY``` and put you api_key in the value. Congrats Microsoft has got your API key but at least you did not hard code it into your application
* It restarts and now you are ready to go
