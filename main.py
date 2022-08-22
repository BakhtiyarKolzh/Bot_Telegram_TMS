#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import asyncio

import database
import telegrambot


database_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data_file.json")


async def telegram():
    await telegrambot.start

async def execute():
    await database.start()


task1 = asyncio.create_task(telegram())
task2 = asyncio.create_task(execute())


async def main():
    await task1
    await task2


if __name__=='__main__':
    asyncio.run(main())



