from aiohttp import web
import aiohttp
import asyncio
from rich import print
from yaml import load, dump
from datetime import datetime


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://51.15.17.205:9000/tick/') as resp:

            info = await resp.json()
            info['timestamp'] = datetime.timestamp(datetime.now())

            data = dump(info)
            filename = f"./data/{datetime.now().isoformat()}.yaml"
            with open(filename, "w") as f:
                f.write(data)

        return web.json_response(info)

loop = asyncio.get_event_loop()

loop.run_until_complete(main())

# run_until_complete(main())
