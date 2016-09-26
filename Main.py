# coding=utf-8
import discord
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

# TODO: NO GLOBAL VARIABLES
previous_playing_message = None
prefix_qualifier = '>'
prefix_debug = '>!!'
prefix_information = '>!'
prefix_question = '>?'
ATSUI = '153789058059993088'
allowed_testing = ['154488551596228610', '164476517101993984']
testing_mode = False
BOT = '225810441610199040'
server_exclude = ['110373943822540800']
exclusion_max = len(server_exclude)
tunnel_receive_a = None
tunnel_receive_b = None
tunnel_enable = False
server_linked = []
player_joined = []
table_limits = [['Blackjack'], [6]]
room_status = ['Waiting', 'In Progress']
minigame_session = [['Testing room', 'Blackjack', 'Testing', '0']]
client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as ' + client.user.name)
    print('Discord ID: ' + client.user.id)
    print('------')
    print(client)
    print('Created by SamuiNe <https://github.com/SamuiNe>')
    global previous_playing_message
    previous_playing_message = 'with pointers'
    if testing_mode:
        await client.change_status(game=discord.Game(name='Testing mode enabled'), idle=False)
    else:
        await client.change_status(game=discord.Game(name='with pointers'), idle=False)
    token.close()
    print('Discord Bot (Sophia) Version 0.0.6, Ready.')


