#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import asyncio
from collections import OrderedDict

import database
import TelegramBot

database_dict = OrderedDict()
database_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data_file.json")


def call_telegram():
    return TelegramBot.start


async def execute(data):
    while True:
        await asyncio.sleep(1000)
        if isinstance(data, OrderedDict) and len(data):
            database.execute_command(database_path, data)
            print("Commands length count {}".format(len(data)))
            await asyncio.sleep(300)


async def run(data):
    await execute(data)
    await call_telegram()


if __name__ == "__main__":
    run(database_dict)
