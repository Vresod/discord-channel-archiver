import argparse
import json
import requests
from time import sleep

parser = argparse.ArgumentParser(description='Slowly posts entire channel archives into another channel')
parser.add_argument('filename',help='the file that is parsed')
parser.add_argument('webhook',help='the webhook that is used to post to a channel')
args = parser.parse_args()

messages:list['dict'] = json.load(open(args.filename))
messages.sort(key=lambda msg: int(msg['id']))

for message in messages:
	data = {
		'username': message['author']['username'],
		'avatar_url':f"https://cdn.discordapp.com/avatars/{message['author']['id']}/{message['author']['avatar']}.webp",
		'tts': False,
		# 'allowed_mentions': {"parse":[]},
		'content':message.get('content'),
		'embeds':message.get('embeds')
	}
	upload_after = False
	if not data.get('content') and not data.get('embeds'):
		data['content'] = "\n".join([ i['url'] for i in message['attachments']] )
	else:upload_after = True
	rate_limited = True
	while rate_limited:
		r = requests.post(f"{args.webhook}?wait=true",data=data)
		r_json = r.json()
		if r.status_code == 429 and r_json['message'] == "You are being rate limited.": sleep(r_json['retry_after'] / 100)
		else: rate_limited = False
		print("final passthrough" if not rate_limited else None)
	if not upload_after: continue
	rate_limited = True
	while rate_limited:
		r = requests.post(f"{args.webhook}?wait=true",data={"username":data['username'],"":data['avatar_url'],"content":"\n".join([ i['url'] for i in message['attachments']])})
		r_json = r.json()
		if r.status_code == 429 and r_json['message'] == "You are being rate limited.": sleep(r_json['retry_after'] / 100)
		else: rate_limited = False