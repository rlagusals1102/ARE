import time
import serial

import cv2
import numpy as np
import imutils
from imutils.video import VideoStream
from imutils.video import FPS

class memory:
    def __init__(self):
        self.counts = 0
        return

    def count(self):
        self.counts += 1

    def clear(self):
        self.counts = 0

def load_model():
    net = cv2.dnn.readNetFromCaffe('MobileNetSSD_deploy.prototxt.txt', 'MobileNetSSD_deploy.caffemodel')
    return net


def video_stream():
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    fps = FPS().start()
    return vs, fps


def detect_objects(frame, net):
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    return (h, w, detections)

def draw_objects(frame, detections, h, w):
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        idx = int(detections[0, 0, i, 1])

        if confidence > 0.7 and object[idx] == "person":
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            label = "{}: {:.2f}%".format(object[idx], confidence * 100)
            cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
            person.count()



def main():
    model = load_model()
    vs, fps = video_stream()

    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=1920, height=1080)
        h, w, detections = detect_objects(frame, model)
        draw_objects(frame, detections, h, w)

        if person.counts > 0:
            cv2.putText(frame, "person: {}".format(person.counts), (20, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        print("[RESULT] person count : {}".format(person.counts))

        if person.counts == 1:
            cv2.putText(frame, "Warning!", (1600, 925), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            ser_text1 = "Warning!"
            ser.write(ser_text1.encode() + b'\n')
        elif person.counts == 0:
            cv2.putText(frame, "Normal", (1600, 925), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            ser_text2 = "Normal"
            ser.write(ser_text2.encode() + b'\n')
        
        fps.update()

        person.clear()

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    fps.stop()
    print("Time: {:.2f}".format(fps.elapsed()))
    print("FPS: {:.2f}".format(fps.fps()))

    cv2.destroyAllWindows()
    vs.stop()

if __name__ == "__main__":
    object = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]
    person = memory()

    COLORS = np.random.uniform(0, 255, size=(len(object), 3))

    # COM 3 or 5
    ser = serial.Serial('COM5', 9600)

    main()