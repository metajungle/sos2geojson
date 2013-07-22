#!/usr/bin/env python
import os
import sys
import types

from owslib.sos import SensorObservationService

import urllib2
import yaml
import json

from util import uri_pretty, bbox2geometry
from util import add_query_params_v1, name_for_filename

#
# INTERNAL
#

def _properties_default(offering, **kwargs):
    """
    Default function for constructing the 'properties'
    of a GeoJSON feature from a sensor offering
    """
    return { "Offering Id" : offering.id,
             "Description" : offering.description,
             "Observed properties" :
             [uri_pretty(p) for p in offering.observed_properties] }

def _properties_alt(offering, **kwargs):
    """
    Generates alternative GeoJSON feature 'properties'
    object from a sensor offering
    """
    prop = { "offering-id" : offering.id,
             "offering-name" : offering.name,
             "offering-description" : offering.description,
             "offering-properties" : offering.observed_properties,
             "offering-formats" : offering.response_formats }
    if offering.begin_position:
        prop["offering-start"] = str(offering.begin_position)
    if offering.end_position:
        prop["offering-end"] = str(offering.end_position)
    # make use of all the arguments 
    for key, value in kwargs.iteritems():
        prop[key] = value
    return prop

def _features_from_offerings(offerings, p_fn=_properties_default, extra=None):
    """
    Collects features from a sensor offering list
    Parameters:
        offerings - array of sensor Offerings
        p_fn - function that takes an Offering object and returns
               a dictionary used for GeoJSON features properties
        extra - dictionary to extend the GeoJSON feature properties dictionary
    """
    if extra is None:
        extra = {}
    features = []
    for key in offerings.keys():
        offering = offerings[key]
        # for now, only consider offerings with 'proper' bbox
        bbox = bbox2geometry(offering.bbox)
        if bbox != None:
            features.append({
                "type" : "Feature",
                "geometry" : bbox,
                "properties": p_fn(offering, **extra)
            })
        else:
            print("Skipping %s - not a point" % offering.id)
    return features

def _features_from_endpoint(endpoint, p_fn=_properties_default, extra=None):
    """
    Generates a GeoJSON feature collection from an SOS endpoint
    Parameters:
        endpoint - SOS service endpoint
        p_fn - function that takes an Offering object and returns
               a dictionary used for GeoJSON features properties
        extra - dictionary to extend the GeoJSON feature properties dictionary
    """
    if extra is None:
        extra = {}
    # make endpoint available
    extra["service-endpoint"] = endpoint 
    response = urllib2.urlopen(add_query_params_v1(endpoint), timeout=60)
    xml = response.read()
    sos = SensorObservationService(None, xml=xml)
    try:
        title = sos.identification.title
        # make title available
        extra["service-title"] = title
    except AttributeError:
        title = None
    return title, _features_from_offerings(sos.contents, p_fn, extra)

def _feature_collection_from_features(features):
    """
    Returns a feature collection from the given set of features
    """
    layer = {
        "type": "FeatureCollection",
        "features": features
    }
    return layer

def _process_sos_endpoint(endpoint, output_dir, idx=0, filename=None):
    """
    Processes a single SOS endpoint and writes to file 
    """
    title, features = _features_from_endpoint(endpoint)
    collection = _feature_collection_from_features(features)
    # create a GeoJSON layer filename
    if filename is None:
        if title is None:
            filename = "sos-layer%s.geojson" % idx
        else:
            filename = "%s.geojson" % name_for_filename(title)
    else:
        if filename.rfind(".geojson") == -1:
            filename = "%s.geojson" % filename
    # dump to JSON
    with open(os.path.join(output_dir, filename), "w") as f:
        # pretty print by default 
        f.write(json.dumps(collection, indent=4))

def _create_layer_output_dir(rootdir):
    """
    Creates the output directory for the GeoJSON layers
    """
    if not os.path.exists(rootdir):
        try:
            os.makedirs(rootdir)
        except OSError:
            sys.stderr.write("Could not create root output " + 
                             "directory, aborting\n")
            return None
    return True

