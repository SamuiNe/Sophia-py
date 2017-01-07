# coding=utf-8

# Other required python built-in modules
import random
import traceback
import sys

# Other modules
import psutil


__version__ = '0.2.20'


# TODO: Add poll command
async def command_process(asyncio, discord, bot_system, chat_tunnel, system, sophia, message, message_low, tunnel_info):
    if message_low == system.prefix + 'about':
        await sophia.send_message(message.channel, 'Hello! I am Sophia. Please treat me well!')

    elif message_low == system.prefix + 'botversion':
        await sophia.send_message(message.channel, 'My current version is ' + __version__ +
            ', which is last updated at 2016/12/18.')

    elif message_low == system.prefix + 'help':
        await bot_system.command_help(system, sophia, message)

    elif message_low.startswith(system.prefix + 'command'):
        await bot_system.individual_command_help(system, sophia, message)

    elif message_low == system.prefix + 'infocheck':
        await bot_system.info_check(sophia, message)

    elif message_low.startswith(system.prefix + 'tunnelcheck'):
        await chat_tunnel.tunnel_information(sophia, message, tunnel_info)

# Old command question prefix

    if message_low == system.prefix + 'ping':
        ping_message = 'pong!'
        await bot_system.detailed_ping(system, sophia, message, ping_message)

    elif message_low == system.prefix + 'pong':
        ping_message = 'ping!'
        await bot_system.detailed_ping(system, sophia, message, ping_message)

    elif message_low == system.prefix + 'hello':
        mess_len = len(str(message.author))
        await sophia.send_message(message.channel, 'Hello ' + str(message.author)[:mess_len - 5] + ' o/')

    elif message_low == system.prefix + 'sarachan' or message_low == system.prefix + 'sara':
        await sophia.send_message(message.channel, 'http://sophia.samuine.net/content/scratchwalls.gif')

    elif message_low == system.prefix + 'invite':
        await bot_system.server_invite(sophia, message)

    elif message_low.startswith(system.prefix + 'tunnel'):
        if message_low.startswith(system.prefix + 'tunnellink'):
            await chat_tunnel.tunnel_link(system, discord, sophia, message, tunnel_info)

        elif message_low.startswith(system.prefix + 'tunnelenable'):
            await chat_tunnel.tunnel_enable(system, sophia, message, message_low, tunnel_info)

        elif message_low.startswith(system.prefix + 'tunnelmode'):
            await chat_tunnel.tunnel_mode(system, sophia, message, tunnel_info)

        elif message_low.startswith(system.prefix + 'tunnelcreate'):
            await chat_tunnel.tunnel_create(discord, system, sophia, message, tunnel_info)

        elif message_low.startswith(system.prefix + 'tunnelleave'):
            await chat_tunnel.tunnel_leave(system, sophia, message, tunnel_info)

        elif message_low.startswith(system.prefix + 'tunneldelete'):
            await  chat_tunnel.tunnel_delete(asyncio, system, sophia, message, tunnel_info)

    elif message_low.startswith(system.prefix + 'triggertoggle'):
        permission_check = await chat_tunnel.permission_check(system, message)
        await bot_system.trigger_toggle(system, sophia, message, message_low, permission_check)

# Old command debug prefix

    if message.author.id in system.ATSUI:
        if message_low.startswith(system.prefix + 'eval'):
            message_content = message.content.split(' ', maxsplit=1)

            if len(message_content) > 1:
                if message_content[1] not in system.forbidden_eval:
                    try:
                        message_send = eval(message_content[1])
                    except BaseException:
                        await sophia.send_message(message.channel,
                                system.eval_error_message[random.randrange(
                                system.eval_error_length)] + '\n' +
                                '```py\n' + traceback.format_exc() + '```')

                    else:
                        await sophia.send_message(message.channel, message_send)
                else:
                    await sophia.send_message(message.channel, 'nope')
            else:
                await sophia.send_message(message.channel, ':eyes:')

        elif message_low == system.prefix + 'secret':
            await sophia.send_message(message.channel, 'Nothing to see here!')

        elif message_low.startswith(system.prefix + 'prefixchange'):
            await bot_system.prefix_change(system, sophia, message)

        elif message_low == system.prefix + 'status':
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

        elif message_low == system.prefix + 'suspend':
            await asyncio.sleep(5)
            await sophia.send_message(message.channel, 'Suspend complete')

        elif message_low.startswith(system.prefix + 'playchange'):
            game_message = message.content.split(' ', maxsplit=1)
            system.previous_playing_message = game_message[1]

            await sophia.change_presence(game=discord.Game(name=game_message[1]))
            await sophia.send_message(message.channel, 'Playing message has successfully updated.')

        elif message_low.startswith(system.prefix + 'testmode'):
            await bot_system.testing_mode(system, discord, sophia, message, message_low)

        elif message_low == system.prefix + 'rest':
            await sophia.send_message(message.channel, 'I will rest for now. Good night!')
            await sophia.logout()

        elif message_low == system.prefix + 'whack':
            await sophia.send_message(message.channel, 'o-ow!')
            await asyncio.sleep(5)
            await sophia.send_message(message.channel, 'zzz')
            await sophia.logout()

        elif message_low.startswith(system.prefix + 'changename'):
            await bot_system.change_name(sophia, message)

        elif message_low.startswith(system.prefix + 'changeavatar'):
            await bot_system.change_avatar(sophia, message)

        elif message_low.startswith(system.prefix + 'leaveserver'):
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
