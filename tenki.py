import random

async def handle_tenki(channel):
    responses = ["しらん", "あつい"]
    response = random.choice(responses)
    await channel.send(response)
