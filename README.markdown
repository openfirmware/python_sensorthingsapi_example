# Python OGC SensorThings API Examples

Some examples of using the HTTP REST API for OGC SensorThings API to query data.

Note that these examples are using the secondary URL for the Arctic Connect SensorThings API Service. A new URL will become the main URL in late 2020.

Disclaimer: I do not know Python; hopefully the REST API usage instructions come through the examples.

## Requirements

I tested this with Python 3.6.6 on MacOS 10.13.

ArcticConnect is using [FROST Server](https://github.com/FraunhoferIOSB/FROST-Server) for serving OGC SensorThings API. The code may work when pointed to another OGC SensorThings API service, with slightly different results.

## Examples

For retrieving a list of sensor stations and their locations for mapping, try these:

* [List "Thing" entities and their coordinates](01_list_things.py)
* [Same as above, but only requiring 1 HTTP request](02_list_things_smart.py)

Sometimes you know when a Datastream of data has already been created in STA, and you need the simplest way to retrieve the observation data.

* [Retrieve the Observation data for Datastream time series](03_basic_data_query.py)
    - Includes handling paging, sorting
* [Filter the Observation data by time interval](04_observations_filter.py)
* [Include the "Feature of Interest" entity for moving Observation data](05_moving_features.py)
* [Use the "select" query to minimize the response body size](06_minimize_bandwidth.py)
    - Compare `250 KB` vs `42 KB` vs `18 KB` in different methods

If you have a geographic region of interest (bounding box or polygon), you can do some filtering based on that.

* [Use a bounding box for finding stations](07_stations_bounds.py)
* Use a polygon to filter all Datastreams for "Air Temperature" in a desired region
* For a moving sensor, get only observations that occurred in a polygon

## License

MIT License
