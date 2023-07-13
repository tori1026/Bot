import asyncio
import datetime
import pytz

async def check_voice_channels(client):
    while True:
        now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

        if now.hour == 0 and now.minute == 0:  # 日付が変わるタイミング
            for guild in client.guilds:  # サーバーを順にチェック
                for voice_channel in guild.voice_channels:  # ボイスチャンネルを順にチェック
                    # ボイスチャンネルにメンバーがいるかチェック
                    if voice_channel.members:
                        # テキストチャンネルIDを指定
                        text_channel = client.get_channel(1003353000787591309)

                        # テキストチャンネルにスタンプを送信
                        nero_emoji = "<:nero:1128342167354613910>"
                        await text_channel.send(f"{voice_channel.name}に起きてる人がいます！{nero_emoji}")

        # 次の日付が変わるタイミングまで待機
        await asyncio.sleep((24 - now.hour) * 60 * 60 - now.minute * 60 - now.second)
