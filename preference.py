#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

class preference:
    def __init__(self):
        self.pref = {}
        prefFile = open('preference.txt')
        lines = prefFile.readlines()
        prefFile.close()
        for line in lines:
            print line
            if (line.strip() != '') and (line.strip()[0] != '#'):
                prefName = line.split('=')[0].strip()
                prefValue = line.split('=')[1].strip()
                # handle the value of type boolean
                if prefValue.upper() == "TRUE" or prefValue.upper() == "1":
                    prefValue = True
                else:
                    prefValue = False
                self.pref[prefName] = prefValue
                
if __name__ == '__main__':
    p = preference()
    for i in p.pref:
        print('{0} =  {1}'.format(i, p.pref[i]))