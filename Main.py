# coding=utf-8
import discord
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

# TODO: Add customizable command prefix
prefixQualifier = '<'
prefixDebug = '<!!'
prefixInformation = '<!'
prefixQuestion = '<?'
ATSUI = '153789058059993088'
allowedTesting = '154488551596228610'
testingMode = False
BOT = '225810441610199040'
serverExclude = ['110373943822540800', '154488551596228610']
exclusionMax = len(serverExclude)
tunnelReceiveA = None
tunnelReceiveB = None
tunnelEnable = False
client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as ' + client.user.name)
    print('Discord ID: ' + client.user.id)
    print('------')
    print(client)
    print('Created by SamuiNe <https://github.com/SamuiNe>')
    if testingMode:
        await client.change_status(game=discord.Game(name='Testing mode enabled'), idle=False)
    else:
        await client.change_status(game=discord.Game(name='with pointers'), idle=False)
    print('Discord Bot (Sophia) Version 0.03, Ready.')


@client.event
async def on_message(message):
    print(message)
    messagelow = message.content.lower()

    isallowed = True
    isperson = True

    if message.author.id == BOT:
        isperson = False

    if testingMode:
        if message.server.id != allowedTesting:
            isperson = False

    if isperson:
        # TODO: Allow multiple combinations of servers for chat tunnelling

        # Checks if the chat tunnelling mode is enabled and if the tunnelReceiveA and tunnelReceiveB is not none
        if tunnelEnable and tunnelReceiveA is not None and tunnelReceiveB is not None:
                if tunnelReceiveA == message.channel:
                    await client.send_message(tunnelReceiveB, str(message.author) + 
                        ' - ' + message.content)
                elif tunnelReceiveB == message.channel:
                    await client.send_message(tunnelReceiveA, str(message.author) + 
                        ' - ' + message.content)

        if message.content.startswith(prefixQualifier):
            if message.content.startswith(prefixQuestion):
                if messagelow == prefixQuestion + 'about':
                    await client.send_message(message.channel, 'Hello! I am Sophia. Please treat me well!')

                elif message.content == prefixQuestion + 'help' or message.content == prefixQuestion + 'commands':
                    await client.send_message(message.channel, "Here are the commands I recognize at the moment:\n\n" +
                        "*Question commands* (starts with `" + prefixQuestion + "`)\n" +
                        "`about`, `help` (`commands`), `invite`\n" +
                        "*Information commands* (starts with `" + prefixInformation + "`)\n" +
                        "`hello`, `sara` (`sarachan`), `ping` (`pong`)\n" +
                        "*Trigger commands*\n" +
                        ":coffee:, :tea:, `cawfee`, `gween tea`, " +
                        "`\u0028\u256f\u00b0\u25a1\u00b0\uff09\u256f\ufe35 \u253b\u2501\u253b`\n" +
                        "...with 9 secret commands!")

            elif message.content.startswith(prefixInformation):
                if message.content == prefixInformation + 'hello':
                    messlen = len(str(message.author))
                    await client.send_message(message.channel, 'Hello ' + str(message.author)[:messlen-5] + ' o/')

                elif messagelow == prefixInformation + 'sarachan' or messagelow == prefixInformation + 'sara':
                    await client.send_message(message.channel, 'https://puu.sh/r5mt4/f9eb13dc29.gif')

                # TODO: Add discord link to the discord server and continue to polish the bot
                # elif messagelow == prefixInformation + 'invite':
                    # await client.send_message(message.channel, 'You can invite me via the link below. ' +
                    # 'No permissions required!\n' +
                    # 'https://discordapp.com/oauth2/authorize?client_id=225810441610199040&scope=bot&permissions=0')

                elif messagelow == prefixInformation + 'ping':
                    await client.send_message(message.channel, 'pong!')

                elif messagelow == prefixInformation + 'pong':
                    await client.send_message(message.channel, 'ping!')

                elif messagelow == prefixDebug + 'debug':
                    # if message.author.id == ATSUI:
                    await client.send_message(message.channel, '`Author`: ' + str(message.author) +
                        ' `' + str(message.author.id) + '`\n' +
                        '`MessLen`: ' + str(len(str(message.content))) + '\n' +
                        '`Channel`: ' + str(message.channel) + ' `' + str(message.channel.id) + '`\n' +
                        '`Server`: ' + str(message.server.name) + ' `' + str(message.server.id) + '`')

                elif messagelow.startswith(prefixDebug + 'tunnellink'):
                    if message.author.id == ATSUI:
                        global tunnelReceiveA
                        global tunnelReceiveB
                        channelid = message.channel.id

                        if str(messagelow)[-1:] == 'a':
                            # await client.send_message(message.channel, 'Debug info: ' + str(message.channel))
                            tunnelReceiveA = discord.utils.get(message.server.channels, id=channelid)
                            # await client.send_message(message.channel, tunnelReceiveA)
                            # await client.send_message(tunnelReceiveA, 'Test successful')
                            await client.send_message(message.channel, 'Channel A assignment successful')

                        elif str(messagelow)[-1:] == 'b':
                            # await client.send_message(message.channel, 'Debug info: ' + str(message.channel))
                            tunnelReceiveB = discord.utils.get(message.server.channels, id=channelid)
                            # await client.send_message(message.channel, tunnelReceiveB)
                            # await client.send_message(tunnelReceiveB, 'Test successful')
                            await client.send_message(message.channel, 'Channel B assignment successful')

                elif messagelow.startswith(prefixDebug + 'tunnelenable'):
                    if message.author.id == ATSUI:
                        tunnelenableparameter = str(messagelow)[16:]
                        await client.send_message(message.channel, tunnelenableparameter)

                        if tunnelenableparameter == 'yes' or tunnelenableparameter == '1':
                            global tunnelEnable
                            tunnelEnable = True
                            await client.send_message(message.channel, 'Message tunneling enabled')

                        elif tunnelenableparameter == 'no' or tunnelenableparameter == '0':
                            global tunnelEnable
                            tunnelEnable = False
                            await client.send_message(message.channel, 'Message tunneling disabled')

                elif messagelow == prefixDebug + 'tunnelinfo':
                    if message.author.id == ATSUI:
                        if tunnelReceiveA is not None:
                            tunnelida = tunnelReceiveA.id
                        else:
                            tunnelida = 'None'

                        if tunnelReceiveB is not None:
                            tunnelidb = tunnelReceiveB.id
                        else:
                            tunnelidb = 'None'

                        await client.send_message(message.channel, '`Linked channel A`: ' + str(tunnelReceiveA) +
                            ' `' + tunnelida + '`' +
                            '\n' + '`Linked channel B`: ' + str(tunnelReceiveB) +
                            ' `' + tunnelidb + '`' +
                            '\n' + '`Tunnel Boolean`: ' + str(tunnelEnable))

                elif messagelow.startswith(prefixDebug + 'prefixchange'):
                    if message.author.id == ATSUI:
                        tempcollection = ['<', None, None, None]
                        exceptioncheck = False
                        findqualifier = ' '
                        findcheckbefore = 0
                        findcheckafter = 0
                        findcount = 0
                        processcount = 2
                        tempcounter = 0
                        exceptioncounter = 0
                        processedprefix = [0, None, None, None, None, None]

                        while findcheckafter != -1 and findcount != 5:
                            findcheckbefore = findcheckafter
                            findcheckafter = messagelow.find(findqualifier, findcheckbefore)

                            if findcheckafter != -1:
                                findcount += 1
                                processedprefix[findcount] = findcheckafter

                        while processedprefix[processcount] is not None and processcount != 6:
                            tempcollection[tempcounter] = messagelow[processedprefix[processcount - 1] + 1:
                                (processedprefix[processcount] - processedprefix[processcount - 1]) - 2]
                            tempcounter += 1
                            processcount += 1
                        ''' Old Code
                        if processedprefix[2] is not None:
                            tempqualifier = messagelow[processedprefix[1] + 1: \
                                (processedprefix[2] - processedprefix[1]) - 2]

                        if processedprefix[3] is not None:
                            tempquestion = messagelow[processedprefix[2] + 1: \
                                (processedprefix[3] - processedprefix[2]) - 2]

                        if processedprefix[4] is not None:
                            tempinformation = messagelow[processedprefix[3] + 1: \
                                (processedprefix[4] - processedprefix[3]) - 2]

                        if processedprefix[5] is not None:
                            tempdebug = messagelow[processedprefix[4] + 1: \
                                (processedprefix[5] - processedprefix[4]) - 2]
                        '''

                        if tempcollection[exceptioncounter] is not None and \
                                tempcollection[exceptioncounter + 1] is not None:

                            while tempcollection[exceptioncounter] is not None and \
                                    [exceptioncounter + 1] is not None and exceptioncounter != 4:

                                exceptioncounter += 1
                                if not tempcollection[exceptioncounter].startswith(tempcollection[0]):
                                    exceptioncheck = True
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
                            await client.send_message(message.channel, 'Prefix change failed.')
                            await client.send_message(message.channel, 'Debug information:\n' + str(findcheckbefore) +
                                ' ' + str(findcheckafter) + ' ' + str(findcount) + ' ' + str(processcount) + ' ' +
                                str(tempcounter) + ' ' + str(exceptioncounter) + '\n' +
                                str(exceptioncheck) + '\n' +
                                '>' + processedprefix[0] + ' ' + processedprefix[1] + ' ' + processedprefix[2] + ' ' +
                                processedprefix[3] + ' ' + processedprefix[4] + ' ' + processedprefix[5] + '\n' +
                                '>>' + tempcollection[0] + ' ' + tempcollection[1] + ' ' + tempcollection[2] + ' ' +
                                tempcollection[3])
                        else:
                            global prefixQualifier
                            global prefixQuestion
                            global prefixInformation
                            global prefixDebug
                            prefixQualifier = tempcollection[0]
                            prefixQuestion = tempcollection[1]
                            prefixInformation = tempcollection[2]
                            prefixDebug = tempcollection[3]
                            await client.send_message(message.channel, 'Prefix change success.')
                            await client.send_message(message.channel, 'Debug information:\n' + str(findcheckbefore) +
                                ' ' + str(findcheckafter) + ' ' + str(findcount) + ' ' + str(processcount) + ' ' +
                                str(tempcounter) + ' ' + str(exceptioncounter) + '\n' +
                                str(exceptioncheck) + '\n' +
                                '>' + processedprefix[0] + ' ' + processedprefix[1] + ' ' + processedprefix[2] + ' ' +
                                processedprefix[3] + ' ' + processedprefix[4] + ' ' + processedprefix[5] + '\n' +
                                '>>' + tempcollection[0] + ' ' + tempcollection[1] + ' ' + tempcollection[2] + ' ' +
                                tempcollection[3])

                elif messagelow == prefixDebug + 'suspend':
                    if message.author.id == ATSUI:
                        await asyncio.sleep(5)
                        await client.send_message(message.channel, 'Suspend complete')

                elif message.content.startswith(prefixDebug + 'playchange'):
                    if message.author.id == ATSUI:
                        gamemessage = str(message.content)[14:]
                        await client.change_status(game=discord.Game(name=gamemessage), idle=False)
                        await client.send_message(message.channel, 'Playing message successfully updated')

                elif message.content.startswith(prefixDebug + 'testingmode'):
                    if message.author.id == ATSUI:
                        testingmodeparameter = str(messagelow)[15:]
                        await client.send_message(message.channel, testingmodeparameter)

                        if testingmodeparameter == 'yes' or testingmodeparameter == '1':
                            global testingMode
                            testingMode = True
                            await client.send_message(message.channel, 'Testing mode enabled')

                        elif testingmodeparameter == 'no' or testingmodeparameter == '0':
                            global testingMode
                            testingMode = False
                            await client.send_message(message.channel, 'Testing mode disabled')

                elif messagelow == prefixDebug + 'rest':
                    if message.author.id == ATSUI:
                        await client.send_message(message.channel, 'I will rest for now. Good night!')
                        await client.logout()

                elif messagelow == prefixDebug + 'whack':
                    if message.author.id == ATSUI:
                        await client.send_message(message.channel, 'o-ow!')
                        await asyncio.sleep(5)
                        await client.send_message(message.channel, 'zzz')
                        await client.logout()

                elif messagelow == prefixDebug + 'selfdestruct':
                    if message.author.id == ATSUI:
                        await client.send_message(message.channel, ':boom:')
                        await client.logout()

        elif message.content == '\u0028\u256f\u00b0\u25a1\u00b0\uff09\u256f\ufe35 \u253b\u2501\u253b':
            await client.send_message(message.channel, '┬─┬﻿ ノ( ゜-゜ノ)')

        else:
            exclusioncounter = 0

            while exclusioncounter != exclusionMax:
                if message.server.id == serverExclude[exclusioncounter]:
                    isallowed = False
                    exclusioncounter += 1
                else:
                    exclusioncounter += 1

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

client.run('Insert 1 Token(s) to Play')
