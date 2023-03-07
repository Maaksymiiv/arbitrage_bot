import requests
import json
import aiohttp, asyncio

delete_list = ["ACAUSDT", "ICXUSDT", "MIRUSDT", "MANUSDT", "MCUSDT", "DEGOUSDT",
               "WMTUSDT", "BRISEUSDT", "HNTUSDT", "REVUUSDT", "AIUSDT", "CHRUSDT",
               "DSLAUSDT", "GFTUSDT", "BUYUSDT", "LOVEUSDT", "XEXMUSDT"]

async def get_kucoin_prices():
    async with aiohttp.ClientSession() as session:
        result_list = []
        url = "https://api.kucoin.com/api/v1/market/allTickers"
        response = await session.get(url=url)
        if response.status == 200:

            data = await response.json()

            all_symbols = data.get('data').get('ticker')
            for item in all_symbols:
                try:
                    symbol = item.get('symbol').replace("-", "")
                    last_price = item.get('last')
                    if symbol not in delete_list and "USDT" in symbol:
                        vol = int(item.get("volValue").split(".")[0])
                        ask_price = item.get('buy')
                        bid_price = item.get('sell')
                        symbol_link = symbol[0:-4]
                        quote = symbol[-4:]
                        link = f"https://www.kucoin.com/trade/{symbol_link}-{quote}"
                        if vol > 30000 and "3" not in symbol:
                            result_list.append(
                                {
                                    "symbol": symbol,
                                    "ask_price": ask_price,
                                    "bid_price": bid_price,
                                    "volume": vol,
                                    "link": link
                                }
                            )
                except:
                    continue

            with open(r"data\kucoin_price.json", "w", encoding="utf-8") as file:
                json.dump(result_list, file, indent=4, ensure_ascii=False)
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
            with open(r"data\kucoin_price.json", "w", encoding="utf-8") as file:
                json.dump(result, file, indent=4, ensure_ascii=False)

async def main():
    await get_kucoin_prices()

if __name__ == '__main__':
    asyncio.run(main())