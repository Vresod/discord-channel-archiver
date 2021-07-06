import json
import requests
import dotenv
from extra import RequestType

from sys import argv as args

config = {
	**dotenv.dotenv_values('example.env'), # first load example.env,
	**dotenv.dotenv_values('.env'), # then load .env
}

token = ('Bot ' if config['BOT']  != 'False' else '') + config['TOKEN']

config['BOT'] = True if config['TOKEN'].startswith('Bot ') else config['BOT']

STARTPOINT = "https://discord.com/api/v9"

def request_endpoint(endpoint,method:RequestType=RequestType.GET,data:dict={}):
	"""
	gets an endpoint in form "/users/@me"
	"""
	if method == RequestType.GET: return json.loads(requests.get(STARTPOINT + endpoint,headers={'Authorization':token}).text)
	elif method == RequestType.POST: return json.loads(requests.post(STARTPOINT + endpoint,headers={'Authorization':token},data=data).text)
	else: raise ValueError(f'Unsupported method {method.name!r}')

if __name__ == "__main__":
	user = request_endpoint("/users/@me")
	print(f'Logged in as {user.get("username")}#{user.get("discriminator")}')
	try: channel = int(args[1])
	except ValueError: channel = int(args[2])
	except ValueError:
		print('No channel provided, exiting program')
		exit(1)
	messages = []
	oldest_snowflake:int = 0
	LIMIT = 100
	wanted_attrs = {'content','author','id','timestamp','edited_timestamp','attachments','embeds','reactions','pinned','type','referenced_message'}
	while True:
		current_messages:list = request_endpoint(f'/channels/{channel}/messages?limit={LIMIT}&{"before=" + oldest_snowflake if oldest_snowflake else ""}')
		for message in current_messages:
			temp_message = {}
			for i in wanted_attrs:
				temp_message[i] = message.get(i)
			messages.append(temp_message)
			oldest_snowflake = message['id']
		if len(current_messages) != LIMIT:
			break
	messages.reverse()
	with open("dump.json","w") as dumpfile: json.dump(messages,dumpfile)