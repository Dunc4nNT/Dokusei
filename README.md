# Dokusei

Personal Discord Bot

## Links

- [Website](https://dunc4nnt.github.io/Dokusei-Website/)
- [Documentation](https://dunc4nnt.github.io/Dokusei-Docs/)
- [Dashboard](https://dunc4nnt.github.io/Dokusei-Dashboard/)

## Prerequisites

The following software is required to run the bot.

- [Python v3.10 or higher](https://www.python.org/downloads/)
- [PostgreSQL v14 or higher](https://www.postgresql.org/download/)

## Installation

### Step 1. Python Venv and Dependencies

1. Run `py -m venv venv` inside a terminal and activate it
2. Install all the dependencies by running `pip install -r requirements.txt`

### Step 2. Create Database

Open up the PSQL tool and create a role and database by writing the following:

```sql
CREATE ROLE dokusei WITH LOGIN PASSWORD 'verysecurepassword';
CREATE DATABASE dokusei OWNER dokusei;
```


### Step 3. Config

Rename `config.py.example` to `config.py` and fill in the following values:

```py
"bot": {
    "token": "", # your bot's token
    "description": "Personal Discord Bot",
    "logging_webhook": "", # optional webhook to post logging stuff in
    "stats_webhook": "", # optional webhook to post stats in
},
"translate": {
    "primary_language": "en", # language code from https://cloud.google.com/translate/docs/languages
},
"database": {
    "host": "127.0.0.1",
    "port": 5432,
    "user": "dokusei",
    "password": "verysecurepassword", # change this to whatever password  you created
    "database": "dokusei",
},
"links": {
    "repository": "https://github.com/Dunc4nNT/Dokusei",
    "website": "https://dunc4nnt.github.io/Dokusei-Website/",
    "docs": "https://dunc4nnt.github.io/Dokusei-Docs/",
    "dashboard": "https://dunc4nnt.github.io/Dokusei-Dashboard/",
    "support": "soon™",
},
"dev": {
    "mode": RunMode.PRODUCTION, # RunMode.DEVELOPMENT / RunMode.PRODUCTION
    "version": VersionInfo(
        major=0, minor=0, micro=1, releaselevel="alpha", serial=0
    ),
},
```

### Step 4. Initialising the database

Run the `prepare.py` file by typing `py prepare.py`

### Step 5. Running the Bot

Run the `main.py` file by typing `py main.py`
