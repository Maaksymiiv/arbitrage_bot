import json
import aiohttp, asyncio

async def get_bitrue_prices():
    async with aiohttp.ClientSession() as session:
        url = 'https://www.bitrue.com/api/v1/ticker/24hr'
        response = await session.get(url=url)
        data = await response.json()
        result = []
        for item in data:
            symbol = item.get('symbol')
            ask_price = item.get('askPrice')
            bid_price = item.get('bidPrice')
            volume = float(item.get('quoteVolume'))
            link = f'https://www.bitrue.com/trade/{symbol[0:-4].lower()}_usdt'

            if volume > 100000 and "USDT" in symbol and "3" not in symbol and "5" not in symbol:
                result.append(
                    {
                        "symbol": symbol,
                        "ask_price": ask_price,
                        "bid_price": bid_price,
                        "volume": volume,
                        "link": link
                    }
                )
        with open(r'data\bitrue_price.json', 'w', encoding='utf-8') as file:
            json.dump(result, file, indent=4, ensure_ascii=False)

async def main():
    await get_bitrue_prices()

if __name__ == '__main__':
    asyncio.run(main())

