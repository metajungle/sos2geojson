#!/usr/bin/env python
import unittest

from sos2geojson import util 

class TestUtil(unittest.TestCase):

  def test_name_pretty(self):
    name = util.name_pretty('first_next_third')
    self.assertEqual(name, 'First Next Third')
    
  def test_name_for_filename(self):
    name = util.name_for_filename('This Is My Title')
    self.assertEqual(name, 'this-is-my-title')
    
  def test_uri_pretty(self):
    uri = util.uri_pretty('http://mmisw.org/ont/cf/parameter/air_temperature')
    self.assertEqual(uri, 'Air Temperature')
    uri = util.uri_pretty('http://mmisw.org/ont/cf/parameter/air_pressure_at_sea_level')
    self.assertEqual(uri, 'Air Pressure At Sea Level')
    uri = util.uri_pretty('http://mmisw.org/ont/cf/parameter/sea_water_electrical_conductivity')
    self.assertEqual(uri, 'Sea Water Electrical Conductivity')
    uri = util.uri_pretty('http://mmisw.org/ont/cf/parameter/currents')
    self.assertEqual(uri, 'Currents')
    uri = util.uri_pretty('http://mmisw.org/ont/cf/parameter/sea_water_salinity')
    self.assertEqual(uri, 'Sea Water Salinity')
    uri = util.uri_pretty('http://mmisw.org/ont/cf/parameter/sea_floor_depth_below_sea_surface')
    self.assertEqual(uri, 'Sea Floor Depth Below Sea Surface')
    uri = util.uri_pretty('http://mmisw.org/ont/cf/parameter/sea_water_temperature')
    self.assertEqual(uri, 'Sea Water Temperature')
    uri = util.uri_pretty('http://mmisw.org/ont/cf/parameter/waves')
    self.assertEqual(uri, 'Waves')
    uri = util.uri_pretty('http://mmisw.org/ont/cf/parameter/winds')
    self.assertEqual(uri, 'Winds')
    
    uri = util.uri_pretty('urn:ogc:def:phenomenon:mmisw.org:cf:wind_speed')
    self.assertEqual(uri, 'Wind Speed')
    uri = util.uri_pretty('urn:ogc:def:phenomenon:mmisw.org:cf:wind_from_direction')
    self.assertEqual(uri, 'Wind From Direction')
    uri = util.uri_pretty('urn:ogc:def:phenomenon:mmisw.org:cf:air_temperature')
    self.assertEqual(uri, 'Air Temperature')
    
if __name__ == "__main__":
  unittest.main()
  
  
  