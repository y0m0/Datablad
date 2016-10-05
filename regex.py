#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# regex.py
#
import re

with open('regex.txt') as file:
    for line in file:
        print(line)
        value = re.split('    ', line)
        print(value)
