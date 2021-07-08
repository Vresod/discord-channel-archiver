import dotenv # allows a convenient config format
from extra import RequestClass
from extra import dump_json 
import argparse

parser = argparse.ArgumentParser(description='Archive discord channels')
parser.add_argument("channel",help="channel to be archived",type=int)
parser.add_argument("--token",'-t',help="token to be used")
parser.add_argument("--bot",'-b',help="token to be used",action='store_true')
args = parser.parse_args()

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
if __name__ == "__main__":
	request_endpoint = RequestClass(token)
	user = request_endpoint("/users/@me")
	print(f'Logged in as {user.get("username")}#{user.get("discriminator")}')
	channel = args.channel
	print(f"Dumping channel #{request_endpoint(f'/channels/{channel}')['name']}") # tell the user what channel they're dumping by name, to make sure they got the correct one. also nested f-strings lol
	dump_json(channel,'dump.json',config,LIMIT,WANTED_ATTRS,request_endpoint)