import socket
import threading
import time
import sys
import json

HOST = "irc.chat.twitch.tv"
PORT = 6667
NICK = "VoxaryBot" 
OAUTH_TOKEN = "oauth:*******************************" # censoring to avoid unauthorized access to the bot´s account
try:
    with open("settings.json", "r") as settingsfile:
        settingsdata = json.load(settingsfile)
        print("Reading settings.json...")

    with open("moderation.json", "r") as modfile:
        modActionTriggers = json.load(modfile)
    modActions = {
        action: [word.strip() for word in words.split(",")]
        for action, words in modActionTriggers.items()
    }
except FileNotFoundError:
    print("Error: Settings files not found. Please run setup.exe")
    time.sleep(5)
GreetMessage = settingsdata['BotOnlineMessage']
CHANNEL = settingsdata['Channel'].lower()
print(f"Channel set to {CHANNEL}")

def load_commands():
    global commands_data
    try:
        with open("commands.json", "r") as cmdfile:
            commands_data = json.load(cmdfile)
            print("Commands loaded from commands.json")
    except FileNotFoundError:
        print("Commands.json not found, please run setup.exe")
    except Exception as e:
        print(f"Error loading commands.json: {e}")
        commands_data = {}

running = True
def connect_to_twitch():
    try:
        sock = socket.socket()
        sock.connect((HOST, PORT))
        sock.settimeout(1.0)
        print("Connected to Twitch IRC...")
        
        sock.send(f"PASS {OAUTH_TOKEN}\r\n".encode("utf-8"))
        sock.send(f"NICK {NICK}\r\n".encode("utf-8"))
        sock.send(f"JOIN #{CHANNEL}\r\n".encode("utf-8"))
        print(f"Connected to {CHANNEL}´s Chat")
        print(f"Sending message confirming successful connection to {CHANNEL}´s Chat...")
        sock.send(f"PRIVMSG #{CHANNEL} :{GreetMessage}\r\n".encode("utf-8"))
        print("available console commands: say <message>, reloadcommands, exit")
        return sock
    except Exception as e:
        print(f"Error connecting to Twitch IRC: {e}")
        return None

def monitor_input(sock):
    global running
    while running:
        user_input = input()
        if user_input.strip().lower() == "exit":
            try:
                sock.send(f"PRIVMSG #{CHANNEL} :{NICK} shutting down...\r\n".encode("utf-8"))
                print("Sent disconnect message to chat.")
            except Exception as e:
                print(f"Error sending disconnect message: {e}")
            running = False
            break
        elif user_input.lower().startswith("say "):
            message = user_input[4:].strip()
            if message:
                sock.send(f"PRIVMSG #{CHANNEL} :{message}\r\n".encode("utf-8"))
                print(f"Sent via bot: {message}")
            else:
                print("Usage: say <message>")
        elif user_input.strip().lower() == "reloadcommands":
            load_commands()
   
def handle_command(command, username, sock):
    cmd = command.split(" ")[0].lower()

    if cmd == "!aboutbot":
        return f"I'm {NICK}, a twitch utility bot programmed by Voxarys. Nice to meet you, {username}! VoHiYo"

    if cmd == "!commands":
        all_cmds = list(commands_data.keys())
        all_cmds.append("!aboutbot")
        if "!exit" in all_cmds:
            all_cmds.remove("!exit")

        cmd_list = ", ".join(sorted(all_cmds))
        return f"@{username} Available commands: {cmd_list}"

    if cmd in commands_data:
        response = commands_data[cmd]
        response = response.replace("{user}", username)
        return response

    if cmd == "!exit":
        if username.lower() == CHANNEL.lower():
            shutdown_message = f"PRIVMSG #{CHANNEL} :{NICK} disconnecting from {CHANNEL}'s Chat and shutting down...\r\n"
            sock.send(shutdown_message.encode("utf-8"))
            print("Exit command received. Disconnecting...")
            time.sleep(2)
            sock.close()
            sys.exit()
        else:
            return f"@{username} you do not have permission to use this command! Only {CHANNEL} can use it!"

    return None

def moderate(username: str, message: str):
    matches = []
    for action, keywords in modActions.items():
        for keyword in keywords:
            if keyword.lower() in modActions.items():
                matches.append(action, keyword)
    return matches

def run_bot(sock):
    global running
    buffer = ""

    while running:
        try:
            buffer += sock.recv(2048).decode("utf-8", errors="ignore")
            lines = buffer.split("\r\n")
            buffer = lines.pop()

            for response in lines:
                if response.startswith("PING"):
                    sock.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
                    continue

                if "PRIVMSG" in response:
                    parts = response.split(":", 2)
                    if len(parts) >= 3:
                        info = parts[1].split("!")
                        username = info[0]
                        message = parts[2].strip()           
                        modActionRequired = moderate(username, message)
                        if modActionRequired:
                            for action, keyword in badWordMatches:
                                reason = modActionTriggers['reason']
                                print(f"Taking {action} action against {username} (said '{keyword}')")
                                if action == Warn:
                                    sock.send(f"PRIVMSG #{CHANNEL} :/warn {username} {reason} Consequence: Warning".encode("utf-8"))
                                elif action == Timeout:
                                    silenceTime = modActionTriggers['TimeoutTime']
                                    sock.send(f"PRIVMSG #{CHANNEL} :/timeout {username} {silenceTime} {reason} Consequence: Timeout of {silenceTime} seconds.")
                                elif action == Ban:
                                    sock.send(f"PRIVMSG #{CHANNEL} :/ban {username} {reason} Consequence: Ban.")  
                        else:
                            print(f"{username}: {message}")

                        try:
                            with open("uniqueChatters", "r") as chattersFile:
                                usernames = {line.strip() for line in chattersFile}
                        except FileNotFoundError:
                            usernames = set()
                        if username not in usernames:
                            with open("uniqueChatters.txt", "a") as chattersFile:
                                print(username)

                        if message.startswith("v!") or message.startswith("!"):
                            reply_text = handle_command(message.lower(), username, sock)
                            if reply_text:
                                reply = f"PRIVMSG #{CHANNEL} :{reply_text}\r\n"
                                sock.send(reply.encode("utf-8"))
                                print(f"Replied to {message} from {username}")
                        elif message.endswith("viewers PogChamp") and "just raided the channel with" in message:
                            raider = message.split(" ")[0]
                            print(f"{raider} just raided the channel, shoutout in progress...")
                            sock.send(f"PRIVMSG #{CHANNEL} :/shoutout {raider}".encode("utf-8"))
                        

        except socket.timeout:
            continue
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)
            break
        
if __name__ == "__main__":
    load_commands()
    sock = connect_to_twitch()
    if sock:
        input_thread = threading.Thread(target=monitor_input, args=(sock,))
        input_thread.daemon = True
        input_thread.start()

        try:
            run_bot(sock)
        except KeyboardInterrupt:
            print("Bot manually stopped.")
        finally:
            sock.close()
            print("Socket closed. Now exiting.")
            time.sleep(2)
    else:
        print("Failed to connect to Twitch IRC. Exiting...")
        time.sleep(2)