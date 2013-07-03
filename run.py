from sos2geojson.sos2geojson import sos2geojson 
from sos2geojson.sos2geojson import process_from_yaml 

# where services as defined
SERVICES_FILE = 'services.yaml'

# the root output folder for all generated GeoJSON layers
ROOT_OUTPUT_DIR = 'layers'

def main():
    process_from_yaml(ROOT_OUTPUT_DIR, SERVICES_FILE)

if __name__ == "__main__":
    main()

