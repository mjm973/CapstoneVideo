from flask import Flask, render_template, request, url_for, jsonify, redirect, Response
from cam import VideoCamera
from setInterval import setInterval
import requests

app = Flask(__name__)

ip = 'localhost'
port = 4242

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

    jsUrl = url_for('static', filename='js/mock.js')
    cssUrl = url_for('static', filename='css/main.css')

    return render_template('index.html', js=jsUrl, css=cssUrl)

# api route to receive and check password
@app.route('/pass/', methods=['POST'])
def password():
    pass

# api route to receive confirmation that the key has been insterted
@app.route('/key/', methods=['POST'])
def key():
    global bLockLocked

    bLockLocked = True
    print("Key received!")

    return jsonify({
        'status': "ok",
        'msg': "key received",
        'value': bLockLocked,
        'success': True
    })

# client A queries this regularly on server A to read filesystem
@app.route('/check/', methods=['POST'])
def forceCheck():
    if bLockLocked:
        result = checkKey()
        return jsonify([result])

    return jsonify([True])

@app.route('/fs/')
def fs():
    global bFeed
    #path ="C:\Users\Mateo Juvera\Desktop\USBBackup\key.txt"
    path = 'C:/Users/Mateo Juvera/Desktop/USBBackup/kaey.txt'

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
    while True:
        frame = cam.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# wrapper for camera sorcery
def videoFeed(cam):
    return Response(gen(cam), mimetype='multipart/x-mixed-replace; boundary=frame')

# callback that will check if the key has been inserted
def checkKey(caller=None):
    print('Checking for key...')

    path = 'C:/Users/Mateo Juvera/Desktop/USBBackup/key.txt'

    try:
        with open(path, 'r') as file:
            print(file.read())
            result = sendKey()
            print("Key sent!")
            if caller is not None:
                caller.cancel()
            return result
    except:
        return False

# called once key has been insterted (on server A) to unlock bLockLocked (on server B) and display password prompt (on client A)
def sendKey():
    req = requests.post('http://localhost:5000/key/', data = {})

    res = req.json()

    print(res)
    print(res['success'])

    return res['success']

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

# set our key checking to an interval
# check = setInterval(0.5, checkKey)

if __name__ == '__main__':
    print("Running multithreaded...")
    app.run(host='localhost', port=5050, threaded=True)
