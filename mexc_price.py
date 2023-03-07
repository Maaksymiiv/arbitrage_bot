import json
import aiohttp, asyncio

delete_list =["GMTUSDT", "DOGGOUSDT", "BRISEUSDT", "BABYDOGEUSDT", "GRVUSDT",
              "SQUIDGROWUSDT", "PLCUCUSDT", "PLCUUSDT", "PITUSDT", "VOLTUSDT", "MIRUSDT", "QIUSDT", "HEROUSDT", "UNQUSDT", "QUACKUSDT",
              "BPUSDT", "XSPECTARUSDT", "DIEUSDT", "VELOUSDT"]

async def get_mexc_prices():
    async with aiohttp.ClientSession() as session:
        url_vol = "https://api.mexc.com/api/v3/ticker/24hr"
        response = await session.get(url=url_vol, ssl=False)
        if response.status == 200:
            data = await response.json()
            result = []
            for item in data:
                symbol = item.get("symbol")
                if symbol not in delete_list and "USDT" in symbol:
                    last = float(item.get('lastPrice'))
                    ask_price = item.get('askPrice')
                    bid_price = item.get('bidPrice')
                    vol = int(item.get("volume").split(".")[0])
                    amt = last * vol
                    symbol_link = symbol[0:-4]
                    quote = symbol[-4:]
                    link = f"https://www.mexc.com/exchange/{symbol_link}_{quote}"
                    if amt > 30000 and "3" not in symbol and "5" not in symbol:
                        result.append(
                            {
                                "symbol": symbol,
                                "ask_price": ask_price,
                                "bid_price": bid_price,
                                "volume": amt,
                                "link": link
                            }
                        )
            with open(r"data\mexc_price.json", "w", encoding="utf-8") as file:
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
            with open(r"data\mexc_price.json", "w", encoding="utf-8") as file:
                json.dump(result, file, indent=4, ensure_ascii=False)

async def main():
    await get_mexc_prices()

if __name__ == '__main__':
    asyncio.run(main())