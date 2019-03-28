It's pizzabot.

# General Pizzabot Setup

The current setup for pizzabot is quite manual. 

## Packages Required

Pizzabot relies on a number of Python libraries. `pip install` the following:

- `flask`
- `flask-restful`
- `flask-cors`
- `slackclient`

## Slack API Key

You'll need an API key in order to connect to Slack. Follow their
[setup instructions](https://api.slack.com/bot-users) and store this key in a
file named `api.token` in the root directory of the repo.

## MariaDB Setup

A MariaDB instance is used to store pizzachat data. The current setup assumes
you have configured MariaDB to only listen on a local socket. The following
commands will create the users, databases and tables required:

- `CREATE DATABASE pizzachat;`
- `CREATE TABLE pizzachat.foodlist (date TIMESTAMP(0), who VARCHAR(100), what VARCHAR(1000));`
- `CREATE USER 'pizzabot'@'localhost';`
- `GRANT ALL PRIVILEGES ON pizzachat.* TO 'pizzabot'@'localhost';`
- `FLUSH PRIVILEGES;`

## Launching Pizzabot Components

There are two primary scripts that will need to be launched in order for
pizzabot to function properly. Currently this done by launching them each in a
screen.

- `pizzabot.py`
- `foodlist_api.py`

### Client dev env setup

To set up a new dev env for the frontend:

- Install and run [Docker](https://docs.docker.com/engine/installation/mac/)
- `cd app` to get to the directory with the `docker-compose.yml` file
- `docker-compose build` to build the container
- `docker-compose up` to run the container and start webpack-dev-server
- visit `localhost:6789` in the browser

The browser console will show error output from webpack and debugging info from Redux. You can also install the [React Developer Tools](https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi?hl=en) to debug React.
