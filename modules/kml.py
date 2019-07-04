#!/usr/bin/env python3
# kml.py
# - returns KML string that draws the specified geohash or coordinate.
# KML (Keyhole Markup Language):
# https://developers.google.com/kml/
#

if __name__ == "__main__":
    from codec import decode_to_range
else:
    from .codec import decode_to_range

# kml_from_latlngs()
def kml_from_latlngs(latlng0, latlng1, title='title'):
    (lat0, lng0) = latlng0
    (lat1, lng1) = latlng1
    return (
        '<?xml version="1.0" encoding="UTF-8"?>' +
        '<kml xmlns="http://www.opengis.net/kml/2.2">' +
          '<Placemark>' +
            '<name>%s</name>' % (title) +
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
          '</Placemark>' +
        '</kml>')

# kml_from_geohash()
def kml_from_geohash(geohash, title='title'):
    ((lat0, lat1), (lng0, lng1)) = decode_to_range(geohash)
    return kml_from_latlngs((lat0, lng0), (lat1, lng1), title)

if __name__ == "__main__":
    print(kml_from_latlngs((35.123, 135.123), (35.124, 135.124)))
