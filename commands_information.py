# coding=UTF-8

import commands_debug

async def information_process(sys, asyncio, discord, bot_system, room, chat_tunnel, system, sophia, message,
        message_low, tunnel_info, room_info):
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

    elif message.author.id in system.ATSUI:
        await commands_debug.debug_process(sys, asyncio, discord, bot_system, room, system, sophia, message,
                message_low, room_info)
