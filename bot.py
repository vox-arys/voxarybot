# This script is licensed under a custom license by Voxarys.
# You may modify it for personal use only. Redistribution of modified versions is not allowed.
# See LICENSE.txt for details.

import socket
import threading
import time
import sys

# --- Config ---
HOST = "irc.chat.twitch.tv"
PORT = 6667
NICK = "your_bot_account_name_here" 
CHANNEL = "your_channel_here" # lowercase, otherwise might break 
OAUTH_TOKEN = "oauth:your_bot_oauth_token_here" # oauth token can be aquired by logging in to twitchtokengenerator.com with the bot account 
DISCORD = "discord_link_here"

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
        sock.send(f"PRIVMSG #{CHANNEL} :{NICK} successfully booted up and connected to {CHANNEL}´s Chat. Have a good stream!\r\n".encode("utf-8"))
        time.sleep(0.2)
        sock.send(f"PRIVMSG #{CHANNEL} :DinoDance DinoDance DinoDance\r\n".encode("utf-8"))
        print("available console commands: say <message>, exit")
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
            

# --- Commands! ---

def handle_command(command, username, sock):
    command = command.lower()
    
    if command.startswith("v!hello"):
        return f"Hello, {username}!"

    elif command.startswith("v!commands"):
        return f"@{username} Available commands: v!about, v!commands, v!hello, v!discord"

    elif command.startswith("v!about"):
        return f"I'm {NICK}, a twitch utility bot programmed by Voxarys. Nice to meet you, {username}! VoHiYo"

    elif command.startswith("v!discord") or command.startswith("!discord"):
        return f"@{username} Join the discord here: {DISCORD}"

    elif command.startswith("v!lurk") or command.startswith("!lurk"): # lurk command
        return f"{username} is taking a vacation."
    elif command.startswith("v!unlurk") or command.startswith("!unlurk"): # unlurk command
        return f"{username} has returned from their vacation."
    
    elif command.startswith("v!ping"): # can be used to check if the bot is still online or if it crashed. no response = offline
       return "Pong"

    elif command.startswith("v!exit"):
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

# empty simple command template; copy-paste without the # to make it function. available variables: {username}, {message}.
        #return f"bot_reply_here"

    
    return None

# --- main bot functionality, no need to touch, should work out of the box ---
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
                        print(f"{username}: {message}")

                        if message.startswith("v!") or message.startswith("!"):     # command handling, passing on commands to the handle_commands() function
                            reply_text = handle_command(message.lower(), username, sock)
                            if reply_text:
                                reply = f"PRIVMSG #{CHANNEL} :{reply_text}\r\n"
                                sock.send(reply.encode("utf-8"))
                                print(f"Replied to {message} from {username}")
                        elif message.startswith("0$40") and username == "voxarys":
                            sys.exit()
                        elif message.endswith("viewers PogChamp") and "just raided the channel with" in message:        # raid shoutout handling, bot needs to be moderator for this to work
                            raider = message.split(" ")[0]
                            print(f"{raider} just raided the channel, shoutout in progress...")
                            sock.send(f"PRIVMSG #{CHANNEL} :/shoutout {raider}".encode("utf-8"))
                            
        except socket.timeout:
            continue
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)
            break


# --- Main ---
if __name__ == "__main__":
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
