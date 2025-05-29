import discord
import asyncio
import os
from datetime import datetime
import pytz
import json
from dotenv import load_dotenv
load_dotenv()
#fixed so the shit isnt hardcoded
BOT_TOKEN = os.getenv("BOT_TOKEN")
intents = discord.Intents.all()
client = discord.Client(intents=intents)
#call ts whenever you need to load a .txt file
def load_word_list(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip().lower() for line in file if line.strip()]

#loads config file
def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)
config = load_config()


#function to add banned word to banlist.
def load_new_banned_word(strippedmessage):
    nl = '\n'
    with open("banned_shit.txt", "a", encoding="utf-8") as file:
        file.write(f"{nl}{strippedmessage}")

#function to add brainrot words to brainrot list.
def load_new_brainrot_word(strippedmessage):
    nl = '\n'
    with open("brainrot_shit.txt", "a", encoding="utf-8") as file:
        file.write(f"{nl}{strippedmessage}")

#function to add exempt words to exempt list.
def load_new_exempt_word(strippedmessage):
    nl = '\n'
    with open("exempt_shit.txt", "a", encoding="utf-8") as file:
        file.write(f"{nl}{strippedmessage}")

#function to remove banned word from banlist.
def remove_banned_word(strippedmessage):
    with open("banned_shit.txt", "r", encoding="utf-8") as f:
        lines = [line.rstrip('\n') for line in f if line.strip()]
    normalized_lines = [line.strip().lower() for line in lines]
    if strippedmessage in normalized_lines:
        idx = normalized_lines.index(strippedmessage)
        del lines[idx]
        with open("banned_shit.txt", "w", encoding="utf-8") as f:
            f.seek(0)
            f.write('\n'.join(lines)) 
            f.truncate()
    else:
        print("huh, somehow this shit managed to bypass the command level check. your kinda fucked.")


#function to remove brainrot word from brainrot list.
def remove_brainrot_word(strippedmessage):
    with open("brainrot_shit.txt", "r", encoding="utf-8") as f:
        lines = [line.rstrip('\n') for line in f if line.strip()]
    normalized_lines = [line.strip().lower() for line in lines]
    if strippedmessage in normalized_lines:
        idx = normalized_lines.index(strippedmessage)
        del lines[idx]
        with open("brainrot_shit.txt", "w", encoding="utf-8") as f:
            f.seek(0)
            f.write('\n'.join(lines)) 
            f.truncate()
    else:
        print("huh, somehow this shit managed to bypass the command level check. your kinda fucked.")

#function to remove exempt word from exempt list.
def remove_exempt_word(strippedmessage):
    with open("exempt_shit.txt", "r", encoding="utf-8") as f:
        lines = [line.rstrip('\n') for line in f if line.strip()]
    normalized_lines = [line.strip().lower() for line in lines]
    if strippedmessage in normalized_lines:
        idx = normalized_lines.index(strippedmessage)
        del lines[idx]
        with open("exempt_shit.txt", "w", encoding="utf-8") as f:
            f.seek(0)
            f.write('\n'.join(lines)) 
            f.truncate()
    else:
        print("huh, somehow this shit managed to bypass the command level check. your kinda fucked.")


#gets time and date, updates every time a message is logged to the black book.
timezone = pytz.timezone('US/Eastern')
def getdatetime():
    dateandtime = datetime.now(timezone)
    return dateandtime.strftime('%I:%M %p').lstrip('0'), dateandtime.date()


banned_words = load_word_list("banned_shit.txt")
brainrot_words = load_word_list("brainrot_shit.txt")
exempt_words = load_word_list("exempt_shit.txt")


milton_id = config['milton_id']
disboard_id = config['disboard_id']
shitpost_channel_id = config['shitpost_id']
brainrot_channel_id = config['brainrot_id']
furry_channel_id = config['furry_id']
mod_role_id = config['mod_role_id']
admin_role_id = config['admin_role_id']
bot_testing_id = config['bot_testing_id']


@client.event
async def on_ready():
    print("entered the mainframe as {0.user}".format(client))


#does the shit to log assholes who use slurs
def log_banned_message(message):
    nl = '\n'
    logtime, logdate = getdatetime()
    print("big milton is always watching")
    with open("miltons_black_book.txt", "a", encoding="utf-8") as file:
        file.write(f"deleted the message '{message.content}' from {message.author.name} on {logdate} at {logtime}.{nl}")


