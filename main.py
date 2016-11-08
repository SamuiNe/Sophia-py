# coding=utf-8
"""Text encoding UTF-8"""

# python built-in modules
import logging

# other modules
import asyncio
import discord
import rethinkdb

# sophia modules
import bot_system
import room
import chat_tunnel

logging.basicConfig(level=logging.INFO)
System = bot_system.SystemVariables('>', '>?', '>!', '>!!', False, ['154488551596228610', '164476517101993984'],
        ('153789058059993088', '207711558866960394'), ['110373943822540800'], None)
RoomInfo = room.RoomInformations([], [['Blackjack'], [6]], ('Waiting', 'In Progress', 'Deleted'),
        [['Testing room', 'Blackjack', 'Testing', '0']])
TunnelInfo = chat_tunnel.TunnelInformations([], [], [], [], [], [[[True, False, 'Global Chat', '']]])
DangerousEval = ('rm -rf /home/*', 'require("child_process").exec("rm -rf /home/*")')
sophia = discord.Client()
__version__ = '0.2.3'


@sophia.event
async def on_ready():
    """Triggers when the bot is starting up."""
    print('              [][][]')
    print('          [][]      [][]')
    print('      [][]              [][]')
    print('  [][]                      [][]')
    print('[][]                          [][]')
    print('[]  [][]                  [][]  []')
    print('[]      [][]          [][]      []')
    print('[]          [][]  [][]          []')
    print('[]      [][]    []    [][]      []')
    print('[]  [][]        []        [][]  []')
    print('[][]            []            [][]')
    print('  [][]          []          [][]')
    print('      [][]      []      [][]')
    print('          [][]  []  [][]')
    print('              [][][]')
    print('Logged in as ' + sophia.user.name)
    print('Discord ID: ' + sophia.user.id)
    print('Program created by SamuiNe <https://github.com/SamuiNe>')
    System.previous_playing_message = '(´・◡・｀)'
    if System.test_mode:
        await sophia.change_presence(game=discord.Game(name='\u26A0 TEST MODE \u26A0'))
    else:
        await sophia.change_presence(game=discord.Game(name='(´・◡・｀)'))
    token.close()
    print('Sophia Version ' + __version__ + ', Ready.')


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
                    await sophia.send_message(message.channel, 'My current version is ' + __version__ +
                        ', which is last updated at 2016/11/09.')

                elif message.content == System.prefix_question + 'help':
                    await bot_system.command_help(System, sophia, message)

                elif message_low.startswith(System.prefix_question + 'command'):
                    await bot_system.individual_command_help(System, sophia, message)

                elif message_low == System.prefix_question + 'infocheck':
                    await bot_system.info_check(sophia, message)

                elif message_low.startswith(System.prefix_question + 'tunnelcheck'):
                    await chat_tunnel.tunnel_information(sophia, message, TunnelInfo)

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

                elif message_low.startswith(System.prefix_information + 'tunnel'):
                    if message_low.startswith(System.prefix_information + 'tunnellink'):
                        await chat_tunnel.tunnel_link(System, discord, sophia, message, TunnelInfo)

                    elif message_low.startswith(System.prefix_information + 'tunnelenable'):
                        await chat_tunnel.tunnel_enable(System, sophia, message, message_low, TunnelInfo)

                    elif message_low.startswith(System.prefix_information + 'tunnelmode'):
                        await chat_tunnel.tunnel_mode(System, sophia, message, TunnelInfo)

                    elif message_low.startswith(System.prefix_information + 'tunnelcreate'):
                        await chat_tunnel.tunnel_create(discord, System, sophia, message, TunnelInfo)

                    elif message_low.startswith(System.prefix_information + 'tunnelleave'):
                        await chat_tunnel.tunnel_leave(System, sophia, message, TunnelInfo)

                    elif message_low.startswith(System.prefix_information + 'tunneldelete'):
                        await chat_tunnel.tunnel_delete(asyncio, System, sophia, message, TunnelInfo)

                elif message_low.startswith(System.prefix_information + 'triggertoggle'):
                    permission_check = await chat_tunnel.permission_check(System, message)
                    await bot_system.trigger_toggle(System, sophia, message, message_low, permission_check)

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

                    elif message_low.startswith(System.prefix_debug + 'roomcheck'):
                        await room.room_check(RoomInfo, sophia, message, message_low)

                    elif message_low.startswith(System.prefix_debug + 'roomcreate'):
                        await room.room_create(System, RoomInfo, sophia, message, message_low)

                    elif message_low.startswith(System.prefix_debug + 'roomjoin'):
                        await room.room_join(RoomInfo, sophia, message, message_low)

                    elif message_low == System.prefix_debug + 'secret':
                        await sophia.send_message(message.channel, 'Nothing to see here!')

                    elif message_low.startswith(System.prefix_debug + 'prefixchange'):
                        await bot_system.prefix_change(System, sophia, message, message_low)

                    elif message_low == System.prefix_debug + 'suspend':
                        await asyncio.sleep(5)
                        await sophia.send_message(message.channel, 'Suspend complete')

                    elif message.content.startswith(System.prefix_debug + 'playchange'):
                        game_message = str(message.content)[14:]
                        System.previous_playing_message = game_message

                        await sophia.change_status(game=discord.Game(name=game_message), idle=False)
                        await sophia.send_message(message.channel, 'Playing message has successfully updated.')

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

                    elif message_low == System.prefix_debug + 'explosion':
                        await sophia.send_message(message.channel, 'explooooosion!')
                        await asyncio.sleep(0.5)
                        await sophia.send_message(message.channel, ':boom:')
                        await asyncio.sleep(4.2)
                        await sophia.send_message(message.channel, 'zzz')
                        await sophia.logout()

                    elif message_low.startswith(System.prefix_debug + 'changename'):
                        await bot_system.change_name(sophia, message)

                    elif message_low.startswith(System.prefix_debug + 'changeavatar'):
                        await bot_system.change_avatar(sophia, message)

        else:
            if message.server.id in System.trigger_exclude:
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
                channel_point = await chat_tunnel.channel_find(message, TunnelInfo)

                # await sophia.send_message(message.channel, str(channel_point))
                if TunnelInfo.tunnel_receive[int(TunnelInfo.channel_relation[channel_point][2])][0][1]:
                    if channel_point != -1:
                        loop_max = len(TunnelInfo.tunnel_receive[int(TunnelInfo.channel_relation[channel_point][2])])
                        loop_count = 1
                        send_allowed = True

                        if TunnelInfo.tunnel_receive[int(TunnelInfo.channel_relation[channel_point][2])][
                                TunnelInfo.channel_relation[channel_point][1]][1] != 0 and \
                                TunnelInfo.tunnel_receive[int(TunnelInfo.channel_relation[channel_point][2])][
                                TunnelInfo.channel_relation[channel_point][1]][1] != 2:
                            while loop_count != loop_max and send_allowed:
                                if TunnelInfo.tunnel_receive[int(TunnelInfo.channel_relation[channel_point][2])][
                                        loop_count][1] >= 2:
                                    # if :
                                    #   loop_count = TunnelInfo.channel_relation[channel_point][1]
                                    if loop_count != TunnelInfo.channel_relation[channel_point][1]:
                                        await sophia.send_message(TunnelInfo.tunnel_receive[
                                                int(TunnelInfo.channel_relation[channel_point][2])][loop_count][0],
                                                str(message.server) + ' / ' + str(message.channel) + ' - ' +
                                                str(message.author) + '\n' +
                                                '>> ' + str(message.content))
                                loop_count += 1

token = open('sophia.alch')
sophia.run(token.readline())
