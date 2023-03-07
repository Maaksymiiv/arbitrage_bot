import json
import aiohttp, asyncio

async def get_btcex_prices():
    async with aiohttp.ClientSession() as session:
        url = "https://api.btcex.com/api/v1/public/coin_gecko_spot_ticker"
        response = await session.get(url=url)
        all_data = await response.json()

        data = all_data.get('result')
        result = []
        for item in data:
            symbol = item.get('ticker_id')
            ask_price = item.get('ask')
            bid_price = item.get('bid')
            volume = float(item.get('target_volume'))
            link = f"https://www.btcex.com/en-us/spot/{symbol}-SPOT"

            if volume > 100000:
                result.append(
                    {
                        "symbol": symbol.replace('-', ""),
                        "ask_price": ask_price,
                        "bid_price": bid_price,
                        "volume": volume,
                        "link": link
                    }
                )
        with open(r'data\btcex_price.json', 'w', encoding='utf-8') as file:
            json.dump(result, file, indent=4, ensure_ascii=False)

async def main():
    await get_btcex_prices()

if __name__ == '__main__':
    asyncio.run(main())