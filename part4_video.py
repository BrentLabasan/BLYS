import cv2
from darkflow.net.build import TFNet
import numpy as np
import time
from playsound import playsound

import threading

from pygame import mixer # Load the required library
mixer.init()


targetObject = 'scissors'

timer = 0
isTargetObjectPresent = False

global FiveSecondsOfActivityElapsed
FiveSecondsOfActivityElapsed = False

playFinishedSound = True


def f(f_stop):
    # do something here ...

    # print('wutt')


    global isTargetObjectPresent
    print('isTargetObjectPresent:', isTargetObjectPresent)
    global FiveSecondsOfActivityElapsed
    print('FiveSecondsOfActivityElapsed:', FiveSecondsOfActivityElapsed)

    if isTargetObjectPresent == True:
        global timer
        timer += 1

        mixer.music.load('click.wav')
        mixer.music.play()

        if timer >= 5:
            print("5 seconds has elasped. timer >= 5. FiveSecondsOfActivityElapsed = True")
            FiveSecondsOfActivityElapsed = True

    if not f_stop.is_set():
        # call f() again in 60 seconds
        threading.Timer(1, f, [f_stop]).start()

f_stop = threading.Event()
# start calling f now and every 60 sec thereafter
f(f_stop)


options = {
    'model': 'cfg/yolo.cfg',
    'load': 'bin/yolov2.weights',
    'threshold': 0.2,
    'gpu': 1.0
}

tfnet = TFNet(options)
colors = [tuple(255 * np.random.rand(3)) for _ in range(10)]

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

while True:
    stime = time.time()
    ret, frame = capture.read()
    if ret:
        results = tfnet.return_predict(frame)
        for color, result in zip(colors, results):
            tl = (result['topleft']['x'], result['topleft']['y'])
            br = (result['bottomright']['x'], result['bottomright']['y'])
            label = result['label']

            # print(label)

            if label == targetObject:
                # print(targetObject, 'detected')

                isTargetObjectPresent = True
            else:
                # print('timer reset')
                # timer = 0

                isTargetObjectPresent = False

            confidence = result['confidence']
            text = '{}: {:.0f}%'.format(label, confidence * 100)
            frame = cv2.rectangle(frame, tl, br, color, 5)
            frame = cv2.putText(
                frame, text, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

        frame = cv2.putText(frame, targetObject + ' has been on the screen for ' + str(timer) + ' seconds', (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0) , 2)

        if FiveSecondsOfActivityElapsed == False:
            frame = cv2.putText(frame, 'OBJECTIVE: Hold up a scissors to the webcam for 5 seconds', (50,150), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0) , 2)
        else:
            frame = cv2.putText(frame, 'Success!! You held up a scissors to the webcam for 5 seconds', (50,150), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0) , 2)
            if playFinishedSound == True:
                mixer.music.load('send_im.wav')
                mixer.music.play()
                playFinishedSound = False

        cv2.imshow('frame', frame)
        
        # print('FPS {:.1f}'.format(1 / (time.time() - stime)))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        f_stop.set()
        break

capture.release()
cv2.destroyAllWindows()
