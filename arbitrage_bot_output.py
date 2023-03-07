import json
from aiogram import types, Dispatcher
from aiogram.utils.markdown import hbold, hlink
from aiogram.dispatcher import FSMContext
import emoji
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

#get prices
from binance_price import get_binance_prices
from kucoin_price import get_kucoin_prices
from bybit_price import  get_bybit_prices
from huobi_price import get_huobi_prices
from okx_price import get_okx_prices
from mexc_price import get_mexc_prices
from gateio_price import get_getio_prices
from bitfinex_price import get_bitfinex_prices
from bitmart_price import get_bitmart_prices
from bitget_price import get_bitget_prices
from lbank_price import get_lbank_prices
from xtcom_price import get_xtcom_prices

#get spred
from find_arbitrage.find_arbitrage import get_arbitrage

white_users = [5153991526, 637548689, 676132376]


# @dp.message_handler(Text(equals="Find Arbitrage"))
async def all_arbitrage(message: types.Message, state: FSMContext):
    while (await state.get_data()).get("parsing_continue"):

        if message.from_user.id in white_users:
            rem = types.ReplyKeyboardRemove()
            await message.answer("please wait...", reply_markup=rem)

            #all function get prices
            await get_binance_prices()
            await get_kucoin_prices()
            await get_bybit_prices()
            await get_huobi_prices()
            await get_okx_prices()
            await get_mexc_prices()
            await get_getio_prices()
            await get_bitfinex_prices()
            await get_bitmart_prices()
            await get_bitget_prices()
            await get_lbank_prices()
            await get_xtcom_prices()

            #open all price files
            with open(r"data\binance_price.json", "r", encoding="utf-8") as file:
                binance_data = json.load(file)
            with open(r"data\kucoin_price.json", "r", encoding="utf-8") as file:
                kucoin_data = json.load(file)
            with open(r"data\bybit_price.json", "r", encoding="utf-8") as file:
                bybit_data = json.load(file)
            with open(r"data\huobi_price.json", "r", encoding="utf-8") as file:
                huobi_data = json.load(file)
            with open(r"data\okx_price.json", "r", encoding="utf-8") as file:
                okx_data = json.load(file)
            with open(r"data\mexc_price.json", "r", encoding="utf-8") as file:
                mexc_data = json.load(file)
            with open(r"data\gateio_price.json", "r", encoding="utf-8") as file:
                gateio_data = json.load(file)
            with open(r"data\bitfinex_price.json", "r", encoding="utf-8") as file:
                bitfinex_data = json.load(file)
            with open(r"data\bitmart_price.json", "r", encoding="utf-8") as file:
                bitmart_data = json.load(file)
            with open(r"data\bitget_price.json", "r", encoding="utf-8") as file:
                bitget_data = json.load(file)
            with open(r"data\lbank_price.json", "r", encoding="utf-8") as file:
                lbank_data = json.load(file)
            with open(r"data\xtcom.price.json", "r", encoding="utf-8") as file:
                xt_data = json.load(file)

            #function output
            async def output_message(first_data, twice_data, firstex, twicex):
                get_arbitrage(first_data, twice_data, firstex, twicex)
                with open(r"data\spred.json", "r", encoding="utf-8") as file:
                    spred = json.load(file)
                for item in spred:
                    spred = item.get('spred')
                    if float(spred) > 5:
                        em = emoji.emojize(':money-mouth_face:')
                    else:
                        em = ''
                    if item.get("ex1") == firstex:
                        await message.answer(f"{em}{hbold(firstex)} -> {hbold(twicex)}\n\n"
                                             f"{hbold(firstex)} {hlink(item.get('symbol'), item.get(firstex+'_link'))}:\n"
                                             f"{hbold('Ask: ')} {hbold(item.get(firstex+'_price'))}\n"
                                             f"{hbold('Volume: ')} {hbold(item.get(firstex+'_volume'))}\n"
                                             f"{hbold('Liquidity: ')} {hbold(item.get(firstex+'_order_book'))} USDT\n\n"
                                             f"{hbold(twicex)} {hlink(item.get('symbol'), item.get(twicex+'_link'))}:\n"
                                             f"{hbold('Bid: ')} {hbold(item.get(twicex+'_price'))}\n"
                                             f"{hbold('Volume: ')} {hbold(item.get(twicex+'_volume'))}\n"
                                             f"{hbold('Liquidity: ')} {hbold(item.get(twicex+'_order_book'))} USDT\n\n"
                                             f"{hbold('SPRED: +')} {hbold(item.get('spred'))}%", disable_web_page_preview=True)
                    else:
                        await message.answer(f"{em}{hbold(twicex)} -> {hbold(firstex)}\n\n"
                                             f"{hbold(twicex)} {hlink(item.get('symbol'), item.get(twicex+'_link'))}:\n"
                                             f"{hbold('Ask: ')} {hbold(item.get(twicex + '_price'))}\n"
                                             f"{hbold('Volume: ')} {hbold(item.get(twicex + '_volume'))}\n"
                                             f"{hbold('Liquidity: ')} {hbold(item.get(twicex+'_order_book'))} USDT\n\n"
                                             f"{hbold(firstex)} {hlink(item.get('symbol'), item.get(firstex+'_link'))}:\n"
                                             f"{hbold('Bid: ')} {hbold(item.get(firstex + '_price'))}\n"
                                             f"{hbold('Volume: ')} {hbold(item.get(firstex + '_volume'))}\n"
                                             f"{hbold('Liquidity: ')} {hbold(item.get(firstex+'_order_book'))} USDT\n\n"
                                             f"{hbold('SPRED: +')} {hbold(item.get('spred'))}%", disable_web_page_preview=True)

            #BINANCE AND KUCOIN
            await output_message(binance_data, kucoin_data, "Binance", "Kucoin")

            #BINANCE AND BYBIT
            await output_message(binance_data, bybit_data, "Binance", "Bybit")

            # #BINANCE AND HUOBI
            await output_message(binance_data, huobi_data, "Binance", "Huobi")

            # #BINANCE AND OKX
            await output_message(binance_data, okx_data, "Binance", "OKX")

            # #BINANCE AND MEXC
            await output_message(binance_data, mexc_data, "Binance", "Mexc")

            #BINANCE AND GATEIO
            await output_message(binance_data, gateio_data, "Binance", "GateIo")

            #BINANCE AND BITFINEX
            await output_message(binance_data, bitfinex_data, "Binance", "Bitfinex")

            #BINANCE AND BITMART
            await output_message(binance_data, bitmart_data, "Binance", "Bitmart")

            #BINANCE AND BITGET
            await output_message(binance_data, bitget_data, "Binance", "Bitget")

            #BINANCE AND LATOKEN
            await output_message(binance_data, lbank_data, "Binance", "Lbank")

            #BINANCE AND XT
            await output_message(binance_data, xt_data, "Binance", "XT")

            # #KUKOIN AND BYBIT
            await output_message(kucoin_data, bybit_data, "Kucoin", "Bybit")

            # #KUCOIN AND HUOBI
            await output_message(kucoin_data, huobi_data, "Kucoin", "Huobi")

            # #KUCOIN AND OKX
            await output_message(kucoin_data, okx_data, "Kucoin", "OKX")

            # #KUCOIN AND MEXC
            await output_message(kucoin_data, mexc_data, "Kucoin", "Mexc")

            #KUCOIN AND GATEIO
            await output_message(kucoin_data, gateio_data, "Kucoin", "GateIo")

            #KUCOIN AND BITFINEX
            await output_message(kucoin_data, bitfinex_data, "Kucoin", "Bitfinex")

            #KUCOIN AND BITMART
            await output_message(kucoin_data, bitmart_data, "Kucoin", "Bitmart")

            #KUCOIN AND BITGET
            await output_message(kucoin_data, bitget_data, "Kucoin", "Bitget")

            #KUCOIN AND LATOKEN
            await output_message(kucoin_data, lbank_data, "Kucoin", "Lbank")

            #KUCOIN AND XT
            await output_message(kucoin_data, xt_data, "Kucoin", "XT")

            # #BYBIT AND HUOBI
            await output_message(bybit_data, huobi_data, "Bybit", "Huobi")

            # #BYBIT AND OKX
            await output_message(bybit_data, huobi_data, "Bybit", "OKX")

            # #BYBIT AND MEXC
            await output_message(bybit_data, mexc_data, "Bybit", "Mexc")

            #BYBIT AND GATEIO
            await output_message(bybit_data, gateio_data, "Bybit", "GateIo")

            #BYBIT AND BITFINEX
            await output_message(bybit_data, bitfinex_data, "Bybit", "Bitfinex")

            #BYBIT AND BITMART
            await output_message(bybit_data, bitmart_data, "Bybit", "Bitmart")

            #BYBIT AND BITGET
            await output_message(bybit_data, bitget_data, "Bybit", "Bitget")

            #BYBIT AND LATOKEN
            await output_message(bybit_data, lbank_data, "Bybit", "Lbank")

            #BYBIT AND XT
            await output_message(bybit_data, xt_data, "Bybit", "XT")

            # #HUOBI AND OKX
            await output_message(huobi_data, okx_data, "Huobi", "OKX")

            # #HUOBI AND MEXC
            await output_message(huobi_data, mexc_data, "Huobi", "Mexc")

            # #HUOBI AND GATEIO
            await output_message(huobi_data, gateio_data, "Huobi", "GateIo")

            #HUOBI ABD BITFINEX
            await output_message(huobi_data, bitfinex_data, "Huobi", "Bitfinex")

            #HUOBI AND BITMART
            await output_message(huobi_data, bitmart_data, "Huobi", "Bitmart")

            #HUOBI AND BITGET
            await output_message(huobi_data, bitget_data, "Huobi", "Bitget")

            #HUOBI AND LATOKEN
            await output_message(huobi_data, lbank_data, "Huobi", "Lbank")

            #HUOBI AND XT
            await output_message(huobi_data, xt_data, "Huobi", "XT")

            #OKX AND MEXC
            await output_message(okx_data, mexc_data, "OKX", "Mexc")

            #OKX AND GATEIO
            await output_message(okx_data, gateio_data, "OKX", "GateIo")

            #OKX AND BITFINEX
            await output_message(okx_data, bitfinex_data, "OKX", "Bitfinex")

            #OKX AND BITMART
            await output_message(okx_data, bitmart_data, "OKX", "Bitmart")

            #OKX AND BITGET
            await output_message(okx_data, bitget_data, "OKX", "Bitget")

            #OKX AND LATOKEN
            await output_message(okx_data, lbank_data, "OKX", "Lbank")

            #OKX AND XT
            await output_message(binance_data, xt_data, "OKX", "XT")

            #MEXC AND GATEIO
            await output_message(mexc_data, gateio_data, "Mexc", "GateIo")

            #MEXC AND BITFINEX
            await output_message(mexc_data, bitfinex_data, "Mexc", "Bitfinex")

            #MEXC AND BITMART
            await output_message(mexc_data, bitmart_data, "Mexc", "Bitmart")

            #MEXC AND BITGET
            await output_message(mexc_data, bitget_data, "Mexc", "Bitget")

            #MEXC AND LATOKEN
            await output_message(mexc_data, lbank_data, "Mexc", "Lbank")

            #MEXC AND XT
            await output_message(mexc_data, xt_data, "Mexc", "XT")

            #GATEIO AND BITFINEX
            await output_message(gateio_data, bitfinex_data, "GateIo", "Bitfinex")

            #GATEIO AND BITMART
            await output_message(gateio_data, bitmart_data, "GateIo", "Bitmart")

            #GATEIO AND BITGET
            await output_message(gateio_data, bitget_data, "GateIo", "Bitget")

            #GATEIO AND LATOKEN
            await output_message(gateio_data, lbank_data, "GateIo", "Lbank")

            #GATEIO AND XT
            await output_message(gateio_data, xt_data, "GateIo", "XT")

            #BITFINEX AND BITMART
            await output_message(bitmart_data, bitmart_data, "Bitfinex", "Bitmart")

            #BITFINEX AND BITGET
            await output_message(bitfinex_data, bitget_data, "Bitfinex", "Bitget")

            #BITFINEX AND LATOKEN
            await output_message(bitfinex_data, lbank_data, "Bitfinex", "Lbank")

            #BITFINEX AND XT
            await output_message(bitfinex_data, xt_data, "Bitfinex", "XT")

            #BITMART AND BITGET
            await output_message(bitmart_data, bitget_data, "Bitmart", "Bitget")

            #BITMART AND BITGET
            await output_message(bitmart_data, lbank_data, "Bitmart", "Lbank")

            #BITMART AND XT
            await output_message(bitmart_data, xt_data, "Bitmart", "XT")

            #BITGETAND LATOKEN
            await output_message(bitget_data, lbank_data, "Bitget", "Lbank")

            #BITGET AND XT
            await output_message(bitget_data, xt_data, "Bitget", "XT")

            #LBANK AND XT
            await output_message(lbank_data, xt_data, "Lbank", "XT")

            but_s = KeyboardButton('/start')
            sb = ReplyKeyboardMarkup(resize_keyboard=True).add(but_s)

            if (await state.get_data()).get('parsing_continue'):
                sb = ReplyKeyboardRemove()

            await message.answer("Its done!!", reply_markup=sb)
        else:
            await message.answer('You don`t have access to the bot, contact the owner @maksymiiv')
            break

def register_handler_output(dp: Dispatcher):
    dp.register_message_handler(all_arbitrage, commands='findArbitrage')