@client.event
async def on_message(message):
    print(message)
    messagelow = message.content.lower()

    isallowed = True
    isperson = True

    if message.author.id == BOT:
        isperson = False

    if testing_mode:
        if message.server.id not in allowed_testing:
            isperson = False

    if isperson:
        # TODO: Allow multiple combinations of servers for chat tunnelling

        # Checks if the chat tunnelling mode is enabled and if the tunnel_receive_a and tunnel_receive_b is not none
        if tunnel_enable and tunnel_receive_a is not None and tunnel_receive_b is not None:
                if tunnel_receive_a == message.channel:
                    await client.send_message(tunnel_receive_b, str(message.author) + 
                        ' - ' + message.content)
                elif tunnel_receive_b == message.channel:
                    await client.send_message(tunnel_receive_a, str(message.author) + 
                        ' - ' + message.content)

        if message.content.startswith(prefix_qualifier):
            if message.content.startswith(prefix_question):
                if messagelow == prefix_question + 'about':
                    await client.send_message(message.channel, 'Hello! I am Sophia. Please treat me well!')

                elif message.content == prefix_question + 'help' or message.content == prefix_question + 'commands':
                    await client.send_message(message.channel, 'Here are the commands I recognize at the moment:\n\n' +
                        '*Question commands* (starts with `' + prefix_question + '`)\n' +
                        '`about`, `help` (`commands`)\n' +
                        '*Information commands* (starts with `' + prefix_information + '`)\n' +
                        '`hello`, `sara` (`sarachan`), `invite`, `ping` (`pong`), `roomjoin`, `roomcheck`\n' +
                        '*Trigger commands*\n' +
                        ':coffee:, :tea:, `cawfee`, `gween tea`, ' +
                        '`\u0028\u256f\u00b0\u25a1\u00b0\uff09\u256f\ufe35 \u253b\u2501\u253b`\n' +
                        '...with 11 secret commands!')

            elif message.content.startswith(prefix_information):
                if message.content == prefix_information + 'hello':
                    mess_len = len(str(message.author))
                    await client.send_message(message.channel, 'Hello ' + str(message.author)[:mess_len-5] + ' o/')

                elif messagelow == prefix_information + 'sarachan' or messagelow == prefix_information + 'sara':
                    await client.send_message(message.channel, 'https://puu.sh/r5mt4/f9eb13dc29.gif')

                # TODO: Add discord link to the discord server and continue to polish the bot
                elif messagelow == prefix_information + 'invite':
                    await client.send_message(message.channel,
                        'You can take me to your discord server by clicking the link below' + '\n' +
                        'Please note that you will need at least "administrator" to add bots!' +
                        'https://discordapp.com/oauth2/authorize?client_id=225810441610199040&scope=bot&permissions=0' +
                        '\n\n' +
                        'Interested in joining my discord guild? You can visit it by using the invite link below!' +
                        '\n' +
                        'https://discord.gg/SpTWKDd')

                elif messagelow == prefix_information + 'ping':
                    await client.send_message(message.channel, 'pong!')

                elif messagelow == prefix_information + 'pong':
                    await client.send_message(message.channel, 'ping!')

                elif messagelow.startswith(prefix_information + 'roomcreate'):
                    global minigame_session
                    global table_limits
                    find_qualifier = ' '
                    find_room_id = messagelow.find(find_qualifier, 0)

                    await client.send_message(message.channel, 'Room created.')

                elif messagelow.startswith(prefix_information + 'roomjoin'):
                    global minigame_session
                    global table_limits
                    global player_joined
                    find_qualifier = ' '
                    find_room_id = messagelow.find(find_qualifier, 0)
                    find_room_password = messagelow.find(find_qualifier, find_room_id + 1)
                    room_id = messagelow[find_room_id + 1: find_room_id + 2]
                    room_player_count = len(minigame_session[int(room_id)]) - 3
                    game_name = table_limits[0].index(minigame_session[int(room_id)][1])
                    roomcapacity = table_limits[1][game_name]
                    is_allowed = True
                    
                    if minigame_session[int(room_id)][1] is not None and minigame_session[int(room_id)][2] != '':
                        # await client.send_message(message.channel, "Password exists")
                        if find_room_password is not -1:
                            # await client.send_message(message.channel, "User enters a password")
                            if message.content[find_room_password + 1:] != minigame_session[int(room_id)][2]:
                                # await client.send_message(message.channel, \
                                    # "Password does not match with the room password")
                                is_allowed = False
                        else:
                            # await client.send_message(message.channel, "User dun goofed")
                            is_allowed = False
                    '''await client.send_message(message.channel, message.content[find_room_password + 1:] +
                        str(len(message.content[find_room_password + 1:])) + '\n' +
                        minigame_session[int(room_id)][2] + str(len(minigame_session[int(room_id)][2])))'''

                    if is_allowed:
                        if room_player_count <= roomcapacity:
                            if message.author not in player_joined:
                                await client.send_message(message.channel, 'yes')
                                minigame_session[int(room_id)].append(message.author)
                                player_joined.append(message.author)
                                await client.send_message(message.channel, 'You are now in room ' + str(room_id) + '.')

                            else:
                                await client.send_message(message.channel, 'no')
                                await client.send_message(message.channel, 'Unable to join since you are in a room.')
                        else:
                            await client.send_message(message.channel, 'Unable to join since the room is full.')
                    else:
                        await client.send_message(message.channel, "Invalid room ID or room password.")

                elif messagelow.startswith(prefix_information + 'roomcheck'):
                    global minigame_session
                    find_qualifier = ' '
                    find_room_id = messagelow.find(find_qualifier, 0)
                    room_id = messagelow[find_room_id + 1:]
                    loop_limit = len(minigame_session[int(room_id)])
                    loop_count = 4
                    game_name = table_limits[0].index(minigame_session[int(room_id)][1])
                    is_password = False

                    if minigame_session[int(room_id)][1] is not None and minigame_session[int(room_id)][1] != '':
                        is_password = True

                    await client.send_message(message.channel, 'yes')

                    roominformation = '`Room Name`: ' + minigame_session[int(room_id)][0] + \
                        ' `Password`: ' + str(is_password) + '\n' + \
                        '`ID`: ' + str(room_id) + '\n' + \
                        '`Status`: ' + str(room_status[int(minigame_session[int(room_id)][3])]) + '\n' + \
                        '`Minigame`: ' + str(minigame_session[int(room_id)][1]) + \
                        ' `Player`: ' + str(loop_limit - 4) + ' / ' + str(table_limits[1][game_name]) + \
                        '\n' + '`Player List`: \n'

                    while loop_count != loop_limit:
                        if loop_count != loop_limit - 1:
                            roominformation += str(minigame_session[int(room_id)][loop_count]) + ', '
                        else:
                            roominformation += str(minigame_session[int(room_id)][loop_count])
                        loop_count += 1

                    await client.send_message(message.channel, roominformation)

                elif messagelow == prefix_debug + 'debug':
                    # if message.author.id == ATSUI:
                    await client.send_message(message.channel, '`Author`: ' + str(message.author) +
                        ' `' + str(message.author.id) + '`\n' +
                        '`MessLen`: ' + str(len(str(message.content))) + '\n' +
                        '`Channel`: ' + str(message.channel) + ' `' + str(message.channel.id) + '`\n' +
                        '`Server`: ' + str(message.server.name) + ' `' + str(message.server.id) + '`')

                elif messagelow.startswith(prefix_debug + 'tunnellink'):
                    if message.author.id == ATSUI:
                        global tunnel_receive_a
                        global tunnel_receive_b
                        channelid = message.channel.id

                        if str(messagelow)[-1:] == 'a':
                            # await client.send_message(message.channel, 'Debug info: ' + str(message.channel))
                            tunnel_receive_a = discord.utils.get(message.server.channels, id=channelid)
                            # await client.send_message(message.channel, tunnel_receive_a)
                            # await client.send_message(tunnel_receive_a, 'Test successful')
                            await client.send_message(message.channel, 'Channel A assignment successful')

                        elif str(messagelow)[-1:] == 'b':
                            # await client.send_message(message.channel, 'Debug info: ' + str(message.channel))
                            tunnel_receive_b = discord.utils.get(message.server.channels, id=channelid)
                            # await client.send_message(message.channel, tunnel_receive_b)
                            # await client.send_message(tunnel_receive_b, 'Test successful')
                            await client.send_message(message.channel, 'Channel B assignment successful')

                elif messagelow.startswith(prefix_debug + 'tunnel_enable'):
                    if message.author.id == ATSUI:
                        tunnel_enableparameter = str(messagelow)[16:]
                        await client.send_message(message.channel, tunnel_enableparameter)

                        if tunnel_enableparameter == 'yes' or tunnel_enableparameter == '1':
                            global tunnel_enable
                            tunnel_enable = True
                            await client.send_message(message.channel, 'Message tunneling enabled')

                        elif tunnel_enableparameter == 'no' or tunnel_enableparameter == '0':
                            global tunnel_enable
                            tunnel_enable = False
                            await client.send_message(message.channel, 'Message tunneling disabled')

                elif messagelow == prefix_debug + 'tunnelinfo':
                    if message.author.id == ATSUI:
                        if tunnel_receive_a is not None:
                            tunnelida = tunnel_receive_a.id
                        else:
                            tunnelida = 'None'

                        if tunnel_receive_b is not None:
                            tunnelidb = tunnel_receive_b.id
                        else:
                            tunnelidb = 'None'

                        await client.send_message(message.channel, '`Linked channel A`: ' + str(tunnel_receive_a) +
                            ' `' + tunnelida + '`' +
                            '\n' + '`Linked channel B`: ' + str(tunnel_receive_b) +
                            ' `' + tunnelidb + '`' +
                            '\n' + '`Tunnel Boolean`: ' + str(tunnel_enable))

                elif messagelow.startswith(prefix_debug + 'prefixchange'):
                    if message.author.id == ATSUI:
                        processindex = [0, None, None, None, None, None]
                        tempcollection = ['<', None, None, None, None]
                        exceptioncheck = False
                        find_qualifier = ' '
                        # findcheckbefore = 0
                        findcheckafter = 0
                        findcount = 0
                        processcount = 1
                        tempcounter = 0
                        exceptioncounter = 0

                        while findcheckafter != -1 and findcount != 5:
                            findcheckbefore = findcheckafter
                            findcheckafter = messagelow.find(find_qualifier, findcheckbefore + 1)

                            if findcheckafter != -1:
                                findcount += 1
                                processindex[findcount] = findcheckafter

                        while processindex[processcount] is not None and processcount != 5:
                            if processcount == 4:
                                tempcollection[tempcounter] = messagelow[(processindex[processcount] + 1):]
                            else:
                                tempcollection[tempcounter] = messagelow[processindex[processcount] + 1:
                                processindex[processcount + 1]]

                            tempcounter += 1
                            processcount += 1
                        ''' Old Code
                        if processindex[2] is not None:
                            tempqualifier = messagelow[processindex[1] + 1: \
                                (processindex[2] - processindex[1]) - 2]

                        if processindex[3] is not None:
                            tempquestion = messagelow[processindex[2] + 1: \
                                (processindex[3] - processindex[2]) - 2]

                        if processindex[4] is not None:
                            tempinformation = messagelow[processindex[3] + 1: \
                                (processindex[4] - processindex[3]) - 2]

                        if processindex[5] is not None:
                            tempdebug = messagelow[processindex[4] + 1: \
                                (processindex[5] - processindex[4]) - 2]
                        '''

                        if tempcollection[exceptioncounter] is not None and \
                                tempcollection[exceptioncounter + 1] is not None:

                            while tempcollection[exceptioncounter] is not None and exceptioncounter != 4:

                                if tempcollection[0] not in tempcollection[exceptioncounter]:
                                    exceptioncheck = True
                                exceptioncounter += 1
                        ''' Old code
                        if tempqualifier is not None and tempquestion is not None:
                            if tempquestion is not None and not tempquestion.startswith(tempqualifier):
                                exceptioncheck = True

                            if tempinformation is not None and not tempinformation.startswith(tempqualifier):
                                exceptioncheck = True

                            if tempdebug is not None and not tempinformation.startswith(tempqualifier):
                                exceptioncheck = True
                        '''

                        if exceptioncheck:
                            await client.send_message(message.channel, 'Prefix change failed')
                            '''await client.send_message(message.channel, 'Debug information:\n' + str(findcheckbefore) +
                                ' ' + str(findcheckafter) + ' ' + str(findcount) + ' ' + str(processcount) + ' ' +
                                str(tempcounter) + ' ' + str(exceptioncounter) + '\n' +
                                str(exceptioncheck) + '\n' +
                                '> ' + str(processindex[0]) + ' ' + str(processindex[1]) + ' ' +
                                str(processindex[2]) + ' ' + str(processindex[3]) + ' ' +
                                str(processindex[4]) + ' ' + str(processindex[5]) + '\n' +
                                '>> ' + str(tempcollection[0]) + ' ' + str(tempcollection[1]) + ' ' +
                                str(tempcollection[2]) + ' ' + str(tempcollection[3]) + '\n' +
                                'L> ' + str(len(str(tempcollection[0]))) + ', ' + str(len(str(tempcollection[1]))) +
                                ', ' + str(len(str(tempcollection[2]))) + ', ' + str(len(str(tempcollection[3]))))
                            '''

                        else:
                            global prefix_qualifier
                            global prefix_question
                            global prefix_information
                            global prefix_debug
                            prefix_qualifier = tempcollection[0]
                            prefix_question = tempcollection[1]
                            prefix_information = tempcollection[2]
                            prefix_debug = tempcollection[3]

                            await client.send_message(message.channel, 'Prefix change success')
                            '''await client.send_message(message.channel, 'Debug information:\n' + str(findcheckbefore) +
                                ' ' + str(findcheckafter) + ' ' + str(findcount) + ' ' + str(processcount) + ' ' +
                                str(tempcounter) + ' ' + str(exceptioncounter) + '\n' +
                                str(exceptioncheck) + '\n' +
                                '> ' + str(processindex[0]) + ' ' + str(processindex[1]) + ' ' +
                                str(processindex[2]) + ' ' + str(processindex[3]) + ' ' +
                                str(processindex[4]) + ' ' + str(processindex[5]) + '\n' +
                                '>> ' + str(tempcollection[0]) + ' ' + str(tempcollection[1]) + ' ' +
                                str(tempcollection[2]) + ' ' + str(tempcollection[3]) + '\n' +
                                'L> ' + str(len(str(tempcollection[0]))) + ', ' + str(len(str(tempcollection[1]))) +
                                ', ' + str(len(str(tempcollection[2]))) + ', ' + str(len(str(tempcollection[3]))))
                            '''

                elif messagelow == prefix_debug + 'suspend':
                    if message.author.id == ATSUI:
                        await asyncio.sleep(5)
                        await client.send_message(message.channel, 'Suspend complete')

                elif message.content.startswith(prefix_debug + 'playchange'):
                    if message.author.id == ATSUI:
                        global previous_playing_message
                        gamemessage = str(message.content)[14:]
                        previous_playing_message = gamemessage

                        await client.change_status(game=discord.Game(name=gamemessage), idle=False)
                        await client.send_message(message.channel, 'Playing message successfully updated')

                elif message.content.startswith(prefix_debug + 'testingmode'):
                    if message.author.id == ATSUI:
                        testing_modeparameter = str(messagelow)[15:]
                        await client.send_message(message.channel, testing_modeparameter)

                        if testing_modeparameter == 'yes' or testing_modeparameter == '1':
                            global testing_mode
                            testing_mode = True

                            await client.change_status(game=discord.Game(name='alchemy experiments'), idle=False)
                            await client.send_message(message.channel, 'Testing mode enabled')

                        elif testing_modeparameter == 'no' or testing_modeparameter == '0':
                            global testing_mode
                            testing_mode = False

                            await client.change_status(game=discord.Game(name=previous_playing_message), idle=False)
                            await client.send_message(message.channel, 'Testing mode disabled')

                elif messagelow == prefix_debug + 'rest':
                    if message.author.id == ATSUI:
                        await client.send_message(message.channel, 'I will rest for now. Good night!')
                        await client.logout()

                elif messagelow == prefix_debug + 'whack':
                    if message.author.id == ATSUI:
                        await client.send_message(message.channel, 'o-ow!')
                        await asyncio.sleep(5)
                        await client.send_message(message.channel, 'zzz')
                        await client.logout()

                elif messagelow == prefix_debug + 'selfdestruct':
                    if message.author.id == ATSUI:
                        await client.send_message(message.channel, ':boom:')
                        await client.logout()

                elif messagelow.startswith(prefix_debug + 'changename'):
                    if message.author.id == ATSUI:
                        find_qualifier = ' '
                        name_position = message.content.find(find_qualifier, 0)
                        username = message.content[name_position+1:]
                        # client.send_message(message.channel, str(len(username)) + username)
                        await client.edit_profile(password='', username=username)
                        await client.send_message(message.channel, 'Bot name successfully changed')

        elif message.content == '\u0028\u256f\u00b0\u25a1\u00b0\uff09\u256f\ufe35 \u253b\u2501\u253b':
            await client.send_message(message.channel, '┬─┬﻿ ノ( ゜-゜ノ)')

        else:
            if message.server.id in server_exclude:
                isallowed = False

            if isallowed:
                if messagelow == 'cawfee':
                        await asyncio.sleep(1)
                        await client.send_message(message.channel, 'gween tea')

                elif messagelow == 'gween tea':
                        await asyncio.sleep(1)
                        await client.send_message(message.channel, 'cawfee')

                elif message.content == '\u2615':
                        await asyncio.sleep(1)
                        await client.send_message(message.channel, ':tea:')

                elif message.content == '\U0001F375':
                        await asyncio.sleep(1)
                        await client.send_message(message.channel, ':coffee:')

token = open('sophia.uwaa')
client.run(token.readline())
