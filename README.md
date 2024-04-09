# Chris Caruso <> Metronome Technical Challenge

# Part 1 - Reading APIs and Setting To CSV

## Setup

Requires Python 3

### Create and activate a virtual env

Navigate into the root directory ex: `cd ~/Dev/git/MetronomeTechnical`

Create a virtual env ex: `python3 -m venv metronome-env`

Activate via `source metronome-env/bin/activate`

(Deactivate when complete with `deactivate`)

### Install requirements

With the venv active, install with `pip3 install -r requirements.txt` inside the `1_read_csv` dir.

### Set Secret

Set the API key as the token on line #77 of `main.py` before running

## Run

### Run

Run the script from the root directory with `python3 main.py`

The output CSV will appear in the `1_read_csv` directory upon completion.

I would also try my API key from the demo to see more diverse billing outcomes.

## Notes

I tried to keep the structure as simple as possible for speed of testing and build out.

I would have potentially dug a little further into what fields to return if we had the chance to refine the reqs a little more.

Overall I am pretty happy with this.

# Part 2 - SQL

## Setup and Notes

All the SQL is under the `2_sql_queries` directory.

I added all of the relevant tables to Supabase to work through some of the queries. You will see a thread that I lack some of the busienss domain knowlege to the Metronome data structure. Some of the queries are rudimentary.

Note, I also ran into quite some confusion, particualrly around timeframes requested, currency formatting (cents vs dollars) and consumption units. I documented them to the best of my ability in the files.
