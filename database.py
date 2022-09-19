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


def define_action(action: dict):
    for user, commands in action.items():
        digits = list()
        control = commands.pop(0)
        directory = commands.pop(0)
        [digits.append(cmd) for cmd in commands if isinstance(cmd, int)]
        [digits.append(int(cmd)) for cmd in commands if isinstance(cmd, str) and cmd.isdigit()]
        print(f'Command = {user} {control} {directory} {digits}')
        return control, directory, digits


def retrieve_paths_by_numbers(paths, commands):
    digits = set()
    output = list()
    if isinstance(commands, list):
        if 0 in commands: return paths
        for num in sorted(commands):
            if isinstance(num, int):
                if num not in digits:
                    try:
                        digits.add(num)
                        output.append(paths[num - 1])
                    except:
                        pass
    [print(c) for c in digits]
    return output


def run_command(cdata: tuple):
    def worker(cmd):
        return subprocess.Popen(cmd, shell=True)

    digit, action = cdata
    control, directory, commands = define_action(action)
    paths = path_manager.get_result_rvt_path_list(directory)
    paths = retrieve_paths_by_numbers(paths, commands)
    path_manager.write_revit_path_list_to_file(rvt_path_list_file, paths)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:

        if "DWG" == control:
            cmd = os.path.realpath(r"D:\YandexDisk\RevitExportConfig\BatFiles\ExportBotToDWG.bat")
            if os.path.exists(cmd):
                pool.submit(worker, cmd)
                print(f"Set DWG => ")

        if "NWC" == control:
            cmd = os.path.realpath(r"D:\YandexDisk\RevitExportConfig\BatFiles\ExportBotToNWC.bat")
            if os.path.exists(cmd):
                pool.submit(worker, cmd)
                print(f"Set DWG => ")

        if "PDF" == control:
            cmd = os.path.realpath(r"D:\YandexDisk\RevitExportConfig\BatFiles\ExportBotToPDF.bat")
            if os.path.exists(cmd):
                pool.submit(worker, cmd)
                print(f"Set DWG => ")

    return
