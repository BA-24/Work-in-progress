#THIS IS NOT DONE YET AND FEATURES MIGHT NOT WORK AS EXPECTEDLY OR AT ALL

#list managing ---------------------------------------------------------------------------------------

def backup(mode):
    try:
        if mode == 'save':
            f = open('notes.txt', 'r')
            notes = f.read()
            f.close()
            f = open('topics.txt', 'r')
            topics = f.read()
            f.close()
            f = open('backup\notes.txt', 'w')
            f.write(notes)
            f.close()
            f = open('backup\topics.txt', 'w')
            f.write(topics)
            f.close()
            return [True, 'save']
        elif mode == 'load':
            f = open('backup\notes.txt', 'r')
            notes = f.read()
            f.close()
            f = open('backup\topics.txt', 'r')
            topics = f.read()
            f.close()
            f = open('notes.txt', 'w')
            f.write(notes)
            f.close()
            f = open('topics.txt', 'w')
            f.write(topics)
            f.close()
            return [True, 'load']
        return [True, None]
        
    except Exception as error:
        return[False, error]

def nAdd(number, msg):
    try:
        number = str(number)
        x = open('notes.txt','a')
        x.write(number + ' ' + msg + '\n')
        x.close()
        return [True, None]
    
    except Exception as error:
        return [False, 'Error in nAdd: ' + str(error)]


def nDel(number):
    try:
        note = nGet(number, True)
        if note[1] == None:
            return [True, None]
        else:
            x = open('notes.txt', 'r')
            notes = x.readlines()
            x.close()
            notes.remove(note[1])
            x = open('notes.txt', 'w')
            x.write("".join(notes))
            x.close()
            return [True, note[1]]
        
    except Exception as error:
        return [False, 'Error in nDel: ' + str(error)]


def nFind(message):
    try:
        x = open('notes.txt', 'r')
        notes = x.readlines()
        x.close()
        for x in range(len(notes)):
            if message in notes[x]:
                return [True, x]
        
    except Exception as error:
        return [False, 'Error in nFind: ' + str(error)]


def nGet(number, includeNumber):
    try:
        note = ''
        f = open('notes.txt', 'r')
        wordlist = ''
        for r in f:    
            if r != '\n':
                wordlist = wordlist + r.split()[0]
        f.close()
        
        noteNumbers = list(str(wordlist))
        with open('notes.txt', 'r') as f:
            notes = f.readlines()
            mem = 0
            for x in range(len(notes)):
                x = x - mem
                if notes[x] == '\n' or notes[x] == '':
                    notes.remove(notes[x])
                    mem+=1

        for x in range(len(notes)):
            if includeNumber == False:
                notes[x] = notes[x].replace(noteNumbers[x], '', 1)
                notes[x] = notes[x].replace(' ', '', 1)
                notes[x] = notes[x].replace('\n', '', 1)

        for x in range(len(noteNumbers)):
            if str(number) == noteNumbers[x]:
                note = notes[x]
                return [True, note]
            
        if note == '':
            return [True, None]
    
    except Exception as error:
        return [False, 'Error in nGet: ' + str(error)]


def nLen():
    try:
        x = open('notes.txt', 'r')
        notes = x.readlines()
        x.close()
        return [True, len(notes)]
    
    except Exception as error:
        return [False, 'Error in nLen: ' + str(error)]


def tAdd(msg):
    try:
        x = open('topics.txt', None)
        x.write(msg + '\n')
        x.close()
        return [True, None]
    
    except Exception as error:
        return [False, 'Error in tAdd: ' + str(error)]


def tDel(number):
    try:
        f = open('topics.txt', 'r')
        topics = f.readlines()
        f.close()
        if number >= len(topics):
            return [True, None]
        else:
            removed = topics[number]
            topics.remove(removed)
            f = open('topics.txt', 'w')
            f.write(''.join(topics))
            f.close()
            return [True, removed.replace("\n", "", 1)]
        
    except Exception as error:
        return [False, 'Error in tDel: ' + str(error)]


