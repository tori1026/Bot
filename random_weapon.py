import asyncio
import discord
import json
import random


async def split_team(channel):
	# groups.json ファイルを読み込む
	with open("groups.json", "r") as f:
		data = json.load(f)
	team_a = []
	team_b = []

	for i in range(4):
		# ブキグループを1つランダムに選択する
		selected_group = random.choices(list(data.keys()), weights=[group["weight"] for group in data.values()])[0]
		# ブキグループから2つランダムに選択する
		selected_weapons = random.sample(list(data[selected_group]["weapons"].keys()), 2)
		 # チーム内で同じブキがあった場合は、そのグループの他のブキを再度ランダムに選択する
		while selected_weapons[0] in team_a or selected_weapons[0] in team_b or selected_weapons[1] in team_a or selected_weapons[1] in team_b:
			selected_weapons = random.sample(list(data[selected_group]["weapons"].keys()), 2)
		# 選択したブキをチームに追加する
		team_a.append(selected_weapons[0])
		team_b.append(selected_weapons[1])
		
	# 選択したブキを表示する
	team_a_str = "\n".join([f"- {weapon}" for weapon in team_a])
	team_b_str = "\n".join([f"- {weapon}" for weapon in team_b])
	await channel.send("teamA:\n" + team_a_str)
	await channel.send("teamB:\n" + team_b_str)
	
async def osusume(channel):
    # groups.json ファイルを読み込む
        with open("groups.json", "r") as f:
            data = json.load(f)
            
        # weapons の中からカテゴリをランダムに抽選する
        category = random.choices(list(data.keys()), weights=[w['weight'] for w in data.values()])[0]
        # ランダムに抽選したカテゴリの weapons の中からブキをランダムに抽選する
        weapon = random.choices(list(data[category]['weapons'].keys()), weights=list(data[category]['weapons'].values()))[0]
        
        await channel.send("おすすめは" + weapon + "！\nよかったら使ってみてね！")

