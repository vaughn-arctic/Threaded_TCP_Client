import argparse
import socket
from socket import *
import threading
from deconstructpacket import *
from trivialftp import *


parser = argparse.ArgumentParser(description='Processes input for TFTP')
parser.add_argument('-sp', "--serverport", required=True, type=int, help='Server port number for your desired connection')
args = parser.parse_args()
if args.serverport < 5000 or args.serverport > 65535:
    print("Port range is restricted to between 5000 and 65535, inclusive \n" + "Please try again")
    exit()

main_Socket = socket(AF_INET, SOCK_DGRAM)
main_Socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
main_Socket.bind(("", args.serverport))
print("Main socket ready to receive")

threads = list()

if __name__ == '__main__':
    while True:
        while True:
            try:
                main_Socket.settimeout(5)
                message, clientAddress = main_Socket.recvfrom(2048)
                break
            except:
                print("Listening for clients")

        if message[1] == 1:  # Read request, go into write mode
            print("RRQ received, creating thread")
            filename = unpack_RRQ_WRQ(message)

            # Create thread to handle client file transfer, pass filename and socket
            x = threading.Thread(target=write_mode, args=(clientAddress, args.serverport, filename),
                                            daemon=True)
            x.start()
            threads.append(x)



        elif message[1] == 2:  # Write request, go into read mode
            print("WRQ received, creating thread")
            filename = unpack_RRQ_WRQ(message)

            x = threading.Thread(target=read_mode, args=(clientAddress, args.serverport, filename),
                                            daemon=True)
            x.start()
            threads.append(x)

        elif message[1] == 5:  # Error code received
            print("Received error code, shutting down")
            break

        elif message[1] == 4:  # Received ack
            print("Received ack in main socket from client: ", clientAddress)

        else:  # Received packet of unexpected type
            pass
            # print("Received packet of unexpected type: ", message[1], " ", clientAddress)
    main_Socket.close()
    exit()