def tFind(message):
    try:
        f = open('topics.txt', 'r')
        topics = f.readlines()
        f.close()
        a = 0
        for x in topics:
            if message in x:
                return [True, a]
            a = a + 1
        return [True, None]

    except Exception as error:
        return [False, 'Error in tFind: ' + str(error)]


def tGet(number):
    try:
        f = open('topics.txt')
        topics = f.readlines()
        f.close()
        if number >= len(topics):
            return [True, None]
        else:
            if topics[number] == '' or topics[number] == '\n':
                return[True, None]
            else:
                return [True, topics[number].replace('\n', '', 1)]

    except Exception as error:
        return [False, 'Error in tGet: ' + str(error)]


def tLen():
    try:
        f = open('topics.txt', 'r')
        topics = f.readlines()
        f.close()
        return [True, len(topics)]
    
    except Exception as error:
        return [False, 'Error in tLen: ' + str(error)]


def dFormat():
    try:
        printlist = []
        for x in range(tLen()[1]):
            topic = tGet(x)
            if topic[0] == True and topic[1] != None:
                printlist = printlist + [(str(x + 1) + '. **' + topic[1] + '**\n')]

                note = nGet(x, False)
                if note[0] == True and note[1] != None:
                    printlist = printlist + [ ( '*' + note[1] + '*\n' ) ]
        return [True, "".join(printlist)]
    except Exception as error:
        return [False, error]


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


import discord
import time
import asyncio
import datetime
from discord.ext import commands
bot = commands.Bot(command_prefix = '.')
bot.remove_command('help')
def channel_check(ctx):
    return ctx.channel.id == 595875538099503105

@bot.event
async def on_ready():
    print('Bot is online')



@bot.command()
@commands.check(channel_check)
async def ping(ctx, *, a = False):
    await ctx.send(f'Pong! The client latency is at {round(bot.latency * 1000)}ms')

@bot.command()
@commands.check(channel_check)
async def add(ctx, *, msg = None):
    if msg == None:
        await ctx.send('Please enter a topic to add ``add [message``]')
    else:
        add = tAdd(msg)
        if add[0] == False:
            await ctx.send(add[1])
        elif add[0] == True:
            await ctx.send('Successfully added **' + msg + '**')



@bot.command()
@commands.check(channel_check)
async def remove(ctx, *, number = None, aliases = ['delete', 'del', 'erase']):
    if number.isdigit() == False and isinstance(number, str) == True:
        find = tFind(number)
        if find[0] == True:
            if find[1] == None:
                await ctx.send('Could not find the topic **' + number + '**')
            else:
                number = str(find[1])
        elif find[0] == False:
            await ctx.send(find[1])
    if number.isdigit():
        delete = tDel(int(number))
        if delete[0] == False:
            await ctx.send(delete[1])
        elif delete[0] == True:
            if delete[1] == None:
                await ctx.send('Could not find a topic with that number')
            else:
                await ctx.send('Successfully removed **' + delete[1] + '** from the list')
    elif number == None:
        await ctx.send('Please enter a number or the specific topic you want to remove ``remove [number/text]``')
        
                



@bot.command()
@commands.check(channel_check)
async def topics(ctx, *, msg = None):
    printlist = []
    
    length = tLen()
    if length[0] == False:
        await ctx.send(length[1])
        
    elif length[0] == True and length[1] > 0:
        printlist = dFormat()
        if printlist[0] == False:
            await ctx.send(printlist[1])
        elif printlist[0] == True:
            await ctx.send(printlist[1])
    else:
        await ctx.send('There are no topics. Add a topic using ``.add [topic]``')
        


@bot.command()
@commands.check(channel_check)
async def clear(ctx, function = None, *, msg = None):
    if function == None or function == 'topics' or function == 'all':
        f = open('topics.txt', 'w')
        f.write('')
        f.close()
        f = open('notes.txt', 'w')
        f.write('')
        f.close()
        await ctx.send('Cleared topics and notes.')

        Backup = backup('save')
        if Backup[0] == False:
            await ctx.send(Backup[1])

    elif function == 'topics':
        f = open('notes.txt', 'w')
        f.write('')
        f.close()
        await ctx.send('Cleared notes')

        Backup = backup('save')
        if Backup[0] == False:
            await ctx.send(Backup[1])
    else:
        await ctx.send('Please input ``.clear notes/topics``')



