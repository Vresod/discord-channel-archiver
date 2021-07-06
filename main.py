import json
import requests
import dotenv
from datetime import datetime
from extra import RequestType

from sys import argv as args

config = {
	**dotenv.dotenv_values('example.env'), # first load example.env,
	**dotenv.dotenv_values('.env'), # then load .env
}

token = ('Bot ' if config['BOT']  != 'False' else '') + config['TOKEN']

config['BOT'] = True if config['TOKEN'].startswith('Bot ') else config['BOT']

STARTPOINT = "https://discord.com/api/v9"

WANTED_ATTRS = {'content','author','id','timestamp','edited_timestamp','attachments','embeds','reactions','pinned','type','referenced_message'}
LIMIT = 100

def request_endpoint(endpoint,method:RequestType=RequestType.GET,data:dict={}):
	"""
	gets an endpoint in form "/users/@me"
	"""
	if method == RequestType.GET: return json.loads(requests.get(STARTPOINT + endpoint,headers={'Authorization':token}).text)
	elif method == RequestType.POST: return json.loads(requests.post(STARTPOINT + endpoint,headers={'Authorization':token},data=data).text)
	else: raise ValueError(f'Unsupported method {method.name!r}')

def dump_json_at_end():
	messages = []
	oldest_snowflake:int = 0
	LIMIT = 100
	while True:
		now = datetime.now()
		time = now.strftime("%H:%M:%S")
		current_messages:list = request_endpoint(f'/channels/{channel}/messages?limit={LIMIT}&{"before=" + oldest_snowflake if oldest_snowflake else ""}')
		for message in current_messages:
			temp_message = {}
			for i in WANTED_ATTRS:
				temp_message[i] = message.get(i)
			print(f"[{time}] <{message['author']['username']}#{message['author']['discriminator']}>: {message['content']}")
			oldest_snowflake = message['id']
		if len(current_messages) != LIMIT:
			break
	messages.reverse()
	with open("dump.json","w") as dumpfile: json.dump(messages,dumpfile)

def dump_json_for_each():
	WANTED_ATTRS = {'content','author','id','timestamp','edited_timestamp','attachments','embeds','reactions','pinned','type','referenced_message'}
	oldest_snowflake:int = 0
	with open('dump.json','w') as dumpfile: dumpfile.write('[')
	dumpfile = open('dump.json','a')
	while True:
		messages = []
		current_messages:list = request_endpoint(f'/channels/{channel}/messages?limit={LIMIT}&{"before=" + oldest_snowflake if oldest_snowflake else ""}')
		for message in current_messages:
			temp_message = {}
			for i in WANTED_ATTRS:
				temp_message[i] = message.get(i)
			messages.append(temp_message)
		for message in messages:
			dumpfile.write(json.dumps(message))
			if message != messages[-1]: dumpfile.write(',')
		if len(current_messages) != LIMIT:
			break
	dumpfile.write(']')


if __name__ == "__main__":
	user = request_endpoint("/users/@me")
	print(f'Logged in as {user.get("username")}#{user.get("discriminator")}')
	try: channel = int(args[1])
	except ValueError: channel = int(args[2])
	except ValueError:
		print('No channel provided, exiting program')
		exit(1)
	if config['DUMP_AT_END'] == 'True':
		dump_json_at_end()
	else:
		dump_json_for_each()