from constants import *
import pandas as pd
from utils import arg_parser
import sys

INPUT_CSV_FILE = 'noaa_historical_weather_10yr.csv'

NUM_YEARS = 10.0

CITY_TO_NOAA_NAME = {
    BOSTON: 'BOSTON, MA US',
    JUNEAU: 'JUNEAU AIRPORT, AK US',
    MIAMI: 'MIAMI INTERNATIONAL AIRPORT, FL US',
}


def average_annual_days_of_precipitation(city):
    df_precipitation = df.loc[
        (df['NAME'] == CITY_TO_NOAA_NAME[city])
        & ((df['PRCP'] > 0.0) | (df['SNOW'] > 0.0))
    ]
    print(len(df_precipitation) / NUM_YEARS)


def greatest_daily_temp_change(city, year, month):
    df['TDELTA'] = df['TMAX'] - df['TMIN']
    df['YEAR'] = df['DATE'].dt.year
    df['MONTH'] = df['DATE'].dt.month

    df_filtered = df.loc[df['NAME'] == CITY_TO_NOAA_NAME[city]]

    if year is not None:
        df_filtered = df_filtered.loc[df['YEAR'] == year]

    if month is not None:
        df_filtered = df_filtered.loc[df['MONTH'] == month]

    print(round(df_filtered['TDELTA'].max(), 1))


args = arg_parser.parse_args()

try:
    df = pd.read_csv(INPUT_CSV_FILE, parse_dates=['DATE'])
except Exception:
    sys.exit(f'Error: could not read CSV file: {INPUT_CSV_FILE}')

if args[FUNCTION_NAME] == DAYS_OF_PRECIP:
    average_annual_days_of_precipitation(args[CITY])
elif args[FUNCTION_NAME] == MAX_TEMP_DELTA:
    greatest_daily_temp_change(args[CITY], args[YEAR], args[MONTH])
