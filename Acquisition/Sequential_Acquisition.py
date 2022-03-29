"""
This script allow to use multiple RTSP camera simultaneously and save all the images directly in the same folder with the date (by pressing S 
and selecting the OpenCV window).
The main issue of this script is that it tries to fix the fact that the simultaneosly capture of all the images sequentially
leads to a buffering of the videos and that the stream is not real time. That's why we remove the buffering which leads to non-smooth videos (
but you get the last frame)
"""
import cv2
import random, time
import argparse
import numpy as np
import logging
from datetime import datetime
import queue, threading
import argparse, json

# bufferless VideoCapture
# https://stackoverflow.com/questions/54460797/how-to-disable-buffer-in-opencv-camera
class VideoCapture:
    def __init__(self, name):
        self.cap = cv2.VideoCapture(name)
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()
    # read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()   # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.q.put(frame)
    def read(self):
        return self.q.get()
    def isOpened(self):
        return self.cap.isOpened()
    def release(self):
        return self.cap.release()

def main(cameras,class_name):
    # Load the YOLO model
    # we create the video capture object cap
    caps, rets, frames = [None]*len(cameras), [False]*len(cameras), [None]*len(cameras)
    for rstp_index in range(len(cameras)):
        logging.info("Init camera : %s", cameras[rstp_index])
        caps[rstp_index]=( VideoCapture(cameras[rstp_index]) )
    
    for rstp_index in range(len(cameras)):
        if not caps[rstp_index].isOpened():
            raise IOError(f"We cannot open webcam {cameras[rstp_index]}")

    while True:
        for i in range(len(cameras)):
            if caps[i].isOpened():
                logging.info("Reading cap : %s", str(i))
                # ret, frame = caps[i].read()
                # rets[i]=(ret)
                frame = caps[i].read()
                frames[i]=(frame)
                logging.info("Trying to display frame : %s", str(i))
                # if rets[i]:
                #     im_size_x, im_size_y,_ = np.shape(frames[i])
                #     cv2.imshow(cameras[i], cv2.resize(frames[i], (im_size_y//4,im_size_x//4)))
                im_size_x, im_size_y,_ = np.shape(frames[i])
                cv2.imshow(cameras[i], cv2.resize(frames[i], (im_size_y//4,im_size_x//4)))
        if cv2.waitKey(5) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
        if cv2.waitKey(25) & 0xFF == ord("s"):
            today = datetime.now()
            for p in range(len(caps)):
                # if rets[p]:
                d3 = today.strftime("%d-%m-%y_%H-%M-%S")
                cv2.imwrite("images/"+class_name+'/'+d3+'_cam'+str(p)+'.png',frames[p])
                # else:
                #     print(d3,' : ', 'Error cam ', p, 'not accessible')

    for i in range(len(cameras)):
        if caps[i].isOpened():
            caps[i].release()
    cv2.destroyAllWindows()


################# Dummy Config File: #####################
#### {
####     "cameras" :  [
####         "rtsp://LOGIN:PASSWORD@IP.ADDRESS",
####         "rtsp://LOGIN:PASSWORD@IP.ADDRESS",
####         "rtsp://LOGIN:PASSWORD@IP.ADDRESS",
####         "rtsp://LOGIN:PASSWORD@IP.ADDRESS",
####         ]
#### }
##########################################################

def parse_cfg_json(path):
    data= open(path,"r")
    cams=json.loads(data.read())["cameras"]
    data.close()
    return cams


if __name__=="""__main__""":
    parser = argparse.ArgumentParser(description="Tool for saving simultaneously multiple images from RTSP Cameras.")
    parser.add_argument("-c", "--config", type=str, default="config.json", help="Path to config file with RTSP addresses")
    parser.add_argument("-obj", "--object", type=str, default="mixed", help="Object to Acquire")
    args = parser.parse_args()
    cameras=parse_cfg_json(args.config)
    obj=args.object.lower()
    # classes=['mug', 'shoes', 'mouse', 'book', 'wallet', 'keyboard', 'pencil_case']
    # class_name=classes[0]
    main(cameras, obj)