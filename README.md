# Initial Setup

```
pip3 install -r requirements.txt
```

# Running Script

```
python3 ./historical_weather.py <function-name> [options]
```

## Script Arguments

```
function-name    options
days-of-precip   --city [bos|jnu|mia]
max-temp-delta   --city [bos|jnu|mia] --year [2010|2011|...|2019] --month [1|2|...|12]
```

- `city` is required

The following is only applicable for `max-temp-delta`:

- `year` is optional (required if `month` is specified)

- `month` is optional (also requires `year`)


## Sample Usage

```
python3 ./historical_weather.py days-of-precip --city bos

python3 ./historical_weather.py max-temp-delta --city bos

python3 ./historical_weather.py max-temp-delta --city bos --year 2010

python3 ./historical_weather.py max-temp-delta --city bos --year 2010 --month 1
```

# References

Python `argparse`
- https://docs.python.org/3/howto/argparse.html
- https://docs.python.org/3/library/argparse.html

Other
- https://stackoverflow.com/questions/606561/how-to-get-filename-of-the-main-module-in-python
  - To include the main module name in error messages related to custom argument parsing checks (e.g. if month specified, year is required), to match `argparse` behavior
