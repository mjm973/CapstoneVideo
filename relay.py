import sys
import getopt
from pythonosc import osc_message_builder, udp_client, osc_server, dispatcher
import serial
import threading
import glob

target_host = 'localhost'
target_port = 8888
my_port = 8080
isMac = False

try:
    opts, args = getopt.getopt(sys.argv[1:], "m", ["thost=", "tport=", "mport="])
except getopt.GetoptError:
    print("Option Error")
    sys.exit()

for opt, arg in opts:
    if opt == '--thost':
        target_host = str(arg)
    elif opt == '--tport':
        print (arg)
        target_port = int(arg)
    elif opt == '--mport':
        my_port = int(arg)
    elif opt == '-m':
        isMac = True

# serial setup
ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'COM8'

def find_port(mac):
    global ser
    print('Initializing serial...')
    if mac:
        ports = glob.glob("/dev/tty.*")
        for port in ports:
            ser.port = port
            try:
                ser.open()
                print('Bound to serial port {}'.format(ser.port))
                return
            except:
                print('Failed to open port {}, trying a new one...'.format(ser.port))
    else:
        for x in range(6, 13):
            ser.port = 'COM' + str(x)
            try:
                ser.open()
                print('Bound to serial port {}'.format(ser.port))
                return
            except:
                print('Failed to open port {}, trying a new one...'.format(ser.port))
    print('Failed to open serial port, only listening...')

def relay_message(derp, msg):
    global ser
    print('Relaying: {}'.format(msg))
    ser.write(msg)
    ser.flush()

# osc client setup
client = udp_client.SimpleUDPClient(target_host, target_port)

# osc server setup
disp = dispatcher.Dispatcher()
disp.map("/relay", relay_message)

server = osc_server.ThreadingOSCUDPServer(('localhost', my_port), disp)

print('Server now listening on port {}'.format(my_port))
s_thread = threading.Thread(target=server.serve_forever)
s_thread.start();

# print('Initializing serial...')
# try:
#     for x in range(6, 13):
#         ser.port = 'COM' + str(x)
#         try:
#             ser.open()
#             print('Bound to serial port {}'.format(ser.port))
#
#             while True:
#                 msg = ser.readline()
#                 if (msg is not ''):
#                     print('Sending: {}'.format(msg))
#                     client.send_message("/relay", msg)
#         except:
#             print('Failed to open port {}, trying a new one...'.format(ser.port))
#     print('Failed to open serial port, only listening...')
# except KeyboardInterrupt:
#     server.shutdown()
#     print('bai')

find_port(isMac)

try:
    while True:
        msg = ser.readline()
        if (msg is not ''):
            print('Sending: {}'.format(msg))
            client.send_message("/relay", msg)
except KeyboardInterrupt:
    server.shutdown()
    print('bai')
