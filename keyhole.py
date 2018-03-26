import requests
import sys
import getopt
import time

host = 'localhost'
port = 5000
filepath = 'C:/Users/Mateo Juvera/Desktop/USBBackup/key.txt'

def unlock():
    url = "http://{0}:{1}/key/".format(host, port)
    print(url)
    r = requests.post(url, {})

try:
    opts, args = getopt.getopt(sys.argv[1:], "", ["host", "port"])
except getopt.GetoptError:
    print("Option Error")
    sys.exit()

for opt, arg in opts:
    if opt == '--host':
        host = str(arg)
    elif opt == '--port':
        port = int(arg)

while True:
    print('Checking...')
    try:
        with open(filepath, 'r') as file:
            print('fladoop')
            unlock()
            break
    except:
        time.sleep(1.5)

print('bai')
