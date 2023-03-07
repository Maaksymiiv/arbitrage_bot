import json
import aiohttp, asyncio

async def get_bitfinex_prices():
  async with aiohttp.ClientSession() as session:

    delete_list = ["fUSDT", "AMPUSDT"]

    url = "https://api-pub.bitfinex.com/v2/tickers?symbols=ALL"
    response = await session.get(url=url)
    if response.status == 200:
      data = await response.json()
      result = []
      for item in data:
        full_symbol = item[0]
        if "UST" in full_symbol:
          if ":" in full_symbol:
            symbol = full_symbol.split(":")[0].replace("F0", "").replace("t", "")
            ask_price = item[3]
            bid_price = item[1]
            volume = item[8]
          else:
            symbol = full_symbol[0:-3].replace("F0", "").replace("t", "")
            ask_price = item[3]
            bid_price = item[1]
            volume = item[8] * ask_price
          if symbol+"USDT" not in delete_list and volume > 100000:
            result.append(
              {
                "symbol": symbol+"USDT",
                "ask_price": ask_price,
                "bid_price": bid_price,
                "volume": volume,
                "link": f"https://trading.bitfinex.com/t/{symbol}:UST?type=exchange"
              }
            )
      with open(r"data\bitfinex_price.json", "w", encoding="utf-8") as file:
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
      with open(r"data\bitfinex_price.json", "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

async def main():
  await get_bitfinex_prices()

if __name__ == '__main__':
  asyncio.run(main())