from decimal import Decimal
from commands.db import conn, cursor
from pycoingecko import CoinGeckoAPI


api = CoinGeckoAPI()


async def getbtc(message):
    user_id = message.from_user.id
    cursor.execute('SELECT btc FROM users WHERE user_id = ?', (user_id,))
    i = cursor.fetchone()[0]
    return i


async def getkurs():
    cursor.execute('SELECT kursbtc FROM sett')
    i = cursor.fetchone()
    if i is None:
        cursor.execute('INSERT INTO sett (ads, kursbtc) VALUES (?, ?)', ('', 40000))
        conn.commit()
        i = 40000
    else:
        i = i[0]
    return i


async def sellbtc_db(summ, summ_btc, user_id):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = Decimal(balance) + Decimal(summ)
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), user_id))
    cursor.execute('UPDATE users SET btc = btc - ? WHERE user_id = ?', (int(summ_btc), user_id))
    conn.commit()

async def sellyen_db(summ, summ_yen, user_id):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = Decimal(balance) + Decimal(summ)
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), user_id))
    cursor.execute('UPDATE users SET yen = yen - ? WHERE user_id = ?', (int(summ_yen), user_id))
    conn.commit()



async def bybtc_db(summ, summ_btc, user_id):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = Decimal(balance) - Decimal(summ)
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), user_id))
    cursor.execute('UPDATE users SET btc = btc + ? WHERE user_id = ?', (int(summ_btc), user_id))
    conn.commit()


async def byratting_db(summ, r_summ, user_id):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = Decimal(balance) - Decimal(summ)
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), user_id))
    cursor.execute('UPDATE users SET rating = rating + ? WHERE user_id = ?', (int(r_summ), user_id))
    conn.commit()


async def getexpe(message):
    user_id = message.from_user.id
    cursor.execute('SELECT exp, energy FROM users WHERE user_id = ?', (user_id,))
    i = cursor.fetchone()
    expe, energy = i
    return expe, energy


async def digdb(i, user_id, r, op):
    cursor.execute('UPDATE users SET exp = exp + ? WHERE user_id = ?', (int(op), user_id))
    cursor.execute(f'UPDATE mine SET {r} = {r} + ? WHERE user_id = ?', (int(i), user_id))
    cursor.execute('UPDATE users SET energy = energy - 1 WHERE user_id = ?', (user_id,))
    conn.commit()


async def sell_ruda_db(i, user_id, r, kolvo):
    cursor.execute(f'UPDATE mine SET {r} = {r} - ? WHERE user_id = ?', (int(kolvo), user_id))
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = Decimal(balance) + Decimal(i)
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), user_id))
    conn.commit()


async def getmine(message):
    user_id = message.from_user.id
    cursor.execute(
        'SELECT iron, gold, diamond, amestit, aquamarine, emeralds, matter, plasma, nickel, titanium, cobalt, '
        'ectoplasm, biores, palladium FROM mine WHERE user_id = ?',
        (user_id,))
    i = cursor.fetchone()
    iron, gold, diamond, amestit, aquamarine, emeralds, matter, plasma, nickel, titanium, cobalt, ectoplasm, biores, palladium = i
    return iron, gold, diamond, amestit, aquamarine, emeralds, matter, plasma, nickel, titanium, cobalt, ectoplasm, biores, palladium


async def getenergy(message):
    user_id = message.from_user.id
    cursor.execute('SELECT energy FROM users WHERE user_id = ?', (user_id,))
    i = cursor.fetchone()[0]
    return i


async def getrrating(message):
    user_id = message.from_user.id
    cursor.execute('SELECT rating FROM users WHERE user_id = ?', (user_id,))
    i = cursor.fetchone()[0]
    return i

async def getyenn(message):
    user_id = message.from_user.id
    cursor.execute('SELECT yen FROM users WHERE user_id = ?', (user_id,))
    i = cursor.fetchone()[0]
    return i



async def sellrrating_db(summ, summ_r, user_id):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = Decimal(balance) + Decimal(summ)
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), user_id))
    cursor.execute('UPDATE users SET rating = rating - ? WHERE user_id = ?', (int(summ_r), user_id))
    conn.commit()

async def sellyen_db(summ, summ_r, user_id):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = Decimal(balance) + Decimal(summ)
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), user_id))
    cursor.execute('UPDATE users SET yen = yen - ? WHERE user_id = ?', (int(summ_r), user_id))
    conn.commit()


async def getcorn_garden(id):
    cursor.execute('SELECT corn FROM users WHERE user_id = ?', (id,))
    i = cursor.fetchone()[0]
    return i


async def autoenergy():
    cursor.execute(f'UPDATE users SET energy = energy + 1 WHERE energy < 10 AND status = 0')
    cursor.execute(f'UPDATE users SET energy = energy + 1 WHERE energy < 25 AND status = 1')
    cursor.execute(f'UPDATE users SET energy = energy + 1 WHERE energy < 50 AND status = 2')
    cursor.execute(f'UPDATE users SET energy = energy + 1 WHERE energy < 75 AND status = 3')
    cursor.execute(f'UPDATE users SET energy = energy + 1 WHERE energy < 100 AND status = 4')
    conn.commit()




async def autokursbtc_new():
    try: new_kurs = api.get_price(ids='bitcoin', vs_currencies='usd')['bitcoin']['usd']
    except: return print('error upd btc price')

    if isinstance(new_kurs, (int, float)):
        cursor.execute('UPDATE sett SET kursbtc = ?', (int(new_kurs),))
        conn.commit()
