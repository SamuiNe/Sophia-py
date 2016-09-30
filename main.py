# coding=utf-8
"""Text encoding UTF-8"""

import asyncio
import logging
import discord

import bot_system
import room
import chat_tunnel

System = bot_system.SystemVariables('<', '<?', '<!', '<!!', False, ['154488551596228610', '164476517101993984'],
        '153789058059993088', ['110373943822540800'], None)
RoomInfo = room.RoomInformations([], [['Blackjack'], [6]], ['Waiting', 'In Progress'],
        [['Testing room', 'Blackjack', 'Testing', '0']])
TunnelInfo = chat_tunnel.TunnelInformations([], None, None, False)

logging.basicConfig(level=logging.INFO)
client = discord.Client()


@client.event
async def on_ready():
    """Triggers when the bot is starting up."""
    print('Logged in as ' + client.user.name)
    print('Discord ID: ' + client.user.id)
    print('------')
    print(client)
    print('Created by SamuiNe <https://github.com/SamuiNe>')
    System.previous_playing_mesage = 'with pointers'
    if System.test_mode:
        await client.change_presence(game=discord.Game(name='with alchemy'), idle=False)
    else:
        await client.change_presence(game=discord.Game(name='with pointers'), idle=False)
    token.close()
    print('Discord Bot (Sophia) Version 0.0.8, Ready.')