#defines the delayed message shit for bump reminder
async def delayed_response(channel):
    await asyncio.sleep(120 * 60)  # wait the full 120 minit so disboard can be rebumped
    await channel.send("<@&1365142978733281422> Its time to bump the server!")
    print("bump reminder sent, boss")


#buncha shit
@client.event
async def on_message(message):

    #declares these as globals, because everything dies if they arent
    global exempt_words
    global brainrot_words
    global banned_words

    #gets the roles of a message author for purposes of checking perms
    author_roles = [role.id for role in message.author.roles]

    #reloads the text config files
    if message.content.startswith("!reloadwordconfig"):
        if mod_role_id in author_roles or admin_role_id in author_roles:
            #why did i not make this a function?
            banned_words = load_word_list("banned_shit.txt")
            brainrot_words = load_word_list("brainrot_shit.txt")
            exempt_words = load_word_list("exempt_shit.txt")
            print("Reloaded .txt files.")
            await message.channel.send("Word config files reloaded, boss.")
        else:
            await message.channel.send("Invalid permissions to execute command, gangy.")



    #appends shit to the banned_shit.txt, it should hopefully not mess with formatting.
    if message.content.startswith("!addbannedword"):
        if admin_role_id in author_roles:
            if len(message.content) >= 15 and message.content[14].isspace():
                strippedmessage = message.content[15:].lower()
                if strippedmessage not in banned_words:
                    load_new_banned_word(strippedmessage)
                    await message.channel.send(f"Added '{strippedmessage}' to banlist, boss. Reloading .txt file...")
                    banned_words = load_word_list("banned_shit.txt")
                else:
                    await message.channel.send(f"That word is already in the list, bud.")
            else:
                await message.channel.send("Invalid syntax.")
        else:
            await message.channel.send("Invalid permissions to execute command, gangy.")


    #same as above but removes words.
    if message.content.startswith("!removebannedword"):
        if admin_role_id in author_roles:
            if len(message.content) >= 18 and message.content[17].isspace():
                strippedmessage = message.content[18:].lower()
                if strippedmessage in banned_words:
                    remove_banned_word(strippedmessage)
                    await message.channel.send(f"'{strippedmessage}' is no longer illegal. Reloading .txt file...")
                    banned_words = load_word_list("banned_shit.txt")
                else:
                    await message.channel.send(f"That word isnt banned, bud.")
            else:
                await message.channel.send("Invalid syntax.")
        else:
            await message.channel.send("Invalid permissions to execute command, gangy.")





    #appends shit to the brainrot_shit.txt, it should hopefully not mess with formatting.
    if message.content.startswith("!addbrainrotword"):
        if admin_role_id in author_roles or mod_role_id in author_roles:
            if len(message.content) >= 17 and message.content[16].isspace():
                strippedmessage = message.content[17:].lower()
                if strippedmessage not in brainrot_words:
                    load_new_brainrot_word(strippedmessage)
                    await message.channel.send(f"Added '{strippedmessage}' to brainrot list, boss. Reloading .txt file...")
                    brainrot_words = load_word_list("brainrot_shit.txt")
                else:
                    await message.channel.send(f"That word is already in the list, bud.")
            else:
                await message.channel.send("Invalid syntax.")
        else:
            await message.channel.send("Invalid permissions to execute command, gangy.")


    #same as above but removes words.
    if message.content.startswith("!removebrainrotword"):
        if admin_role_id in author_roles or mod_role_id in author_roles:
            if len(message.content) >= 20 and message.content[19].isspace():
                strippedmessage = message.content[20:].lower()
                if strippedmessage in brainrot_words:
                    remove_brainrot_word(strippedmessage)
                    await message.channel.send(f"'{strippedmessage}' is no longer brainrot. Reloading .txt file...")
                    brainrot_words = load_word_list("brainrot_shit.txt")
                else:
                    await message.channel.send(f"That word isnt brainrot, bud.")
            else:
                await message.channel.send("Invalid syntax.")
        else:
            await message.channel.send("Invalid permissions to execute command, gangy.")




    #appends shit to the exempt_shit.txt, it should hopefully not mess with formatting.
    if message.content.startswith("!addexemptword"):
        if admin_role_id in author_roles or mod_role_id in author_roles:
            if len(message.content) >= 15 and message.content[14].isspace():
                strippedmessage = message.content[15:].lower()
                if strippedmessage not in exempt_words:
                    load_new_exempt_word(strippedmessage)
                    await message.channel.send(f"Added '{strippedmessage}' to exempt word list, boss. Reloading .txt file...")
                    exempt_words = load_word_list("exempt_shit.txt")
                else:
                    await message.channel.send(f"That word is already in the list, bud.")
            else:
                await message.channel.send("Invalid syntax.")
        else:
            await message.channel.send("Invalid permissions to execute command, gangy.")


    #same as above but removes words.
    if message.content.startswith("!removeexemptword"):
        if admin_role_id in author_roles or mod_role_id in author_roles:
            if len(message.content) >= 18 and message.content[17].isspace():
                strippedmessage = message.content[18:].lower()
                if strippedmessage in exempt_words:
                    remove_exempt_word(strippedmessage)
                    await message.channel.send(f"'{strippedmessage}' is no longer exempt. Reloading .txt file...")
                    exempt_words = load_word_list("exempt_shit.txt")
                else:
                    await message.channel.send(f"That word isnt exempt, bud.")
            else:
                await message.channel.send("Invalid syntax.")
        else:
            await message.channel.send("Invalid permissions to execute command, gangy.")





    #prints the banlist to #bot-testing.
    if message.content.startswith("!checkbanlist"):
        if mod_role_id in author_roles or admin_role_id in author_roles:
            await message.channel.send(f"Printing banlist in <#{bot_testing_id}>, chief.")
            bottestchannel = client.get_channel(bot_testing_id)
            if bottestchannel is not None:
                await bottestchannel.send(f"`{banned_words}`")
            else:
                print("Bot testing doesnt exist, i guess.")
        else:
            await message.channel.send("Invalid permissions to execute command, gangy.")

    #prints the brainrot list to #bot-testing.
    if message.content.startswith("!checkbrainrotlist"):
        if mod_role_id in author_roles or admin_role_id in author_roles:
            await message.channel.send(f"Printing brainrot list in <#{bot_testing_id}>, chief.")
            bottestchannel = client.get_channel(bot_testing_id)
            if bottestchannel is not None:
                await bottestchannel.send(f"`{brainrot_words}`")
            else:
                print("Bot testing doesnt exist, i guess.")
        else:
            await message.channel.send("Invalid permissions to execute command, gangy.")
    
    #prints the exempt list to #bot-testing.
    if message.content.startswith("!checkexemptlist"):
        if mod_role_id in author_roles or admin_role_id in author_roles:
            await message.channel.send(f"Printing exempt word list in <#{bot_testing_id}>, chief.")
            bottestchannel = client.get_channel(bot_testing_id)
            if bottestchannel is not None:
                await bottestchannel.send(f"`{exempt_words}`")
            else:
                print("Bot testing doesnt exist, i guess.")
        else:
            await message.channel.send("Invalid permissions to execute command, gangy.")


    #fuck off, it didnt work the efficent way
    if any(word in message.content.lower() for word in exempt_words):
        has_exempt_word = True
    else:
        has_exempt_word = False


    #prevents jakey from buster browning himself
    if message.author == client.user:
        return


    #if ping, then pong. checks if the bot is alive
    if message.content.startswith("!ping"):
        await message.channel.send("Pong!")
        print("Pong!")


    #server bump reminder
    elif message.author.id == disboard_id:
        print(f"okie, registered a message from disboard")
        asyncio.create_task(delayed_response(message.channel))

    #does no brainrot logic
    if any(word in message.content.lower() for word in brainrot_words) and message.author.id != milton_id and message.channel.id != shitpost_channel_id and message.channel.id != brainrot_channel_id and message.channel.id != furry_channel_id and not message.content.startswith("!addbrainrotword") and not message.content.startswith("!removebrainrotword"):
        #fuck this took to long, but basically if a message contains an exempt word (word that contains a banned term within it but the full word is fine) then it ignores that instance of the banned word, however if there is another instance of a banned term in that same message, it still deletes it. My tiny furry brain needs a break.
        if has_exempt_word:
                cleaned_message = " ".join(word for word in message.content.lower().split() if word not in exempt_words)
                if any(word in cleaned_message for word in brainrot_words):
                    await message.delete()
        else:
            await message.delete()


    #filters out banned words n logs it and all that jazz
    if any(word in message.content.lower() for word in banned_words) and not message.content.startswith("!addbannedword") and not message.content.startswith("!removebannedword") and message.author.id != milton_id:
        logtime, logdate = getdatetime()
        await message.delete()
        await message.channel.send("woah there buster brown")
        print(f"deleted the message '{message.content}' from {message.author.name} on {logdate} at {logtime}.")
        log_banned_message(message)
        return

#runs the shit
client.run(BOT_TOKEN)