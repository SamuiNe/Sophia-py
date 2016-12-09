# coding=utf-8
"""Text encoding UTF-8"""

# python built-in modules
import logging
import sys
import random
import traceback

# other modules
import asyncio
import discord
import psutil

# sophia modules
import commands
import bot_system
import room
import chat_tunnel

logging.basicConfig(level=logging.INFO)
System = bot_system.SystemVariables(
        prefix_qualifier='>',
        prefix_question='>?',
        prefix_information='>!',
        prefix_debug='>>',
        test_mode=False,
        allowed_testing=['154488551596228610', '164476517101993984'],
        atsui=('153789058059993088', '207711558866960394'),
        trigger_exclude=['110373943822540800'],
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
__version__ = '0.2.13'


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
    print('Logged in as ' + sophia.user.name + ', Discord ID ' + sophia.user.id + '.')
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
                await commands.question_process(bot_system, chat_tunnel, System, sophia, message, message_low,
                    TunnelInfo, __version__)

            elif message.content.startswith(System.prefix_information):
                await commands.information_process(asyncio, discord, bot_system, chat_tunnel, System, sophia, message,
                    message_low, TunnelInfo)

            elif message.content.startswith(System.prefix_debug):
                if message.author.id in System.ATSUI:
                    if message_low.startswith(System.prefix_debug + 'eval'):
                        message_qualifier = ' '
                        message_index = message.content.find(message_qualifier, 0)
                        message_split = message.content[message_index + 1:]

                        if message_split != '' and message_index != -1:
                            if message_split not in System.forbidden_eval:
                                try:
                                    message_send = eval(message_split)
                                except BaseException:
                                    await sophia.send_message(message.channel,
                                        System.eval_error_message[random.randrange(
                                        System.eval_error_length)] + '\n' +
                                        '```py\n' + traceback.format_exc() + '```')

                                else:
                                    await sophia.send_message(message.channel, message_send)
                            else:
                                await sophia.send_message(message.channel, 'nope')
                        else:
                            await sophia.send_message(message.channel, ':eyes:')
                    else:
                        await commands.debug_process(sys, asyncio, discord, psutil, bot_system, room,
                            System, sophia, message, message_low, RoomInfo)

        else:
            # await sophia.send_message(message.channel, 'message OK')
            await commands.trigger_commands(asyncio, sophia, message, message_low)

            if message.channel.id in TunnelInfo.channel_linked:
                await chat_tunnel.chat_tunnel_process(sophia, message, TunnelInfo)

    else:
        if message.channel.id in TunnelInfo.channel_linked and message.author.id != sophia.user.id:
            channel_point = await chat_tunnel.channel_find(message, TunnelInfo)
            tunnel_id = int(TunnelInfo.channel_relation[channel_point][2])
            channel_id = TunnelInfo.channel_relation[channel_point][1]

            # await sophia.send_message(message.channel, 'Switched to False')
            TunnelInfo.tunnel_receive[tunnel_id][channel_id][2] = message.channel.id
            TunnelInfo.tunnel_receive[tunnel_id][channel_id][3] = False

        if message.author.id == sophia.user.id and System.ping_information:
            await bot_system.detailed_ping_edit(System, sophia, message)


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
