"""Encoding and discord bot essentials"""
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
    """These lines of code triggers when the bot has logged in and ready to go."""
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
    """These lines of message triggers when the bot receives a message from the text chat."""
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

        if tunnelEnable and tunnelReceiveA is not None and tunnelReceiveB is not None:
                if tunnelReceiveA == message.channel:
                    await client.send_message(tunnelReceiveB, str(message.author) + 
                        ' - ' + message.content)
                elif tunnelReceiveB == message.channel:
                    await client.send_message(tunnelReceiveA, str(message.author) + 
                        ' - ' + message.content)

        if message.content.startswith('<'):
            if message.content.startswith(prefixQuestion):
                if messagelow == '<?about':
                    await client.send_message(message.channel, 'Hello! I am Sophia. Please treat me well!')

                elif message.content == prefixQuestion + 'help' or message.content == prefixQuestion + 'commands':
                    await client.send_message(message.channel, "Here are the commands I recognize at the moment:\n\n" +
                        "*Question commands* (starts with `" + prefixQuestion + "`)\n" +
                        "`about`, `messages`, `help` (`commands`), `invite`\n" +
                        "*Information commands* (starts with `<!`)\n" +
                        "`hello`, `sara` (`sarachan`), `ping` (`pong`)\n" +
                        "*Trigger commands*\n" +
                        ":coffee:, :tea:, `cawfee`, `gween tea`, " +
                        "`\u0028\u256f\u00b0\u25a1\u00b0\uff09\u256f\ufe35 \u253b\u2501\u253b`\n" +
                        "...with 9 secret commands!")

            elif message.content.startswith(prefixInformation):
                if message.content == prefixInformation + 'hello':
                    messlen = len(str(message.author))
                    await client.send_message(message.channel, 'Hello ' + str(message.author)[:messlen-5] + ' o/')

                elif messagelow == '<!sarachan' or messagelow == '<!sara':
                    await client.send_message(message.channel, 'https://puu.sh/r5mt4/f9eb13dc29.gif')

                # TODO: Add discord link to the discord server and continue to polish the bot
                # elif messagelow == prefixInformation + 'invite':
                    # await client.send_message(message.channel, 'You can invite me via the link below. ' +
                    # 'No permissions required!\n' +
                    # 'https://discordapp.com/oauth2/authorize?client_id=225810441610199040&scope=bot&permissions=0')

                elif messagelow == '<!ping':
                    await client.send_message(message.channel, 'pong!')

                elif messagelow == '<!pong':
                    await client.send_message(message.channel, 'ping!')

                elif messagelow == '<!!debug':
                    # if message.author.id == ATSUI:
                    await client.send_message(message.channel, '`Author`: ' + str(message.author) +
                        ' `' + str(message.author.id) + '`\n' +
                        '`MessLen`: ' + str(len(str(message.content))) + '\n' +
                        '`Channel`: ' + str(message.channel) + ' `' + str(message.channel.id) + '`\n' +
                        '`Server`: ' + str(message.server.name) + ' `' + str(message.server.id) + '`')

                elif messagelow.startswith('<!!tunnellink'):
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

                elif messagelow.startswith('<!!tunnelenable'):
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

                elif messagelow == '<!!tunnelinfo':
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

                elif messagelow == '<!!prefixchange iknowwhatwouldhappen':
                    if message.author.id == ATSUI:
                        await client.send_message(message.channel, 'Prefix change failed since Atsui is lazy')

                elif messagelow == '<!!suspend':
                    if message.author.id == ATSUI:
                        await asyncio.sleep(5)
                        await client.send_message(message.channel, 'Suspend complete')

                elif message.content.startswith('<!!playchange'):
                    if message.author.id == ATSUI:
                        gamemessage = str(message.content)[14:]
                        await client.change_status(game=discord.Game(name=gamemessage), idle=False)
                        await client.send_message(message.channel, 'Playing message successfully updated')

                elif message.content.startswith('<!!testingmode'):
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

                elif messagelow == '<!!rest':
                    if message.author.id == ATSUI:
                        await client.send_message(message.channel, 'I will rest for now. Good night!')
                        await client.logout()

                elif messagelow == '<!!whack':
                    if message.author.id == ATSUI:
                        await client.send_message(message.channel, 'o-ow!')
                        await asyncio.sleep(5)
                        await client.send_message(message.channel, 'zzz')
                        await client.logout()

                elif messagelow == '<!!selfdestruct':
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
