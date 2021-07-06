import json
import requests
import dotenv
from extra import RequestType

from sys import argv as args

config = {
	**dotenv.dotenv_values('example.env'), # first load example.env,
	**dotenv.dotenv_values('.env'), # then load .env
}

token = ('Bot ' if config['BOT'] else '') + config['TOKEN']

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
	print(channel)