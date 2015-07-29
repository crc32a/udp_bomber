import hashlib
import hmac
import json
import socket
import six
import sys
import time
import uuid
import zlib


hash_algo = hashlib.sha256
hash_len = 32

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


def usage(prog):
    print("usage is {0} <ip> <port> <n_pkts_per_sec>\n".format(prog))
    print("")



if __name__ == "__main__":

    if len(sys.argv) < 4:
        usage(sys.argv[0])
        sys.exit()

    (ip, port) = (sys.argv[1], int(sys.argv[2]))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    uuids = []
    pkts_per_second = int(sys.argv[3])

    for i in six.moves.xrange(0,pkts_per_second):
        uuids.append(str(uuid.uuid4()))

    pkt_counter = 0
    while True:
        for uuid in uuids:
            if pkt_counter % 1000 == 0:
                print("sent {0} packets".format(pkt_counter))
            obj = {"id": uuid, "seq": pkt_counter}
            pkt = wrap_envelope(obj, "testkey")
            pkt_counter += 1
            len = sock.sendto(pkt, (ip, port))
        time.sleep(1.0)

