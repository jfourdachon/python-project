
from aiohttp import web
import aiohttp
import asyncio
from rich import print
from yaml import load, dump
from datetime import datetime


async def _tick_():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://51.15.17.205:9000/tick/') as resp:
            print(resp.status)
            print(await resp.text())
            info = await resp.json()

        return aiohttp.web.json_response(info)

loop = asyncio.get_event_loop()


async def tick_all(request):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://51.15.17.205:9000/tick/Julien') as resp:
            
                info = await resp.json()
                info['timestamp'] = datetime.timestamp(datetime.now())
                data = dump(info)
                filename = f"./tick/data/{datetime.now()}.yaml"
                with open(filename, "w") as f:
                    f.write(data)
                
        return aiohttp.web.json_response(info)

    except Exception as exp:
        raise exp

loop = asyncio.get_event_loop()
