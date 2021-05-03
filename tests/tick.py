from aiohttp import web
import aiohttp
import asyncio
from rich import print

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://51.15.17.205:9000/tick/') as resp:
            print(resp.status)
            print(await resp.text())


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
