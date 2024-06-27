import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor

# Создаем словарь с фракциями и их участниками
fractions = {
    'Государственные работы': ['участник 1', 'участник 2', 'участник 3'],
    'Другая фракция': ['участник 4', 'участник 5', 'участник 6']
}

# Создаем словарь с титулами и их значениями
titles = {
    'Рядовой': 1,
    'Сержант': 2,
    'Лейтенант': 3,
    'Капитан': 4,
    'Майор': 5,
    'Подполковник': 6,
    'Полковник': 7,
    'Генерал-майор': 8,
    'Генерал-лейтенант': 9,
    'Генерал армии': 10
}

# Обработка команды "Моя фракция"
async def my_fraction(message: types.Message):
    user = message.from_user.username
    for fraction, members in fractions.items():
        if user in members:
            await message.reply(f'Вы состоите в фракции "{fraction}"')
            return
    await message.reply('Вы не состоите ни в одной фракции')

# Обработка команды "Фракции"
async def get_fractions(message: types.Message):
    fractions_list = '\n'.join([f'• {fraction}' for fraction in fractions.keys()])
    await message.reply(f'Доступные фракции:\n{fractions_list}')

# Обработка команды "Титулы"
async def get_titles(message: types.Message):
    titles_list = '\n'.join([f'• {title}: {value}' for title, value in titles.items()])
    await message.reply(f'Доступные титулы:\n{titles_list}')

def reg(dp: Dispatcher):
        dp.register_message_handler(my_fraction, lambda message: message.text.lower().startswith('моя фракция'))
        dp.register_message_handler(get_fraction, lambda message: message.text.lower().startswith('фракции'))
        dp.register_message_handler(get_titles, lambda message: message.text.lower().startswith('титулы'))
