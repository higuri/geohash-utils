#!/usr/bin/env python3
# kml.py
# - returns KML string that draws the specified geohash or coordinate.
# KML (Keyhole Markup Language):
# https://developers.google.com/kml/
#

from .codec import decode_to_range

# from_latlngs()
def from_latlngs(regions, title='KML Document'):
    retval = (
        '<?xml version="1.0" encoding="UTF-8"?>' +
        '<kml xmlns="http://www.opengis.net/kml/2.2">' +
        '<Document><name>%s</name>'
    )
    for (i, region) in enumerate(regions):
        # TODO: error check
        (lat0, lng0) = region[0]
        (lat1, lng1) = region[1]
        retval += (
          '<Placemark>' +
            '<name>%d</name>' % (i + 1) +
            '<Polygon>' +
              '<outerBoundaryIs>' +
                '<LinearRing>' +
                  '<coordinates>' +
                    '%f,%f ' % (lng0, lat0)  +
                    '%f,%f ' % (lng1, lat0)  +
                    '%f,%f ' % (lng1, lat1)  +
                    '%f,%f ' % (lng0, lat1)  +
                    '%f,%f ' % (lng0, lat0)  +
                  '</coordinates>' +
                '</LinearRing>' +
              '</outerBoundaryIs>' +
            '</Polygon>' +
          '</Placemark>')
    retval += '</Document></kml>'
    return retval

# from_geohash()
def from_geohash(geohashes, title='KML Document'):
    regions = []
    for geohash in geohashes:
        ((lat0, lat1), (lng0, lng1)) = decode_to_range(geohash)
        regions.append(((lat0, lng0), (lat1, lng1)))
    return from_latlngs(regions, title)