def _parse_yaml(yaml_filename):
    """
    Parses the YAML configuration file and returns a list of triples 
    containing ("endpoint", "output_folder", "filename")
    """
    try:
        with open(yaml_filename) as file_yaml:
            services = yaml.load(file_yaml)
            endpoints = []
            for (idx, folder) in enumerate(services.keys()):
                for endpoint_info in services[folder]:
                    filename = None
                    # check if the service endpoint comes with a name to use
                    if isinstance(endpoint_info, types.DictType):
                        endpoint = endpoint_info.keys()[0]
                        filename = endpoint_info[endpoint]
                    else:
                        endpoint = endpoint_info
                    # collect endpoints 
                    val = (endpoint, folder, filename)
                    endpoints.append((endpoint, folder, filename))
            return endpoints
    except IOError:
        sys.stderr.write("Could not find configuration file: %s\n" % 
                         yaml_filename)
    return None

def _process_services_from_yaml(rootdir, yaml_filename):
    """
    Processes all SOS services given in configuration file
    Parameters:
        rootdir - root output directory 
        yaml_filename - configuration file in YAML
    """
    endpoint_data = _parse_yaml(yaml_filename)
    if endpoint_data is None:
        return 
        
    if not _create_layer_output_dir(rootdir):
        return

    for (idx, _endpoint) in enumerate(endpoint_data): 
        endpoint, folder, filename = _endpoint
        try:
            output_dir = os.path.join(rootdir, folder)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            # process endpoint 
            _process_sos_endpoint(endpoint, output_dir, 
                                  idx, filename)
        except OSError:
            sys.stderr.write("Could not create output directory %s\n" % 
                             output_dir)


def _process_all_services_from_yaml(yaml_filename, p_fn=_properties_default, pretty=False):
    """
    Processes all SOS services given in configuration file
    Parameters:
        rootdir - root output directory 
        yaml_filename - configuration file in YAML
        p_fn - function that takes an Offering object and returns
               a dictionary used for GeoJSON features properties
        pretty - true if pretty print, false if minified
    """
    endpoint_data = _parse_yaml(yaml_filename)
    if endpoint_data is None:
        return 
        
    features = []
    for (idx, _endpoint) in enumerate(endpoint_data): 
        endpoint, _folder, _filename = _endpoint
        # collect features from all endpoints 
        _title, fs = _features_from_endpoint(endpoint, p_fn)
        features.extend(fs)

    # create feature collection for all features 
    collection = _feature_collection_from_features(features)
    if pretty:
        return json.dumps(collection, indent=4)
    return json.dumps(collection, separators=(',',':'))


#
# PUBLIC
#

def process_from_yaml(rootdir, yaml_filename):
    """
    Processes all SOS services given in configuration file
    Parameters:
        rootdir - root output directory 
        yaml_filename - configuration filename in YAML
    """
    _process_services_from_yaml(rootdir, yaml_filename)

def process_all_from_yaml(rootdir, out_filename, yaml_filename):
    """
    Processes all services into a single GeoJSON file
    """
    if not _create_layer_output_dir(rootdir):
        return
    
    geojson = _process_all_services_from_yaml(yaml_filename, p_fn=_properties_alt)
    try:
        with open(os.path.join(rootdir, out_filename), "w") as f:
            # pretty print by default 
            f.write(geojson)
    except IOError:
        sys.stderr.write("Could not write file: %s\n" % 
                         out_filename)

def sos2geojson(endpoints, p_fn=_properties_default, extra=None, pretty=False):
    """
    Generates a GeoJSON feature collection from an SOS endpoint
    Parameters:
        endpoints - list SOS service endpoints, or a single endpoint
        p_fn - function that takes an Offering object and returns
               a dictionary used for GeoJSON features properties
        extra - dictionary to extend the GeoJSON feature properties dictionary
        pretty - true if pretty print, false if minified
    """
    if extra is None:
        extra = {}
    features = []
    if isinstance(endpoints, types.ListType):
        for endpoint in endpoints:
            _title, fs = _features_from_endpoint(endpoint, p_fn, extra)
            features.extend(fs)
    elif isinstance(endpoints, basestring):
        _title, fs = _features_from_endpoint(endpoints, p_fn, extra)
        features.extend(fs)
    collection = _feature_collection_from_features(features)
    if pretty:
        return json.dumps(collection, indent=4)
    return json.dumps(collection, separators=(',',':'))
  