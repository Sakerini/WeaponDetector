#run python3 main.py -i localhost -o 5010 -f 10
from flask import Flask, Response, render_template
import numpy as np
import argparse
import cv2
import base64
from flask_socketio import SocketIO
from model.detect import *



app = Flask(__name__, template_folder='template')


@app.route('/')
def main():
	return(render_template('index.html'))

socketio = SocketIO(app)


@socketio.on('input')
def test_message(input):
	input = base64.b64decode(input.split(",")[1])

	nparr = np.fromstring(input, np.uint8)
	img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

	# cv2.imshow('lalala', img)
	# if cv2.waitKey() & 0xff == 27: quit()

	height, width, channels = img.shape

	re = detect(img, height, width)

	socketio.emit('rec', re)
	# print(re)


if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--ip", type=str, required=True,
		help="ip address of the device")
	ap.add_argument("-o", "--port", type=int, required=True,
		help="ephemeral port number of the server (1024 to 65535)")
	ap.add_argument("-f", "--frame-count", type=int, default=32,
		help="# of frames used to construct the background model")
	args = vars(ap.parse_args())

	# app.run(host=args["ip"], port=args["port"], debug=True,
	# 	threaded=True, use_reloader=False)

	socketio.run(app, port=args["port"])
