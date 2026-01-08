# VoxaryBot
scuffed python-based twitch utility bot.


# Setup
1. download the newest version from releases and save it in a new folder.
2. run setup.exe and follow the instructions
3. go to your twitch chat and send "/mod voxarybot"
4. whenever you´re ready to stream, just run bot.exe. you should see a message from the bot in your chat.

note: the bot is set up to automatically shoutout raiders, but this functionality works based on the incoming raid response by streamelements. if streamelements isn´t set up, then auto-shoutouts will not work.

note 2: the bot is set up to shut itself down upon receiving Sery_Bot´s raidout message. if Sery_Bot isn´t set up, you will have to shut down the bot manually after stream.

note 3: the chat moderation features are still in what equates to open beta. I give zero guarantee that it will work.

note 4: testing the bot in action has revealed that none of the features mentioned in the above notes currently work. I will fix that

# How to add Commands
1. navigate to where you saved the bot
2. open commands.json with any text editor program
3. add your commands in the same format as the pre-made commands: "!command": "what the command does"
4. make sure to add a comma "," to the end of the second-to-last line, otherwise it will not work and error out.
5. save commands.json.
6. start the bot, or send reloadcommands in the bot´s console window if it´s already running.

you can edit any commands at any time, even during stream. Just remember to reload the commands after changing anything.


# [CURRENTLY BROKEN] How to use the moderation features [BETA] 
1. navigate to where you saved the bot
2. open moderation.json with any text editor program
3. the moderation settings are in the format of "action": "trigger1, trigger2", with the exceptions of TimeoutTime and reason
 - TimeoutTime is the time the chatter is timed out when they trigger a timeout
 - reason is the reason the chatter receives when they trigger a moderation action, with the addition of "Consequence: [action]"
4. to add a keyword, just add it to the trigger words at the desired action. only the pre-made actions (Warn, Timeout, Ban) are valid, any custom actions are ignored.
5. again, make sure to add a comma "," to the end of the second-to-last line.
6. save moderation.json.

unlike with commands, you cannot reload changes to moderation.json without closing and restarting the bot. I´m working on that.


# Console Commands
These commands can be used by the person using the bot, in the bot´s console window:
- say [message] - say something via the bot.
- reloadcommands - reload commands.json
- exit - disconnect and shut down the bot


# What is planned
- allow for moderation.json changes to be reloaded during runtime
- logging chat to a file
- adding settings to enable/disable unique chatter logging and chat logging


# How the bot works (aka Technical Overview)
upon running setup.exe, 3 .json files are created, those being:
- settings.json, containing the channel name and the message the bot sends to chat upon startup.
- commands.json, containing all commands that the bot has special responses to. can be reloaded any time by sending "reloadcommands" in the bot window, wich calls the load_commands() function again.
- moderation.json, containing moderation-related stuff.

when bot.exe is launched, it reads these files and connects to the channel set in settings.json. It then sends a message, also set in settings.json, to that same chat.
After that, the bot goes into listening mode, in which it logs all chat messages to its console. In case a message starts with a "!", it passes it along to the handle_command() function, which, as the name implies, handles the commands. It looks at the text after the "!" and responds with whatever is assigned to that command in commands.json.

When the bot detects a word in the message which is also found in moderation.json, it takes the username, the keyword that triggered the action, and the action, and does a "/" command for that action in the twitch chat. This is also why the bot has to be a moderator of the channel for full functionality. This functionality is currently broken.

The Auto-Shoutout and end-of-stream-autoshutdown work by listening for specific messages from specific users, in this case it´s the default incoming raid message by Streamelements for the shoutouts, and the default message that Sery_Bot sends when you raid out which tells users where the raid went for the auto-shutdown.

The bot doesn´t know, nor care, who is a moderator, who is a VIP, etc.. It doesn´t even know who the broadcaster is. In essence, all it does is listen to twitch chat and respond if needed. It only does what it is told via the .json files.
