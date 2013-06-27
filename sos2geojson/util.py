import os

import geojson
import json

from urlparse import urlparse

def add_query_params_v1(endpoint):
  """adds SOS v1.0.0 query parameters"""
  return endpoint + "?service=SOS&request=GetCapabilities&version=1.0.0"

def bbox2geometry(bbox):
  """returns GeoJSON geometry object representing the bounding box"""
  assert len(bbox) == 4
  minx = float(bbox[0])
  miny = float(bbox[1])
  maxx = float(bbox[2])
  maxy = float(bbox[3])
  if minx == maxx and miny == maxy:
    # create geometry, encode in GeoJSON, decode into object so
    # it can be included in the larger GeoJSON being generated 
    return json.loads(geojson.dumps(geojson.Point([minx, miny])))
  return None

def name_pretty(name):
  return name.replace('_', ' ').title()

def name_for_filename(name):
  """returns a substitute name suitable for a filename"""
  return name.lower().replace(' ', '-')

def uri_pretty(uri):
  """tries to provide a 'pretty' name for a URI"""
  o = urlparse(uri)
  if o.scheme == 'http':
    if o.fragment != '':
      return name_pretty(o.fragment)
    try:
      path = o.path
      return name_pretty(path[path.rindex('/') + 1:]) 
    except ValueError:
      pass
  elif o.scheme == 'urn':
    try:
      path = o.path
      return name_pretty(path[path.rindex(':') + 1:])
    except ValueError:
      pass
  return property

  
  
  