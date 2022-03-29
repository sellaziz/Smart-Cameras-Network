"""
Script to get a simple interface to sort images in folders (and figure out the images to blur)
Navigation : <-- S, --> D
Move File : F
"""
from tkinter import *

from PIL import Image, ImageTk
import os, shutil
from os import listdir
from os.path import isfile, join
import logging
from datetime import datetime
import argparse

now = datetime.now() # current date and time
date_time = now.strftime("%m_%d_%Y-%H_%M_%S")
logging.basicConfig(filename=f'move_img_{date_time}.log', level=logging.DEBUG)
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
logging.info(f'Log time : {date_time}')
frame_x,frame_y=1600,720
size=(frame_x,frame_y)

class Window(Frame):
    # based on https://pythonbasics.org/tkinter-image/
    def __init__(self, master=None,img_list=None, dest=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)
        self.img_list=img_list
        self.idx=0
        load = Image.open(self.img_list[0])
        load.thumbnail(size, Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)
        events=[('d', self.next_img),
                ('s', self.prev_img)
                # (),
                # (),
                ]
        events_w_arg=[
                      ('f', self.move_img_to, dest)
                    #   ('s', self.prev_img)
                      ]
        for key, func in events:
            master.bind(key,func)
        for key, func, arg in events_w_arg:
            master.bind(key,lambda event: func(event,arg))
    
    def next_img(self, event):
        if self.idx>=len(self.img_list)-1: return#, ""#f"Out of range {len(self.img_list)} {self.idx+1}"
        self.idx+=1
        # print(f"Next {self.idx}")
        load = Image.open(self.img_list[self.idx])
        load.thumbnail(size, Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)
    
    def prev_img(self, event):
        if self.idx-1<0: return #, ""#f"Out of range {len(self.img_list)} {self.idx-1}" 
        self.idx-=1
        # print(f"Prev {self.idx}")
        load = Image.open(self.img_list[self.idx])
        load.thumbnail(size, Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)
    
    def move_img_to(self, event, dest):
        assert os.path.exists(dest), 'Folder Does not exist'
        file = os.path.basename(self.img_list[self.idx])
        try:
            shutil.move(self.img_list[self.idx], os.path.join(dest,file))
            logging.info(f'Move : {self.img_list[self.idx]} -> {os.path.join(dest,file)}')
            self.img_list.remove(self.img_list[self.idx])
            if not self.idx-1<0:
                self.prev_img(event)
            else:
                self.next_img(event)
        except e:
            print(f"Error {e}")
    


if __name__=="__main__":
    root = Tk()
    parser = argparse.ArgumentParser(description='Simple GUI to move images from input folder to Destination Folder.')
    parser.add_argument('-i','--input', required=True, type=str, default="test",
                        help='Input Folder')
    parser.add_argument('-o','--output', required=True, type=str, default="new",
                        help='Output Folder')
    args = parser.parse_args()
    input_pth=args.input
    img_lisr = [join(input_pth, f) for f in listdir(input_pth) if isfile(join(input_pth, f))]
    app = Window(root, img_lisr, args.output)
    root.wm_title("Tkinter window")
    root.geometry(str(frame_x)+"x"+str(frame_y))
    root.mainloop()