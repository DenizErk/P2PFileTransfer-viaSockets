import socket
import json
from datetime import datetime

serverPort = 8000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The server is ready to receive')
print('')

while 1:
    connectionSocket, addr = serverSocket.accept()

    sentence = connectionSocket.recv(1024)

    t = datetime.now()
    current_time = t.strftime("%H:%M:%S")

    #json_object = json.loads(sentence.decode())

    decoded_message = sentence.decode()

    temp_eval = eval(decoded_message)
    json_dump = json.dumps(temp_eval)
    json_object = json.loads(json_dump)

    with open(json_object['requested_content']+'.png', 'rb+') as infile:
        sending_item = infile.read()

    infile.close()

    connectionSocket.send(sending_item)

    with open('uploader_log.txt', 'a') as logtxt:
        temp_log_text = json_object['requested_content']+'.png, to ' + \
            str(addr[0]) + ' ip address.(' + current_time + ')'
        logtxt.write(temp_log_text + '\n')
        print(temp_log_text)

    connectionSocket.close()
