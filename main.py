# coding=utf-8
"""Text encoding UTF-8"""

import asyncio
import logging
import discord

import bot_system
import room
import chat_tunnel

logging.basicConfig(level=logging.INFO)
System = bot_system.SystemVariables('>', '>?', '>!', '>!!', False, ['154488551596228610', '164476517101993984'],
        ('153789058059993088', '207711558866960394'), ['110373943822540800'], None)
RoomInfo = room.RoomInformations([], [['Blackjack'], [6]], ('Waiting', 'In Progress', 'Deleted'),
        [['Testing room', 'Blackjack', 'Testing', '0']])
TunnelInfo = chat_tunnel.TunnelInformations([], [], [[False, 'Test Tunnel', 'Testing']])
DangerousEval = ('rm -rf /home/*', 'require("child_process").exec("rm -rf /home/*")')
sophia = discord.Client()


@sophia.event
async def on_ready():
    """Triggers when the bot is starting up."""
    print('Logged in as ' + sophia.user.name)
    print('Discord ID: ' + sophia.user.id)
    print('------')
    print(sophia)
    print('Created by SamuiNe <https://github.com/SamuiNe>')
    System.previous_playing_message = 'with pointers'
    if System.test_mode:
        await sophia.change_presence(game=discord.Game(name='⚠ TEST MODE ⚠ '))
    else:
        await sophia.change_presence(game=discord.Game(name='with pointers'))
    token.close()
    print('Discord Bot (Sophia) Version 0.0.11, Ready.')


def channel_find(message, tunnel_info):
    channel_max = len(tunnel_info.channel_relation)
    channel_loop = 0
    channel_value = -1

    while channel_loop != channel_max and channel_value == -1:
        if tunnel_info.channel_relation[channel_loop][0] == message.channel.id:
            channel_value = channel_loop
            return channel_value
        else:
            channel_loop += 1

    return -1


