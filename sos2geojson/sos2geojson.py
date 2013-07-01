#!/usr/bin/env python
import os
import sys

from owslib.sos import SensorObservationService
#from owslib.fes import FilterCapabilities
#from owslib.ows import OperationsMetadata
#from owslib.crs import Crs
#from datetime import datetime

import urllib2
import yaml 
import json 

import util

# where services as defined
SERVICES_FILE = 'services.yaml'

# the root output folder for all generated GeoJSON layers 
ROOT_OUTPUT_DIR = 'layers'


#
# "INTERNAL" 
#

def collect_features(offerings, p_fn):
  """
  Collects features from a sensor offering list
  """
  features = []
  for key in offerings.keys():
    offering = offerings[key]
    # for now, only consider offerings with 'proper' bbox
    bbox = util.bbox2geometry(offering.bbox)
    if bbox != None:
      features.append({
        "type" : "Feature", 
        "geometry" : bbox, 
        "properties": p_fn(offering)
      })
    else:
      print "Skipping %s" % offering.id
  return features
  
def offering_geojson_properties_default(offering):
  """
  Default function for constructing the 'properties' 
  of a GeoJSON feature from a sensor offering
  """
  return { "Offering Id" : offering.id, 
           "Description" : offering.description, 
           "Observed properties" : 
           [util.uri_pretty(p) for p in offering.observed_properties] }

def offering_geojson_properties_alt(offering):
  """
  Generates alternative GeoJSON feature 'properties' 
  object from a sensor offering
  """
  p = { "offering-id" : offering.id, 
           "offering-name" : offering.name, 
           "offering-description" : offering.description, 
           "offering-properties" : offering.observed_properties, 
           "offering-formats" : offering.response_formats }
  if offering.begin_position:
    p["offering-start"] = str(offering.begin_position)
  if offering.end_position:
    p["offering-end"] = str(offering.end_position)
  return p

def generate_geojson(offerings, geojson_prop_fn=offering_geojson_properties_default):
  """
  Generates GeoJSON from a sensor offering list, 
  using the given function to construct the GeoJSON
  feature properties object 
  """
  layer = {
      "type": "FeatureCollection",
      "features": collect_features(offerings, geojson_prop_fn) 
  }
  return layer

def process_sos_endpoint(endpoint, output_dir, idx, filename=None):
  """
  Processes a single SOS endpoint
  """
  response = urllib2.urlopen(util.add_query_params_v1(endpoint), timeout=60)
  xml = response.read()
  sos = SensorObservationService(None, xml=xml)
  # generate GeoJSON layer structure 
  layer = generate_geojson(sos.contents)
  # create a GeoJSON layer filename
  if filename == None:
    try:
      filename = "%s.geojson" % util.name_for_filename(sos.identification.title)
    except AttributeError:
      # provide a name if we cannot find one 
      filename = "sos-layer%s.geojson" % idx
  else:
    filename = "%s.geojson" % filename
  # dump to JSON
  with open(os.path.join(output_dir, filename), "w") as f:
      f.write(json.dumps(layer, indent=4))

def process_services():
  """
  Processes all SOS services given in configuration file
  """
  if not os.path.exists(ROOT_OUTPUT_DIR): 
    try:
      os.makedirs(ROOT_OUTPUT_DIR) 
    except OSError:
      sys.stderr.write("Could not create root output directory, aborting\n")
      return 
      
  with open(SERVICES_FILE) as f:
    services = yaml.load(f)
    for (idx, folder) in enumerate(services.keys()):
      try:
        output_dir = os.path.join(ROOT_OUTPUT_DIR, folder)
        if not os.path.exists(output_dir):
          os.makedirs(output_dir)
        for endpoint_info in services[folder]:
          filename = None
          # check if the service endpoint comes with a name to use
          if isinstance(endpoint_info, dict):
            endpoint = endpoint_info.keys()[0]
            filename = endpoint_info[endpoint]
          else:
            endpoint = endpoint_info
          process_sos_endpoint(endpoint, output_dir, idx, filename)
      except OSError:
        sys.stderr.write("Could not create output directory %s\n" % output_dir)


#
# API
#

def sos2geojson(endpoint, file, feature_properties=offering_geojson_properties_default):
  """
  Converts an SOS endpoint to a GeoJSON layer and writes it to the given file
  Parameters:
    endpoint - SOS service endpoint
    file - file to write GeoJSON to
    feature_properties - function that takes an Offering object and returns 
                         a dictionary used for GeoJSON features properties 
  """
  response = urllib2.urlopen(util.add_query_params_v1(endpoint), timeout=60)
  xml = response.read()
  sos = SensorObservationService(None, xml=xml)
  # generate GeoJSON layer structure 
  layer = generate_geojson(sos.contents, feature_properties)
  # dump to JSON
  with open(file, "w") as f:
      f.write(json.dumps(layer, indent=4))

def main():
  process_services()
  
if __name__ == "__main__":
  main()
  
  
  