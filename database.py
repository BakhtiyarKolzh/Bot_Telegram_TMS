#!/usr/bin/env python
# -*- coding: utf-8 -*-

import concurrent.futures
import json
import os
import subprocess
import time
from collections import OrderedDict
from multiprocessing import Lock

import path_manager

mutex = Lock()
rvt_path_list_file = os.path.realpath(r"D:\YandexDisk\RevitExportConfig\revit_path_list_bot.txt")


def deserialize_json_data(path):
    if not os.path.isfile(path): return
    if os.path.isfile(path):
        with mutex:
            try:
                with open(path, "r", encoding='utf-8') as file:
                    return json.load(file)
            except Exception as exc:
                time.sleep(0.5)
                print(exc)


def update_json_data(path, data):
    store = deserialize_json_data(path)
    data = (store | data if isinstance(store, dict) else data)
    if isinstance(data, dict):
        write_json_data(path, data)
        print("Save data count {}\n".format(len(data)))
    return data


def write_json_data(filepath, data: dict):
    if isinstance(data, dict):
        with mutex:
            try:
                if len(data):
                    filepath = os.path.realpath(filepath)
                    with open(filepath, "w", encoding='utf-8') as jsn:
                        json.dump(data, jsn, ensure_ascii=False)
                else:
                    open(filepath, "w").close()
            except Exception as exc:
                time.sleep(0.5)
                print(exc)


def stream_read_json(filepath="data_file.json"):
    if os.path.isfile(filepath):
        with open(filepath, 'r', encoding='utf8') as jsn:
            try:
                data: dict = json.load(jsn)
                if data and len(data):
                    print(data.items())
                    order = OrderedDict(data)
                    action = order.popitem(last=False)
            except json.JSONDecodeError as e:
                return print(e)
            else:
                data = dict(order) if len(order) else dict()
                write_json_data(filepath, data)
        return action


def retrieve_paths_by_numbers(paths, numbers):
    digits = set()
    output = list()
    if isinstance(numbers, list):
        [digits.add(num) for num in numbers if isinstance(num, int)]
        [digits.add(int(num)) for num in numbers if isinstance(num, str) and num.isdigit()]
        [print(num) for num in digits]
        if 0 in digits: return paths
        for num in sorted(digits):
            try:
                digits.add(num)
                output.append(paths[num - 1])
            except:
                pass
    return output


def run_command(data: dict):
    def worker(cmd):
        return subprocess.Popen(cmd, shell=True)

    control = data.get('control')
    numbers = data.get('numbers')
    directory = data.get('directory')
    paths = path_manager.get_result_rvt_path_list(directory)
    paths = retrieve_paths_by_numbers(paths, numbers)
    print(f'\tfinal => {control} {paths} {directory}')
    path_manager.write_revit_path_list_to_file(rvt_path_list_file, paths)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:

        if "DWG" == control and len(paths):
            cmd = os.path.realpath(r"D:\YandexDisk\RevitExportConfig\BatFiles\ExportBotToDWG.bat")
            if os.path.exists(cmd):
                pool.submit(worker, cmd)
                print(f"Set DWG => ")
                time.sleep(300)

        if "NWC" == control and len(paths):
            cmd = os.path.realpath(r"D:\YandexDisk\RevitExportConfig\BatFiles\ExportBotToNWC.bat")
            if os.path.exists(cmd):
                pool.submit(worker, cmd)
                print(f"Set NWC => ")

        if "PDF" == control and len(paths):
            cmd = os.path.realpath(r"D:\YandexDisk\RevitExportConfig\BatFiles\ExportBotToPDF.bat")
            if os.path.exists(cmd):
                pool.submit(worker, cmd)
                print(f"Set PDF => ")

    return
