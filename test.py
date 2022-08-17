#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import os
# import codecs
# from pathlib import WindowsPath
#
#
# def get_basename(filepath):
#     fullname = os.path.basename(filepath)
#     filename, ext = os.path.splitext(fullname)
#     return filename
#
#
# def calc_numbers(basename):
#     return len(basename) + sum(float(i) for i in basename if i.isdigit())
#
#
# source = os.path.realpath(r"D:\YandexDisk\RevitExportConfig\revit_file_list.txt")
# with codecs.open(source, mode='r', encoding='utf-8', errors='ignore') as fl:
#     collection = [WindowsPath(line) for line in fl.readlines() if line]
#     decorated = [(calc_numbers(line.name), line) for line in collection]
#     decorated.sort()
#
# result = [os.path.realpath(filepath) for i, filepath in decorated]

