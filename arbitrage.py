import time
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from arbitrage_bot_output import register_handler_output
from aiogram.dispatcher.filters.state import State, StatesGroup

stared_time = time.time()

logging.basicConfig(level=logging.INFO)
bot = Bot(token="5536388865:AAG5UFhyTxOKaRqYa_ATMDrjUzm7duJWGvk", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

def get_keyboad() -> ReplyKeyboardMarkup:
    find_arbitrage_button = "/findArbitrage"
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton(find_arbitrage_button))
    return kb

state: FSMContext

class F(StatesGroup):
    liq = State()
    spr = State()

@dp.message_handler(commands="start")
async def start(message: types.Message, state: FSMContext):
    await state.update_data({"parsing_continue": True})
    with open(r"data\liq.txt", "r", encoding="utf-8") as file:
        liquid = file.read()
    with open(r"data\spr.txt", "r", encoding="utf-8") as file:
        spred = file.read()
    await message.reply("Hi arbitrager!\n"
                        f"Yor setting:\nligudity - {liquid}\n"
                        f"spred - {spred}\n\n"
                        f"click /setting to change minimal liquidity and spred\n", reply_markup=get_keyboad())

register_handler_output(dp)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

@dp.message_handler(commands="setting", state=None)
async def setting(message: types.Message):
    await F.liq.set()
    await message.answer("Enter minimal liquidity", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state=F.liq)
async def ge_liquidity(message: types.Message, state: FSMContext):
    if is_number(message.text):
        if float(message.text) > 0:
            await state.update_data({"liq": int(message.text)})
            async with state.proxy() as data:
                data['liq'] = message.text
            await message.reply(f"Successful, you value of liquidity is")
    else:
        await message.reply("wrong... you don`t enter a number and you value of liquidity set automatic on 1000")
        async with state.proxy() as data:
            data['liq'] = 1000
        await state.update_data({'liq': 1000})
    await F.next()
    await message.answer("Enter minimal spred(%)")

@dp.message_handler(state=F.spr)
async def get_spred(message: types.Message, state: FSMContext):
    if is_number(message.text):
        if float(message.text) > 0:
            await state.update_data({'spr': float(message.text), 'parsing_continue': True})
            async with state.proxy() as data:
                data['spr'] = message.text
            await message.reply(f"Successful, you value of spred is %", reply_markup=get_keyboad())
    else:
        await message.reply("wrong... you don`t enter a number and you value of spred set automatic on 3%", reply_markup=get_keyboad())
        async with state.proxy() as data:
            data['spr'] = 3
        await state.update_data({'spr': 3, 'parsing-continue:': True})

    async with state.proxy() as data:
        liquid = data['liq']
        spr = data['spr']
    with open(r'data\liq.txt', "w", encoding='utf-8') as file:
        file.write(liquid)
    with open(r'data\spr.txt', "w", encoding='utf-8') as file:
        file.write(spr)

    await state.reset_state(with_data=False)

@dp.message_handler(commands="stop")
async def stop_parsing(message: types.Message, state: FSMContext):
    await state.update_data({"parsing_continue": False})
    await message.reply("Bot stopped")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)