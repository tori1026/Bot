import discord
import os

from omikuji import handle_omikuji
from random_weapon import split_team, osusume
from tenki import handle_tenki

# bot access TOKEN
TOKEN = os.environ["DISCORD_TOKEN"]

# 接続に必要なオブジェクトを生成
client = discord.Client(intents=discord.Intents.all())

players = {}


# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    channel = message.channel
    # bot自身が送信者の場合は無視
    if message.author.bot:
        return

    # 編成分けを行うブキガチャ
    if message.content == "!split":
        await split_team(channel)

    # おすすめブキの表示
    if message.content == "!osusume":
        await osusume(channel)

    # 現在の天気の表示
    if message.content == "!tenki":
        await handle_tenki(channel)

    # おみくじを引く
    if message.content == "!omikuji":
        love, work, health, money = await omikuji.draw_omikuji()
        # 恋愛運、仕事運、健康運、金運を取得
        result = await omikuji.get_result(love, work, health, money)
        # 星の数を表す文字列を取得
        love_str, work_str, health_str, money_str = await omikuji.omikuji_str(love, work, health, money)
        # 結果を表示
        result_message = (
            f'あなたの今日の運勢は{result}！\n'
            f'恋愛運 : {love_str}\n'
            f'仕事運 : {work_str}\n'
            f'健康運 : {health_str}\n'
            f'金運　 : {money_str}'
        )
        await channel.send(result_message)


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)