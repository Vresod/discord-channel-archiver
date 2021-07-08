import dotenv # allows a convenient config format
from extra import RequestClass
from extra import dump_json 
import argparse

parser = argparse.ArgumentParser(description='Archive discord channels')
parser.add_argument("channel",help="channel to be archived",type=int)
parser.add_argument("--token",'-t',help="token to be used",dest="TOKEN")
parser.add_argument("--bot",'-b',help="whether the token is that of a bot",action='store_true',dest="BOT")
parser.add_argument("--filename",'-f',help="whether",dest="FILENAME")

args = vars(parser.parse_args())

args = {k:v for k,v in args.items() if v is not None}
if not args['BOT']: del args['BOT']

# dotenv config
config = {
	**dotenv.dotenv_values('example.env'),
	**dotenv.dotenv_values('.env'),
	**args
}

# bot tokens require "Bot " before them
token = ('Bot ' if config['BOT']  != 'False' else '') + config['TOKEN']

if __name__ == "__main__":
	request_endpoint = RequestClass(token)
	user = request_endpoint("/users/@me")
	print(f'Logged in as {user.get("username")}#{user.get("discriminator")} to {config["FILENAME"]}')
	channel = config['channel']
	print(f"Dumping channel #{request_endpoint(f'/channels/{channel}')['name']}") # tell the user what channel they're dumping by name, to make sure they got the correct one. also nested f-strings lol
	dump_json(channel,config['FILENAME'],config,request_endpoint)