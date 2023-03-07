import json
import aiohttp, asyncio

delete_list = ["FIDAUSDT", "CTXCUSDT", "IRISUSDT", "XECUSDT", "CMPUSDT", "RPLUSDT", "ETHFUSDT", "ACAUSDT", "CELRUSDT",
               'HOTUSDT', "LOOKSUSDT", "CELRUSDT", "TUSDT", "NKNUSDT", "RLCUSDT", "WTCUSDT", "ARDRUSDT", "RUNEUSDT", "TRUUSDT",
               "TVKUSDT", "AMPUSDT", "OSMOUSDT", "LOOKSUSDT", "TELUSDT", "RLCUSDT", "DFIUSDT", "RAREUSDT", "DUSKUSDT", "ANTUSDT", "CHRUSDT",
               "PHAUSDT", "AGIXUSDT", "DUSKUSDT", "FISUSDT", "PHAUSDT", "ETHWUSDT", "PONDUSDT", "ENJUSDT", "AERGOUSDT", "PIUSDT",
               "FEGUSDT", "GEARUSDT", "XEMUSDT"]

async def get_xtcom_prices():
    async with aiohttp.ClientSession() as session:
        url = "https://sapi.xt.com/v4/public/ticker"
        response = await session.get(url=url)
        if response.status == 200:

            all_data = await response.json()

            data = all_data.get('result')
            result = []
            for item in data:
                symbol = item.get('s')
                ask_price = item.get('ap')
                bid_price = item.get('bp')
                volume = float(item.get('v'))
                link = f"https://www.xt.com/tradePro/{symbol}"
                if volume > 30000 and "usdt" in symbol and "3" not in symbol.upper().replace('_', '') not in delete_list:
                    result.append(
                        {
                            "symbol": symbol.upper().replace('_', ''),
                            "ask_price": ask_price,
                            "bid_price": bid_price,
                            "volume": volume,
                            "link": link
                        }
                    )
            with open(r'data\xtcom.price.json', 'w', encoding='utf-8') as file:
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
            with open(r"data\xtcom.price.json", "w", encoding="utf-8") as file:
                json.dump(result, file, indent=4, ensure_ascii=False)

async def main():
    await get_xtcom_prices()

if __name__ == '__main__':
    asyncio.run(main())

