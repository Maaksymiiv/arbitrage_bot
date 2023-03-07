import json
import aiohttp, asyncio

delete_list = ["TABOOUSDT"]

async def get_whitebit_prices():
    async with aiohttp.ClientSession() as session:

        url = "https://whitebit.com/api/v1/public/tickers"
        response = await session.get(url=url)
        if response.status == 200:
            data = await response.json()
            symbols = data.get('result')
            result = []
            for item in symbols:
                if "USDT" in item:
                    symbol = item.replace("_", "")
                    tick = symbols.get(item)
                    ticker = tick.get('ticker')

                    ask_price = ticker.get('ask')
                    bid_price = ticker.get('bid')
                    volume = float(ticker.get('deal'))

                    symbol_link = symbol[0:-4]
                    link = f'whitebit.com/ua/trade/{symbol_link}-USDT?type=spot'

                    if volume > 100000 and symbol not in delete_list:
                        result.append(
                            {
                                "symbol": symbol,
                                "ask_price": ask_price,
                                "bid_price": bid_price,
                                "volume": volume,
                                "link": link
                            }
                        )
            with open(r"data\whitebit_price.json", "w", encoding="utf-8") as file:
                json.dump(result, file, indent=4, ensure_ascii=False)
        else:
            result = []
            result.append(
                {
                    "symbol": "-",
                    "ask_price": "-",
                    "bid_price": "-",
                    "volume": 0,
                    "link": "-"
                }
            )
            with open(r"data\okx_price.json", "w", encoding="utf-8") as file:
                json.dump(result, file, indent=4, ensure_ascii=False)


async def main():
    await get_whitebit_prices()

if __name__ == "__main__":
    asyncio.run(main())