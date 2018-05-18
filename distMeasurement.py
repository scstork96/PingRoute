# Shannon Stork
# EECS 325 Project 2

import socket
import time
import json
import urllib.request
from math import radians, fabs, sin, cos, tan, atan2, sqrt

class distMeasurement:

    # This method sends out a probe and computes the RTT and number of hops.
    def compute(self, hostip, hostname):
        # The following code was adapted from github user wbw20.
        # Initializes sockets on the local host to get data to and from the destination host.
        icmp = socket.getprotobyname("icmp")
        udp = socket.getprotobyname("udp")
        receive = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
        port = 33434
        ttl = 32
        # Modifies the fields of the sending socket, bind the receiving socket, and set the timeout.
        send.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        receive.settimeout(ttl)
        msg = "measurement for class project. questions to student abc123@case.edu or professor mxr136@case.edu"
        payload = bytes(msg + 'a' * (1472 - len(msg)), 'ascii')
        # Used to calculate rtt.
        start = time.time()
        end = time.time()
        # Sends a UDP probe to the destination and waits for a response.
        send.sendto(payload, (hostname.strip(), port))
        address = None
        name = None
        try:
            # Attempts to read icmp response.
            data, address = receive.recvfrom(2048)
            end = time.time()
            address = address[0]
            try:
                name = socket.gethostbyaddr(address)[0]
            except socket.error:
                name = address
        except socket.error:
            pass
        finally:
            send.close()
            receive.close()
        # The following code was adapted from github user SWhelan.
        # From the format of the header, we know that byte 20 is 3 for destination unreachable,
        # byte 21 is 3 for port unreachable, and byte 36 is the ttl.
        destinationStatus = (data[20])
        portStatus = (data[21])
        newttl = (data[36])
        # Error handling (adapted from SWhelan):
        response_source_ip = socket.inet_ntoa(data[40:44])
        response_destination_ip = socket.inet_ntoa(data[44:48])
        icmp_source_ip = socket.inet_ntoa(data[12:16])
        icmp_destination_ip = socket.inet_ntoa(data[16:20])
        destination_ip = hostip
        if (
                # The message is not ICMP destination / port unreachable
                destinationStatus != 3 or portStatus != 3 or
                # The destination IP on the IPv4 packet within the ICMP does not match the destination
                response_destination_ip != destination_ip or
                # The source IP on the ICMP packet is not the destination
                icmp_source_ip != destination_ip
        ):
            print("An error occurred sending an ICMP message to " + hostname + ".")
        hops = ttl - newttl
        rtt = (end - start) * 1000
        responseLength = len(data) - 48
        return hops, rtt, responseLength

    #This method computes all values for a host.
    def computehost(self, host):
        # Initializes the host and computes variable values.
        hostip = socket.gethostbyname(host.strip())
        hops, rtt, numbytes = self.compute(hostip, host)
        # Generates the output
        print("Host = " + host)
        print("Hop count = " + str(hops) + " hops")
        print(str(numbytes) + " bytes in the ICMP error message")
        print("RTT = " + str(rtt) + " ms")

    # The following code is adapted from StackOverflow.
    def main(self):
        # Open the targets text file in read mode
        f = open('targets.txt', 'r')
        list = f.read().splitlines()
        # For every target
        for x in list:
            # measure the hops/ get info for that target
            self.computehost(x)
        # Close the target file
        f.close()


measure = distMeasurement()
if __name__ == "__main__": measure.main()
