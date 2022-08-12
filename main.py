#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import os
from collections import defaultdict

import TelegramBot

enable = True
generalDict = defaultdict(list)
session = os.getenv('IMGUR_CLIENT_ID')


async def CallTelegramBotBasic(session):
    # dictItem = importModule
    # Logic TelegramBot
    print (type(TelegramBot.start))
    return


async def ActionFunction(generalDict):
    while enable:
        await asyncio.sleep(5)
        if len(generalDict) != 0:
            # Execute Action BatFile StartFile
            await asyncio.sleep(1000)


async def MainGeneralFunction(session, generalDict):
    await CallTelegramBotBasic(session)
    await ActionFunction(generalDict)


if __name__ == "__main__":
    MainGeneralFunction(session, generalDict)

    #######################################################
    ########################