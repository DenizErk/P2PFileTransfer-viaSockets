import socket
import json
from datetime import datetime

serverIP = '25.255.255.255'
serverPort = 8000
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


while 1:

    will_announce = {"Announced_Chunks": []}

    with open('Announced_Chunks.txt', 'r') as infile:
        for line in infile:
            for word in line.split():
                will_announce['Announced_Chunks'].append(word)
    infile.close()

    req_message = input('Name of file to download : ')

    chunknames = [req_message+'_1',
                  req_message+'_2', req_message+'_3',
                  req_message+'_4', req_message+'_5']

    Successful_Download = True
    i = 0
    j = 0

    while i < 5:
        temp_chunk_info = bytearray()
        with open('Content_Dictionary.txt', 'r') as infile:
            all_message = infile.read()

            temp_eval = eval(all_message)

            json_dump = json.dumps(temp_eval)
            json_object = json.loads(json_dump)

            temp_chunks_json = {'requested_content':  chunknames[i]}
            temp_chunks_json2 = json.dumps(
                {'requested_content':  chunknames[i]})
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                clientSocket.connect(
                    (json_object[chunknames[i]][j], serverPort))
                # print("Bağlantı Sağlandı")
                clientSocket.send(temp_chunks_json2.encode())
                # print("test1")
                while True:

                    bytesRead = clientSocket.recv(1024)
                    # print(len(bytesRead))
                    if len(bytesRead) <= 0:
                        break
                    temp_chunk_info += bytesRead

                with open(chunknames[i] + '.png', 'wb+') as outfile:
                    outfile.write(temp_chunk_info)
                outfile.close()
                clientSocket.close()
                t = datetime.now()
            except:
                pass

            try:
                with open(chunknames[i] + '.png', 'r') as test_success:

                    test_success.close()
                    Successful_Download = True
            except:
                Successful_Download = False

            if Successful_Download == True:
                print(chunknames[i], ' downloaded from ',
                      json_object[chunknames[i]][j] + " ip address .( Successful )")

                current_time = t.strftime("%H:%M:%S")

                with open('downloader_log.txt', 'a') as logtxt:
                    temp_log_text = chunknames[i] + '.png, from ' + \
                        str(json_object[chunknames[i]][j]) + \
                        ' ip address.(' + current_time + ')'
                    logtxt.write(temp_log_text + '\n')

                with open('Announced_Chunks.txt', 'a+') as announced_chunks:
                    if(chunknames[i] in will_announce['Announced_Chunks']):
                        pass
                    else:
                        announced_chunks.write(chunknames[i]+' ')

            else:
                print(chunknames[i], ':',
                      "( Couldn't be downloaded from " + json_object[chunknames[i]][j] + "! Retrying from another peer )")

                if j <= len(json_object[chunknames[i]])-1:
                    j += 1
                    if j < len(json_object[chunknames[i]]):
                        i -= 1
                    else:
                        j = 0
                        print(
                            'CHUNK "' + chunknames[i] + '" CANNOT BE DOWNLOADED FROM ONLINE PEERS')

        i += 1
        infile.close()

    print('')
    try:
        for chunk in chunknames:
            with open(chunk + '.png', 'rb') as infile:
                infile.close()

        with open(req_message + '.png', 'wb') as outfile:
            for chunk in chunknames:
                with open(chunk + '.png', 'rb') as infile:
                    outfile.write(infile.read())
                infile.close()

        print("Download successful.")

    except:
        print("Chunks of the file to be download are not complete.")
    try:
        announced_chunks.close()
    except:
        pass
