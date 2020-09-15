# In this case a sensor is moving, and each Observation occurs at a
# different geographic location. We can ask OGC SensorThings API to
# include the "Feature of Interest" entity for each Observation, which
# includes the GeoJSON for the feature being observed.
# 
# Multiple Observations may share the exact same "Feature of Interest"
# entity, if they occur in the "same location". This can even occur
# across Observations from different Datastreams or Thing hierarchies,
# but in that case some intentional client-side logic has to be used to
# coalesce usage of "Feature of Interest" entities.
import requests
import json

# Direct link to Datastream entity.
# Unfortunately for this example I do not have an example of a moving
# Datastream. The handling of "Features of Interest" is the same though,
# so we can still retrieve the Observation location.
DATASTREAM_URL = "https://arctic-sta.gswlab.ca/FROST-Server/v1.0/Datastreams(46)"
# The unit can be retrieved from the "Unit of Measurement" in the
# Datastream entity. Or hard-coded/cached.
unit = "˚C"

# Get Observations, sorted by time descending.
# We use default paging, so this gets the most recent 100 Observations.
# (Different STA server implementations may have different page sizes,
# and some let you modify the page size, up to a limit.)
# 
# '$expand' usage: http://docs.opengeospatial.org/is/15-078r6/15-078r6.html#47
# '$orderby' usage: http://docs.opengeospatial.org/is/15-078r6/15-078r6.html#50
response = requests.get(
	f'{DATASTREAM_URL}/Observations',
	params=[
		('$orderby', 'phenomenonTime desc'),
		('$expand', f'FeatureOfInterest')
	]
)
observation_entities = response.json()
total = observation_entities['@iot.count']
observations = observation_entities['value']

print(f'I downloaded {len(observations)} Observations of the {total} matching Observations in STA')

# Switch sort order to ascending by phenomenonTime
observations.reverse()

# Print out the data, with the coords from GeoJSON
for observation in observations:
	timestamp = observation['phenomenonTime']
	result = observation['result']
	
	# The GeoJSON feature could be something other than a Point, however
	# it is unlikely. For robustness this should be checked.
	geojson_type = observation['FeatureOfInterest']['feature']['type']
	if geojson_type != "Point":
		print(f"Warning: unhandled GeoJSON type: {geojson_type}")

	coords = observation['FeatureOfInterest']['feature']['coordinates']
	print(f"{timestamp}, {result} {unit}, {coords[1]} E, {coords[0]} N")
