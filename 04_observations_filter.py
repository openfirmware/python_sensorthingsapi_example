# Sometimes you may have a sensor already preconfigured to send data to
# OGC SensorThings API, and you know the URL for that sensor, and you
# want the Observation data.
# 
# Here is how to retrieve some of the Observation data for a given
# Datastream, and filter by time interval. Paging is ignored.
import requests
import json

# Direct link to Datastream entity.
# 
# As we are hard-coding the link, we can assume we already have cached
# the "Unit of Measurement" attributes; if not, we can GET this URL and
# download them.
# 
# We could also retrieve other metadata, such as the Sensor entity (for
# information about the device or procedure), or the Observed Property
# (for referring to definitions and comparing to other ontologies).
DATASTREAM_URL = "https://arctic-sta.gswlab.ca/FROST-Server/v1.0/Datastreams(46)"

# Dates for filters must be in ISO8601 format.
# (I found that "-0600" DOES NOT work, but "-06:00" does work for time
# zone offsets. "Z" is also valid.)
INTERVAL_START = "2020-09-14T19:00:00.000Z"
INTERVAL_END = "2020-09-14T21:00:00.000Z"

# Get Observations, sorted by time ascending, in a given time interval.
# We use "ge" and "le" in the filters, so the time interval will be
# inclusive.
# 
# The time range filter may be left open-ended, without a start or end,
# as long as one end of the filter is applied.
# 
# '$filter' usage: http://docs.opengeospatial.org/is/15-078r6/15-078r6.html#54
# '$orderby' usage: http://docs.opengeospatial.org/is/15-078r6/15-078r6.html#50
response = requests.get(
	f'{DATASTREAM_URL}/Observations',
	params=[
		('$orderby', 'phenomenonTime asc'),
		('$filter', f'phenomenonTime ge {INTERVAL_START} and phenomenonTime le {INTERVAL_END}')
	]
)
observation_entities = response.json()
total = observation_entities['@iot.count']
observations = observation_entities['value']
# Do something with Observation data
print(f'Found {len(observations)} Observations of {total} Matching')

# Filters could be used on result values as well, to ignore specific
# "NODATA" values:
# ('$filter', f'result ne -9999')
