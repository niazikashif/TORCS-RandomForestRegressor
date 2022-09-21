import piskle
import sys
import argparse
import socket

import driver
import re

timeA = 0
loaded_model = piskle.load('Accel.pskl')
loaded_model1 = piskle.load('Brake.pskl')
loaded_model2 = piskle.load('Gear.pskl')
loaded_model3 = piskle.load('Steer.pskl')


def tokenizeAndConcat(data, buf):
    x=re.findall(r"\((.*?)\)",buf)
    for y in x:
        data+=",".join(re.findall("-?\d*\.?\d+",y))+","
    return data

if __name__ == '__main__':
    pass

# Configure the argument parser
parser = argparse.ArgumentParser(description = 'Python client to connect to the TORCS SCRC server.')

parser.add_argument('--host', action='store', dest='host_ip', default='localhost',
                    help='Host IP address (default: localhost)')
parser.add_argument('--port', action='store', type=int, dest='host_port', default=3001,
                    help='Host port number (default: 3001)')
parser.add_argument('--id', action='store', dest='id', default='SCR',
                    help='Bot ID (default: SCR)')
parser.add_argument('--maxEpisodes', action='store', dest='max_episodes', type=int, default=1,
                    help='Maximum number of learning episodes (default: 1)')
parser.add_argument('--maxSteps', action='store', dest='max_steps', type=int, default=0,
                    help='Maximum number of steps (default: 0)')
parser.add_argument('--track', action='store', dest='track', default=None,
                    help='Name of the track')
parser.add_argument('--stage', action='store', dest='stage', type=int, default=3,
                    help='Stage (0 - Warm-Up, 1 - Qualifying, 2 - Race, 3 - Unknown)')

arguments = parser.parse_args()

# Print summary
print('Connecting to server host ip:', arguments.host_ip, '@ port:', arguments.host_port)
print('Bot ID:', arguments.id)
print('Maximum episodes:', arguments.max_episodes)
print('Maximum steps:', arguments.max_steps)
print('Track:', arguments.track)
print('Stage:', arguments.stage)
print('*********************************************')

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error as msg:
    print('Could not make a socket.')
    sys.exit(-1)

# one second timeout
sock.settimeout(1.0)

shutdownClient = False
curEpisode = 0

verbose = False

d = driver.Driver(arguments.stage)

while not shutdownClient:
    while True:
        print('Sending id to server: ', arguments.id)
        buf = arguments.id + d.init()
        print('Sending init string to server:', buf)
        try:
            sock.sendto(buf.encode(), (arguments.host_ip, arguments.host_port))
        except socket.error as msg:
            print("Failed to send data...Exiting...")
            sys.exit(-1)
            
        try:
            buf, addr = sock.recvfrom(1000)
            print('Received data from server:', buf.decode())
            if buf.decode().find("***identified***") >= 0:
                break
        except socket.error as msg:
            print("didn't get response from server...")


    currentStep = 0
    
    while True:
        # wait for an answer from server
        buf = None
        try:
            buf, addr = sock.recvfrom(1000)
        except socket.error as msg:
            print("didn't get response from server...")
        
        if verbose:
            print('Received: ', buf)
        
        if buf != None and buf.decode().find('***shutdown***') >= 0:
            d.onShutDown()
            shutdownClient = True
            print('Client Shutdown')
            break
        
        if buf != None and buf.decode().find('***restart***') >= 0:
            d.onRestart()
            print('Client Restart')
            break
        
        currentStep += 1
        if currentStep != arguments.max_steps:
            if buf != None:
                tokenized = "" #making an empty string
                tokenized = tokenizeAndConcat(tokenized,buf.decode())  #tokeniziing the buf

                buf = d.drive(buf.decode())     # call the d.drive function
                tokenized = tokenizeAndConcat(tokenized, buf)  # tokenizing the data recieved from d.drive and concating
                ListA = tokenized.split(',')  # converting to a list
                print(ListA)
                #====================Removing all the unnecessary elements
                for i in range(12):
                    ListA.pop(-1)

                for i in range(7):
                    ListA.pop(1)

                for i in range(5):
                    ListA.pop(37)


                    # print(ListA)
                # for i in range(len(ListA)):
                #     if ListA[i]!='':
                #         ListA[i]=float(ListA[i])

                print(ListA)
                # making the list lenght 62
                while(len(ListA)>15):
                    ListA.pop(-1)

                print(ListA)


                #print(loaded_model4.predict([ListA])[0])
                # calling the setvalues with models
                d.setValues(loaded_model.predict([ListA])[0],loaded_model1.predict([ListA])[0],loaded_model2.predict([ListA])[0],loaded_model3.predict([ListA])[0])



        else:
            buf = '(meta 1)'
        
        if verbose:
            print('Sending: \n',buf)
        
        if buf != None:
            try:
                sock.sendto(buf.encode(), (arguments.host_ip, arguments.host_port))
            except socket.error as msg:
                print("Failed to send data...Exiting...")
                sys.exit(-1)
    
    curEpisode += 1
    
    if curEpisode == arguments.max_episodes:
        shutdownClient = True
        

sock.close()

