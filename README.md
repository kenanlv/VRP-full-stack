# Full-Stack-VRP

  The Vehicle Routing Problem is a combinational optimization problem in which the goal is to find optimal routes for multiple vehicles to visiting sets of locations. It generalizes the Traveling Sales Man problem.
  Different to the general VRP, where all vehicles come out from the same depot. We want to focus on optimizing routes that going into the depot. 
  > Imagine you and your friends are going to the place for some event. Some of your friends have a car, and some do not. What is the optimum way to distribute for carpool such that everyone will get to the event place with the minimum of driving distance. 
  
Though the problem changed to multiple deports to a single destination, we could still apply the same algorithm for VRP in our problem. We used Inter/Intra local route search in our case.

- Backend:
    - We choose to use flask as our backend framework, and PostgreSQL as our database to store the user information. 
    - Usd Google Oauth API for user to login. We also generated our JWT when retrieving data from the database.
    - Inter/Intra local search algorithm provided by the ortools for optimizing the routes.
    - Periodic timer for the route calculating and sending emails to the user. 
    - Nginx server to connect with flask through uWSGI, all static files are handled by Nginx.

- Frontend:
    - Used Vue framework

- Dockerized the whole package so that the server could run on different operating systems.
  - Flask + Nginx + WSGI
  - PostgreSQL
  - Huey periodic timer
- Freed local machine by setting up a remote docker-machine for deploying the webserver remotely. 
      
## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Backend

#### Prerequisites

> You will need Docker and Node.js installed on your local machine.

> Register for **Google developer consol** and get the Google API keys as environment variables for the project. 
Find the useful information [here](https://developers.google.com/).

    APIs needed to register and obtain secret keys:

    Google Oauth, 
    Google Places, 
    Google Distance Matrix, 
    Google Geocoding, 
    Google Maps Static

> Have your web server and your domain set up properly and obtain the access token and secret key accordingly.

For writing the secrete keys into the environment variables, please refer to the **".env"** file for proper input format.

#### Build and deploy
After pulled this project, go to the docker-compose.yml directory and type in the following command.

```
npm install
npm run build
docker-compose build
docker-compose up -d db
docker-compose run --rm web /bin/bash -c "python -c  'import database; database.init_db()'"
docker-compose up
```
Only run those following commands
```
docker-compose run --rm web /bin/bash -c "python -c  'import database; database.init_db()'"
```
When you **first** build and run the project, this will initialized your database and bootstrap the datatable.
After the initialization, you could skip these two commands, and simply do "docker-compose up"


#### Running the tests *(only for routing calculating function)*

Refering to [test.py]([here](https://developers.google.com/).) under flaskr folder. 

Write out your own problem to testing your solver.



## Authors

* **Tony Fei** - [GitHub page](https://github.com/sa-tony)
* **Kenan Lv** - [GitHub page](https://github.com/kenanlv)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [Inter/Intra Local Search](https://github.com/topics/vehicle-routing-problem?l=python)

## Further Readings

* The Taxi-problem
* Dail-a-ride

# 
