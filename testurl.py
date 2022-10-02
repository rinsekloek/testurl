#!/usr/bin/python3
from csv import reader
import threading
import random
import socket
import time

def socket_timing(host,port,family):
    s = socket.socket(family, socket.SOCK_STREAM )
    s.settimeout(2.0)
    start = time.time()
    try:
      s.connect((host,port))
      s.close()
    except socket.error:
      return False
    return (time.time()-start)*1000

# function that loops through alexa top 1000 and tests ipv4 vs ipv6 latency
def testtop1000():
  # open file in read mode
  with open('top-1m.csv', 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    data = list(csv_reader)
    #random.shuffle(data)
    ip4pref=0
    ip6pref=0
    nodualstack=0
    rows=0
    nodiff=noipv4conn=noipv6conn=0
    limit = 100
    ip4faster=ip6faster=0

# Iterate over each row in the csv using reader objec
    for row in data:
        if (rows == limit): break
        rows+=1
        # row variable is a list that represents a row in csv
        hostname = row[1]
        # Only dual stack hosts
        try:
          ip =  socket.getaddrinfo(hostname,None, socket.AF_INET)[0][4][0]
          ip6 = socket.getaddrinfo(hostname, None, socket.AF_INET6)[0][4][0]
          #print(f"{ip} vs {ip6}")
        except:
            print(f"\033[91m {hostname} is no dual stack ")
            nodualstack+=1
            continue
        result   = socket_timing(ip,80,socket.AF_INET)
        result6  = socket_timing(ip6,80,socket.AF_INET6)
        if (result == False):
            noipv4conn+=1
            continue
        if (result6 == False):
            noipv6conn+=1
            continue

        if (result6 > result): 
            ip4pref+= 1
            ip4faster += (result6 - result)
            print(f"\033[92m {hostname} is ipv4 faster {(result6 - result)} ")
        elif (result >= result6): 
            ip6pref += 1
            ip6faster += (result - result6)
            print(f"\033[94m {hostname} is ipv6 faster {(result - result6)} ")
        else:
            nodiff += 1
    
    
    print(f"Hosts: {rows}") 
    print(f"Ipv4 fail {noipv4conn}")
    print(f"Ipv6 fail {noipv6conn}")
    print(f"IPv6 faster: {ip6pref}")
    print(f"IPv6 faster in time: {ip6faster}")
    print(f"IPv4 faster: {ip4pref}")
    print(f"IPv4 faster in time: {ip4faster}")
    print(f"No Dualstck: {nodualstack}")
    print(f"No Differ: {nodiff}")


if __name__ == "__main__":
    testtop1000()
