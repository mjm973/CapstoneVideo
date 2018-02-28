from flask import Flask, render_template, request, url_for, jsonify, redirect, Response
import socket
from pythonosc import osc_message_builder, udp_client, osc_bundle_builder, osc_server, dispatcher

from cam import VideoCamera

app = Flask(__name__)

ip = 'localhost'
port = 4242

client = udp_client.UDPClient(ip, port)

bFeed = False

@app.route('/')
def root():
    jsUrl = url_for('static', filename='js/main.js')
    cssUrl = url_for('static', filename='css/main.css')

    return render_template('index.html', js=jsUrl, css=cssUrl)

@app.route('/fs/')
def fs():
    global bFeed
    #path ="C:\Users\Mateo Juvera\Desktop\USBBackup\key.txt"
    path = 'C:/Users/Mateo Juvera/Desktop/USBBackup/key.txt'

    jsUrl = url_for('static', filename='js/main.js')
    cssUrl = url_for('static', filename='css/main.css')

    res = []
    try:
        with open(path, 'r') as file:
            pass
        res = [True]
        bFeed = True
        #return render_template('index.html', js=jsUrl, css=cssUrl, msg='yay
    except:
        #return render_template('index.html', js=jsUrl, css=cssUrl, msg=':c')
        # res = [False]
        bFeed = False

    return jsonify([bFeed])
    # return jsonify(res)
    #return redirect('/')

def gen(cam):
    while True:
        frame = cam.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/feed/')
def cam_test():
    global bFeed
    if bFeed:
        return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return redirect('/')

@app.errorhandler(404)
def not_found(err):
    return redirect('/')
