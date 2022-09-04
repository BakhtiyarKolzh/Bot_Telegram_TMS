#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import datetime

import telegrambot



# async def telegram():
#     loop = asyncio.get_event_loop()
#     loop.create_task(main())
#     await asynctelebot.executor.start_polling(loop)
#
#
# async def execute():
#     await database.run()
#
#
# # task1 = asyncio.create_task(telegram())
# task2 = asyncio.create_task(execute())


async def request():
    task1 = asyncio.create_task(telegrambot.run_polling())
    # task2 = asyncio.create_task(method1())
    # return await asyncio.gather(task2, task1)


async def method1():
    for _ in range(10):
        now = str(datetime.datetime.now())
        print("method111 {} ".format(now))
        await asyncio.sleep(1)
    print("completed method111")
    return


async def method2():
    for _ in range(10):
        now = str(datetime.datetime.now())
        print("method222 {} ".format(now))
        await asyncio.sleep(1)
    print("completed method222")
    return


async def main():
    results = await asyncio.gather(request(), method2())
    print(len(results))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(request())
        loop.run_until_complete(loop.shutdown_asyncgens())
    finally:
        loop.close()
