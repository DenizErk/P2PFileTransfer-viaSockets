import socket
import os
import math
import time
import json

serverIP = '25.255.255.255'
serverPort = 5001
server_address = (serverIP, serverPort)

# Create a UDP socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Calculates size of chunks

content_name = input('Enter a file name :')

filename = content_name+'.png'
c = os.path.getsize(filename)
# print(c)
CHUNK_SIZE = math.ceil(math.ceil(c)/5)
# print(CHUNK_SIZE)


# Seperates the file to chunks
index = 1
with open(filename, 'rb') as infile:
    chunk = infile.read(int(CHUNK_SIZE))
    while chunk:
        chunkname = content_name+'_'+str(index)+'.png'
        print("chunk name is: " + chunkname + "\n")
        with open(chunkname, 'wb+') as chunk_file:
            chunk_file.write(chunk)
            index += 1
            chunk = infile.read(int(CHUNK_SIZE))
            chunk_file.close()

chunknames = [content_name+'_1',
              content_name+'_2', content_name+'_3',
              content_name+'_4', content_name+'_5']

chunk_set = {'chunks': [chunknames[0], chunknames[1],
                        chunknames[2], chunknames[3], chunknames[4]]}


# Broadcasts all chunks every 60 seconds
while True:

    with open('Announced_Chunks.txt', 'r') as infile:
        for line in infile:
            for word in line.split():
                chunk_set['chunks'].append(word)
    infile.close()

    json_dump = json.dumps(chunk_set)
    json_object = json.loads(json_dump)
    clientSocket.sendto(json_dump.encode("utf-8"), server_address)

    chunk_set = {'chunks': [chunknames[0], chunknames[1],
                            chunknames[2], chunknames[3], chunknames[4]]}

    time.sleep(10)

clientSocket.close()
