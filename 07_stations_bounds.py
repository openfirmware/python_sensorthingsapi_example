# Find Stations in a bounding box. If Stations are moving, then only
# Stations *currently* in the bounding box will be returned.
# 
# Each "Station" is a "Thing" entity. We start by searching for Things,
# and including the "Locations" so we may do additional filtering. The
# filtering will use the PostGIS intersects to let us check for
# intersecting a polygon of our choosing. Any [Well-Known Text](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry)
# representation should work here.
# 
# Regarding "moving stations": "Thing" entities with changing "Location"
# entities could instead search their "HistoricalLocation" entities to
# find where they have been in the past.
# 
# **Do you have to use WKT?** Yes, I do not see any examples without
# WKT in the specification (http://docs.opengeospatial.org/is/15-078r6/15-078r6.html).
import requests
import json

# Root of SensorThings API Service (exclude trailing slash)
STA_URL = "https://arctic-sta.gswlab.ca/FROST-Server/v1.0"
# I picked this polygon to narrow down 3 results to 1.
FILTER_GEOM = "POLYGON ((-106 68, -106 70, -105 70, -105 68, -106 68))"

# Get root "Things" collection, but embed the linked Location entities
# inside the response.
# 
# This uses '$expand' to embed a sub-collection into the JSON response.
# We then use '$filter' to match the geometry in the 'Locations/location'
# field (note the attribute name is nested because we have 
# "expanded" the relationship).
# 
# '$filter' usage: http://docs.opengeospatial.org/is/15-078r6/15-078r6.html#54
# filter queries: http://docs.opengeospatial.org/is/15-078r6/15-078r6.html#table_23
# '$expand' usage: http://docs.opengeospatial.org/is/15-078r6/15-078r6.html#47
response = requests.get(
	f'{STA_URL}/Things',
	params=[
		('$expand', 'Locations'),
		('$filter', f"geo.intersects(Locations/location, geography'{FILTER_GEOM}')")
	]
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
