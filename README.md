<p align="center">
<a  href="www.vrpcommute.tk">
       <img align="center" height=85 src="https://github.com/kenanlv/VRP-full-stack/blob/master/src/assets/logo.svg">
   </a>
 <p/>

# VRP-Full-Stack

  
  The Vehicle Routing Problem is a combinational optimization problem in which the goal is to find optimal routes for multiple vehicles to visiting sets of locations. It generalizes the Traveling Sales Man problem.
  Different to the general VRP, where all vehicles come out from the same depot. We want to focus on optimizing routes that going into the depot. 
  > Imagine you and your friends are going to the place for some event. Some of your friends have a car, and some do not. What is the optimum way to distribute for carpool such that everyone will get to the event place with the minimum of driving distance. 
  
Though the problem changed to multiple deports to a single destination, we could still apply the same algorithm for VRP in our problem. We used Inter/Intra local route search in our case.

- Backend:
    - We choose to use flask as our backend framework, and PostgreSQL as our database to store the user information. 
    - Used Google Oauth API for user to login. We also generated our JWT when retrieving data from the database.
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
      
## Demo
  > **Log-in page**
<p align="center">
  <img width="800" height="400" src="https://github.com/kenanlv/VRP-full-stack/blob/master/flaskr/templates/demo_pic/login_page.png">
</p>

  > **Registration page**
<p align="center">
  <img width="800" height="400" src="https://github.com/kenanlv/VRP-full-stack/blob/master/flaskr/templates/demo_pic/register.png">
</p>

  > **Successfully registered notification page**
<p align="center">
  <img width="800" height="400" src="https://github.com/kenanlv/VRP-full-stack/blob/master/flaskr/templates/demo_pic/register_completion.png">
</p>

  > **Vehicle Routing Calculation**
  
  > **Google API**
<p align="center">
  <img width="500" height="350" src="https://github.com/kenanlv/VRP-full-stack/blob/master/flaskr/templates/demo_pic/GoogleLocalSearchSolver.png">
</p>
  
  > **Our designed inter/intra local search**
<p align="center">
  <img width="500" height="350" src="https://github.com/kenanlv/VRP-full-stack/blob/master/flaskr/templates/demo_pic/SolverNotGoogle.png">
</p>
  

  > **Email templates: customer and driver**
<p align="center">
  <img width="300" height="500" src="https://github.com/kenanlv/VRP-full-stack/blob/master/flaskr/templates/demo_pic/customer_temp_email.PNG">
  <img width="300" height="500" src="https://github.com/kenanlv/VRP-full-stack/blob/master/flaskr/templates/demo_pic/driver_email_no_one.PNG">
  <img width="250" height="500" src="https://github.com/kenanlv/VRP-full-stack/blob/master/flaskr/templates/demo_pic/driver_email.PNG">
</p>

#

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.


### Prerequisites

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

### Setting up SendGrid

The SendGrid API is used for distributing and sending emails to users. Please refer to the ```email_sender_helper.py``` to see how we implemented the API OR use [SendGrid Documentation](https://sendgrid.com/docs/) for more information.

We used our own SendGrid email templates hosting on the SendGrid website. However, we encourage that you make your own templates. *(We also included an example email template HTML in under the flaskr folder: ```driver_email.html```)* You could certainly have the templates locally and ease the process of modifying the templates.


### Setting up ```.env``` file
After pulled this project, go to the docker-compose.yml directory and make an ```.env``` file with 
following environment variables:
```.env
SECRET_KEY=hvkjhjkls              # Used for encryption. PLEASE GENERATE YOUR OWN SECRET
GOOGLE_CLIENT_SECRET=[YOUR_KEY]   # Google OAuth secret
GOOGLE_CLIENT_ID=[YOUR_KEY]       # Google OAuth client ID
DEST_ID=[YOUR_PLACE_ID]           # Google Place ID for your destination
SENDGRID_API_KEY=[YOUR_KEY]       # Sendgrid API to send Email
API_KEY_DIS=[YOUR_KEY]            # Google Places API key
API_KEY_GEO=[YOUR_KEY]            # Google Places API key
SOLVER_START_TIME=12              # Time of day that solver will start
PICK_UP_TIME=10                   # Time of day that drivers start to pick up passengers
SOLVER_TIME_SPAN=15               # Time in seconds for solver to run
POSTGRES_USER=postgres            # Default username for database
POSTGRES_PASSWORD=[YOUR_PWD]      # Password for database
POSTGRES_DB=postgres              # Default database name
```

### Build and deploy
After pulled this project, go to the docker-compose.yml directory and type in the following command.

```shell script
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


### Running the tests *(only for routing calculating function)*

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
