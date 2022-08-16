#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import asyncio

import database
import TelegramBot

database_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data_file.json")


def call_telegram():
    return TelegramBot.start


def remove(path):
    if os.path.isfile(path):
        try:
            os.unlink(path)
        except:
            pass
    return


async def execute():
    while True:
        await asyncio.sleep(100)
        database_dict = database.deserialize_json_data(database_path)
        if not isinstance(database_dict, dict): await asyncio.sleep(1000)
        if isinstance(database_dict, dict) and not len(database_dict): remove(database_path)
        if isinstance(database_dict, dict) and len(database_dict): database.execute_commands(database_path)


async def run():
    await call_telegram()
    await execute()


if __name__ == "__main__":
    run()
