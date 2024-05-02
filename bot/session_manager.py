import sqlite3
import logging
import aiosqlite
import random

# ログの設定
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

def setup_database():
    logging.debug("Setting up the database.")
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            user_id TEXT,
            username TEXT,
            points INTEGER DEFAULT 1000,
            spectate_count INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()
    logging.debug("Database setup completed.")

async def register_participant(session_id, user_id, username):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    try:
        # データベースからユーザーを検索
        c.execute("SELECT * FROM participants WHERE session_id=? AND user_id=?", (session_id, user_id))
        result = c.fetchone()
        if result is None:
            # ユーザーがまだ登録されていなければ、データベースに追加
            c.execute("INSERT INTO participants (session_id, user_id, username, points) VALUES (?, ?, ?, 1000)",
                      (session_id, user_id, username))
            conn.commit()
            logging.info(f"New participant added: {username} for session {session_id}")
        else:
            # ユーザーがすでに存在する場合は追加しない
            logging.info(f"Participant {username} already registered for session {session_id}")
    except Exception as e:
        logging.error(f"Error in registering participant: {e}")
    finally:
        conn.close()


def list_participants(session_id):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute("SELECT user_id, username, points FROM participants WHERE session_id=?", (session_id,))
    participants = c.fetchall()
    conn.close()
    print(f"Listing participants for session {session_id}: {participants}")  # デバッグ情報の出力
    return participants


async def choose_spectators(session_id, participants, num_spectators):
    if len(participants) < 9:
        # 9人未満の場合はランダムに選ぶ
        spectators = random.sample(participants, min(num_spectators, len(participants)))
    else:
        # 参加者を観戦回数が少ない順にソートしてから上位 num_spectators を選ぶ
        sorted_participants = sorted(participants, key=lambda x: x[4])  # spectate_count でソート
        spectators = sorted_participants[:num_spectators]
    
    async with aiosqlite.connect('bot.db') as conn:
        async with conn.cursor() as c:
            for spectator in spectators:
                await c.execute("UPDATE participants SET spectate_count = spectate_count + 1 WHERE user_id=?", (spectator[0],))
            await conn.commit()
    
    return spectators




