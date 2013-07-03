#!/usr/bin/env python
import unittest
import os

from owslib.sos import SensorObservationService
from sos2geojson import sos2geojson

class TestSOS2GeoJSON(unittest.TestCase):

  sos = None

  def setUp(self):
    """load example SOS Capabilities document"""
    file = os.path.join(os.path.dirname(__file__), "resources/ndbc-capabilities.xml")
    with open(file) as f:
      xml = f.read()
      self.sos = SensorObservationService(None, xml=xml)
    
  def test_count_offerings(self):
    """count sensor offerings"""
    self.assertEqual(len(self.sos.contents), 838)

  def test_count_geojson_features(self):
    """count generated GeoJSON features"""
    # generate GeoJSON layer structure 
    features = sos2geojson._features_from_offerings(self.sos.contents)
    self.assertEqual(len(features), 805)

if __name__ == "__main__":
  unittest.main()
  
  
  