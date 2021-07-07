import json
import requests
import dotenv # allows a convenient config format
from datetime import datetime # needed for verbosity
from extra import RequestType # enum for requests

from sys import argv as args # arguments

# dotenv config
config = {
	**dotenv.dotenv_values('example.env'),
	**dotenv.dotenv_values('.env'),
}

# bot tokens require "Bot " before them
token = ('Bot ' if config['BOT']  != 'False' else '') + config['TOKEN']

# startpoint, as in before endpoint
STARTPOINT = "https://discord.com/api/v9"

# stuff we don't throw away about the messages
WANTED_ATTRS = {'content','author','id','timestamp','edited_timestamp','attachments','embeds','reactions','pinned','type','referenced_message'}
LIMIT = 100 # amount of messages grabbed per request

def request_endpoint(endpoint,method:RequestType=RequestType.GET,data:dict={}):
	"""
	gets an endpoint in form "/users/@me". only GET and POST are supported
	"""
	if method == RequestType.GET: return json.loads(requests.get(STARTPOINT + endpoint,headers={'Authorization':token}).text)
	elif method == RequestType.POST: return json.loads(requests.post(STARTPOINT + endpoint,headers={'Authorization':token},data=data).text)
	# only GET and POST are supported
	else: raise ValueError(f'Unsupported method {method.name!r}')

def dump_json_at_end():
	messages = []
	oldest_snowflake:int = 0
	while True:
		time = datetime.now().strftime("%H:%M:%S")
		current_messages:list = request_endpoint(f'/channels/{channel}/messages?limit={LIMIT}&{"before=" + oldest_snowflake if oldest_snowflake else ""}')
		for message in current_messages:
			temp_message = {}
			for i in WANTED_ATTRS:
				temp_message[i] = message.get(i)
			messages.append(temp_message)
			print(f"[{time}] <{message['author']['username']}#{message['author']['discriminator']}>: {message['content']}")
			oldest_snowflake = message['id']
		if len(current_messages) != LIMIT:
			break
	messages.reverse()
	with open("dump.json","w") as dumpfile: json.dump(messages,dumpfile)

def dump_json_for_each():
	oldest_snowflake:int = 0
	with open('dump.json','w') as dumpfile: dumpfile.write('[')
	dumpfile = open('dump.json','a')
	while True:
		time = datetime.now().strftime("%H:%M:%S")
		messages = []
		current_messages:list = request_endpoint(f'/channels/{channel}/messages?limit={LIMIT}&{"before=" + oldest_snowflake if oldest_snowflake else ""}')
		for message in current_messages:
			temp_message = {}
			for i in WANTED_ATTRS:
				temp_message[i] = message.get(i)
			messages.append(temp_message)
			print(f"[{time}] <{message['author']['username']}#{message['author']['discriminator']}>: {message['content']}")
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
	print(f"Dumping channel #{request_endpoint(f'/channels/{channel}')['name']}")
	if config['DUMP_AT_END'] == 'True':
		dump_json_at_end()
	else:
		dump_json_for_each()