from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,InlineKeyboardButton

zero = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Главное меню')],],
    resize_keyboard=True, 
    input_field_placeholder='Выберите пункт меню',
    )

main_panel = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Анализ истории игр'), KeyboardButton(text='Анализ винрейта')], # first row
    [KeyboardButton(text='Прогноз победы на герое'), KeyboardButton(text='Оптимальный драфт героев')],
    [KeyboardButton(text='Изменить DOTA ID')],],
    resize_keyboard=True, 
    input_field_placeholder='Выберите пункт меню',
    )


repeat_id = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Что это такое?', callback_data='what')],
    [InlineKeyboardButton(text='Попробовать еще раз', callback_data='start')],
])


start_panel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Что это такое?', callback_data='what')],
    [InlineKeyboardButton(text='Оправить DOTA ID', callback_data='start')],
])

what_panel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Как найти свой DOTA ID?', url='https://dota2guru.ru/kak-posmotret-id-v-dota-2-uznaem-svoj-ajdi-v-dote-2/')],
    [InlineKeyboardButton(text='Отправить DOTA ID', callback_data='start')],
])
