from aiogram import Dispatcher, types
from commands.db import reg_user
from assets import kb
import random
import config as cfg


async def on_start(message):
    await reg_user(message.from_user.id)
    sticker_id = 'CAACAgQAAxkBAAEKs6JlSQUtGTtSzXGVcJGBe0PwnWkI9QACRwkAAm0NeFIe5FE9nk15XTME'
    await message.answer_sticker(sticker=sticker_id)

    await message.answer(f'''🤖 Добро пожаловать на борт, Кто-то! Меня зовут FGM, твой верный игровой бот.

🎮 У меня есть множество интересных команд и игр, чтобы скрасить твоё время, будь ты один или в компании друзей! (Кстати, вместе всегда веселее) 💙
🔍 Познакомиться со всеми моими возможностями ты можешь, введя команду «помощь».

<a href="https://t.me/FGMINFO">🔈 Наш канал</a>
<a href="https://t.me/FGMOFF">💬 Наш чат</a>''', disable_web_page_preview=True, reply_markup=kb.start())

    await message.answer(f'''🚀 Не уверен, с чего начать своё приключение?
Присоединяйся к нашему официальному чату FGM: https://t.me/FGMOFF''', disable_web_page_preview=True)


async def win_luser():
    win = ['🙂', '😋', '😄', '🤑', '😃', '😇']
    loser = ['😔', '😕', '😣', '😞', '😢']
    rwin = random.choice(win)
    rloser = random.choice(loser)
    return rwin, rloser


async def yznat_cmd(message: types.Message):
    if message.reply_to_message:
        mentioned_user_id = message.reply_to_message.from_user.id
        await message.answer(f"ID человека: {mentioned_user_id}")
    else:
        await message.answer("Сообщение пользователя не было отмечено.")

async def geturl(id, txt):
    url = f'<a href="tg://user?id={id}">{txt}</a>'
    return url



async def report(message: types.Message):
    try:
        if message.text == '/report' or message.text == '/r' or not message.reply_to_message:
            await bot.send_message(message.chat.id, '''Вот информация за систему репортов ⛔️

⚠️ | Правила по использованию репортов
     [1️⃣] Материться, оскорблять кого-либо, проявлять неуважение к администрации и тому подобное.
      [2️⃣] Капсить, писать неразборчиво, использовать спам, писать один и тот-же текст несколько раз получивши на него ответ.
      [3️⃣] Всячески дразнить администрацию и отвлекать от работы.
      [4️⃣] Запрещено интересоваться/писать вещи которые ни коем образом ни относятся к игре
      [5️⃣] Запрещена реклама в любом её проявлении
      [6️⃣] Запрещено обращаться к своим друзьям администраторам по личным вопросам
      7️⃣ | Запрещено клеветать на игроков, обвинять их в нарушениях, которые они не совершали.
      [8️⃣] Репорт работает по принципу - Вопрос/Просьба/Жалоба (исключение - Приветствие) и не иначе. Иные формы обращения будут оставаться без ответа и будет выдано наказание.

[⚠️] | Форма отправки репорта - /report [сообщение]

[⛔️] | Прошу вас соблюдать правила отправки репорта

''')
        else:
            members = await message.chat.get_member(message.reply_to_message.from_user.id)
            info = await bot.get_chat_member(message.chat.id, message.from_user.id)
            report = message.text.replace('/r ', '')
            report = report.replace('/report ', '')
            admins = await bot.get_chat_administrators('@' + message.chat.username)
            send = 0
            for admin in admins:
                if admin.user.username != 'Group_Moder_bot':
                    try:
                        await bot.send_message(admin.user.id, f'[📬] | Репорт по причине: ' + str(report) + f'\n\nhttps://t.me/{message.chat.username}/{message.reply_to_message.message_id}')
                    except:
                        pass
                    send += 1

            if send == 0:
                await bot.send_message(message.chat.id, '[👮] | Админы не оповещены, для отправки им репортов надо чтобы они запустили меня в лс!')
            else:
                await bot.send_message(message.chat.id, '''[✅] | ваш репорт был успешно отправлен администрации''')
    except Exception as e:
        print(e)


def reg(dp: Dispatcher):
    dp.register_message_handler(on_start, commands=['start'])
    dp.register_message_handler(report, commands=['r'])
    dp.register_message_handler(yznat_cmd, lambda message: message.text.lower().startswith(('узнать ид', 'узнать ID', 'ID'))) 

