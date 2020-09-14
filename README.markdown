# Python OGC SensorThings API Examples

Some examples of using the HTTP REST API for OGC SensorThings API to query data.

Note that these examples are using the secondary URL for the Arctic Connect SensorThings API Service. A new URL will become the main URL in late 2020.

## Requirements

I tested this with Python 3.6.6 on MacOS 10.13.

## Examples

For retrieving a list of sensor stations and their locations for mapping, try these:

* [List "Thing" entities and their coordinates](01_list_things.py)
* [Same as above, but only requiring 1 HTTP request](02_list_things_smart.py)

Sometimes you know when a Datastream of data has already been created in STA, and you need the simplest way to retrieve the observation data.

* Retrieve the Observation data for Datastream time series
    * Includes handling paging, sorting
* Filter the Observation data by time interval
* Include the "Feature of Interest" entity for moving Observation data
* Use the "select" query to minimize the response body size

If you have a geographic region of interest (bounding box or polygon), you can do some filtering based on that.

* Use a bounding box for finding stations
* Use a polygon to filter 


## License

MIT License
