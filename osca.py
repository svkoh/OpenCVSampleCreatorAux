#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import cv
from preference import *
from recordline import *

pref = preference()
idxFile = pref.pref.get('Index File Name')
mode = pref.pref.get('Mode')
loop = pref.pref.get('Loop')

idx = {}


box = [-1, -1, 0, 0]
drawing_box = 0

def draw_box(image, rect):
    cv.Rectangle(image, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), cv.Scalar(0xff, 0x00, 0x00))

def draw_rectangle_callback(event, x, y, flags, param):
    global drawing_box
    global box
    global flush
    if event == cv.CV_EVENT_MOUSEMOVE:
        if drawing_box:
            box[2] = x - box[0];
            box[3] = y - box[1];
    elif event == cv.CV_EVENT_LBUTTONDOWN:
        drawing_box = 1
        box = [x, y, 0, 0]
    elif event == cv.CV_EVENT_LBUTTONUP:
        drawing_box = 0
        if box[2] < 0:
            box[0] += box[2]
            box[2] *= -1
        if box[3] < 0:
            box[1] += box[3]
            box[3] *= -1
        draw_box(param, box)
    elif event == cv.CV_EVENT_MBUTTONDOWN:
        print box
        if box[0] > 0:
            box[2] = x - box[0]
            box[3] = y - box[1]
            if box[2] < 0:
                box[0] += box[2]
                box[2] *= -1
            if box[3] < 0:
                box[1] += box[3]
                box[3] *= -1
            draw_box(param, box)

if __name__ == '__main__':
    # Files to be processed
    srcv = sys.argv[1:]
    size = len(srcv)
    
    # If the mode is Modify, we should read the idx file first
    if mode == 'Modify':
        f = open(idxFile, 'r')
        for line in f.readlines():
            rl = recordline(line)
            idx[rl.filename] = rl
        f.close()
        
    # Process each file
    i = 0
    while i < size and i >= 0:
        # Load and show img
        img = cv.LoadImageM(srcv[i])
        cv.NamedWindow(srcv[i])
        cv.ShowImage(srcv[i], img)
        
        if srcv[i] not in idx:
            idx[srcv[i]] = recordline(srcv[i])
            
        temprl = idx[srcv[i]]
        
        # create a temp img to manipulate
        src = cv.CreateImage(cv.GetSize(img), 8, 3)
        cv.Copy(img, src)
        temp = cv.CreateImage(cv.GetSize(img), 8, 3)
        cv.SetMouseCallback(srcv[i], draw_rectangle_callback, img)
        while 1:
            cv.Copy(img, temp)
            if drawing_box:
                draw_box(temp, box)
            cv.ShowImage(srcv[i], temp)
            cv.Copy(src, img)
            draw_box(img, box)
            cv.ShowImage(srcv[i], img)
            key = cv.WaitKey(15)
            if key == 115: # char 's'
                if box[0] > 0:
                    temprl.add(box)
                    print temprl.toString()
            elif key == 83: # char 'S'
                idx[srcv[i]] = temprl
            elif key == 19: # CTRL + s
                f = open(idxFile, 'w')
                for rl in idx:
                    f.write(idx[rl].toString() + '\n')
            elif key == 114: # char 'r'
                temprl = recordline(srcv[i])
            elif key == 2424832: # left arrow, process the previous image
                box = [-1, -1, 0, 0]
                cv.DestroyWindow(srcv[i])
                i -= 2
                break
            elif key == 2555904: # right arrow, process next image
                box = [-1, -1, 0, 0]
                cv.DestroyWindow(srcv[i])
                break
            elif key == 27: # ESC; Use ESC to stop processing current image
                box = [-1, -1, 0, 0]
                cv.DestroyWindow(srcv[i])
                break
            elif key == 113: # char 'q'; Whenever we can use 'q' to quit
                box = [-1, -1, 0, 0]
                cv.DestroyWindow(srcv[i])
                i = -2 - size
                break
           # else:  # used for getting the code of the key you pressed
           #     print key
           
        i += 1
        if loop:
            if i < 0:
                i += size
            if i >= size:
                i -= size
     
