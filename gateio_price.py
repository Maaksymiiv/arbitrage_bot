import json
import aiohttp, asyncio
async def get_getio_prices():
    async with aiohttp.ClientSession() as session:
        url = "https://api.gateio.ws/api/v4/spot/tickers"

        delete_list = ["IOTAUSDT", "BRISEUSDT", "BABYDOGEUSDT", "ELTUSDT", "KISHUUSDT", "PLCUUSDT", "QUACKUSDT",
                       "DEGOUSDT", "GRVUSDT", "DATAUSDT", "PITUSDT", "BNCUSDT", "GFTUSDT", "SQUIDGROWUSDT", "QIUSDT", "FAMEUSDT", "UNQUSDT", "TORNUSDT"]
        response = await session.get(url=url)
        if response.status == 200:
            data = await response.json()
            result = []
            for item in data:
                symbol = item.get('currency_pair').replace("_", "")
                if "USDT" in symbol and "3" not in symbol:
                    ask_price = item.get('lowest_ask')
                    bid_price = item.get('highest_bid')
                    quote_volume = float(item.get('quote_volume'))

                    symbol_link = symbol[0:-4]
                    quote =  symbol[-4:]
                    link = f"https://www.gate.io/ru/trade/{symbol_link}_{quote}"
                    if quote_volume > 30000 and symbol not in delete_list and "5" not in symbol:
                        result.append(
                            {
                                "symbol": symbol,
                                "ask_price": ask_price,
                                "bid_price": bid_price,
                                "volume": quote_volume,
                                "link": link
                            }
                        )
            with open(r"data\gateio_price.json", "w", encoding="utf-8") as file:
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
            with open(r"data\gateio_price.json", "w", encoding="utf-8") as file:
                json.dump(result, file, indent=4, ensure_ascii=False)

async def main():
    await get_getio_prices()

if __name__ == '__main__':
    asyncio.run(main())
