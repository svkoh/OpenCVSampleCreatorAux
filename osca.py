#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import cv

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
    srcv = sys.argv[1:]
    size = len(srcv)
    f = open('abc.idx', 'a')
    for i in srcv:
        object_cnt = 0
        saving_msg = ''
        img = cv.LoadImageM(i)
        cv.NamedWindow(i)
        cv.ShowImage(i, img)
        src = cv.CreateImage(cv.GetSize(img), 8, 3)
        cv.Copy(img, src)
        temp = cv.CreateImage(cv.GetSize(img), 8, 3)
        cv.SetMouseCallback(i, draw_rectangle_callback, img)
        while 1:
            cv.Copy(img, temp)
            if drawing_box:
                draw_box(temp, box)
            cv.ShowImage(i, temp)
            cv.Copy(src, img)
            draw_box(img, box)
            cv.ShowImage(i, img)
            key = cv.WaitKey(15)
            if key == 115:
                if box[0] > 0:
                    object_cnt += 1
                    saving_msg += '    {0} {1} {2} {3}'.format(box[0], box[1], box[2], box[3])
                    print i + '    {0}'.format(object_cnt) + saving_msg
            elif key == 83:
                f.write(i + '    {0}'.format(object_cnt) + saving_msg + '\n')
                print 'Saving item "' + i + '    {0}'.format(object_cnt) + saving_msg + '"'
            elif key == 114:
                object_cnt = 0
                saving_msg = ''
            elif key == 27:
                box = [-1, -1, 0, 0]
                break
        cv.DestroyWindow(i)