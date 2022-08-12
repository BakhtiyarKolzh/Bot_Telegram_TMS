#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os
import re

from natsort import natsorted

########################################################################################################################


include_folders = ["AR", "AS", "KJ", "KR", "KG", "OV", "VK", "EOM", "EM", "PS", "SS"]
include = re.compile(r".*(?:" + "|".join(include_folders) + ")$")
detach = re.compile(r".*\S(отсоединено)$")
backup = re.compile(r".*(\S\d\d\d+)$")
suffix = '.rvt'


########################################################################################################################


def get_file_size(path):
    size = os.path.getsize(path)
    return size


def get_basename(file_path):
    fullname = os.path.basename(file_path)
    filename, ext = os.path.splitext(fullname)
    return filename


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
                print(path)

    return revit_paths


def get_result_rvt_path_list(project_dir_path):
    revit_paths = []
    source = get_revit_directories(project_dir_path)
    print("source: - " + source)
    if isinstance(source, str):
        temp = get_rvt_paths_by_directory(source)
        print("temp: - " + str(temp))
        revit_paths.extend(temp)
    if isinstance(source, list):
        temp = [get_rvt_paths_by_directory(dir) for dir in source]
        print("temp: - " + str(temp))
        revit_paths.append(temp)

    revit_paths.sort(key=lambda x: get_basename(x))
    print("sort: - " + str(revit_paths))
    return revit_paths



def get_numeric_revit_path_list(revit_paths):
    result = []
    for i, filepath in enumerate(revit_paths):
        path = str(i + 1) + ".\t" + get_basename(filepath)
        result.append(path)
        print(path)
    return


def write_revit_path_list_file(revit_paths):
    directory = os.path.dirname(os.path.dirname(os.path.realpath(os.getcwd())))
    output_path = os.path.join(directory, 'revit_file_list.txt')
    print('Revit files list located path is: ' + str(output_path) + '\n')
    with codecs.open(output_path, mode='w', encoding='utf-8', errors='ignore') as f:
        [f.write(item + "\n") for item in revit_paths]
    return


#######################################################################################################################
