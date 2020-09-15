# Find all "Air Temperature" data inside a polygon for a given time
# range.
# 
# In this case, we start by searching for "Air Temperature" in the STA's
# Observed Properties collection. There may be more than one, so we have
# to have some sort of way to select the "Air Temperature" we mean. Each
# Observed Property entity has a "definition" attribute that should link
# to an external Ontology, and that can be queried to determine if it is
# the "same". Alternatively the "description" attribute can be verified
# by a human.
# 
# After selecting the Observed Property, we can ask for Datastreams that
# are in the polygon. Each Datastream has an "observedArea" attribute
# that auto-fills with a GeoJSON object (point or polygon) that covers
# all its Features of Interest. This works with '$filter', and gives us
# all Datastreams that have ever had an Observation occur with an FOI
# in that polygon.
import requests
import json

# Root of SensorThings API Service (exclude trailing slash)
STA_URL = "https://arctic-sta.gswlab.ca/FROST-Server/v1.0"

# Get all "ObservedProperties" entities that have the name
# "Air Temperature".
# 
# Note that in $filter, strings must be single-quoted only.
response = requests.get(
	f'{STA_URL}/ObservedProperties',
	params=[('$filter', "name eq 'Air Temperature'")]
)
op_entities = response.json()
obs_props = op_entities['value']

print(f'Found {len(obs_props)} Observed Properties:')

for op in obs_props:
	print(f'Observed Property: {op["name"]}')
	print(f'\t{op["description"]}')
	print(f'\t{op["definition"]}')
	print()

# At this point a user or process must select the correct Observed
# Property. We will hard-code the correct one.
OBSERVED_PROPERTY_URL = "https://arctic-sta.gswlab.ca/FROST-Server/v1.0/ObservedProperties(1)"

FILTER_GEOM = "POLYGON ((-106 68, -106 70, -105 70, -105 68, -106 68))"

# Get all "Datastream" entities in the polygon.
response = requests.get(
	f'{OBSERVED_PROPERTY_URL}/Datastreams',
	params=[
		('$filter', f"geo.intersects(observedArea, geography'{FILTER_GEOM}')")
	]
)
datastream_entities = response.json()
datastreams = datastream_entities['value']

print(f'Found {len(datastreams)} Datastreams')

for datastream in datastreams:
	print(f'Datastream: {datastream["name"]}')
	print(f'\t{datastream["description"]}')
	print()

# Next each datastream is queried for Observations that lie in the
# polygon bounds. While we could have used $expand to combine these
# requests, this has a significant impact on server performance with
# these kind of joined queries.
