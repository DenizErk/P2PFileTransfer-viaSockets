import socket
import json
from datetime import datetime

# 2.2.0-A
serverPort = 5001

# Create a UDP socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
serverSocket.bind(('', serverPort))
print("The server is ready to receive")
print("")
chunks = {}
hostedContents = {}

while 1:

    message, clientAddress = serverSocket.recvfrom(2048)
    #print('received {} bytes from {}'.format(len(message), clientAddress))
    #print('"{}" : {}'.format(clientAddress, message.decode("utf-8")))

    # 2.2.0-B

    decoded_Message = message.decode("utf-8")

    t = datetime.now()
    current_time = t.strftime("%H:%M:%S")

    temp_eval = eval(decoded_Message)
    json_dump = json.dumps(temp_eval)
    json_object = json.loads(json_dump)

    index = 0
    print(
        clientAddress[0], ": The following chunks were announced from this ip address. (" + current_time + ")")

    while index < len(json_object['chunks']):
        temp_chunk_name = json_object['chunks'][index]
        print(temp_chunk_name + " ", end='')
        hostedContents.setdefault(clientAddress[0], []).append(temp_chunk_name)

        if (temp_chunk_name in chunks):
            if (clientAddress[0] in chunks[temp_chunk_name]):
                pass
            else:
                chunks[temp_chunk_name].append(clientAddress[0])

        else:
            chunks[temp_chunk_name] = [clientAddress[0]]

        index += 1

    f = open("Content_Dictionary.txt", "w")
    json.dump(chunks, f)
    f.close()
    print("")
    print("")

serverSocket.close()
