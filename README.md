# voxarybot-public
twitch utility bot with a modular command system, hopefully not requiring advanced python knowledge.

requires Python to be installed.
the script was made and tested with Python 3.13.1. there is no guarantee that the script works with other python versions.

# Setup
the bot requires minimal setup, without that it won´t work.
1. Make a new twitch account, called anything that signifies it as a bot to minimize confusion, for example "VoxaryBot".
2. log in to twitchtokengenerator.com with the bot account, and generate a oauth token.
3. download and open the bot.py script and, under Config, replace:
	- your_bot_account_name_here with your bot´s account name
	- your_channel_here with your twitch username, so the bot knows which chat to connect to
	- your_bot_oauth_token_here with your bot´s oauth token from twitchtokengenerator. make sure to keep the oauth: part, otherwise it won´t work
	- discord_link_here with the invite link to your discord
4. save the script.
5. run the script by double-leftclicking the .py file
6. when setup correctly, you should see a message in your twitch chat from your bot account as soon as you run the script, that is as follows: "[BotAccount] successfully booted up and connected to [TwitchChannel]´s Chat. Have a good stream!", [BotAccount] being your bot´s username and [TwitchChannel] being your username.

That´s it. If you run into issues with the script BEFORE modifying it besides the setup, as stated in LICENSE.txt, feel free to make an issue here on github.
   
