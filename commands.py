# coding=UTF-8

__version__ = '0.2.18'


async def question_process(bot_system, chat_tunnel, system, sophia, message, message_low, tunnel_info):
    if message_low == system.prefix_question + 'about':
        await sophia.send_message(message.channel, 'Hello! I am Sophia. Please treat me well!')

    elif message_low == system.prefix_question + 'botversion':
        await sophia.send_message(message.channel, 'My current version is ' + __version__ +
            ', which is last updated at 2016/12/14.')

    elif message.content == system.prefix_question + 'help':
        await bot_system.command_help(system, sophia, message)

    elif message_low.startswith(system.prefix_question + 'command'):
        await bot_system.individual_command_help(system, sophia, message)

    elif message_low == system.prefix_question + 'infocheck':
        await bot_system.info_check(sophia, message)

    elif message_low.startswith(system.prefix_question + 'tunnelcheck'):
        await chat_tunnel.tunnel_information(sophia, message, tunnel_info)

async def information_process(asyncio, discord, bot_system, chat_tunnel, system, sophia, message,
        message_low, tunnel_info):
    if message_low == system.prefix_information + 'ping':
        ping_message = 'pong!'
        await bot_system.detailed_ping(system, sophia, message, ping_message)

    elif message_low == system.prefix_information + 'pong':
        ping_message = 'ping!'
        await bot_system.detailed_ping(system, sophia, message, ping_message)

    elif message.content == system.prefix_information + 'hello':
        mess_len = len(str(message.author))
        await sophia.send_message(message.channel, 'Hello ' + str(message.author)[:mess_len - 5] + ' o/')

    elif message_low == system.prefix_information + 'sarachan' or \
                    message_low == system.prefix_information + 'sara':
        await sophia.send_message(message.channel, 'http://sophia.samuine.net/content/scratchwalls.gif')

    elif message_low == system.prefix_information + 'invite':
        await bot_system.server_invite(sophia, message)

    elif message_low.startswith(system.prefix_information + 'tunnel'):
        if message_low.startswith(system.prefix_information + 'tunnellink'):
            await chat_tunnel.tunnel_link(system, discord, sophia, message, tunnel_info)

        elif message_low.startswith(system.prefix_information + 'tunnelenable'):
            await chat_tunnel.tunnel_enable(system, sophia, message, message_low, tunnel_info)

        elif message_low.startswith(system.prefix_information + 'tunnelmode'):
            await chat_tunnel.tunnel_mode(system, sophia, message, tunnel_info)

        elif message_low.startswith(system.prefix_information + 'tunnelcreate'):
            await chat_tunnel.tunnel_create(discord, system, sophia, message, tunnel_info)

        elif message_low.startswith(system.prefix_information + 'tunnelleave'):
            await chat_tunnel.tunnel_leave(system, sophia, message, tunnel_info)

        elif message_low.startswith(system.prefix_information + 'tunneldelete'):
            await  chat_tunnel.tunnel_delete(asyncio, system, sophia, message, tunnel_info)

    elif message_low.startswith(system.prefix_information + 'triggertoggle'):
        permission_check = await chat_tunnel.permission_check(system, message)
        await bot_system.trigger_toggle(system, sophia, message, message_low, permission_check)

async def debug_process(sys, asyncio, discord, psutil, bot_system, room, system, sophia, message,
        message_low, room_info):

    if message_low.startswith(system.prefix_debug + 'roomcheck'):
        await room.room_check(room_info, sophia, message, message_low)

    elif message_low.startswith(system.prefix_debug + 'roomcreate'):
        await room.room_create(system, room_info, sophia, message, message_low)

    elif message_low.startswith(system.prefix_debug + 'roomjoin'):
        await room.room_join(room_info, sophia, message, message_low)

    elif message_low == system.prefix_debug + 'secret':
        await sophia.send_message(message.channel, 'Nothing to see here!')

    elif message_low.startswith(system.prefix_debug + 'prefixchange'):
        await bot_system.prefix_change(system, sophia, message, message_low)

    elif message_low == system.prefix_debug + 'status':
        await sophia.send_message(message.channel, 'Current Sophia status:\n' +
            '`CPU`  ' + '%5s' % str(psutil.cpu_percent()) + '% - `' +
            str(psutil.cpu_count()) + ' logical CPU(s)`\n' +
            '`RAM`  ' + '%5s' % str(psutil.virtual_memory().percent) + '% - ' +
            str( round(((sys.getallocatedblocks() * 512) / 1024 ** 2), 2)) + ' `(py)` / ' +
            str(round(psutil.virtual_memory().used / (1024 ** 2), 2)) +
            ' ' + ' / ' + str(round(psutil.virtual_memory().total / (1024 ** 2), 2)) + ' `MB`\n' +
            '`Disk` ' + '%5s' % str(psutil.disk_usage('/').percent) + '% - ' +
            str(round((psutil.disk_usage('/').used / 1024 ** 2), 2)) + ' / ' +
            str(round(psutil.disk_usage('/').total / (1024 ** 2), 2)) + ' `MB`')

    elif message_low == system.prefix_debug + 'suspend':
        await asyncio.sleep(5)
        await sophia.send_message(message.channel, 'Suspend complete')

    elif message.content.startswith(system.prefix_debug + 'playchange'):
        game_message = str(message.content)[14:]
        system.previous_playing_message = game_message

        await sophia.change_presence(game=discord.Game(name=game_message))
        await sophia.send_message(message.channel, 'Playing message has successfully updated.')

    elif message.content.startswith(system.prefix_debug + 'testmode'):
        await bot_system.testing_mode(system, discord, sophia, message, message_low)

    elif message_low == system.prefix_debug + 'rest':
        await sophia.send_message(message.channel, 'I will rest for now. Good night!')
        await sophia.logout()

    elif message_low == system.prefix_debug + 'whack':
        await sophia.send_message(message.channel, 'o-ow!')
        await asyncio.sleep(5)
        await sophia.send_message(message.channel, 'zzz')
        await sophia.logout()

    elif message_low.startswith(system.prefix_debug + 'changename'):
        await bot_system.change_name(sophia, message)

    elif message_low.startswith(system.prefix_debug + 'changeavatar'):
        await bot_system.change_avatar(sophia, message)

    elif message_low.startswith(system.prefix_debug + 'leaveserver'):
        await sophia.send_message(message.channel, 'Server leave success')
        await sophia.leave_server(message.server)

async def trigger_commands(asyncio, sophia, message, message_low):
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
