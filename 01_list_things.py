# In this example, a user wants to get a list of all the sensor stations
# and the station locations, and plot them on a map. The metadata for
# the stations can then be used later to load Observation data.
import requests
import json

# Root of SensorThings API Service (exclude trailing slash)
STA_URL = "https://arctic-sta.gswlab.ca/FROST-Server/v1.0"

# Get root "Things" collection.
# With no additional query parameters, a list of entities up to the
# default paging limit count will be returned by STA.
response = requests.get(f'{STA_URL}/Things')
thing_entities = response.json()

# As we didn't filter the collection, @iot.count will be the number of
# these entities in the STA database. The number of entities in the
# 'value' array will be limited by the paging limit, but will draw from
# this same collection.
server_things_count = thing_entities['@iot.count']

print(f'Server has {server_things_count} Things.')

# This list of "Thing" entities will all have the same schema, as
# defined by the specification:
# http://docs.opengeospatial.org/is/15-078r6/15-078r6.html#25
things = thing_entities['value']

print(f'Found {len(things)} entities:')

# Loop through the Thing entities and print some information
for thing in things:
	print(f'Thing: {thing["name"]}')
	print(thing['description'])

	# We need to download the most recent Location entity to get the
	# latitude/longitude. This is available at the URL in the 
	# Locations navigationLink.
	location_response = requests.get(thing['Locations@iot.navigationLink'])
	location_entities = location_response.json()

	# Auto-select first Location. There are multiple "Locations" as STA
	# will support different encodings for the same location. Currently
	# only GeoJSON is supported, so we just assume here, but in later
	# versions of STA it might be necessary to check.
	last_location = location_entities['value'][0]
	coords = last_location['location']['coordinates']

	# Print some info about this place. The 'location' should contain
	# valid GeoJSON. We assume it is a point.
	print(f'Located at: {coords[1]}˚ N, {coords[0]}˚ E')
	print()
