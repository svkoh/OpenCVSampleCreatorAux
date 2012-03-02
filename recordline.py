#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import string

class recordline:
    def __init__(self, line = ''):
        rec = line.split()
        
        self.filename = ''
        self.objects = []
        self.objcnt = 0
        
        if len(rec) > 0:
            self.filename = rec[0]
            rec.remove(self.filename)
            
        if len(rec) > 0:
            for i in range(len(rec)):
                rec[i] = string.atoi(rec[i])
            self.objcnt = rec[0]
            
            for i in range(self.objcnt):
                self.objects.append(list(rec[i * 4 + 1 : i * 4 + 5]))
    
    def add(self, object):
        if self.objects.count(object) == 0:
            self.objects.append(object)
            self.objcnt += 1
            
    def remove(self, object):
        while self.objects.count(object) != 0:
            self.objects.remove(object)
            self.objcnt -= 1
            
    def toString(self):
        str = '{0}    {1}'.format(self.filename, self.objcnt)
        if self.objcnt == 0:
            return str
        for i in range(self.objcnt):
            str += '    {0:>4}    {1:>4}    {2:>4}    {3:>4}'.format(self.objects[i][0], self.objects[i][1], self.objects[i][2], self.objects[i][3])
        return str
        
if __name__ == '__main__':
    rl = recordline('001.png    2      25      20      40      40     900     600    1240     810')
    print(rl.toString())
    print('rl.add([20, 20, 40, 40]):')
    rl.add([20, 20, 40, 40])
    print(rl.toString())
    print('rl.add([182, 176, 229, 223]):')
    rl.add([182, 176, 229, 223])
    print(rl.toString())
    print('rl.add([998, 600, 1240, 810]):')
    rl.add([998, 600, 1240, 810])
    print(rl.toString())
    print('rl.add([762, 654, 900, 840]):')
    rl.add([762, 654, 900, 840])
    print(rl.toString())
    print('rl.remove([182, 176, 229, 223]):')
    rl.remove([182, 176, 229, 223])
    print(rl.toString())
    print('rl.remove([762, 654, 900, 840]):')
    rl.remove([762, 654, 900, 840])
    print(rl.toString())