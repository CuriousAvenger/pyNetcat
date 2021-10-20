#!/usr/bin/python
from socket import *
import socket
import sys
import getopt

def usage():
    print('''
Usage:
    python netcat.py <options>

Options:
    -h, --help          Show help menu
    -s, --send          Send payload
    -i, --ip            Host's ip to connect
    -l, --listen        Start the listener
    -p, --port          Host's port to connect
    -c, --connect       Connect to the host
    -r, --receive       Receive incoming data
    -t, --start         Start communicating
''')

def main(argv):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create a socket handler
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) #Avoid the usage of reused ports


    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    #Get this pc's ip address
    
    try:
        opts, args = getopt.getopt(argv, 's:p:i:lhcrt', ['send=', 'port=', 'ip=', 'listener', 'help', 'connect', 'receive', 'start'])
    except Exception as e:
        print("Error: " +str(e).capitalize())
        usage()
        sys.exit(2)

    for opt, args in opts:        
        if opt in ('-s', '--send'):
            #In order to send, you first have to connect
            #So use -c first and then use this command
            sendPayload = args
            s.send(sendPayload.encode("UTF-8"))

        elif opt in ('-r', '--receive'):
            #Once you are connect you can send and recv
            #Any kind of acknowledgment from the host
            response = s.recv(4096)
            print(response.decode("UTF-8"))
            
        elif opt in ('-p', '--port'):
        	#The port you want to use
            givenPort = args 
        elif opt in ('-i', '--ip'):
        	#Host's ip you want to connect
            givenIP = args

        elif opt in ('-l', '--listener'):
            try:
                s.bind(('', int(givenPort)))
                print('[*] Listening on 0.0.0.0:' +str(givenPort))
                s.listen(1) #Start listening for one connection
                conn, addr = s.accept()#Accept connections
                print('[+] Connected: '+str(addr[0])+ ' Port: '+str(addr[1]))
                print(conn.recv(1024).decode("UTF-8"))
                while 1:
                	#Start communication
                    command = input(str(IPAddr)+': ')
                    conn.send(bytes(command, "UTF-8"))
                    data = conn.recv(1024).decode()
                    print("[" +str(addr[0])+ "]: " +data)
                    
            except KeyboardInterrupt:
                print('\nSession terminated using [ctrl-c]...')
                sys.exit(2)
            
        elif opt in ('-c', '--connect'):
            s.connect((givenIP, int(givenPort)))            

        elif opt in ('-t', '--start'):
            try:
                #This start an inital communication if
                #The host is also using the same netcat
                s.send(str.encode('[*] Connection Established!'))
                #Sending ack to the host, saying the above
                while 1:
                	#Start communication
                    data = s.recv(1024).decode("UTF-8")
                    print("["+givenIP+ "]: " +data)
                    command = input(str(IPAddr)+': ')
                    s.send(bytes(command,"UTF-8"))           

            except KeyboardInterrupt:
                print('\nSession terminated using [ctrl-c]...')
                sys.exit(2)
            
        elif opt in ('-h', '--help'):
            usage()
            sys.exit(2) 
        else:
            usage()
            sys.exit(2)

if __name__ == '__main__':
    main(sys.argv[1:])

