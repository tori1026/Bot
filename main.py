
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
        
    #おみくじを引く
    if message.content == "!omikuji":
        await handle_omikuji(channel)


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
