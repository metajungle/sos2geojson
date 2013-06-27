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

def collect_features(offerings):
  """collects features from a sensor offering list"""
  features = []
  for key in offerings.keys():
    offering = offerings[key]
    # for now, only consider offerings with 'proper' bbox
    bbox = util.bbox2geometry(offering.bbox)
    if bbox != None:
      features.append({
        "type" : "Feature", 
        "geometry" : bbox, 
        "properties": {
          "Offering Id" : offering.id, 
          "Description" : offering.description, 
          "Observed properties" : [util.uri_pretty(p) for p in offering.observed_properties] 
        }
      })
    else:
      print "Skipping %s" % offering.id
  return features

def generate_geojson(offerings):
  """generates GeoJSON from a sensor offering list"""
  layer = {
      "type": "FeatureCollection",
      "features": collect_features(offerings) 
  }
  return layer

def process_sos_endpoint(endpoint, output_dir, idx):
  """processes a single SOS endpoint"""
  response = urllib2.urlopen(util.add_query_params_v1(endpoint), timeout=60)
  xml = response.read()
  sos = SensorObservationService(None, xml=xml)
  # generate GeoJSON layer structure 
  layer = generate_geojson(sos.contents)
  # create a GeoJSON layer filename
  try:
    filename = "%s.geojson" % util.name_for_filename(sos.identification.title)
  except AttributeError:
    # provide a name if we cannot find one 
    filename = "sos-layer%s.geojson" % idx
  # dump to JSON
  with open(os.path.join(output_dir, filename), "w") as f:
      f.write(json.dumps(layer, indent=4))

def process_services():
  """processes all SOS services given in configuration file"""
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
        for endpoint in services[folder]:
          process_sos_endpoint(endpoint, output_dir, idx)
      except OSError:
        sys.stderr.write("Could not create output directory %s\n" % output_dir)


def main():
  process_services()
  
if __name__ == "__main__":
  main()
  
  
  