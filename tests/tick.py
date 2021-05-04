from aiohttp import web
import aiohttp
import asyncio
from rich import print
from yaml import load, dump
from datetime import datetime
import requests


async def main():
    async with aiohttp.ClientSession() as session:
        # async with session.get('http://51.15.17.205:9000/tick/') as resp:

        #     info = await resp.json()
        #     info['timestamp'] = datetime.timestamp(datetime.now())

        #     data = dump(info)
        #     filename = f"./data/{datetime.now().isoformat()}.yaml"
        #     with open(filename, "w") as f:
        #         f.write(data)

        # return web.json_response(info)

        query = """mutation {
            createTicker(input: {data: {symbol: "TestJulien" , price: 600000}}) {
                ticker {
                    symbol
                    price
                }
            }
        }"""

        url = 'https://dbschool.alcyone.life/graphql'
        r = requests.post(url, json={'query': query})
        print(r.status_code)
        print(r.text)

loop = asyncio.get_event_loop()

loop.run_until_complete(main())

# run_until_complete(main())
