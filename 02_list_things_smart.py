# This is like the first example, except we use some of query features
# of OGC SensorThings API to reduce the number of requests we need to
# perform.
# 
# The last example had a "n + 1" problem where an extra request is
# needed for each "Thing" to get the "Location". Here we solve this by
# asking STA to bundle the Locations when we ask for the Things, so we
# only need one request.
import requests
import json

# Root of SensorThings API Service (exclude trailing slash)
STA_URL = "https://arctic-sta.gswlab.ca/FROST-Server/v1.0"

# Get root "Things" collection, but embed the linked Location entities
# inside the response.
# 
# This uses '$expand' to embed a sub-collection into the JSON response.
# In later examples, this will be shown in nested usage.
# 
# '$expand' usage: http://docs.opengeospatial.org/is/15-078r6/15-078r6.html#47
response = requests.get(
	f'{STA_URL}/Things',
	params=[('$expand', 'Locations')]
)
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

	# Auto-select first Location
	last_location = thing['Locations'][0]
	coords = last_location['location']['coordinates']

	# Print some info about this place. The 'location' should contain
	# valid GeoJSON. We assume it is a point.
	print(f'Located at: {coords[1]}˚ N, {coords[0]}˚ E')
	print()
