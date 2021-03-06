from enum import IntEnum
from datetime import datetime
from typing import Union
import requests
import json

__all__ = ['RequestType','RequestClass','dump_json','RequestError']

STARTPOINT = "https://discord.com/api/v9"
# stuff we don't throw away about the messages
LIMIT = 100 # amount of messages grabbed per request


class RequestType(IntEnum): # make an enum of request types; this probably already exists in requests but i couldn't find it
	GET = 1
	POST = 2
	# we dont need the rest of the types but we'll have them anyways
	PATCH = 3
	DELETE = 4
	HEAD = 5
	OPTIONS = 6
	PUT = 7
	TRACE = 8

class RequestError(Exception): pass

class RequestClass:
	def __init__(self,token): self.token = token
	def __call__(self, endpoint,method:RequestType=RequestType.GET,data:dict={}):
		"""
		gets an endpoint in form "/users/@me". only GET and POST are supported
		"""
		if method == RequestType.GET: d = json.loads(requests.get(STARTPOINT + endpoint,headers={'Authorization':self.token}).text)
		elif method == RequestType.POST: d = json.loads(requests.post(STARTPOINT + endpoint,headers={'Authorization':self.token},data=data).text)
		# only GET and POST are supported
		else: raise ValueError(f'Unsupported method {method.name!r}')
		if isinstance(d,dict) and (code := str(d.get('code'))).startswith(('4','5')):
			raise RequestError(f"Returned HTTP code {code!r}, which is errorful")
		return d

def dump_json(channel:Union[int,str],config:dict,request_endpoint:RequestClass):
	"""
	dumps every message in a discord channel to filename
	"""
	filename = config['FILENAME']
	quiet = config['QUIET']
	oldest_snowflake:int = 0
	dump_at_end = config['DUMP_AT_END']
	file_mode = 'w' if dump_at_end else 'a' # write if dump at end, else append
	with open(filename,'w') as dumpfile: dumpfile.write('[' if not dump_at_end else '') # make the file and be sure its empty
	dumpfile = open(filename,file_mode)
	messages = []
	while True:
		time = datetime.now().strftime("%H:%M:%S")
		if not dump_at_end: messages = [] # empty the messages list if dump_at_end
		current_messages:list = request_endpoint(f'/channels/{channel}/messages?limit={LIMIT}&{"before=" + oldest_snowflake if oldest_snowflake else ""}')
		for message in current_messages:
			messages.append(message)
			oldest_snowflake = message['id']
			if not quiet:
				print(f"[{time}] <{message['author']['username']}#{message['author']['discriminator']}>: {message['content']}") # print in format "[00:00:00] <DiscordUser#0001> Sample text"
				[print(i['url']) for i in message['attachments']]
		# do weird lower-level json shenanigans if not dump at end
		if not dump_at_end:
			for message in messages:
				dumpfile.write(json.dumps(message))
				if message != messages[-1]: dumpfile.write(',')
		if len(current_messages) < LIMIT: # stop looping if this is the last one, ie we got less than the limit
			break
	if dump_at_end: json.dump(messages,dumpfile) # write all messages to the file at the end
	else: dumpfile.write(']') # finish off the json array we've been creating the whole time
