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


box = [-1, -1, -1, -1] # left-top and right-bottom points of the select box
drawing_box = 0 # flag indicating the state of drawing
border = 'init' # indicating the selected border

def draw_box(image, rect):
    cv.Rectangle(image, (rect[0], rect[1]), (rect[2], rect[3]), cv.Scalar(0xff, 0x00, 0x00))
    # print "drawing a box"

def draw_border(image, rect, border): 
# border is in 'left', 'top', 'right', 'bottom'
    if border == "left":
        point1 = (rect[0], rect[1])
        point2 = (rect[0], rect[3])
    elif border == "top":
        point1 = (rect[0], rect[1])
        point2 = (rect[2], rect[1])
    elif border == "right":
        point1 = (rect[2], rect[1])
        point2 = (rect[2], rect[3])
    elif border == "bottom":
        point1 = (rect[0], rect[3])
        point2 = (rect[2], rect[3])
                
    cv.Line(image, point1, point2, cv.Scalar(0x00, 0x00, 0xff))

def get_border(box, x, y): 
# return border in 'left', 'top', 'right', 'bottom', 'lefttop', 'righttop', 'leftbottom', 'rightbottom'
    lrange = -10 # set the accuracy of the selection of border, 9px as an example
    rrange = 10
    boder_range = range(lrange, rrange)
    if x - box[0] in boder_range:
        if y - box[1] in boder_range:
            return 'lefttop'
        elif y - box[3] in boder_range:
            return 'leftbottom'
        elif y - box[1] > rrange and y - box[3] < lrange:
            return 'left'
    if x - box[2] in boder_range:
        if y - box[1] in boder_range:
            return 'righttop'
        elif y - box[3] in boder_range:
            return 'rightbottom'
        elif y - box[1] > rrange and y - box[3] < lrange:
            return 'right'
    if y - box[1] in boder_range and x - box[0] > rrange and x - box[2] < lrange:
        return 'top'
    if y - box[3] in boder_range and x - box[0] > rrange and x - box[2] < lrange:
        return 'bottom'
        
    return 'none'

def draw_rectangle_callback(event, x, y, flags, param):
    global drawing_box
    global box
    global border
    global src
    if event == cv.CV_EVENT_MOUSEMOVE:
        if drawing_box:
            cv.Copy(src, param[1])
            # print border
            if border == 'init':
                box[2] = x;
                box[3] = y;
                draw_box(param[1], box)
            elif border == 'left': # here and below are adjusting the select box
                box [0] = x;
                draw_box(param[1], box)
                draw_border(param[1], box, 'left')
            elif border == 'right':
                # print "moving right border"
                box [2] = x;
                draw_box(param[1], box)
                draw_border(param[1], box, 'right')
            elif border == 'top':
                box [1] = y;
                draw_box(param[1], box)
                draw_border(param[1], box, 'top')
            elif border == 'bottom':
                box [3] = y;
                draw_box(param[1], box)
                draw_border(param[1], box, 'bottom')
            elif border == 'lefttop':
                box [0] = x;
                box [1] = y;
                draw_box(param[1], box)
                draw_border(param[1], box, 'left')
                draw_border(param[1], box, 'top')
            elif border == 'righttop':
                box [2] = x;
                box [1] = y;
                draw_box(param[1], box)
                draw_border(param[1], box, 'right')
                draw_border(param[1], box, 'top')
            elif border == 'leftbottom':
                box [0] = x;
                box [3] = y;
                draw_box(param[1], box)
                draw_border(param[1], box, 'left')
                draw_border(param[1], box, 'bottom')
            elif border == 'rightbottom':
                box [2] = x;
                box [3] = y;
                draw_box(param[1], box)
                draw_border(param[1], box, 'right')
                draw_border(param[1], box, 'bottom')
    elif event == cv.CV_EVENT_LBUTTONDOWN:
        drawing_box = True
        if box[0] < 0:
            box = [x, y, x, y]
        else:
            border = get_border(box, x, y)
            if border == 'none': # to clear the selected rect, just click any area that is not near the border
                box = [-1, -1, -1, -1];
                drawing_box = False
                border = 'init'
                cv.Copy(src, param[1])
            # print border
    elif event == cv.CV_EVENT_LBUTTONUP:
        drawing_box = 0
        if box[2] < box[0]:
            tmp = box[0]
            box[0] = box[2]
            box[2] = tmp
        if box[3] < box[1]:
            tmp = box[1]
            box[1] = box[3]
            box[3] = tmp
        draw_box(param[1], box)
    # elif event == cv.CV_EVENT_MBUTTONDOWN:
        # print box
        # if box[0] > 0:
            # box[2] = x - box[0]
            # box[3] = y - box[1]
            # if box[2] < 0:
                # box[0] += box[2]
                # box[2] *= -1
            # if box[3] < 0:
                # box[1] += box[3]
                # box[3] *= -1
            # draw_box(param, box)
    
    cv.ShowImage(param[0], param[1])

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
        global src
        src = cv.LoadImageM(srcv[i])
        cv.NamedWindow(srcv[i])
        cv.ShowImage(srcv[i], src)
        
        img = cv.CreateImage(cv.GetSize(src), 8, 3)
        cv.Copy(src, img)
        
        if srcv[i] not in idx:
            idx[srcv[i]] = recordline(srcv[i])
            
        temprl = idx[srcv[i]]
        
        
        # temp = cv.CreateImage(cv.GetSize(img), 8, 3)
        cv.SetMouseCallback(srcv[i], draw_rectangle_callback, [srcv[i], img])
        while 1:
            # cv.Copy(img, temp)
            # if drawing_box:
                # draw_box(temp, box)
            # cv.ShowImage('temp', temp)
            # cv.Copy(src, img)
            # draw_box(img, box)
            # cv.ShowImage(srcv[i], img)
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
                box = [-1, -1, -1, -1]
                cv.DestroyWindow(srcv[i])
                i -= 2
                break
            elif key == 2555904: # right arrow, process next image
                box = [-1, -1, -1, -1]
                cv.DestroyWindow(srcv[i])
                break
            elif key == 27: # ESC; Use ESC to stop processing current image
                box = [-1, -1, -1, -1]
                cv.DestroyWindow(srcv[i])
                break
            elif key == 113: # char 'q'; Whenever we can use 'q' to quit
                box = [-1, -1, -1, -1]
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
     
