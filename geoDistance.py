# Shannon Stork
# EECS 325 Project 2

import socket
import time
import json
import urllib.request
import geoip2.database
from math import radians, fabs, sin, cos, tan, atan2, sqrt

class geoDistance:

    # This method computes the latitude and longistude coordinates given an IP address.
    def coordinates(self, host):
        hostip = socket.gethostbyname(host.strip())
        reader = geoip2.database.Reader('GeoLite2-City.mmdb')
        response = reader.city(host)
        lat = response.location.latitude
        lon = response.location.longitude
        return radians(lat), radians(lon)

    # This method was written with the assistance of various haversine articles on StackOverflow.
    # It computes the geographical distance between two hosts.
    def geodistance(self, host):
        hostip = socket.gethostbyname(host.strip())
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))
        localip = s.getsockname()[0]
        locallat, locallon = radians(41.5046068), radians(-81.60973509999997)
        hostlat, hostlon = self.coordinates(hostip)
        latchange = fabs(hostlat - locallat)
        lonchange = fabs(hostlon - locallon)
        # Haversine
        a = sin(latchange / 2) ** 2 + (cos(locallat) * cos(hostlat) * sin(lonchange / 2) ** 2)
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        # The distance is the result of the haversine formula times earth's radius.
        distance = 6371 * c
        print("Host = " + host)
        print("Geo distance = " + str(distance) + "km")

    # The following code is adapted from StackOverflow.
    def main(self):
        # Open the targets text file in read mode
        f = open('targets.txt', 'r')
        list = f.read().splitlines()
        # For every target
        for x in list:
            # measure the hops/ get info for that target
            self.geodistance(x)
        # Close the target file
        f.close()


measure = geoDistance()
if __name__ == "__main__": measure.main()