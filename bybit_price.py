import json
import aiohttp, asyncio

delete_symbols = ["MAGICUSDT", "AUDIOUSDT", "RNDRUSDT", "REEFUSDT"]

async def get_bybit_prices():
    async with aiohttp.ClientSession() as session:
        url = 'https://api-testnet.bybit.com/derivatives/v3/public/tickers?category=linear'
        resp = await session.get(url=url)
        if resp.status == 200:
            data = await resp.json()

            all_symbols = data.get('result').get('list')
            result_list = []
            for item in all_symbols:
                symbol = item.get("symbol")
                price = item.get("markPrice")
                ask_price = item.get("askPrice")
                bid_price = item.get("bidPrice")
                symbol_link = symbol[0:-4]
                quote = symbol[-4:]
                link = f"https://www.bybit.com/uk-UA/trade/spot/{symbol_link}/{quote}"
                if symbol not in delete_symbols and "USDT" in symbol:
                    result_list.append(
                        {
                            "symbol": symbol,
                            "bid_price": bid_price,
                            "ask_price": ask_price,
                            "volume": "-",
                            "link": link
                        }
                    )
            with open(r"data\bybit_price.json", "w", encoding="utf-8") as file:
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
            with open(r"data\bybit_price.json", "w", encoding="utf-8") as file:
                json.dump(result, file, indent=4, ensure_ascii=False)

async def main():
    await get_bybit_prices()


if __name__ == '__main__':
    asyncio.run(main())