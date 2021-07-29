import dotenv # allows a convenient config format
from extra import *
import argparse

parser = argparse.ArgumentParser(description='Archive discord channels')
parser.add_argument("channel",help="channel to be archived",type=int)
parser.add_argument("--token",'-t',help="token to be used",dest="TOKEN")
parser.add_argument("--bot",'-b',help="whether the token is that of a bot",action='store_true',dest="BOT")
parser.add_argument("--filename",'-f',help="file that gets written to",dest="FILENAME")
parser.add_argument("--quiet",'-q',help="disables logging to STDOUT",dest="QUIET",action='store_true')

args = vars(parser.parse_args())

args = {k:v for k,v in args.items() if v}
# if not args['BOT']: del args['BOT']

# dotenv config
config = {
	**dotenv.dotenv_values('example.env'),
	**dotenv.dotenv_values('.env'),
	**args
}

config = {k:v if v not in ('True','False') else v=='True' for k,v in config.items()}

# bot tokens require "Bot " before them
token = ('Bot ' if config['BOT'] else '') + config['TOKEN']

if __name__ == "__main__":
	request_endpoint = RequestClass(token)
	user = request_endpoint("/users/@me")
	print(f'Logged in as {user["username"]}#{user["discriminator"]}')
	channel = config['channel']
	name = request_endpoint(f'/channels/{channel}').get('name')
	print(f"Dumping channel {('#' + name) if name else channel} to {config['FILENAME']}") # tell the user what channel they're dumping by name, to make sure they got the correct one. also nested f-strings lol
	dump_json(channel,config,request_endpoint)