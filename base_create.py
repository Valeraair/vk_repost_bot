import sqlite3

db = sqlite3.connect('repost.sqlite3')
cur = db.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS input('
            'chat_name text, '
            'bot_tel text, '
            'bot_pass text, '
            'chat_link text, '
            'candidate text)')
db.commit()
with open('input_data.txt', 'r', encoding='utf-8') as inp:
    full = inp.readlines()
    for i in range(len(full)):
        data = full[i].strip().split('$')
        cur.execute('INSERT INTO input(chat_name, bot_tel, bot_pass, chat_link, candidate) '
                    'VALUES("%s", "%s", "%s", "%s", "%s")' % (data[0], data[1], data[2], data[3], data[4]))
        db.commit()
    db.close()