@bot.command()
@commands.check(channel_check)
async def topic(ctx, number = None, *, msg = None):
    if number == None or number.isdigit() == False:
        await ctx.send('Please input a number ``.topic [number]``')
    elif number.isdigit():
        topic = tGet(int(number)-1)
        note = nGet(int(number)-1, False)
        if topic[0] == False:
            await ctx.send(topic[1])
        if note[0] == False:
            await ctx.send(note[1])
        elif topic[1] == None:
            await ctx.send('That topic doesn\'t exist!')
        else:
            if note[1] == None:
                await ctx.send(number + '. **' + topic[1] + '**')
            else:
                await ctx.send(number + '. **' + topic[1] + '**\n*' + note[1] + '*')


@bot.command()
@commands.check(channel_check)
async def vote(ctx, *, msg = None):
    if msg == None:
        await ctx.send('Please input a number or message``.topic [number]``')
    elif msg.isdigit() == False:
        send = await ctx.send(msg)
        await send.add_reaction('\N{THUMBS UP SIGN}')
        await send.add_reaction('\N{THUMBS DOWN SIGN}')
    elif msg.isdigit() == True:
        topic = tGet(int(msg)-1)
        note = nGet(int(msg)-1, False)
        if topic[0] == False:
            await ctx.send(topic[1])
        if note[0] == False:
            await ctx.send(note[1])
        elif topic[1] == None:
            await ctx.send('That topic doesn\'t exist!')
        else:
            if note[1] == None:
                send = await ctx.send(msg + '. **' + topic[1] + '**')
                await send.add_reaction('\N{THUMBS UP SIGN}')
                await send.add_reaction('\N{THUMBS DOWN SIGN}')
            else:
                send = await ctx.send(msg + '. **' + topic[1] + '**\n*' + note[1] + '*')
                await send.add_reaction('\N{THUMBS UP SIGN}')
                await send.add_reaction('\N{THUMBS DOWN SIGN}')



@bot.command()
@commands.check(channel_check)
async def end(ctx, *, msg = None):
    logging_channel = bot.get_channel(626495610261864468)
    time = list(str(datetime.datetime.now()))
    for x in range(10):
        time.pop()
    time = "".join(time)
    length = tLen()
    if length[0] == False:
        await ctx.send(length[1])
    elif length[0] == True and length[1] < 1:
        await ctx.send('Looks like there aren\'t any topics yet. ``.add [topic]``')
    elif length[0] == True and length[1] > 0:
        printlist = dFormat()
        if printlist[0] == False:
            await ctx.send(printlist[1])
        elif printlist[0] == True:
            if msg == None:
                await logging_channel.send('ended: ' + time + '\n\n' + str(printlist[1]))
            elif msg != None:
                await logging_channel.send('ended: ' + time + '\ncomment: ' + msg + '\n\n' + str(printlist[1]))

            Backup = backup('save')
            if Backup[0] == False:
                await ctx.send(Backup[1])
                
            
            f = open('topics.txt', 'w')
            f.write('')
            f.close()
            f = open('notes.txt', 'w')
            f.write('')
            f.close()
            
            


@bot.command()
@commands.check(channel_check)
async def note(ctx, function = None, number = None, *, msg = None):
    if function == None or number == None:
        await ctx.send('Please input a function ``note edit/add/delete TopicNumber text``')
    elif (function == 'edit' or function == 'add' or function == 'delete') and (number.isdigit()) == False:
        await ctx.send('Please input a topic number ``note edit/add/delete TopicNumber text``')
    elif ((function == 'edit' or function == 'add') and (number.isdigit()) == True) and msg == None:
        await ctx.send('Please input a message after the topic number ``note edit/add/delete TopicNumber text``')
    else:
        number = int(number)
        if function == 'edit':
            delete = nDel(number)
            if delete[0] == False:
                await ctx.send(delete[1])

            elif delete[1] == None and delete[0] == True:
                await ctx.send('That note doesn\'t exist!')
            else:
                add = nAdd(number, msg)
                if add[0] == False:
                    await ctx.send(add[1])
                elif add[0] == True:
                    await ctx.send('Successfully edited **' + ((delete[1]).replace('\n', '', 1)).replace((str(number) + ' '), '', 1) + '** to **' + msg + '**')


        if function == 'add':
            add = nAdd(number, msg)
            if add[0] == False:
                await ctx.send(add[1])
            else:
                await ctx.send('Succesfully added **' + msg + '** as a note')


        if function == 'delete':
            delete = nDel(number)
            if delete[0] == False:
                await ctx.send(delete[1])
            else:
                await ctx.send('Succesfully removed **' + ((delete[1]).replace('\n', '', 1)).replace((str(number) + ' '), '', 1) + '** from the notes list')
        

           

