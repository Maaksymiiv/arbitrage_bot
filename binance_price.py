import json
import aiohttp, asyncio

delete_binance_symbols_list = ["BTTUSDT", "MFTUSDT", "FTTUSDT", "BULLUSDT", "SRMUSDT", "HNTUSDT",
                               "TRIBEUSDT", "MCUSDT", "ACAUSDT", "ANCUSDT", "BIFIUSDT", "MIRUSDT", "CVCUSDT",
                               "TORNUSDT", "NBSUSDT", "MITHUSDT", "GTOUSDT", "REPUSDT", "BTGUSDT", "TCTUSDT",
                               "MDXUSDT", "CHRUSDT", "ASTRUSDT", "XEMUSDT"]

async def get_binance_prices():
    async with aiohttp.ClientSession() as session:
        url = "https://api.binance.com/api/v3/ticker/24hr"
        response = await session.get(url=url)
        if response.status == 200:
            data = await response.json()
            result = []
            for item in data:
                symbol = item.get('symbol')
                if symbol not in delete_binance_symbols_list:
                    bid_price = item.get('bidPrice')
                    ask_price = item.get('askPrice')
                    volume = float(item.get('volume'))
                    last_price = float(item.get('lastPrice'))
                    if volume != 0 and "USDT" in symbol:
                        result.append(
                            {
                                "symbol": symbol,
                                "bid_price": bid_price,
                                "ask_price": ask_price,
                                "volume": volume * last_price,
                                "link": f"https://www.binance.com/ru/trade/{symbol}?theme=dark&type=spot"
                            }
                        )

            with open(r"data\binance_price.json", "w", encoding="utf-8") as file:
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
            with open(r"data\binance_price.json", "w", encoding="utf-8") as file:
                json.dump(result, file, indent=4, ensure_ascii=False)

async def main():
    await get_binance_prices()

if __name__ == '__main__':
    asyncio.run(main())