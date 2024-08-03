from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from . import keyboards as kb
from app.database import requests as rq
import requests
import asyncio
from main import bot
from aiogram.exceptions import TelegramBadRequest
 

async def parse(url):

    res = await asyncio.to_thread(requests.get, url)
    return res.json()


router = Router()



@router.message(CommandStart())
async def start_command(message: Message):
    if await rq.check_user(message.from_user.id):
        
        dota_id = await rq.get_dota_id(message.from_user.id)
        await message.delete()

        await message.answer(text=f'Ваш DOTA ID: {dota_id}', reply_markup=kb.main_panel)
    else:
        await message.delete()
        await message.answer(text=f'Привет 👋\nЯ бот, который поможет тебе в Dota2 \nЯ анализирую твою историю, собираю активные данные и подсказываю как лучше 😇\nСначала мне нужно узнать твой DOTA ID', reply_markup=kb.start_panel)

@router.callback_query(F.data == 'what')
async def what(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(text=f'DOTA ID – это код вашего профиля, по которому вас можно будет найти.', reply_markup=kb.what_panel)
    

    
class Register(StatesGroup):
    tg_id = State()
    dota_id = State()
    
class Update(StatesGroup):
    dota_id = State()
    
class Hwr(StatesGroup):
    heroname = State()
    
class Odh(StatesGroup):
    heronames = State()
    
@router.message(F.text == 'Изменить DOTA ID')
async def change(message: Message, state: FSMContext):
    await state.set_state(Update.dota_id)
    await message.delete()
    await message.answer(text=f'Введите новый DOTA ID:')


@router.message(Update.dota_id)
async def finish_change(message: Message, state: FSMContext):
    await rq.update_dota_id(message.from_user.id, message.text)
    dota_id = await rq.get_dota_id(message.from_user.id)
    try:
        for i in range(message.message_id, 0, -1):
            await bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest as ex:
        if ex.message == "Bad Request: message to delete not found":
            await message.answer(text=f'Ваш DOTA ID: {dota_id}', reply_markup=kb.main_panel)
            await state.clear()


@router.callback_query(F.data == 'start')
async def start(callback: CallbackQuery, state: FSMContext):
    
    await callback.message.delete()
    await state.set_state(Register.dota_id)
    await callback.message.answer(text=f'Отправьте свой DOTA ID:')
    
@router.message(Register.dota_id)
async def dota_id(message: Message, state: FSMContext):
    if message.text:
        try:
            for i in range(message.message_id, 0, -1):
                await bot.delete_message(message.from_user.id, i)
        except TelegramBadRequest as ex:
            if ex.message == "Bad Request: message to delete not found":
                
                await rq.set_user(tg_id=message.from_user.id, dota_id=message.text)
                dota_id = await rq.get_dota_id(message.from_user.id)
                await message.answer(text=f'Ваш DOTA ID: {dota_id}', reply_markup=kb.main_panel)
                await state.clear()
    else:
        await message.answer(text='Необходимо отправить DOTA ID.', reply_markup=kb.repeat_id)



@router.message(F.text == 'Анализ истории игр')
async def first(message: Message):

    dota_id = await rq.get_dota_id(message.from_user.id)
    await message.delete()
    mes = await message.answer(text=f'Обрабатываем ваш запрос\nПожалуйста, подождите 😇')
    text = await parse(f'http://77.73.132.75/DotaApi.DOTAApi/userHistoryAnalysis?playerid={dota_id}')
    await bot.delete_message(message.chat.id, mes.message_id)

    await message.answer(text=text.get('result'), reply_markup=kb.main_panel)


@router.message(F.text == 'Анализ винрейта')
async def second(message: Message):
    dota_id = await rq.get_dota_id(message.from_user.id)
    await message.delete()
    mes = await message.answer(text=f'Обрабатываем ваш запрос\nПожалуйста, подождите 😇')

    text = await parse(f'http://77.73.132.75/DotaApi.DOTAApi/analyzeHeroWinRates?playerid={dota_id}')
    await bot.delete_message(message.chat.id, mes.message_id)

    await message.answer(text=text.get('result'), reply_markup=kb.main_panel)

    
    
@router.message(F.text == 'Прогноз победы на герое')
async def thethy(message: Message, state: FSMContext):
    await message.delete()
    await state.set_state(Hwr.heroname)
    await message.answer(text=f'Отправьте имя героя\nпример: lina')
    
  
@router.message(Hwr.heroname)
async def thethys(message: Message, state: FSMContext):
    dota_id = await rq.get_dota_id(message.from_user.id)
    heroname = message.text
    mes = await message.answer(text=f'Обрабатываем ваш запрос\nПожалуйста, подождите 😇')

    text = await parse(f'http://77.73.132.75/DotaApi.DOTAApi/analyzeHeroWinRatesAndPredictSuccess?playerid={dota_id}&heroname={heroname}')
    
    await bot.delete_message(message.chat.id, mes.message_id)

    await message.answer(text=text.get('result'), reply_markup=kb.main_panel)
    await state.clear()
    
@router.message(F.text == 'Оптимальный драфт героев')
async def forthy(message: Message, state: FSMContext):
    await message.delete()

    await state.set_state(Hwr.heroname)
    await message.answer(text=f'Оправьте имена героев противника через запятую\nпример: slark, anti-mag, lion, witch-doctor, lina')
    

@router.message(Odh.heronames)
async def forthys(message: Message, state: FSMContext):

    heronames = list((message.text).split(','))
    q = ''
    async for name in heronames:
        q += f'{name}%2C%20'
    mes = await message.answer(text=f'Обрабатываем ваш запрос\nПожалуйста, подождите 😇')

    dota_id = await rq.get_dota_id(message.from_user.id)
    text = await parse(f'http://77.73.132.75/DotaApi.DOTAApi/OptimalDraftHeroRecommender?playerid={dota_id}&Enemydraft={q}')
    await bot.delete_message(message.chat.id, mes.message_id)

    await message.answer(text=text.get('result'), reply_markup=kb.main_panel)
    await state.clear() 
    

@router.message()
async def star(message: Message):
    await message.answer('Данной команды нет в боте, попробуйте /start')