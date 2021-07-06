# discord-channel-archiver 
`discord-channel-archiver` is a channel archiver written in discord.py

## what does it do
repeatedly requesting `https://discord.com/api/v9/channels/{channel.id}/messages` to obtain messages, filtering their contents to only include the attributes we want, and dumping it to a file

## how does it work
It uses discord.py & a bot to archive a channel

## how do I set it up?
1. `pip install -r requirements.txt` to install requirements
2. Copy `example.env` into a new file named `.env` and fill in the information.

## how do I run it?
`python main.py [channel ID]`