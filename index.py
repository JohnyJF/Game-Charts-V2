import requests
from bs4 import BeautifulSoup
import time
import json
import subprocess as cmd
import os

data = {}
data['steam'] = []
data['twitch'] = []

def steamData():
	r = requests.get('https://steamcharts.com/')
	soup = BeautifulSoup(r.text, 'html.parser')
	table = soup.find('table', attrs={'id':'top-games', 'class':'common-table'})
	table_body = table.find('tbody')
	rows = table_body.find_all('tr')

	for row in rows:
		game_id = row.find('a')['href']
		name = row.find('a').text
		name = name[7:-6]
		players = row.find('td', attrs={'class':'num'}).text

		data['steam'].append({
			'id': game_id,
			'name': name,
			'players': players
			})
		print(game_id+ ': ' + name + ': ' + players)


def twitchData():
	r = requests.get('https://twitchtracker.com/games/live')
	soup = BeautifulSoup(r.text, 'html.parser')

	names = []
	ids = []
	vs = []

	games = soup.find_all('div', attrs={'class':'ri-name'})
	for game in games:
		game_id = game.find('a')['href']

		names.append(game.text[1:-2])
		ids.append(game_id)
		print(game_id + ': ' + game.text[1:-2])	

	viewers = soup.find_all('div', attrs={'class':'to-number-lg'})
	for viewer in viewers:
		vs.append(viewer.text)
		print(viewer.text)

	for i in range(0, len(names)):
		data['twitch'].append({
			'id': ids[i],
			'name': names[i],
			'viewers': vs[i]
			})


while True:
	os.remove("data.json")

	data['steam'] = []
	data['twitch'] = []
	steamData()
	twitchData()
	with open('data.json', 'w') as outfile:
		json.dump(data, outfile)
	time.sleep(3)
	message = ""
	cp = cmd.run("git add .")
	cp = cmd.run(f"git commit -m '{message}'", check=True, shell=True)
	cp = cmd.run("git push -u origin master -f", check=True, shell=True)
	print('passed')
	time.sleep(10)
	print('passed 2')