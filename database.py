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


def remove(path):
    if os.path.isfile(path):
        try:
            os.unlink(path)
        except:
            pass
    return


def add_item_to_dictionary(data, key, value):
    if isinstance(value, list):
        data[key] = value
        return data


def write_json_data(path, data):
    if not isinstance(data, dict): return
    with mutex:
        print(data.items())
        try:
            path = os.path.realpath(path)
            with open(path, "w") as jsn:
                json.dump(data, jsn, ensure_ascii=False)
                return True
        except Exception as exc:
            time.sleep(0.5)
            print(exc)


def deserialize_json_data(path):
    if not os.path.isfile(path): return
    if os.path.isfile(path):
        with mutex:
            try:
                with open(path, "r") as file:
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


def stream_read_json(filepath="data_file.json"):
    if os.path.isfile(filepath):
        with open(filepath, 'w+', encoding='utf8') as jsn:
            try:
                data: dict = json.load(jsn)
                if data and len(data):
                    order = OrderedDict(data)
                    action = order.popitem(last=False)
                    json.dump(order, jsn, ensure_ascii=False)
            except json.JSONDecodeError as e:
                return print(e)
            return action


def define_action(action: dict):
    control, directory, commands = None, None, None
    for user, commands in action.items():
        control = commands.pop(0)
        directory = commands.pop(0)
        commands = [int(cmd) for cmd in commands if cmd.isdigit()]
        print(f'Action = {control} {directory} {commands}')
    return control, directory, commands


def retrieve_paths_by_numbers(paths, commands):
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


def run_command(action: dict):
    def worker(cmd):
        return subprocess.Popen(cmd, shell=True)

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
