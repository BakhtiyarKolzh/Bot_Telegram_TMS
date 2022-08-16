#!/usr/bin/env python
# -*- coding: utf-8 -*-

from natsort import natsorted
import codecs
import os
import re

########################################################################################################################


include_folders = ["AR", "AS", "KJ", "KR", "KG", "OV", "VK", "EOM", "EM", "PS", "SS"]
include = re.compile(r".*(?:" + "|".join(include_folders) + ")$")
detach = re.compile(r".*\S(отсоединено)$")
backup = re.compile(r".*(\S\d\d\d+)$")
enum = re.compile(r'\d+$')
suffix = '.rvt'


########################################################################################################################


def get_file_size(path):
    size = os.path.getsize(path)
    return size


def get_basename(filepath):
    fullname = os.path.basename(filepath)
    filename, ext = os.path.splitext(fullname)
    return filename


def get_last_numbers(filepath):
    result = 0
    name = get_basename(filepath)
    match = enum.match(name)
    if match is not None:
        res = match.group()
        if res.isdigit():
            result = res
    return result


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


def get_result_rvt_path_list(project_dir_path):
    revit_paths = []
    dir_source = get_revit_directories(project_dir_path)
    if isinstance(dir_source, str):
        temp_list = get_rvt_paths_by_directory(dir_source)
        revit_paths.extend(temp_list)
    if isinstance(dir_source, list):
        for dir in dir_source:
            temp_list = get_rvt_paths_by_directory(dir)
            revit_paths.extend(temp_list)

    revit_paths.sort(key=lambda x: get_last_numbers(x))
    return revit_paths


def numerate_path_list(line_list):
    result = []
    for i, path in enumerate(line_list):
        line = str(i + 1) + ". " + get_basename(path)
        result.append(line)
        print(line)
    return result


def write_revit_path_list_file(paths):
    directory = os.path.dirname(os.path.dirname(os.path.realpath(os.getcwd())))
    output_path = os.path.join(directory, 'revit_file_list.txt')
    with codecs.open(output_path, mode='w', encoding='utf-8', errors='ignore') as file:
        [file.write(item + "\n") for item in paths]
    return


def retrieve_paths(paths, commands):
    output = list()
    counts = len(paths)
    if isinstance(commands, list):
        if 0 in commands: return paths
        for num in sorted(commands):
            if isinstance(num, int) and num < counts:
                try:
                    output.append(paths[num - 1])
                except Exception as exc:
                    print("Value {} in {} - {}".format(num, counts, exc))
    return output

#######################################################################################################################
