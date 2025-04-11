# MVP 3 PUC Rio - Micro Appointments API
 
---

# Overview
 
The purpose of this microservice is to register appointments, which we refer to as events. This microservice is highly decoupled and can be used independently, as long as the correct parameters are provided. Swagger can be used for tests without a front-end.
 
## How to Run the MVP with all micro services
 
This project also comes with a Dockerfile, which provides an additional option for starting up. To better understand how to use it, please refer to the docker-compose.yml in the gateway api repository of this MVP.  
 
For the entire MVP to work, the microservices must be executed using a docker-compose.yml in the gateway api repository. This microservice can be run individually, as it is very decoupled from other microservices. Access the port of this microservice and you will have a Swagger interface to perform operations without depending on the front-end.

To learn how to run the full MVP, visit the gateway api repository at the provided link.

***Access the port of this microservice and you will have a Swagger interface to perform operations without depending on the front-end.***

## Local and Env Variables

- When runing this micro service with docker the docker-compose.yml env variables will be used.
 
## How to Run Only This Microservice
 
You must have all the Python libraries listed in requirements.txt installed.  
After cloning the repository, navigate to the root directory through the terminal to execute the commands below.
 
> It is strongly recommended to use virtual environments such as virtualenv (https://virtualenv.pypa.io/en/latest/installation.html).
 
```
(env)$ pip install -r requirements.txt
```
 
This command installs the dependencies/libraries listed in the requirements.txt file.
 
To run the API, simply execute:
 
```
(env)$ flask run --host 0.0.0.0 --port 5000
````

or
 
```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Open [http://localhost:5000/#/](http://localhost:5000/#/) in your browser to check the API status.

# Thanks to the MVP professors

Thanks to the MVP professors, Marisa Silva, Dieinison Braga and Carlos Rocha.

## About This Project
 
This is the third MVP of the Full Stack Development Postgraduate Program at PUCRS University, Rio de Janeiro.
 
**Main component Gateway**: [https://github.com/leonardopaiva/pucrio-mvp-des-fs-advanced-micro-gateway-api](https://github.com/leonardopaiva/pucrio-mvp-des-fs-advanced-micro-gateway-api)


**Student**: Leonardo Souza Paiva  
**Portfolio**: [www.leonardopaiva.com](http://www.leonardopaiva.com)
