from flask import Flask, render_template, request, url_for, jsonify, redirect, Response
from cam import VideoCamera
from setInterval import setInterval
import requests
import json
import sys

app = Flask(__name__)

targetAddress = 'localhost'
targetPort = 5050
password = 123

bPassLocked = True
bLockLocked = True

### ROUTES ###

# root route: shows the video feed if unlocked, otherwise redirects to /locked/
@app.route('/')
def root():
    global bPassLocked
    global bLockLocked

    if redirectLocked():
        return redirect('/locked/')

    return videoFeed(VideoCamera())

# locked route: expects key first, then password
@app.route('/locked/')
def locked():
    if redirectUnlocked():
        return redirect('/')

    jsUrl = url_for('static', filename='js/main.js')
    cssUrl = url_for('static', filename='css/main.css')
    pUrl = url_for('static', filename='svg/phoenix_mono.svg')
    wUrl = url_for('static', filename='svg/wyvern_mono.svg')

    msg = makeMessage()
    mClass, pClass = makeClasses()

    return render_template('index.html', js=jsUrl, css=cssUrl, phoenix=pUrl, msg=msg, mClass=mClass, pClass=pClass)

# api route to receive and check password
@app.route('/pass/', methods=['POST'])
def password():
    global bPassLocked;

    print('Method: {0} || Data: {1}'.format(request.method, request.form))

    form = request.form;
    passString = form['r'] + form['g'] + form['b']

    print("{0} == {1}".format(passString, password))
    if int(passString) == password:
        bPassLocked = False

    return redirect('/')

# api route to receive confirmation that the key has been insterted
@app.route('/key/', methods=['POST'])
def key():
    global bLockLocked

    bLockLocked = False
    print("Key received!")

    return jsonify({
        'status': "ok",
        'msg': "key received",
        'value': bLockLocked,
        'success': True
    })

@app.route('/feed/')
def cam_test():
    global bFeed
    if bFeed:
        return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return redirect('/')

# all other routes should redirect to /
@app.errorhandler(404)
def not_found(err):
    return redirect('/')

### HELPERS ###

# camera sorcery
def gen(cam):
    try:
        while True:
            frame = cam.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    except KeyboardInterrupt:
        print('bai!')
        sys.exit()

# wrapper for camera sorcery
def videoFeed(cam):
    return Response(gen(cam), mimetype='multipart/x-mixed-replace; boundary=frame')

# utility to redirect when locked
def redirectLocked():
    global bLockLocked
    global bPassLocked

    if bLockLocked or bPassLocked:
        return True

    return False

# utility to redirect when unlocked
def redirectUnlocked():
    global bLockLocked
    global bPassLocked

    if bLockLocked or bPassLocked:
        pass
    else:
        return True

    return False

# makes the message to be displayed on lock screen
def makeMessage():
    if bLockLocked:
        return "No system key found. Please insert system key and press return to retry."
    elif bPassLocked:
        return "Enter password:"

    return ""

# makes classes to control lock page behavior
def makeClasses():
    if bLockLocked:
        return ("lock", "hidden")

    return ("", "")

# reads config.json and updates globals accordingly
def readConfig():
    global targetAddress
    global targetPort
    global password

    print('Reading config.json...')
    try:
        with open('config.json', 'r') as file:
            data = json.load(file)
            for key, val in data.items():
                print('{0} : {1}'.format(key, val))
                if key == 'targetAddress':
                    targetAddress = val
                elif key == 'targetPort':
                    targetPort = val
                elif key == 'password':
                    password = val
    except Exception as e:
        print('Error reading JSON... {0}'.format(e))

if __name__ == '__main__':
    #readConfig()
    app.run(host=targetAddress, port=targetPort)
