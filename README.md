# Systems Integration Development Kit #

### Introduction ###

This environment allows you to easily install the development environment and its dependencies.
This is to be used for the 1st project in Systems Integration course from Informatics Engineering at IPVC/ESTG.

### How to I setup my development environment? ###

* Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* Create the necessary Docker Images and Containers by running the following command in the project's root folder:
```
docker-compose up --build -d
```
* Once your are done working in the assignment, you can remove everything by running:
```
docker-compose down
```
* **NOTE:** once you run the command above, the data in the database will be reset. Consider stopping the container instead, if you want to keep the data.
```
# stops all the containers
docker-compose stop

# restarts all the containers 
docker-compose start
```

### Available Resources ###

#### PostgreSQL Database ####

* Available at localhost:5432
  * **username**: is
  * **password**: is
  * **database**: is

#### Python Dev Environment ####

* Python 3.9.15
* You can add pre-installed packages to the **_requirements.txt_** file. Remember that if you add any dependency, you will have to build the Docker images again.
* You can easily use this python environment by opening up a terminal with the following command.
```
docker-compose run dev /bin/bash
```
* You can also run directly a Python script as follows. 
```
docker-compose run --rm dev python db-access/main.py
```
* Every time you use the command **_docker-compose run_**, a new unnamed container will be created. The **_--rm flag_** will automatically remove the created container once the run is over.
* For the XMLRPC server, you can run it in watch mode. This means that any time you edit the source code, the server will be automatically reloaded.
```
docker-compose run --rm dev pymon rpc-server/main.py
```
___
#### _Informatics Engineering @ipvc/estg, 2022-2023_ ####