@client.event
async def on_message(message):
    """Triggers when the bot receives a message."""
    print(message)
    message_low = message.content.lower()

    is_allowed = True
    is_person = True

    if message.author.bot:
        is_person = False

    if System.test_mode:
        if message.server.id not in System.allowed_testing:
            is_person = False

    if is_person:
        # TODO: Allow multiple combinations of servers for chat tunnelling

        # Checks if the chat tunnelling mode is enabled and if the tunnel_receive_a and tunnel_receive_b is not none
        if TunnelInfo.tunnel_enable and TunnelInfo.tunnel_receive_a is not None and \
                TunnelInfo.tunnel_receive_b is not None:
                if TunnelInfo.tunnel_receive_a == message.channel:
                    await client.send_message(TunnelInfo.tunnel_receive_b, str(message.author) +
                        ' - ' + message.content)
                elif TunnelInfo.tunnel_receive_b == message.channel:
                    await client.send_message(TunnelInfo.tunnel_receive_a, str(message.author) +
                        ' - ' + message.content)

        if message.content.startswith(System.prefix_qualifier):
            if message.content.startswith(System.prefix_question):
                if message_low == System.prefix_question + 'about':
                    await client.send_message(message.channel, 'Hello! I am Sophia. Please treat me well!')

                if message_low == System.prefix_question + 'botversion':
                    await client.send_message(message.channel, 'My current version is 0.0.8, which is last updated ' +
                        'at 2016/09/30.')

                elif message.content == System.prefix_question + 'help' or \
                        message.content == System.prefix_question + 'commands':
                    trigger_status = 'Enabled'
                    if message.server.id in System.server_exclude:
                        trigger_status = 'Disabled'

                    await client.send_message(message.channel, 'Here are the commands I recognize at the moment:\n\n' +
                        '*Question commands* (starts with `' + System.prefix_question + '`)\n' +
                        '`about`, `help` (`commands`), `botversion`\n\n' +
                        '*Information commands* (starts with `' + System.prefix_information + '`)\n' +
                        '`hello`, `sara` (`sarachan`), `invite`, `ping` (`pong`),' +
                        ' `roomcreate`, `roomjoin`, `roomcheck`\n\n' +
                        '*Trigger commands* ' + trigger_status + '\n' +
                        ':coffee:, :tea:, `cawfee`, `gween tea`, ' +
                        '`\u0028\u256f\u00b0\u25a1\u00b0\uff09\u256f\ufe35 \u253b\u2501\u253b`, ' +
                        '`\u252c\u2500\u252c\ufeff \u30ce\u0028 \u309c\u002d\u309c\u30ce\u0029`\n' +
                        '...with 12 secret commands!')
            elif message.content.startswith(System.prefix_information):
                if message.content == System.prefix_information + 'hello':
                    mess_len = len(str(message.author))
                    await client.send_message(message.channel, 'Hello ' + str(message.author)[:mess_len-5] + ' o/')

                elif message_low == System.prefix_information + 'sarachan' or \
                        message_low == System.prefix_information + 'sara':
                    await client.send_message(message.channel, 'http://sophia.samuine.net/content/scratchwalls.gif')

                elif message_low == System.prefix_information + 'invite':
                    await client.send_message(message.channel,
                        'You can take me to your discord server by clicking the link below' + '\n' +
                        'Please note that you will need at least "administrator" to add bots!' +
                        'https://discordapp.com/oauth2/authorize?client_id=225810441610199040&scope=bot&permissions=0' +
                        '\n\n' +
                        'Interested in joining my discord guild? You can visit it by using the invite link below!' +
                        '\n' +
                        'https://discord.gg/SpTWKDd')

                elif message_low == System.prefix_information + 'ping':
                    await client.send_message(message.channel, 'pong!')

                elif message_low == System.prefix_information + 'pong':
                    await client.send_message(message.channel, 'ping!')

                elif message_low.startswith(System.prefix_information + 'roomcreate'):
                    await room.room_create(System, RoomInfo, client, message, message_low)

                elif message_low.startswith(System.prefix_information + 'roomjoin'):
                    await room.room_join(RoomInfo, client, message, message_low)

                elif message_low.startswith(System.prefix_information + 'roomcheck'):
                    await room.room_check(RoomInfo, client, message, message_low)

                elif message_low == System.prefix_debug + 'debug':
                    # if message.author.id == ATSUI:
                    await client.send_message(message.channel, '`Author`: ' + str(message.author) +
                        ' `' + str(message.author.id) + '`\n' +
                        '`Bot`: ' + str(message.author.bot) + '\n' +
                        # '`MessLen`: ' + str(len(message.content)) + '\n' +
                        '`Channel`: ' + str(message.channel) + ' `' + str(message.channel.id) + '`\n' +
                        '`Server`: ' + str(message.server.name) + ' `' + str(message.server.id) + '`')

                elif message.author.id in System.ATSUI:
                    if message_low == System.prefix_debug + 'secret':
                        await client.send_message(message.channel, 'Nothing to see here!')

                    elif message_low.startswith(System.prefix_debug + 'tunnellink'):
                            channelid = message.channel.id

                            if str(message_low)[-1:] == 'a':
                                # await client.send_message(message.channel, 'Debug info: ' + str(message.channel))
                                TunnelInfo.tunnel_receive_a = discord.utils.get(message.server.channels, id=channelid)
                                # await client.send_message(message.channel, tunnel_receive_a)
                                # await client.send_message(tunnel_receive_a, 'Test successful')
                                await client.send_message(message.channel, 'Channel A assignment successful')

                            elif str(message_low)[-1:] == 'b':
                                # await client.send_message(message.channel, 'Debug info: ' + str(message.channel))
                                TunnelInfo.tunnel_receive_b = discord.utils.get(message.server.channels, id=channelid)
                                # await client.send_message(message.channel, tunnel_receive_b)
                                # await client.send_message(tunnel_receive_b, 'Test successful')
                                await client.send_message(message.channel, 'Channel B assignment successful')

                    elif message_low.startswith(System.prefix_debug + 'tunnelenable'):
                            tunnel_enable_parameter = str(message_low)[16:]
                            await client.send_message(message.channel, tunnel_enable_parameter)

                            if tunnel_enable_parameter == 'yes' or tunnel_enable_parameter == '1':
                                TunnelInfo.tunnel_enable = True
                                await client.send_message(message.channel, 'Message tunneling enabled')

                            elif tunnel_enable_parameter == 'no' or tunnel_enable_parameter == '0':
                                TunnelInfo.tunnel_enable = False
                                await client.send_message(message.channel, 'Message tunneling disabled')

                    elif message_low == System.prefix_debug + 'tunnelinfo':
                            if TunnelInfo.tunnel_receive_a is not None:
                                tunnelida = TunnelInfo.tunnel_receive_a.id
                            else:
                                tunnelida = 'None'

                            if TunnelInfo.tunnel_receive_b is not None:
                                tunnelidb = TunnelInfo.tunnel_receive_b.id
                            else:
                                tunnelidb = 'None'

                            await client.send_message(message.channel, '`Linked channel A`: ' +
                                str(TunnelInfo.tunnel_receive_a) +
                                ' `' + tunnelida + '`' +
                                '\n' + '`Linked channel B`: ' + str(TunnelInfo.tunnel_receive_b) +
                                ' `' + tunnelidb + '`' +
                                '\n' + '`Tunnel Boolean`: ' + str(TunnelInfo.tunnel_enable))

                    elif message_low.startswith(System.prefix_debug + 'prefixchange'):
                            await bot_system.prefix_change(System, client, message, message_low)

                    elif message_low == System.prefix_debug + 'suspend':
                            await asyncio.sleep(5)
                            await client.send_message(message.channel, 'Suspend complete')

                    elif message.content.startswith(System.prefix_debug + 'playchange'):
                            game_message = str(message.content)[14:]
                            System.previous_playing_message = game_message

                            await client.change_status(game=discord.Game(name=game_message), idle=False)
                            await client.send_message(message.channel, 'Playing message successfully updated')

                    elif message.content.startswith(System.prefix_debug + 'testmode'):
                            testing_mode_parameter = str(message_low)[15:]
                            await client.send_message(message.channel, testing_mode_parameter)

                            if testing_mode_parameter == 'yes' or testing_mode_parameter == '1':
                                System.test_mode = True

                                await client.change_status(game=discord.Game(name='with alchemy'), idle=False)
                                await client.send_message(message.channel, 'Testing mode enabled')

                            elif testing_mode_parameter == 'no' or testing_mode_parameter == '0':
                                System.test_mode = False

                                await client.change_status(game=discord.Game(name=System.previous_playing_message),
                                        idle=False)
                                await client.send_message(message.channel, 'Testing mode disabled')

                    elif message_low == System.prefix_debug + 'rest':
                            await client.send_message(message.channel, 'I will rest for now. Good night!')
                            await client.logout()

                    elif message_low == System.prefix_debug + 'whack':
                            await client.send_message(message.channel, 'o-ow!')
                            await asyncio.sleep(5)
                            await client.send_message(message.channel, 'zzz')
                            await client.logout()

                    elif message_low == System.prefix_debug + 'selfdestruct':
                            await client.send_message(message.channel, ':boom:')
                            await client.logout()

                    elif message_low.startswith(System.prefix_debug + 'changename'):
                            find_qualifier = ' '
                            name_position = message.content.find(find_qualifier, 0)
                            namechange = message.content[name_position + 1:]
                            # await client.send_message(message.channel, str(len(username)) + username)
                            await client.edit_profile(password='', username=namechange)
                            await client.send_message(message.channel, 'Bot name successfully changed')

        else:
            if message.server.id in System.server_exclude:
                is_allowed = False

            if is_allowed:
                if message.content == '\u252c\u2500\u252c\ufeff \u30ce\u0028 \u309c\u002d\u309c\u30ce\u0029':
                    await client.send_message(message.channel, '(╯°□°）╯︵ ┻━┻')

                elif message.content == '\u0028\u256f\u00b0\u25a1\u00b0\uff09\u256f\ufe35 \u253b\u2501\u253b':
                    await client.send_message(message.channel, '┬─┬﻿ ノ( ゜-゜ノ)')

                elif message_low == 'cawfee':
                        await asyncio.sleep(1)
                        await client.send_message(message.channel, 'gween tea')

                elif message_low == 'gween tea':
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
