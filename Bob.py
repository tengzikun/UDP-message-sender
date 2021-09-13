
#zikun a0199547h
from socket import *
import zlib
import sys

def incr(i):
    i = i + 1
    return i

portNumber = int(sys.argv[1])
socket= socket(AF_INET, SOCK_DGRAM)
socket.bind(('', portNumber))
receiveP = 0
corruptP = 0
lastSequence = -1 

while(True):
    try:
        packet, address= socket.recvfrom(64)
        receiveP = incr(receiveP)
        checksum = int.from_bytes(packet[0:4], byteorder = "big")
        seqNum = int.from_bytes(packet[4:8], byteorder = "big")
        length = len(packet) -1
        serversideChecksum = zlib.crc32(packet[8:length])
        package = packet[8:]
        serversideChecksum = zlib.crc32(packet[8:])
        if(checksum == serversideChecksum and (lastSequence != seqNum)):
            socket.sendto(b'ACK', address)
            lastSequence = seqNum
            sys.stdout.buffer.write(package)
            sys.stdout.buffer.flush()
          #  sys.stdout.buffer.close()
        elif(checksum == serversideChecksum and (lastSequence == seqNum)):
            socket.sendto(b'ACK', address)
        else:
            corruptP = incr(corruptP)
            socket.sendto(b"NAK", address)

    except ValueError:
        continue

    finally:
        writer = open('Bob.txt', 'w')
        writer.write(format(corruptP / receiveP, '.2f')) 
        writer.flush()
        writer.close()





