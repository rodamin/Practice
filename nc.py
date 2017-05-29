from socket import *
import sys
import socket
import getopt
import threading
import subprocess

listen = False
command =False
upload = False
excute = ''
target = ''
upload_destination= ''
port = 0

def usage():

    print "DSM Net Tool"
    print ""
    print "Usage: dsmnet.py -t target_host -p port"
    print "-l --listen ===listen on [host]:[port] for imcoming connections"
    print "-e --execute ===execute the given file upon receving a connection"
    print "-c --command ===imitialize a command shell"
    print "-u --upload=destination === upon receving connection upload a file and write to [destination]"

    print ""
    print ""

    print "Examples:"
    print "dsmnet.py -t 192.168.0.1 -p 9999 -l -c"
    print "echo 'ABCD' | ./dsmnet.py -t 192.168.0.1 -p 135"

    sys.exit(0)
def clinet_sender(buffer):
    client =socket(AF_INET,SOCK_STREAM)

    try:
        clinet.connect((target,port))
        if len(buffer):
            client.send(buffer)

        while True:
            recv_len =1
            response =""

            while recv_len:
                 data = client.recv(4096)
                 recv_len = len(data)

                 response += data

                 if recv_len <4096:
                     break
            print response,

            buffer =raw_input("")
            buffer += "\n"

            client.send(buffer)

    except:
        print "[*] Exception! Exiting"
        client.close()
def server_loop():

    global target_host
    if not len(target):
        target = "0.0.0.0"

    server = socket(AF_INET,SOCK_STREAM)
    server.bind((target,port))

    server.listen(5)

    while True:

        client_socket, addr=server.accept()

        client_thread=threading.Thread(target=client_handler, args= (client_socket,))
        client_thread.start()

def run_command():
    command = command.rstrip()
    try:
        output =subprocess.check_output(command, stderr = subprocess.STDOUT, shell=True)
    except:
        output = "Failed to execute command \r\n"

    return output

def client_handler(client_socket):

    global upload
    global execute
    global command

    if len(upload_destination):
        file_buffer = ""

        while True:
            data =client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer

        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer)
            file_descriptot.close()

            client_socket.send("Successfully saved file to %s \r\n" %upload_destination)

        except:
            client_socket.send("Fail to save file to %s \r\n" %upload_destination)
        if len(execute):
            output =run_command(execute)
            client_socket.send(output)
        if command:
            while True:
                client_socket.send("<DSM:#>")

                cmd_buffer = ""

                while "\n" not in cmd_buffer:
                    cmd_buff +=client_socket.recv(1024)

                    response =run_command(cmd_buffer)
                    client_socket.send(response)

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target_host

    if not len(sys.argv[1:]):
        usage()
    try:
        opts,args = getopt.getopt(sys.argv[1:], "hle:t:p:cu",["help","listen","execute","target","port","command","upload"])
    except getopt.GetoptError as err:

        print srt(err)
        usage()

    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e","--execute"):
            execute = a
        elif o in ("-c","--commandshell"):
            command =True
        elif o in ("-u","--upload"):
            upload_destination = a
        elif o in ("-t","--target"):
            target=a
        elif o in ("-p","--port"):
            port= int(a)
        else:
            assert False,"Unhandled Option!"

        if not listen and len(target) and port > 0:
            buffer = sys.stdin.read()
            clint_sender(buffer)

            if listen:
                server_loop()
if __name__ == '__main__':
    main()
