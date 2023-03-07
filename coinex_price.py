import json
import aiohttp, asyncio

async def get_coinex_prices():
    async with aiohttp.ClientSession() as session:
        url = "https://api.coinex.com/v1/market/ticker/all"
        response = await session.get(url=url)
        all_data = await response.json()

        data = all_data.get('data').get('ticker')
        result = []
        for item in data:
            symbol = item
            ticker = data.get(item)

            ask_price = ticker.get('sell')
            bid_price = ticker.get('buy')
            volume = float(ticker.get('vol')) * float(bid_price)
            link = f'https://www.coinex.com/exchange/{symbol[0:-4].lower()}-usdt'
            if "USDT" in symbol and volume > 100000:
                result.append(
                    {
                        "symbol": symbol,
                        "ask_price": ask_price,
                        "bid_price": bid_price,
                        "volume": volume,
                        "link": link
                    }
                )
        with open(r'data\coinex_price.json', 'w', encoding='utf-8') as file:
            json.dump(result, file, indent=4, ensure_ascii=False)

async def main():
    await get_coinex_prices()

if __name__ == '__main__':
    asyncio.run(main())
