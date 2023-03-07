import json
import aiohttp, asyncio

delete_list = ["XNOUSDT", "HTRUSDT", "SSVUSDT", "BABYDOGEUSDT", "BRISEUSDT", "SRMUSDT", "GRVUSDT", "VELOUSDT", "BABYUSDT", "XEMUSDT"]

async def get_huobi_prices():
    async with aiohttp.ClientSession() as session:

        url = "https://api.huobi.pro/market/tickers"

        response = await session.get(url=url)
        if response.status == 200:
            data = await response.json()

            all_symbols = data.get('data')
            result_list = []
            for item in all_symbols:
                symbol = item.get('symbol').upper()
                if symbol not in delete_list and "USDT" in symbol:
                    bid_price = item.get('bid')
                    ask_price = item.get('ask')
                    vol = item.get('vol')
                    symbol_link = symbol[0:-4].lower()
                    quote = symbol[-4:].lower()
                    link = f"https://www.huobi.com/uk-ua/exchange/{symbol_link}_{quote}"
                    if bid_price is not None and vol > 30000:
                        result_list.append(
                            {
                                "symbol": symbol,
                                "ask_price": ask_price,
                                "bid_price": bid_price,
                                "volume": vol,
                                "link": link
                            }
                        )

            with open(r"data\huobi_price.json", "w", encoding="utf-8") as file:
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
            with open(r"data\huobi_price.json", "w", encoding="utf-8") as file:
                json.dump(result, file, indent=4, ensure_ascii=False)

#
async def main():
    await get_huobi_prices()

if __name__ == '__main__':
    asyncio.run(main())