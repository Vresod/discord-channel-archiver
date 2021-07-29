import argparse
import json
from datetime import datetime

parser = argparse.ArgumentParser(description='Prints Discord DMs dumped using discord-channel-archiver')
parser.add_argument('filename',help='the file that is parsed')
args = parser.parse_args()

messages:list = json.load(open(args.filename))
messages.sort(key=lambda msg: int(msg['id']))

for message in messages:
	time = datetime.fromtimestamp(((int(message['id'])>> 22) + 1420070400000) / 1000).strftime("%x %X")
	print(f"[{time}] <{message['author']['username']}#{message['author']['discriminator']}>: {message['content']}") # print in a format that changes depending on your region
	[print(i['url']) for i in message['attachments']]