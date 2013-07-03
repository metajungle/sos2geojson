# SOS2GeoJSON

<img src="https://travis-ci.org/metajungle/sos2geojson.png" title="Travis" />

Takes a list of [Sensor Observation Service (SOS)][ref-ogc-sos] endpoints and puts out GeoJSON feature collections for all the sensor offerings of the services. 

## Install 

See the `requirements.txt` file for dependencies. The dependencies can be installed like this:

    > pip install -r requirements.txt

To then install `sos2geojson`, run:

    > python setup.py install 

## Usage

You can generate GeoJSON from a single service endpoint or from a list of service endpoints. For a single endpoint, use: 

    from sos2geojson.sos2geojson import sos2geojson 
    geojson = sos2geojson("http://sdf.ndbc.noaa.gov/sos/server.php")

You can also provide a list of service endpoints: 

    from sos2geojson.sos2geojson import sos2geojson 
    geojson = sos2geojson(["http://sdf.ndbc.noaa.gov/sos/server.php", 
                           "http://sccoos-obs0.ucsd.edu/sos/server.php"]) 

The GeoJSON can then be written to a file, e.g.:

    with open("/path/to/my/layer.geojson", "w") as f:
        f.write(geojson)

To pretty print the GeoJSON, pass the named parameter `pretty` set to `True`, e.g.:

    from sos2geojson.sos2geojson import sos2geojson 
    geojson = sos2geojson("http://sdf.ndbc.noaa.gov/sos/server.php", pretty=True)

For more detailed options, take a look at the code.

## Command line 

You can also use the included `run.py` script to generate GeoJSON files from the command line. The input is in this case specified in the `services.yaml` configuration file. 

Make sure that `sos2geojson` is on your path and then run the program:

    > python run.py
    
The output will end up in a folder called `layers` by default. This can be modified by changing the `run.py` script. 

If you want to create a single GeoJSON layer for *all* services listed in the `services.yaml` file, run the `all.py` script:

    > python all.py
    
The result will by default be written to `layers/all.geojson`. 

## Tests

To run the unit tests make sure that the project is on your Python path and then run: 

    > python -m unittest discover
    
The above is only for Python 2.7 and up. If you are using Python 2.6, do something like this:

    > export PYTHONPATH=.:$PYTHONPATH
    > python sos2geojson/test/test_util.py
    > python sos2geojson/test/test_sos2geojson.py


[ref-ogc-sos]: http://www.opengeospatial.org/standards/sos "Sensor Observation Service"

