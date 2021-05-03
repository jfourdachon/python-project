
from aiohttp import web
import aiohttp
import asyncio
from rich import print

async def _tick_():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://51.15.17.205:9000/tick/') as resp:
            print(resp.status)
            print(await resp.text())


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

    # $>
    # except Exception as exp:
    # # <!
    #     # !0 return what's wrong in string and the type of the exception should be enough to understand where you're wrong noobs
    #     return web.json_response({'err':{'str':str(exp),'typ':str(type(exp))}}, status=500)
# `< - - - - - - - - - - - -
