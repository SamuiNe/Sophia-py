# coding=utf-8
import discord
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

atsui = '153789058059993088'
bot = '225810441610199040'
botCheck = False
serverExclude = ['110373943822540800', '154488551596228610']
exclusionBoolean = False
exclusionMax = 2
tunnelRecipientChannelIDA = None
tunnelRecipientChannelIDB = None
tunnelEnable = False
client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as ' + client.user.name)
    print('Discord ID: ' + client.user.id)
    print('------')
    print(client)
    print('Created by SamuiNe <https://github.com/SamuiNe>')
    await client.change_status(game=discord.Game(name='with pointers'), idle=False)
    print('Discord Bot (Sophia) Version 0.03, Ready.')


@client.event
async def on_message(message):
    print(message)
    messagelow = message.content.lower()
    global tunnelEnable
    global botCheck
    global exclusionBoolean

    exclusionBoolean = False
    botCheck = False

    if message.author.id == bot:
        botCheck = True

    if botCheck is False:
        if tunnelEnable is True and tunnelRecipientChannelIDA is not None and tunnelRecipientChannelIDB is not None:
                if tunnelRecipientChannelIDA == message.channel:
                        await client.send_message(tunnelRecipientChannelIDB, str(message.author) + ' - ' + message.content)
                elif tunnelRecipientChannelIDB == message.channel:
                        await client.send_message(tunnelRecipientChannelIDA, str(message.author) + ' - ' + message.content)

        if message.content.startswith('<'):
            if message.content.startswith('<?'):
                if messagelow == '<?about':
                    await client.send_message(message.channel, 'Hello! I am Sophia. Please treat me well!')

                elif message.content == '<?help' or message.content == '<?commands':
                    await client.send_message(message.channel, "Here are the commands I recognize at the moment:\n\n" +
                        "*Question commands* (starts with `<?`)\n" +
                        "`about`, `messages`, `help` (`commands`), `invite`\n" +
                        "*Information commands* (starts with `<!`)\n" +
                        "`hello`, `sara` (`sarachan`), `ping` (`pong`)\n" +
                        "*Trigger commands*\n" +
                        ":coffee:, :tea:, `cawfee`, `gween tea`, " +
                        "`\u0028\u256f\u00b0\u25a1\u00b0\uff09\u256f\ufe35 \u253b\u2501\u253b`\n" +
                        "...with 9 secret commands!")

                elif messagelow == '<?messages':
                    counter = 0
                    tmp = await client.send_message(message.channel, 'Calculating messages...')
                    async for log in client.logs_from(message.channel, limit=100):
                        if log.author == message.author:
                            counter += 1
                    await client.edit_message(tmp, 'You have posted {} messages in the past 100 messages.'.format(counter))

            elif message.content.startswith('<!'):
                if message.content == '<!hello':
                    messagelength = len(str(message.author))
                    await client.send_message(message.channel, 'Hello ' + str(message.author)[:messagelength-5] + ' o/')

                elif messagelow == '<!sarachan' or messagelow == '<!sara':
                    await client.send_message(message.channel, 'https://puu.sh/r5mt4/f9eb13dc29.gif')


                #elif messagelow == '<!invite':
                    #await client.send_message(message.channel, 'You can invite me via the link below. ' +
                    #'No permissions required!\n' +
                    #'https://discordapp.com/oauth2/authorize?client_id=225810441610199040&scope=bot&permissions=0')

                elif messagelow == '<!ping':
                    await client.send_message(message.channel, 'pong!')

                elif messagelow == '<!pong':
                    await client.send_message(message.channel, 'ping!')

                elif messagelow == '<!!debug':
                    if message.author.id == atsui:
                        await client.send_message(message.channel,'`Author`: ' + str(message.author) + ' `' + str(message.author.id) + '`\n' +
                            '`Message Length`: ' + str(len(str(message.content))) + '\n' +
                            '`Channel`: ' + str(message.channel) + ' `' + str(message.channel.id) + '`\n' +
                            '`Server`: ' + str(message.server.name) + ' `' + str(message.server.id) + '`')

                elif messagelow.startswith('<!!tunnellink'):
                    if message.author.id == atsui:
                        global tunnelRecipientChannelIDA
                        global tunnelRecipientChannelIDB
                        channelid = message.channel.id

                        if str(messagelow)[-1:] == 'a':
                            #await client.send_message(message.channel, 'Debug info: ' + str(message.channel))
                            tunnelRecipientChannelIDA = discord.utils.get(message.server.channels, id=channelid)
                            #await client.send_message(message.channel, tunnelRecipientChannelIDA)
                            #await client.send_message(tunnelRecipientChannelIDA, 'Test successful')
                            await client.send_message(message.channel, 'Channel A assignment successful')

                        elif str(messagelow)[-1:] == 'b':
                            #await client.send_message(message.channel, 'Debug info: ' + str(message.channel))
                            tunnelRecipientChannelIDB = discord.utils.get(message.server.channels, id=channelid)
                            #await client.send_message(message.channel, tunnelRecipientChannelIDB)
                            #await client.send_message(tunnelRecipientChannelIDB, 'Test successful')
                            await client.send_message(message.channel, 'Channel B assignment successful')

                elif messagelow.startswith('<!!tunnelenable'):
                    if message.author.id == atsui:
                        tunnelenableparameter = str(messagelow)[16:]
                        await client.send_message(message.channel, tunnelenableparameter)

                        if tunnelenableparameter == 'yes' or tunnelenableparameter == '1':
                            tunnelEnable = True
                            await client.send_message(message.channel, 'Message tunneling enabled')

                        elif tunnelenableparameter == 'no' or tunnelenableparameter == '0':
                            tunnelEnable = False
                            await client.send_message(message.channel, 'Message tunneling disabled')

                elif messagelow == '<!!tunnelinfo':
                    if message.author.id == atsui:
                        if tunnelRecipientChannelIDA is not None:
                            tunnelida = tunnelRecipientChannelIDA.id
                        else:
                            tunnelida = 'None'

                        if tunnelRecipientChannelIDB is not None:
                            tunnelidb = tunnelRecipientChannelIDB.id
                        else:
                            tunnelidb = 'None'

                        await client.send_message(message.channel, '`Linked channel A`: ' + str(tunnelRecipientChannelIDA) +
                            ' `' + tunnelida + '`' +
                            '\n' + '`Linked channel B`: ' + str(tunnelRecipientChannelIDB) +
                            ' `' + tunnelidb + '`' +
                            '\n' + '`Tunnel Boolean`: ' + str(tunnelEnable))

                elif messagelow == '<!!suspend':
                    if message.author.id == atsui:
                        await asyncio.sleep(5)
                        await client.send_message(message.channel, 'Suspend complete')

                elif message.content.startswith('<!!playchange'):
                    if message.author.id == atsui:
                        gamemessage = str(message.content)[14:]
                        await client.change_status(game=discord.Game(name=gamemessage), idle=False)
                        await client.send_message(message.channel, 'Playing message successfully updated')

                elif messagelow == '<!!rest':
                    if message.author.id == atsui:
                        await client.send_message(message.channel, 'I will rest for now. Good night!')
                        await client.logout()

                elif messagelow == '<!!whack':
                    if message.author.id == atsui:
                        await client.send_message(message.channel, 'o-ow!')
                        await asyncio.sleep(5)
                        await client.send_message(message.channel, 'zzz')
                        await client.logout()

                elif messagelow == '<!!selfdestruct':
                    if message.author.id == atsui:
                        await client.send_message(message.channel, ':boom:')
                        await client.logout()

        elif message.content == '\u0028\u256f\u00b0\u25a1\u00b0\uff09\u256f\ufe35 \u253b\u2501\u253b':
            await client.send_message(message.channel, '┬─┬﻿ ノ( ゜-゜ノ)')

        else:
            exclusioncounter = 0

            while exclusioncounter != exclusionMax:
                if message.server.id == serverExclude[exclusioncounter]:
                    exclusionBoolean = True
                    exclusioncounter += 1
                else:
                    exclusioncounter += 1

            if exclusionBoolean is False:
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

client.run('MjI1ODEwNDQxNjEwMTk5MDQw.CrujHg.NrRGoAYOUafJer9nOj41z6PO9jc')
