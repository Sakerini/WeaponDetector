#run python3 main.py -i localhost -o 5010 -f 10
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import numpy as np
import threading
import argparse
import time
import cv2

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful for multiple browsers/tabs
# are viewing tthe stream)
outputFrame = None
lock = threading.Lock()

app = Flask(__name__, template_folder='template')

# initialize the video stream and allow the camera sensor to
vs = VideoStream(src=0).start()

@app.route('/')
def main():
	return(render_template('index.html'))


def detect_weapon(frameCount):
	net = cv2.dnn.readNet("model/net.weights", "model/net.cfg")
	classes = ["Weapon"]

	layer_names = net.getLayerNames()
	output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
	colors = np.random.uniform(0, 255, size=(len(classes), 3))

	# grab global references to the video stream, output frame, and
	# lock variables
	global vs, outputFrame, lock

	# initialize total number of frames read thus far
	total = 0

	# loop over frames from the video stream
	while True:
		# read the next frame from the video stream, resize it,
		# convert the frame to grayscale, and blur it
		frame = vs.read()
		height, width, channels = frame.shape

		# if the total number of frames has reached a sufficient
		# number to construct a reasonable background model, then
		# continue to process the frame
		if total > frameCount:
			# Detecting objects
			blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

			net.setInput(blob)
			outs = net.forward(output_layers)

			# Showing information on the screen
			class_ids = []
			confidences = []
			boxes = []
			for out in outs:
				for detection in out:
					scores = detection[5:]
					class_id = np.argmax(scores)
					confidence = scores[class_id]
					if confidence > 0.5:
						# Object detected
						center_x = int(detection[0] * width)
						center_y = int(detection[1] * height)
						w = int(detection[2] * width)
						h = int(detection[3] * height)

						# Rectangle coordinates
						x = int(center_x - w / 2)
						y = int(center_y - h / 2)

						boxes.append([x, y, w, h])
						confidences.append(float(confidence))
						class_ids.append(class_id)

			indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
			# print(indexes)
			if indexes == 0: print("weapon detected")
			font = cv2.FONT_HERSHEY_PLAIN
			for i in range(len(boxes)):
				if i in indexes:
					x, y, w, h = boxes[i]
					label = str(classes[class_ids[i]])
					color = colors[class_ids[i]]
					cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
					cv2.putText(frame, label, (x, y + 30), font, 3, color, 3)

		
		# increment the total number of frames read thus far
		total += 1

		# acquire the lock, set the output frame, and release the
		# lock
		with lock:
			outputFrame = frame.copy()

		
def generate():
	# grab global references to the output frame and lock variables
	global outputFrame, lock

	# loop over frames from the output stream
	while True:
		# wait until the lock is acquired
		with lock:
			# check if the output frame is available, otherwise skip
			# the iteration of the loop
			if outputFrame is None:
				continue

			# encode the frame in JPEG format
			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

			# ensure the frame was successfully encoded
			if not flag:
				continue

		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--ip", type=str, required=True,
		help="ip address of the device")
	ap.add_argument("-o", "--port", type=int, required=True,
		help="ephemeral port number of the server (1024 to 65535)")
	ap.add_argument("-f", "--frame-count", type=int, default=32,
		help="# of frames used to construct the background model")
	args = vars(ap.parse_args())

	# start a thread that will perform motion detection
	t = threading.Thread(target=detect_weapon, args=(
		args["frame_count"],))
	t.daemon = True
	t.start()

	app.run(host=args["ip"], port=args["port"], debug=True,
		threaded=True, use_reloader=False)

# release the video stream pointer
vs.stop()