
from aiohttp import web
import aiohttp
import asyncio
from rich import print
from yaml import load, dump
from datetime import datetime
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import pandas as pd
import matplotlib.pyplot as plt


async def _tick_(request):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://51.15.17.205:9000/tick/Julien') as resp:
            print(resp.status)
            print(await resp.text())
            info = await resp.json()
            response = await resp.json()

            transport = AIOHTTPTransport(
                url='https://dbschool.alcyone.life/graphql')

            async with Client(transport=transport, fetch_schema_from_transport=True) as session:
                print(response)
                for value in response['data']:
                        # Execute single query
                        query = gql(
                            """
                                mutation {
                                  createTicker(input: { data: { symbol: "%s", price: %.2f } }) {
                                    ticker {
                                      symbol
                                      price
                                    }
                                  }
                                }
                            """ % (value['symbol'], float(value['price']))
                        )

                        result = await session.execute(query)
                        print(result)
#
                return aiohttp.web.json_response(dict(json=response))
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


async def plot(request):
    try:
        async with aiohttp.ClientSession() as session:

            req_param = request.rel_url.query['symbol'].split(',') if request.rel_url.query else ["1INCHUSDT", "1INCHDOWNUSDT", "1INCHBUSD", "1INCHUSDT"] 
            req = await request.json() if request.body_exists else {"symbol": req_param}
            print("*************", req["symbol"])
            transport = AIOHTTPTransport(url='https://dbschool.alcyone.life/graphql')
            client = Client(transport=transport, fetch_schema_from_transport=True)

            listofdf = []
            for symbol in req["symbol"]:
                query = gql("""query {
                                tickers(where: { symbol_contains: "%s" }) {
                                    price
                                    created_at
                                }
                            }""" % symbol
                        ) 

                result = await client.execute_async(query)
                histprices = result['tickers']

                histpricesdf = pd.DataFrame.from_dict(histprices)
                histpricesdf = histpricesdf.rename({'price': symbol}, axis=1)
                listofdf.append(histpricesdf)

            dfs = [df.set_index('created_at') for df in listofdf]
            histpriceconcat = pd.concat(dfs, axis=1)
            
            for i, col in enumerate(histpriceconcat.columns):
                histpriceconcat[col].plot()

            plt.title('Price Evolution Comparison')
            plt.xticks(rotation=70)
            plt.legend(histpriceconcat.columns)
            filename = '.'.join([ '-'.join(req["symbol"]), 'png'])
            file_path = f"./tick/plots/{filename}"
            plt.savefig(file_path, bbox_inches='tight')

        return aiohttp.web.FileResponse(f'./{file_path}')
        # return aiohttp.web.json_response(dict(json=result))
    except Exception as e:
        print(e)
        raise e

loop = asyncio.get_event_loop()
