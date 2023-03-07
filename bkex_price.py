import json
import aiohttp, asyncio

delete_list = ["LDOUSDT", "ANKRUSDT", "TRUUSDT", "LDOUSDT", "QUACKUSDT", "FONUSDT", "NEOUSDT", "BABYDOGEUSDT", "RIAUSDT", "FXSUSDT", "APTUSDT"]

async def get_bkex_prices():
    async with aiohttp.ClientSession() as session:
        url = "https://api.bkex.com/v2/q/tickers"
        response = await session.get(url=url)
        all_data = await response.json()

        data = all_data.get('data')
        result = []
        for item in data:
            symbol = item.get('symbol')
            full_symbol = symbol.replace("_", "")
            ask_price = item.get('close')
            bid_price = item.get('open')
            vol = float(item.get('volume')) * float(bid_price)
            link = f'https://www.bkex.com/trade/{symbol}'

            if "USDT" in symbol and vol > 100000 and "3" not in symbol and "5" not in symbol and full_symbol not in delete_list:
                result.append(
                    {
                        "symbol": full_symbol,
                        "ask_price": ask_price,
                        "bid_price": bid_price,
                        "volume": vol,
                        "link": link
                    }
                )
        with open(r'data\bkex_price.json', "w", encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)


async def main():
    await get_bkex_prices()

if __name__ == '__main__':
    asyncio.run(main())
