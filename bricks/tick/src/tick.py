
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
            transport = AIOHTTPTransport(
                url='https://dbschool.alcyone.life/graphql')

            async with Client(transport=transport, fetch_schema_from_transport=True) as session:
                # Execute single query
                query = gql(
                    """
                        query {
                            tickers(where: { symbol_contains: "BTCUSDT" }) {
                                price
                                created_at
                            }
                        }
                    """
                )

                result = await session.execute(query)
                # print(result)

                listofdf = []

                # for item in result:
                #     histpricesdf = pd.DataFrame.from_dict(result)
                #     listofdf.append(histpricesdf)

                # dfs = [df.set_index('created_at') for df in listofdf]
                # histpriceconcat = pd.concat(dfs, axis=1)

                # print(histpriceconcat)
                # for i, col in enumerate(histpriceconcat.columns):
                #     histpriceconcat[col].plot()

                #     plt.title('Price Evolution Comparison')

                #     plt.xticks(rotation=70)
                #     plt.legend(histpriceconcat.columns)

                #     # Saving the graph into a JPG file
                #     plt.savefig('test.png', bbox_inches='tight')

            return aiohttp.web.json_response(result)

    except Exception as exp:
        raise exp

loop = asyncio.get_event_loop()
