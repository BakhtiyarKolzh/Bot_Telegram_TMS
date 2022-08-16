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
        await asyncio.sleep(30)
        if not isinstance(data, OrderedDict): await asyncio.sleep(1200)
        if isinstance(data, OrderedDict) and not len(data): await asyncio.sleep(900)
        if isinstance(data, OrderedDict) and len(data): database.execute_commands(database_path, data)


async def run(data):
    await call_telegram()
    await execute(data)


if __name__ == "__main__":
    run(database_dict)
