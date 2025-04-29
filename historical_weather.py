from constants import *
import pandas as pd
import sqlite3
from utils import arg_parser
import sys

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE noaa (
    station text,
    name text,
    latitude float,
    longitude float,
    elevation float,
    date date,
    awnd float,
    fmtm int,
    pgtm int,
    prcp float,
    snow float,
    snwd float,
    tavg float,
    tmax float,
    tmin float,
    wdf2 int,
    wdf5 int,
    wsf2 float,
    wsf5 float,
    PRIMARY KEY (station, date)
)''')

INPUT_CSV_FILE = 'noaa_historical_weather_10yr.csv'

NUM_YEARS = 10.0

CITY_TO_NOAA_NAME = {
    BOSTON: 'BOSTON, MA US',
    JUNEAU: 'JUNEAU AIRPORT, AK US',
    MIAMI: 'MIAMI INTERNATIONAL AIRPORT, FL US',
}


def run_query(query):
    print(query)
    cursor.execute(query)
    print(round(cursor.fetchone()[0], 1))


def average_annual_days_of_precipitation(city):
    df_precipitation = df.loc[
        (df['NAME'] == CITY_TO_NOAA_NAME[city])
        & ((df['PRCP'] > 0.0) | (df['SNOW'] > 0.0))
    ]
    print(len(df_precipitation) / NUM_YEARS)

    query = f'SELECT COUNT(*)/{NUM_YEARS} FROM noaa WHERE name = "{CITY_TO_NOAA_NAME[city]}" AND (prcp > 0.0 OR snow > 0.0)'
    run_query(query)


def greatest_daily_temp_change(city, year, month):
    df['TDELTA'] = df['TMAX'] - df['TMIN']
    df['YEAR'] = df['DATE'].dt.year
    df['MONTH'] = df['DATE'].dt.month

    df_filtered = df.loc[df['NAME'] == CITY_TO_NOAA_NAME[city]]
    query = f'SELECT (tmax-tmin) FROM noaa WHERE name = "{CITY_TO_NOAA_NAME[city]}"'

    if year is not None:
        df_filtered = df_filtered.loc[df['YEAR'] == year]
        query = query + f' AND CAST(strftime("%Y", date) AS INT) = {year}'

    if month is not None:
        df_filtered = df_filtered.loc[df['MONTH'] == month]
        query = query + f' AND CAST(strftime("%m", date) AS INT) = {month}'

    print(round(df_filtered['TDELTA'].max(), 1))

    query = query + ' ORDER BY 1 DESC LIMIT 1'
    run_query(query)


args = arg_parser.parse_args()

try:
    df = pd.read_csv(INPUT_CSV_FILE, parse_dates=['DATE'])
    df.to_sql('noaa', conn, if_exists='replace')
except Exception:
    sys.exit(f'Error: could not read CSV file: {INPUT_CSV_FILE}')

if args[FUNCTION_NAME] == DAYS_OF_PRECIP:
    average_annual_days_of_precipitation(args[CITY])
elif args[FUNCTION_NAME] == MAX_TEMP_DELTA:
    greatest_daily_temp_change(args[CITY], args[YEAR], args[MONTH])
