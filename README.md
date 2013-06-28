# SOS2GeoJSON

<img src="https://travis-ci.org/metajungle/sos2geojson.png" title="Travis" />

Takes a list of [Sensor Observation Services (SOSs)][ref-ogc-sos] specified in `services.yaml` and puts out a GeoJSON file showing the location of the sensor offerings for each service (the output is by default written to the `layers` folder). 

## Setup

Configure the `services.yaml` file to change which services to contact. 

## Run

    > python sos2geojson/sos2geojson.py

## Test

To run unit tests you need to: 

1. Add project to your Python path
2. Run tests

For example:

    > export PYTHONPATH=.:$PYTHONPATH
    > python sos2geojson/test/test_util.py
    > python sos2geojson/test/test_sos2geojson.py

With Python 2.7, you can automatically discover the tests:

    > python -m unittest discover

[ref-ogc-sos]: http://www.opengeospatial.org/standards/sos "Sensor Observation Service"

## Requirements 

See the `requirements.txt` file