# coding=utf-8
"""Text encoding UTF-8"""

# python built-in modules
import logging
import sys

# other modules
import asyncio
import discord

# sophia modules
import commands_information
import commands_question
import bot_system
import room
import chat_tunnel
logging.basicConfig(level=logging.INFO)
System = bot_system.SystemVariables(
        prefix_qualifier='>',
        prefix_question='>?',
        prefix_information='>!',
        prefix_debug='>!!',
        test_mode=False,
        allowed_testing=['154488551596228610', '164476517101993984'],
        atsui=('153789058059993088', '207711558866960394'),
        trigger_include=['110373943822540800'],
        previous_playing_message=None,
        forbidden_eval=('rm -rf /home/*',
            'require("child_process").exec("rm -rf /home/*")',
            'rm -rf / --nopreserveroot'),
        token_status=False,
        custom_filename_status=False,
        custom_filename_path='',
        eval_error_message=('ya dun goofed', 'AAAAAAAAAAAAAaaaaaaaaaaa',
        'GRAND DAD', 'b-baka!!!', '300 internal server error',
        'i-its not like I want to help you or anything!',
        'git gud', 'did you re-read the code before entering it?',
        'too much php for today?', 'maybe you need some rest?',
        'maybe this might help you?', 'some snek told me this',
        'still better than recursive infinite loop',
        'you\'ve messed up again?', 'try not to rely on eval too much',
        'don\'t worry, at least you\'re improving',
        'maybe you need to understand the code first before evaling?',
        'zzz', ':eyes:', 'wew', '400 bad request', '406 not acceptable',
        '418 I\'m a teapot', '451 unavailable for legal reasons',
        'are you bored at the moment?', 'snek? snek?! snek!!!',
        'you\'ve tried™', 'sdjkfhakjlhfskajhfkjlhf', 'what are you doing?',
        'I am an error message fairy', 'are you having fun?',
        'wew lad', 'how many times are you going to do this?',
        'p-please be gentle', 'you have found a rare item!',
        'I\'ll slap you for this', 'no cookies for you today!',
        'I\'ll revoke your programming certificate', 'again?'))
RoomInfo = room.RoomInformations([], [['Blackjack'], [6]],
        ('Waiting', 'In Progress', 'Deleted'),
        [['Testing room', 'Blackjack', 'Testing', '0']])
TunnelInfo = chat_tunnel.TunnelInformations([], [], [], [], [], [[[True, False, 'Global Chat', '']]])
sophia = discord.Client()
__version__ = '0.2.8'


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
    System.previous_playing_message = System.prefix_question + 'help for help'
    if System.test_mode:
        await sophia.change_presence(game=discord.Game(name='\u26A0 TEST MODE \u26A0'))
    else:
        await sophia.change_presence(game=discord.Game(name=System.previous_playing_message))

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
                await commands_question.question_process(bot_system, chat_tunnel, System, sophia, message, message_low,
                    TunnelInfo, __version__)

            elif message.content.startswith(System.prefix_information):
                await commands_information.information_process(sys, asyncio, discord, bot_system, room, chat_tunnel,
                    System, sophia, message, message_low, TunnelInfo, RoomInfo)

        else:
            if message.server.id in System.trigger_include:
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
                                    if loop_count != TunnelInfo.channel_relation[channel_point][1]:
                                        await sophia.send_message(TunnelInfo.tunnel_receive[
                                                int(TunnelInfo.channel_relation[channel_point][2])][loop_count][0],
                                                str(message.server) + ' / ' + str(message.channel) + ' - ' +
                                                str(message.author) + '\n' +
                                                '>> ' + str(message.content))
                                loop_count += 1

    elif message.author.id == sophia.user.id and len(System.ping_information) != 0:
        if message.channel.id == System.ping_information[0][0]:
            message_content = message.content
            timestamp_value = message.timestamp.hour * 3600000 + \
                    message.timestamp.minute * 60000 + \
                    message.timestamp.second * 1000 + \
                    int(message.timestamp.microsecond / 1000)

            timestamp_difference = timestamp_value - System.ping_information[0][1]
            if timestamp_difference < 0:
                timestamp_difference -= 86400000

            await sophia.edit_message(message, message_content + ' ' + str(timestamp_difference) + '`ms`')
            del System.ping_information[0]


while System.token_status is False:
    try:
        if System.custom_filename_status is False:
            token = open('sophia.alch', 'r')
        else:
            token = open(System.custom_filename_path, 'r')
        sophia.run(token.readline())
        System.token_status = True

    except IOError:
        if System.custom_filename_status is False:
            System.custom_filename_status = True
        print('Failed to find the token file.')
        print('Perhaps the token file is in other file extension?\n')

        print('Please enter the token filename and its file extension.')
        print('To exit out of the program, please enter -1.')

        System.custom_filename_path = input()

        if System.custom_filename_path == '-1':
            print('Exiting out of the program...')
            sys.exit()
