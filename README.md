# Coffee Shop Full Stack

## Full Stack Nano

Udacity has decided to open a new digitally enabled cafe for students to order drinks, socialize, and study hard.

The application contains:

1) Display graphics representing the ratios of ingredients in each drink.
2) Allow public users to view drink names and graphics.
3) Allow the shop baristas to see the recipe information.
4) Allow the shop managers to create new drinks and edit existing drinks.

### Backend

The `./backend` directory contains Flask server with a SQLAlchemy module. This contains all the required endpoints and integrated with Auth0 for authentication.

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contains a Ionic frontend to consume the data from the Flask server. The environment variables that is found within (./frontend/src/environment/environment.ts) is updated  so that the Auth0 configuration details are set up for the backend app. 

[View the README.md within ./frontend for more details.](./frontend/README.md)
