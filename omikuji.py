import discord
import random

async def draw_omikuji():
    # 恋愛運、仕事運、健康運、金運をそれぞれ5段階でランダムに生成
    love = random.randint(1, 5)
    work = random.randint(1, 5)
    health = random.randint(1, 5)
    money = random.randint(1, 5)
    
    # 恋愛運、仕事運、健康運、金運を返す
    return love, work, health, money
    
async def get_result(love, work, health, money):
    # 星の数の合計に応じて、運勢を決定
    total = love + work + health + money
    if total >= 16:
        return '大吉'
    elif total >= 13:
        return '吉'
    elif total >= 10:
        return '中吉'
    elif total >= 7:
        return '小吉'
    else:
        return '凶'
    
async def omikuji_str(love, work, health, money):
    # 星の数を表す文字列を返す
    love_str = '★' * love
    work_str = '★' * work
    health_str = '★' * health
    money_str = '★' * money
    
    return love_str, work_str, health_str, money_str


async def handle_omikuji(channel):
    love, work, health, money = await draw_omikuji()
    # 恋愛運、仕事運、健康運、金運を取得
    result = await get_result(love, work, health, money)
    # 星の数を表す文字列を取得
    love_str, work_str, health_str, money_str = await omikuji_str(love, work, health, money)
    # 結果を表示
    result_message = (
        f'{"恋愛運 :":<8}{love_str}\\n'
        f'{"仕事運 :":<8}{work_str}\\n'
        f'{"健康運 :":<8}{health_str}\\n'
        f'{"金運   :":<8}{money_str}'
)
    await channel.send(result_message)