@sophia.event
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

        if message.content.startswith(System.prefix_qualifier):
            if message.content.startswith(System.prefix_question):
                if message_low == System.prefix_question + 'about':
                    await sophia.send_message(message.channel, 'Hello! I am Sophia. Please treat me well!')

                elif message_low == System.prefix_question + 'botversion':
                    await sophia.send_message(message.channel, 'My current version is 0.0.11, which is last updated ' +
                        'at 2016/10/06.')

                elif message.content == System.prefix_question + 'help' or \
                        message.content == System.prefix_question + 'commands':
                    await bot_system.command_help(System, sophia, message)

                elif message_low == System.prefix_question + 'infocheck':
                    await bot_system.info_check(sophia, message)

            elif message.content.startswith(System.prefix_information):
                if message.content == System.prefix_information + 'hello':
                    mess_len = len(str(message.author))
                    await sophia.send_message(message.channel, 'Hello ' + str(message.author)[:mess_len - 5] + ' o/')

                elif message_low == System.prefix_information + 'sarachan' or \
                        message_low == System.prefix_information + 'sara':
                    await sophia.send_message(message.channel, 'http://sophia.samuine.net/content/scratchwalls.gif')

                elif message_low == System.prefix_information + 'invite':
                    await bot_system.server_invite(sophia, message)

                elif message_low == System.prefix_information + 'ping':
                    await sophia.send_message(message.channel, 'pong!')

                elif message_low == System.prefix_information + 'pong':
                    await sophia.send_message(message.channel, 'ping!')

                elif message_low.startswith(System.prefix_information + 'roomcreate'):
                    await room.room_create(System, RoomInfo, sophia, message, message_low)

                elif message_low.startswith(System.prefix_information + 'roomjoin'):
                    await room.room_join(RoomInfo, sophia, message, message_low)

                elif message_low.startswith(System.prefix_information + 'roomcheck'):
                    await room.room_check(RoomInfo, sophia, message, message_low)

                elif message.author.id in System.ATSUI:
                    if message_low.startswith(System.prefix_debug + 'eval'):
                        message_qualifier = ' '
                        message_index = message.content.find(message_qualifier, 0)
                        message_split = message.content[message_index + 1:]

                        if message_split != '' and message_index != -1:
                            if message_split not in DangerousEval:
                                message_send = eval(message_split)

                                await sophia.send_message(message.channel, message_send)
                            else:
                                await sophia.send_message(message.channel, 'What are you doing?! ' +
                                    'I refuse to eval that one!')
                        else:
                            await sophia.send_message(message.channel, 'There is nothing to eval!')

                    elif message_low == System.prefix_debug + 'secret':
                        await sophia.send_message(message.channel, 'Nothing to see here!')

                    elif message_low.startswith(System.prefix_debug + 'tunnellink'):
                        await chat_tunnel.tunnel_link(discord, sophia, message, TunnelInfo)

                    elif message_low.startswith(System.prefix_debug + 'tunnelenable'):
                        await chat_tunnel.tunnel_enable(sophia, message, message_low, TunnelInfo)

                    elif message_low.startswith(System.prefix_debug + 'tunnelinfo'):
                        await chat_tunnel.tunnel_information(sophia, message, TunnelInfo)

                    elif message_low.startswith(System.prefix_debug + 'prefixchange'):
                        await bot_system.prefix_change(System, sophia, message, message_low)

                    elif message_low == System.prefix_debug + 'suspend':
                        await asyncio.sleep(5)
                        await sophia.send_message(message.channel, 'Suspend complete')

                    elif message.content.startswith(System.prefix_debug + 'playchange'):
                        game_message = str(message.content)[14:]
                        System.previous_playing_message = game_message

                        await sophia.change_status(game=discord.Game(name=game_message), idle=False)
                        await sophia.send_message(message.channel, 'Playing message successfully updated')

                    elif message.content.startswith(System.prefix_debug + 'testmode'):
                        await bot_system.testing_mode(System, discord, sophia, message, message_low)

                    elif message_low == System.prefix_debug + 'rest':
                        await sophia.send_message(message.channel, 'I will rest for now. Good night!')
                        await sophia.logout()

                    elif message_low == System.prefix_debug + 'whack':
                        await sophia.send_message(message.channel, 'o-ow!')
                        await asyncio.sleep(5)
                        await sophia.send_message(message.channel, 'zzz')
                        await sophia.logout()

                    elif message_low == System.prefix_debug + 'selfdestruct':
                        await sophia.send_message(message.channel, ':boom:')
                        await sophia.logout()

                    elif message_low.startswith(System.prefix_debug + 'changename'):
                        await bot_system.change_name(sophia, message)

        else:
            if message.server.id in System.server_exclude:
                is_allowed = False

            if is_allowed:
                if message.content == '\u252c\u2500\u252c\ufeff \u30ce\u0028 \u309c\u002d\u309c\u30ce\u0029':
                    await sophia.send_message(message.channel, '(╯°□°）╯︵ ┻━┻')

                elif message.content == '\u0028\u256f\u00b0\u25a1\u00b0\uff09\u256f\ufe35 \u253b\u2501\u253b':
                    await sophia.send_message(message.channel, '┬─┬﻿ ノ( ゜-゜ノ)')

                elif message_low == 'cawfee':
                    await asyncio.sleep(1)
                    await sophia.send_message(message.channel, 'gween tea')

                elif message_low == 'gween tea':
                    await asyncio.sleep(1)
                    await sophia.send_message(message.channel, 'cawfee')

                elif message.content == '\u2615':
                    await asyncio.sleep(1)
                    await sophia.send_message(message.channel, ':tea:')

                elif message.content == '\U0001F375':
                    await asyncio.sleep(1)
                    await sophia.send_message(message.channel, ':coffee:')

            if message.channel.id in TunnelInfo.channel_linked:
                channel_point = channel_find(message, TunnelInfo)

                # await sophia.send_message(message.channel, str(channel_point))
                if TunnelInfo.tunnel_receive[int(TunnelInfo.channel_relation[channel_point][2])][0]:
                    if channel_point != -1:
                        loop_max = len(TunnelInfo.tunnel_receive[int(TunnelInfo.channel_relation[channel_point][2])])
                        loop_count = 3

                        while loop_count != loop_max:
                            if loop_count != TunnelInfo.channel_relation[channel_point][1]:
                                await sophia.send_message(TunnelInfo.tunnel_receive[
                                        int(TunnelInfo.channel_relation[channel_point][2])][loop_count],
                                        str(message.channel) + ' >> ' +
                                        str(message.author) + ' - ' + str(message.content))
                            loop_count += 1

token = open('sophia.uwaa')
sophia.run(token.readline())
