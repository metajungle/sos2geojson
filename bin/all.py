#!/usr/bin/env python

from sos2geojson.sos2geojson import sos2geojson 
from sos2geojson.sos2geojson import process_all_from_yaml 

# where services as defined
SERVICES_FILE = 'services.yaml'

# the root output folder for all generated GeoJSON layers
ROOT_OUTPUT_DIR = 'layers'

# the filename where the GeoJSON layer should be written
ALL_FILENAME = 'all.geojson'

def main():
    process_all_from_yaml(ROOT_OUTPUT_DIR, ALL_FILENAME, SERVICES_FILE)

if __name__ == "__main__":
    main()

