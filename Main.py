# coding=utf-8
import discord
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

atsui = '153789058059993088'
bot = '225810441610199040'
client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as ' + client.user.name)
    print('Discord ID: ' + client.user.id)
    print('------')
    print(client)
    print('Created by SamuiNe <https://github.com/SamuiNe>')
    await client.change_status(game=discord.Game(name='with pointers'), idle=False)
    print('Discord Bot (Sophia) Version 0.02, Ready.')


@client.event
async def on_message(message):
    print(message)

    if message.content.startswith('<'):
        if message.content.startswith('<?'):
            if message.content == '<?help' or message.content == '<?commands':
                await client.send_message(message.channel, "Here are the commands I recognize at the moment:\n\n" +
                "*Question commands* (starts with `<?`)\n" +
                "`messages`, `help`\n" +
                "*Information commands* (starts with `<!`)\n" +
                "`about` (`commands`), `hello`, `sara` (`sarachan`)")

            elif message.content == '<?messages':
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

            elif message.content == '<!sarachan' or message.content == '<!sara':
                await client.send_message(message.channel, 'https://puu.sh/r5mt4/f9eb13dc29.gif')

            elif message.content == '<!about':
                await client.send_message(message.channel, 'Hello! I am Sophia. Please treat me well!')

            elif message.content == '<!invite':
                await client.send_message(message.channel, 'You can invite me via the link below. No permissions required!\n' +
                'https://discordapp.com/oauth2/authorize?client_id=225810441610199040&scope=bot&permissions=0')

            elif message.content == '<!!debug':
                if message.author.id != bot and message.author.id == atsui:
                    await client.send_message(message.channel, '`Message Content`:\n' + str(message.content) + '\n' +
                            '`Discord ID`: ' + str(message.author.id) + '\n' +
                            '`Author`: ' + str(message.author) + '\n' +
                            '`Message Length`: ' + str(len(str(message.content))))
                    await client.send_message(message.channel, message.channel)
                    await client.send_message(message.channel, message.channel.id)
                    await client.send_message(message.channel,message.server.name)
                    await client.send_message(message.channel,message.server.id)

            elif message.content == '<!!suspend':
                if message.author.id == atsui:
                    await asyncio.sleep(5)
                    await client.send_message(message.channel, 'Suspend complete')

            elif message.content.startswith('<!!playchange'):
                if message.author.id == atsui:
                    gamemessage = str(message.content)[14:]
                    await client.change_status(game=discord.Game(name=gamemessage), idle=False)
                    await client.send_message(message.channel, 'Playing message successfully updated')

            elif message.content == '<!!rest':
                if message.author.id == atsui:
                    await client.send_message(message.channel, 'I will rest for now. Good night!')
                    await client.logout()

            elif message.content == '<!!whack':
                if message.author.id == atsui:
                    await client.send_message(message.channel, 'o-ow!')
                    await asyncio.sleep(5)
                    await client.send_message(message.channel, 'zzz')
                    await client.logout()

            elif message.content == '<!!selfdestruct':
                if message.author.id == atsui:
                    await client.send_message(message.channel, ':boom:')
                    await client.logout()

    elif message.content == '\u0028\u256f\u00b0\u25a1\u00b0\uff09\u256f\ufe35 \u253b\u2501\u253b':
        await client.send_message(message.channel, '┬─┬﻿ ノ( ゜-゜ノ)')

    elif message.content == 'cawfee':
        if message.author.id != bot:
            await asyncio.sleep(1)
            await client.send_message(message.channel, 'gween tea')

    elif message.content == 'gween tea':
        if message.author.id != bot:
            await asyncio.sleep(1)
            await client.send_message(message.channel, 'cawfee')

    elif message.content == '\u2615':
        if message.author.id != bot:
            await asyncio.sleep(1)
            await client.send_message(message.channel, ':tea:')

    elif message.content == '\U0001F375':
        if message.author.id != bot:
            await asyncio.sleep(1)
            await client.send_message(message.channel, ':coffee:')

client.run('MjI1ODEwNDQxNjEwMTk5MDQw.CrujHg.NrRGoAYOUafJer9nOj41z6PO9jc')
