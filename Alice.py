#zikun a0199547h
from socket import *
import zlib
import sys

def incr(i):
    i = i + 1
    return i

    
serverName = ''
initialSequence = 0

corruptP = 0
receivedP = 0

portNum = int(sys.argv[1])
socket = socket(AF_INET, SOCK_DGRAM)
socket.settimeout(0.05)
sequenceNumber = 0

inputMessage = sys.stdin.buffer.read1(50)

while(len(inputMessage) != 0):
    checksum = zlib.crc32(inputMessage) & 0xffffffff
    checksum = checksum.to_bytes(4, byteorder = "big")
    sequenceNumber = initialSequence.to_bytes(4, byteorder = "big")
    inputMessage = checksum+ sequenceNumber + inputMessage

    while(True):
            try:
                socket.sendto(inputMessage,('localhost',portNum))
                response = socket.recvfrom(3)[0]   
                if(response == b"ACK"):
                    initialSequence = incr(initialSequence)
                    receivedP = incr(receivedP)
                    break
                elif(response != b"NAK"):
                    corruptP = incr(corruptP)
                    receivedP = incr(receivedP)
                else:
                    receivedP = incr(receivedP)       
            except timeout:
                continue
            finally:
                writer = open('Alice.txt', 'w')
                writer.write(format(corruptP / receivedP, '.2f')) 
                writer.flush()
                writer.close()
    inputMessage = sys.stdin.buffer.read(50)

                
                

       




