import json
import requests
import dotenv # allows a convenient config format
from datetime import datetime # needed for verbosity
from extra import RequestType # enum for requests
from typing import Union
from io import TextIOWrapper
from os import PathLike
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


def dump_json(channel:Union[int,str],filename:PathLike):
	"""
	dumps every message in a discord channel to filename
	"""
	oldest_snowflake:int = 0
	dump_at_end = config['DUMP_AT_END'] == 'True' # str -> bool
	file_mode = 'w' if dump_at_end else 'a' # write if dump at end, else append
	with open('dump.json','w') as dumpfile: dumpfile.write('[' if not dump_at_end else '') # make the file and be sure its empty
	dumpfile = open('dump.json',file_mode)
	messages = []
	while True:
		time = datetime.now().strftime("%H:%M:%S")
		if not dump_at_end: messages = [] # empty the messages list if dump_at_end
		current_messages:list = request_endpoint(f'/channels/{channel}/messages?limit={LIMIT}&{"before=" + oldest_snowflake if oldest_snowflake else ""}')
		for message in current_messages:
			temp_message = {}
			for i in WANTED_ATTRS:
				temp_message[i] = message.get(i)
			messages.append(temp_message)
			print(f"[{time}] <{message['author']['username']}#{message['author']['discriminator']}>: {message['content']}") # print in format "[00:00:00] <DiscordUser#0001> Sample text"
		# do weird lower-level json shenanigans if dump at end
		if not dump_at_end:
			for message in messages:
				dumpfile.write(json.dumps(message))
				if message != messages[-1]: dumpfile.write(',')
		if len(current_messages) < LIMIT: # stop looping if this is the last one, ie we got less than the limit
			break
	if dump_at_end: json.dump(messages,dumpfile) # write all messages to the file at the end
	else: dumpfile.write(']') # finish off the json array we've been creating the whole time

if __name__ == "__main__":
	user = request_endpoint("/users/@me")
	print(f'Logged in as {user.get("username")}#{user.get("discriminator")}')
	try: channel = int(args[1])
	except ValueError: # tell the user they messed up and quit
		print('No channel provided, exiting program')
		exit(1)
	print(f"Dumping channel #{request_endpoint(f'/channels/{channel}')['name']}") # tell the user what channel they're dumping by name, to make sure they got the correct one. also nested f-strings lol
	dump_json(channel,'dump.json')