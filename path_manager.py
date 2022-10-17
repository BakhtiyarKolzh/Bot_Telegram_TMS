#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os
import re
import time
from multiprocessing import Lock
from pathlib import WindowsPath

########################################################################################################################


include_folders = ["AR", "AS", "KJ", "KR", "KG", "OV", "VK", "EOM", "EM", "PS", "SS"]
include = re.compile(r".*(?:" + "|".join(include_folders) + ")$")
detach = re.compile(r".*\S(отсоединено)$")
backup = re.compile(r".*(\S\d\d\d+)$")
enum = re.compile(r'\d+$')
suffix = '.rvt'
mutex = Lock()


########################################################################################################################


def get_file_size(path):
    size = os.path.getsize(path)
    return size


def get_basename(filepath):
    fullname = os.path.basename(filepath)
    filename, ext = os.path.splitext(fullname)
    return filename


def calc_numbers(filepath):
    basename = WindowsPath(filepath).name
    return len(basename) + sum(float(i) for i in basename if i.isdigit())


def get_revit_directories(input_path):
    global include
    project_dirs = []

    if (os.path.basename(input_path).endswith('RVT')):
        return input_path

    for entry in os.listdir(input_path):
        if include.match(entry):
            path = os.path.join(input_path, entry)
            for sub in os.listdir(path):
                if sub.endswith('RVT'):
                    sub_path = os.path.join(path, sub)
                    project_dirs.append(sub_path)

    return project_dirs


def get_rvt_paths_by_directory(directory):
    revit_paths = []
    if os.path.isdir(directory):
        for filename in os.listdir(directory):
            if filename.endswith(suffix):
                name = filename.rstrip(suffix)
                if backup.match(name): continue
                if detach.match(name): continue
                if (0 < name.find('#')): continue
                path = os.path.join(directory, filename)
                path = os.path.abspath(path)
                revit_paths.append(path)

    return revit_paths


def get_result_rvt_path_list(directory: str) -> list:
    revit_paths = []
    with mutex:
        dir_source = get_revit_directories(directory)
        if isinstance(dir_source, str):
            temp_list = get_rvt_paths_by_directory(dir_source)
            revit_paths.extend(temp_list)
        if isinstance(dir_source, list):
            for dir in dir_source:
                temp_list = get_rvt_paths_by_directory(dir)
                revit_paths.extend(temp_list)

        revit_paths.sort(key=lambda x: calc_numbers(x))
    return revit_paths


def numerate_path_list(line_list):
    result = []
    for i, path in enumerate(line_list):
        line = str(i + 1) + ". " + get_basename(path)
        result.append(line)
        print(line)
    return result


def write_revit_path_list_to_file(filepath, paths):
    [print(p) for p in paths]
    if os.path.isfile(filepath):
        with mutex:
            with codecs.open(filepath, mode='w', encoding='utf-8', errors='ignore') as fl:
                [fl.write(p + "\n") for p in paths]
            return time.sleep(5)

#######################################################################################################################
