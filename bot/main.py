import os
import discord
import json
import random
from datetime import datetime
from discord.ext import commands

import session_manager
from random_weapon import split_team, osusume
from tenki import handle_tenki
from weapon_range import get_weapon_range
from omikuji import draw_omikuji, get_result, omikuji_str

TOKEN = os.environ['DISCORD_TOKEN']

# コマンドプレフィックスを'/'に設定してBotを生成
bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())




def generate_session_id():
    """現在の時刻からセッションIDを生成する。フォーマットは yyyymmddhhmmss。"""
    return datetime.now().strftime("%Y%m%d%H%M%S")

def load_topics(filename="topics.json"):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data["topics"]

def select_random_topic(topics):
    return random.choice(topics)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    session_manager.setup_database()
    global current_session_id
    current_session_id = None

@bot.command()
async def start(ctx):
    global current_session_id
    if current_session_id is not None:
        await ctx.send("A session is already running. Please wait until it finishes.")
        return

    current_session_id = generate_session_id()
    view = SessionView(current_session_id)  # SessionView インスタンスを作成
    message = await ctx.send(f"参加者はスタンプを押してください。参加者を締め切るまでボタンは押さないでください。", view=view)
    await message.add_reaction("🙋")  # 挙手絵文字を追加

@bot.command()
async def end(ctx):
    global current_session_id
    if current_session_id is None:
        await ctx.send("No session is currently running.")
        return

    # セッション終了の処理を実行
    current_session_id = None
    await ctx.send("Session has been ended.")


@bot.command()
async def split(ctx):
    await split_team(ctx.channel)

@bot.command()
async def osusume(ctx):
    await osusume(ctx.channel)

@bot.command()
async def tenki(ctx):
    await handle_tenki(ctx.channel)

@bot.command()
async def omikuji(ctx):
    love, work, health, money = await draw_omikuji()
    result = await get_result(love, work, health, money)
    love_str, work_str, health_str, money_str = await omikuji_str(love, work, health, money)
    result_message = (
        f'あなたの今年の運勢は{result}！\n'
        f'恋愛運 : {love_str}\n'
        f'仕事運 : {work_str}\n'
        f'健康運 : {health_str}\n'
        f'金運　 : {money_str}'
    )
    await ctx.send(result_message)


@bot.event
async def on_reaction_add(reaction, user):
    if user.bot or reaction.message.author.id != bot.user.id:
        return  # ボットのリアクションまたは他のユーザーのメッセージに対するリアクションは無視

    global current_session_id
    print(f"Reaction received: {reaction} from {user.name}")  # デバッグ情報

    await session_manager.register_participant(current_session_id, str(user.id), user.name)

@bot.command()
async def range(ctx, weapon_name):
    weapon_range = get_weapon_range(weapon_name)
    if weapon_range is not None:
        await ctx.send(f"The range of {weapon_name} is {weapon_range}.")
    else:
        await ctx.send(f"Weapon {weapon_name} not found.")

class SessionView(discord.ui.View):
    def __init__(self, session_id):
        super().__init__()
        self.session_id = session_id
        self.add_item(CloseRegistrationButton(session_id))

class CloseRegistrationButton(discord.ui.Button):
    def __init__(self, session_id):
        super().__init__(style=discord.ButtonStyle.red, label="参加締め切り", custom_id=f"close_registration_{session_id}")
        self.session_id = session_id

    async def callback(self, interaction: discord.Interaction):
        participants = session_manager.list_participants(self.session_id)
        if not participants:
            await interaction.response.send_message("参加者が登録されていません。", ephemeral=False)
            return

        response = "参加者:\n" + "\n".join(f"{username} - {points} ポイント" for user_id, username, points in participants)
        # 参加締め切りボタンを含むビューをクリアして新しいメッセージを送信
        await interaction.response.send_message(response, ephemeral=False)  # 応答として新しいメッセージを送信
        self.view.clear_items()  # ボタンを削除する




@bot.command()
async def newgame(ctx):
    global current_session_id
    if not current_session_id:
        await ctx.send("No session is currently active.")
        return

    participants = session_manager.list_participants(current_session_id)  # ここは非同期関数ではないのでawaitは不要
    num_participants = len(participants)
    if num_participants < 9:
        num_spectators = 1
    elif num_participants == 9:
        num_spectators = 1
    elif num_participants == 10:
        num_spectators = 2
    else:
        await ctx.send("Not enough participants for spectators.")
        return

    # 非同期関数をawaitを使って呼び出す
    spectators = await session_manager.choose_spectators(current_session_id, participants, num_spectators)
    spectator_names = ', '.join([s[1] for s in spectators])  # ユーザ名を取得
    await ctx.send(f"Selected spectators: {spectator_names}")





bot.run(TOKEN)
