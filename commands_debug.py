# coding=UTF-8

import traceback
import random
import psutil

async def debug_process(sys, asyncio, discord, bot_system, room, system, sophia, message, message_low, room_info):
    if message_low.startswith(system.prefix_debug + 'eval'):
        message_qualifier = ' '
        message_index = message.content.find(message_qualifier, 0)
        message_split = message.content[message_index + 1:]

        if message_split != '' and message_index != -1:
            if message_split not in system.forbidden_eval:
                try:
                    message_send = eval(message_split)
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

    elif message_low.startswith(system.prefix_debug + 'roomcheck'):
        await room.room_check(room_info, sophia, message, message_low)

    elif message_low.startswith(system.prefix_debug + 'roomcreate'):
        await room.room_create(system, room_info, sophia, message, message_low)

    elif message_low.startswith(system.prefix_debug + 'roomjoin'):
        await room.room_join(room_info, sophia, message, message_low)

    elif message_low == system.prefix_debug + 'secret':
        await sophia.send_message(message.channel, 'Nothing to see here!')

    elif message_low.startswith(system.prefix_debug + 'prefixchange'):
        await bot_system.prefix_change(system, sophia, message, message_low)

    elif message_low == system.prefix_debug + 'mpstatus':
        await sophia.send_message(message.channel, 'Current MP status:\n\n' +
            '`Allocated` ' + str(round(((sys.getallocatedblocks() * 512) / 1024 ** 2), 2)) + ' `(py)` / ' +
            str(round(psutil.virtual_memory().used / (1024 ** 2), 2)) + ' `MP` (' +
            str(psutil.virtual_memory().percent) + '%)\n' +
            '`Available` ' + str(round(psutil.virtual_memory().available / (1024 ** 2), 2)) +
            ' / ' + str(round(psutil.virtual_memory().total / (1024 ** 2), 2)) + ' `MP`')

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

    elif message_low == system.prefix_debug + 'explosion':
        await sophia.send_message(message.channel, 'explooooosion!')
        await asyncio.sleep(0.5)
        await sophia.send_message(message.channel, ':boom:')
        await asyncio.sleep(4.2)
        await sophia.send_message(message.channel, 'zzz')
        await sophia.logout()

    elif message_low.startswith(system.prefix_debug + 'changename'):
        await bot_system.change_name(sophia, message)

    elif message_low.startswith(system.prefix_debug + 'changeavatar'):
        await bot_system.change_avatar(sophia, message)
