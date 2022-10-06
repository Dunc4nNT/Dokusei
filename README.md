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

```json
"BOT": {
    "TOKEN": "", // your bot's token
    "DESCRIPTION": "Personal Discord Bot",
    "STATS_WEBHOOK": "", // optional webhook to post stats in
    "LOGGING_WEBHOOK": "", // optional webhook to post logging stuff in
},
"TRANSLATE": {
    "PRIMARY_LANGUAGE": "en", // language code from https://cloud.google.com/translate/docs/languages
},
"DATABASE": {
    "DSN": "postgres://dokusei:verysecurepassword@127.0.0.1:5432/dokusei", // replace with whatever password you created
},
"LINKS": {
    "REPO": "https://github.com/Dunc4nNT/Dokusei",
    "WEBSITE": "https://dunc4nnt.github.io/Dokusei-Website/",
    "DOCS": "https://dunc4nnt.github.io/Dokusei-Docs/",
    "DASHBOARD": "https://dunc4nnt.github.io/Dokusei-Dashboard/",
    "SUPPORT": "soon™",
},
"DEV": {
    "MODE": "development",  // development/production
    "VERSION": "0.0.1", // just keep it on production, development mode has some extra dev things
},
```

### Step 5. Running the Bot

Run the `main.py` file by typing `py main.py`
