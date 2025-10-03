import time
import json

user = "{user}"
def channelSetup():    
    print("note: all of this can be changed any time via the generated .json files.")
    channel = input("Please enter your Twitch channel name: ").strip()
    try:
        with open("settings.json", "r") as settingsfile:
            settings = json.load(settingsfile)
    except FileNotFoundError:
        settings = {
            "Channel": "placeholderChannelName",
            "BotOnlineMessage": "VoHiYo"
            }
    settings["Channel"] = channel
    with open("settings.json", "w") as settingsfile:
        json.dump(settings, settingsfile, indent=2)

def botGreetSetup():
    botGreetMessage = input("What should the bot say upon startup? Default is VoHiYo. : ")
    with open("settings.json", "r") as settingsfile:
        settings = json.load(settingsfile)
    settings["BotOnlineMessage"] = botGreetMessage
    with open("settings.json", "w") as settingsfile:
        json.dump(settings, settingsfile, indent=2)

def dcSetup():
    discord_link = input("Please enter your Discord invite link: ").strip()
    try:
        with open("commands.json", "r") as commandsfile:
            commands = json.load(commandsfile)
    except FileNotFoundError:
        commands = {
            "!hello": "Hello, {user}!",
            "!discord": f"@{user} Join the discord here: {discord_link}",
            "!lurk": "{user} is taking a vacation.",
            "!unlurk": "{user} has returned from their vacation."
            }
    commands["!discord"] = f"@{user} Join the discord here: {discord_link}"
    with open("commands.json", "w") as commandsfile:
        json.dump(commands, commandsfile, indent=2)

def createModFile():
    try:
        print("reading moderation.json...")
        with open("moderation.json", "r") as modfile:
            moderation = json.load(modfile)
    except FileNotFoundError:
        print("Moderation Settings File not found, creating new one...")
        moderation = {
                "Warn": "place holder 1, placeholder2",
               "Timeout": "bitch, nigga",
               "Ban": "dogehype, streamboo",
               "TimeoutTime": "300",
               "reason": "please watch your language in this chat."
               }
        with open("moderation.json", "w") as modfile:
            json.dump(moderation, modfile, indent=2)
        print("Moderation Settings File created")
if __name__ == "__main__":
    channelSetup()
    dcSetup()
    botGreetSetup()
    createModFile()
    print(f"Setup complete!")
    time.sleep(2)
