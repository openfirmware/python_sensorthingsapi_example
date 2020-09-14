# Sometimes you may have a sensor already preconfigured to send data to
# OGC SensorThings API, and you know the URL for that sensor, and you
# want the Observation data.
# 
# Here is how to retrieve some of the Observation data for a given
# Datastream, using recursive paging.
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
# Use server-side paging to download more data until this number is
# reached.
OBSERVATION_LIMIT = 500


# Get Observations, sorted by time ascending.
# 
# (While we could download the entity to get the
# 'Observations@iot.navigationLink' attribute, we can hard-code it here
# as the URL is always created this way.)
# 
# '$orderby' usage: http://docs.opengeospatial.org/is/15-078r6/15-078r6.html#50
more_results = True
download_url = f'{DATASTREAM_URL}/Observations'
observations = []

while(more_results and len(observations) < OBSERVATION_LIMIT):
	response = requests.get(
		download_url,
		params=[('$orderby', 'phenomenonTime asc')]
	)
	observation_entities = response.json()
	entities = observation_entities["value"]
	print(f'Downloaded {len(entities)} entities: {download_url}')
	observations = observations + entities

	# If the '@iot.nextLink' key is in the response, there is more data
	# on the server. Otherwise, we are at the end of the collection.
	more_results = ('@iot.nextLink' in observation_entities)
	download_url = observation_entities['@iot.nextLink']

print(f'Downloaded {len(observations)} Observations in total.')

# Next the list of Observations will be converted into a simple list of 
# lists. e.g.
# ('2018-02-07T16:24:13.000Z', 13.858),
# ('2018-02-07T16:34:13.000Z', 6.306)
# 
# "Observation" usage: http://docs.opengeospatial.org/is/15-078r6/15-078r6.html#31
# 
# The "phenomenonTime" may be replaced with "resultTime", as some 
data = list(map(lambda observation: (observation['phenomenonTime'], observation['result']), observations))

# Important: We sorted by ascending "phenomenonTime" on the server as
# by default they would be sorted by database ID, which may not
# represent Observations in chronological order (e.g. backfilling older
# data would change this). I have specifically ran into issues with
# JavaScript chart libraries that have errors when the time series data
# isn't sorted.
# 
# The chart libraries also have issues when two points exist for the
# same timestamp. **This can happen in OGC SensorThings API**, as
# multiple Observation entities with the same "phenomenonTime" can exist
# in the same database. Users who download Observations from STA must
# check and remove any duplicates.
# 
# ArcticConnect has customized their STA server to prevent these
# duplicate Observation entities from being created, and instead they
# are "merged" together. Not all implementations do this though so you
# cannot always expect unique Observations.
# 
# TODO: Make this list of data unique on phenomenonTime
print(data)