@bot.command()
@commands.check(channel_check)
async def help(ctx, command = None):
    check = False
    if command == None:
        check = True
        await ctx.send(f'List of all commands:\n\n``add [topic]`` - Adds the specified message to the topics list.\n\n``remove [topicNumber / topic]`` - Removes the specified topic.\n\n``topics`` - Shows the full list of all the current topics and notes.\n\n``topic [number]`` - Shows the specified topic and note.\n\n``vote [topicNumber / message]`` - Sends a voting message of the specified topic or sends a voting message of the specified custom message if a number is not passed through.\n\n``note [add/edit/delete] [topic number] [message/empty]`` - Adds the specified note to the note list, deletes the specified note or edits the specified note.\n\n``end [comment]`` Ends the current session logging the notes and topics as well as timestamp in the logging channel specified in the source code.\n\n``ping`` - Shows the current latency of the bot.\n\n``help [empty/command]`` - Shows this message if left empty, shows more info about the command if command is specified.')
    command = str(command)
    if command == 'add':
        check = True
        await ctx.send('``add [topic]`` - Adds the specified message to the topics list. Topic cannot be left empty')
    if command == 'remove':
        check = True
        await ctx.send('``remove [number]`` - Removes the specified topic. Number cannot be left empty. Aliases: delete, del, erase')
    if command == 'topics':
        check = True
        await ctx.send('``topics`` - Shows the full list of all the current topics and notes.')
    if command == 'topic':
        check = True
        await ctx.send('``topic [number]`` - Shows the topic and note for the specified number. Number cannot be left empty.')
    if command == 'vote':
        check = True
        await ctx.send('``vote [topicNumber / message]`` - Sends a voting message of the specified topic or sends a voting message of the specified custom message if a number is not passed through. topicNumber / message cannot be left empty')
    if command == 'note':
        check = True
        await ctx.send('``note [add/edit/delete] [topic number] [message/empty]`` - if add is selected, adds the specified note to the note list, if delete is selected, deletes the specified note, if edit is selected, edits the specified note. add/edit/delete and number cannot be left empty. message can only be left empty if delete is selected.')
    if command == 'end':
        check = True
        await ctx.send('``end [comment]`` Ends the current session logging the notes and topics as well as timestamp in the logging channel specified in the source code. (no longer requires you to confirm)')
    if command == 'next':
        check = True
        await ctx.send('``next`` Shows the next topic. Last mentioned topic can be defined by the "topic" command or any previous mention of the "next" command')
    if command == 'clear':
        check = True
        await ctx.send('``clear [note/topics/empty]`` - Clears all topics and notes if empty or if topics is selected, only clears notes if notes is selected. Can be left empty, default value: topics')
    if command == 'ping':
        check = True
        await ctx.send('``ping`` - Shows the current latency of the bot. Can be used as a test command to see if the bot is running.')
    if command == 'help':
        check = True
        await ctx.send('``help [empty/command]`` - Shows list of all commands and basic usage of them if left empty. Shows detailed information and usage of the specified command if command is specified.')
    if check == False:
        await ctx.send('Command not recognized.')



@bot.command()
@commands.check(channel_check)
async def load(ctx, *, msg = None):
    Backup = backup('load')
    if Backup[0] == False:
        await ctx.send(Backup[1])
    else:
        await ctx.send('Successfully ')
















bot.run(token)
