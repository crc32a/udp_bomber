#!/usr/bin/env python

import binascii
import hashlib
import socket
import hmac
import uuid
import json
import zlib
import time
import sys

hash_algo = hashlib.sha256
hash_len = 32
nPackets = 100

def printf(format,*args): sys.stdout.write(format%args)

def encode_obj(obj):
    json_bytes = json.dumps(obj).encode('utf-8')
    binary_array = zlib.compress(json_bytes, 9)
    return binary_array

def wrap_envelope(obj, key):
    payload = encode_obj(obj)
    hmc = get_hmac(payload, key)
    envelope = payload + hmc
    return envelope

def get_hmac(payload, key):
    hmc = hmac.new(key.encode("utf-8"), payload, hashlib.sha256)
    return hmc.digest()

(ip,port) = ("192.168.3.48",5555)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

uuids = []
for i in xrange(0,nPackets):
    uuids.append(str(uuid.uuid4()))

pkt_counter  = 0
while True:
    for uuid in uuids:
        if pkt_counter % 1000 == 0:
            printf("sent %d packets\n", pkt_counter)
        obj = {"id": uuid, "seq": pkt_counter}
        pkt = wrap_envelope(obj,"testkey")
        pkt_counter += 1
        len = sock.sendto(pkt, (ip,port))
    time.sleep(1.0)

