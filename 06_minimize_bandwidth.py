# This replicates downloading Observations like #03, but here we use the
# '$select' query to limit the data coming from the server into a
# smaller package, saving some bandwidth.
# 
# #03, no optimization: 			  250 KB
# #06, limiting fields:  			   41 KB
# #06, limiting fields and using CSV:  18 KB
# 
# These bandwidth counts do not include any HTTP compression.
# Server-side gzip can provide a significant size savings, especially
# for repetitive information like time series data.
import requests
import json
import math

# Direct link to Datastream entity.
DATASTREAM_URL = "https://arctic-sta.gswlab.ca/FROST-Server/v1.0/Datastreams(46)"
# Use server-side paging to download more data until this number is
# reached.
OBSERVATION_LIMIT = 500


# Get Observations, sorted by time descending.
# 
# We use '$select' to only ask for the 'phenomenonTime' and 'result'
# attributes for 'Observation' entities, excluding all other attributes.
# 
# '$orderby' usage: http://docs.opengeospatial.org/is/15-078r6/15-078r6.html#50
# '$select' usage: http://docs.opengeospatial.org/is/15-078r6/15-078r6.html#48
more_results = True
download_url = f'{DATASTREAM_URL}/Observations'
observations = []
total_downloaded_bytes = 0

while(more_results and len(observations) < OBSERVATION_LIMIT):
	response = requests.get(
		download_url,
		params=[
			('$orderby', 'phenomenonTime desc'),
			('$select', 'phenomenonTime,result')
		]
	)
	total_downloaded_bytes += len(response.content)
	observation_entities = response.json()
	entities = observation_entities["value"]
	print(f'Downloaded {len(entities)} entities: {download_url}')
	observations += entities

	# If the '@iot.nextLink' key is in the response, there is more data
	# on the server. Otherwise, we are at the end of the collection.
	more_results = ('@iot.nextLink' in observation_entities)
	download_url = observation_entities['@iot.nextLink']

print(f'Downloaded {len(observations)} Observations in total, {math.ceil(total_downloaded_bytes / 1000)} kilobytes.')

# Alternatively, we can download CSV data directly from OGC SensorThings
# API. Not all server implementations support this.
more_results = True
download_url = f'{DATASTREAM_URL}/Observations'
csv_headers = ""
observations = []
total_downloaded_bytes = 0

while(more_results and len(observations) < OBSERVATION_LIMIT):
	response = requests.get(
		download_url,
		params=[
			('$orderby', 'phenomenonTime desc'),
			('$select', 'phenomenonTime,result'),
			('$resultFormat', 'CSV')
		]
	)
	total_downloaded_bytes += len(response.content)
	csv_headers = response.text.split('\n')[0]
	entities = response.text.lstrip(csv_headers + '\n').splitlines()
	observations += entities
	print(f'Downloaded {len(entities)} entities: {download_url}')

	# If the '@iot.nextLink' key is in the response, there is more data
	# on the server. Otherwise, we are at the end of the collection.
	more_results = ('@iot.nextLink' in observation_entities)
	download_url = observation_entities['@iot.nextLink']

print(f'Downloaded {len(observations)} Observations in total, {math.ceil(total_downloaded_bytes / 1000)} kilobytes.')
