# coding=utf-8
"""Text encoding UTF-8"""


class TunnelInformations:
    def __init__(self, server_ban, channel_ban, user_ban, channel_linked, channel_relation, tunnel_receive):
        self.banned_server = server_ban
        self.banned_channel = channel_ban
        self.banned_user = user_ban
        self.channel_linked = channel_linked
        self.channel_relation = channel_relation
        self.tunnel_receive = tunnel_receive


async def tunnel_references(discord, message, tunnel_info, tunnel_password, tunnel_id, channel_id, tunnel_name=None):
    if tunnel_name is not None:
        tunnel_info.tunnel_receive.append([[True, False, tunnel_name, tunnel_password]])

    tunnel_info.tunnel_receive[tunnel_id].append([discord.utils.get(message.server.channels, id=channel_id),
            3, message.channel.id, False,message.author.id, False])
    append_point = len(tunnel_info.tunnel_receive[tunnel_id]) - 1

    tunnel_info.channel_relation.append([message.channel.id, append_point, tunnel_id])
    tunnel_info.channel_linked.append(message.channel.id)


async def tunnel_link_process(discord, sophia, message, tunnel_info, tunnel_password, tunnel_id, channel_id):
    await tunnel_references(discord, message, tunnel_info, tunnel_password, tunnel_id, channel_id)
    await sophia.send_message(message.channel, 'Channel has successfully linked to tunnel room ' + str(tunnel_id) + '.')
    # await sophia.delete_message(message)


async def tunnel_link(system, discord, sophia, message, tunnel_info):
    message_content = message.content.split(' ', maxsplit=2)
    server_id = message.server.id
    channel_id = message.channel.id
    tunnel_password = ''
    role_permission = await permission_check(system, message)
    usage_allowed = await ban_check(message, tunnel_info, server_id, channel_id)

    if len(message_content) > 2:
        tunnel_password = message_content[2]

    # await sophia.send_message(message.channel, str(message.content[message_index + 1: message_password]) + ' ' +
    #                    str(len(message.content[message_index + 1: message_password])))

    try:
        tunnel_id = int(message_content[1])

        tunnel_settings = tunnel_info.tunnel_receive[tunnel_id][0]

    except ValueError:
        await sophia.send_message(message.channel, 'The tunnel room you want to link is invalid.')

    except IndexError:
        await sophia.send_message(message.channel, 'The tunnel room you want to link does not exist.')

    else:
        if usage_allowed:
            if tunnel_settings[0]:
                if role_permission:
                    if tunnel_settings[3] != '':
                        if tunnel_settings[3] == tunnel_password:
                            if channel_id not in tunnel_info.channel_linked:
                                await tunnel_link_process(discord, sophia, message, tunnel_info, tunnel_password,
                                        tunnel_id, channel_id)

                            else:
                                await sophia.send_message(message.channel, 'The channel has already ' +
                                    'linked to an existing tunnel.')
                                # await sophia.delete_message(message)

                        else:
                            await sophia.send_message(message.channel,
                                'The tunnel password you have entered is invalid.')

                    else:
                        if channel_id not in tunnel_info.channel_linked:
                            await tunnel_link_process(discord, sophia, message, tunnel_info, tunnel_password,
                                    tunnel_id, channel_id)

                        else:
                            await sophia.send_message(message.channel,
                                'The channel has already linked to an existing tunnel.')
                            # await sophia.delete_message(message)

                else:
                    await sophia.send_message(message.channel, 'Unable to link channel to tunnel room ' +
                        'since you did not have sufficient role permissions.')
                    # await sophia.delete_message(message)

            else:
                await sophia.send_message(message.channel, 'The tunnel you want to link has already been deleted.')

        else:
            await sophia.send_message(message.channel, 'Your current channel or server is banned ' +
                'from using chat tunneling.')


async def tunnel_enable_process(sophia, message, tunnel_info, tunnel_option, tunnel_id):
    if tunnel_option == 'enable' or tunnel_option == 'yes' or tunnel_option == '1':
        tunnel_info.tunnel_receive[int(tunnel_id)][0][1] = True
        await sophia.send_message(message.channel, 'Tunnel ' + str(tunnel_id) + ' is now enabled.')
        # await sophia.delete_message(message)

    elif tunnel_option == 'disable' or tunnel_option == 'no' or tunnel_option == '2':
        tunnel_info.tunnel_receive[int(tunnel_id)][0][1] = False
        await sophia.send_message(message.channel, 'Tunnel ' + str(tunnel_id) + ' is now disabled.')
        await sophia.delete_message(message)

    else:
        await sophia.send_message(message.channel, 'Unable to change tunnel status since ' +
            'the tunnel status option you have specified is invalid.')


async def tunnel_enable(system, sophia, message, message_low, tunnel_info):
    message_low_content = message_low.split(' ', maxsplit=3)
    channel_id = message.channel.id
    tunnel_password = ''
    role_permission = await permission_check(system, message)

    # await sophia.send_message(message.channel, str(len(tunnel_id)) + ' ' + str(tunnel_id))
    # await sophia.send_message(message.channel, str(message_check))

    if len(message_low_content) > 3:
        tunnel_option = message_low_content[2]
        tunnel_password = message_low_content[3]
    else:
        tunnel_option = message_low_content[2]

    # await sophia.send_message(message.channel, str(len(tunnel_password)) + tunnel_password)
    try:
        tunnel_id = message_low_content[1]
        current_tunnel = tunnel_info.tunnel_receive[int(tunnel_id)]
    except ValueError:
        await sophia.send_message(message.channel, 'The command format you have entered is invalid.\n' +
            'The command format is `' + system.prefix_information + 'tunnelenable `*`tunnel_id option room_password`*')

    except IndexError:
        await sophia.send_message(message.channel, 'Unable to change tunnel status since ' +
            'tunnel you want to enable does not exist.')

    else:
        if tunnel_option != '':
            if role_permission:
                if channel_id in current_tunnel[1][0].id:
                    if current_tunnel[0][3] != '':
                        if current_tunnel[0][3] == tunnel_password:
                            await tunnel_enable_process(sophia, message, tunnel_info, tunnel_option, tunnel_id)

                        else:
                            await sophia.send_message(message.channel, 'Unable to change tunnel status since ' +
                                'the tunnel password you have specified is incorrect.')

                    else:
                        await tunnel_enable_process(sophia, message, tunnel_info, tunnel_option, tunnel_id)

                else:
                    await sophia.send_message(message.channel, 'Unable to change tunnel status since ' +
                        'this channel is not manager of the tunnel room.')
            else:
                await sophia.send_message(message.channel, 'Unable to change tunnel status since ' +
                    'you did not have sufficient role permissions.')

        else:
            await sophia.send_message(message.channel, 'Unable to change tunnel status since ' +
                'you did not specify the tunnel option. ')


async def tunnel_information(sophia, message, tunnel_info):
    # message_qualifier = ' '
    message_content = message.content.split(' ', maxsplit=1)
    tunnel_type_indicator = ('`--`', '`<-`', '`->`', '`<>`')

    # await sophia.send_message(message.channel, str(tunnel_id))

    if len(message_content) > 1:
        try:
            tunnel_id = int(message_content[1])
            current_tunnel = tunnel_info.tunnel_receive[tunnel_id]

        except IndexError:
            await sophia.send_message(message.channel, 'The tunnel ID you have provided does not exist.')

        except ValueError:
            await sophia.send_message(message.channel, 'The tunnel ID you have provided is not a number.')

        else:
            loop_count = 1
            loop_limit = len(current_tunnel)

            if current_tunnel[0][0]:
                if current_tunnel[0][3] != '':
                    is_password = ' `Passworded`'
                else:
                    is_password = ' `No Password`'

                if current_tunnel[0][1]:
                    is_enabled = ' `Enabled`'
                else:
                    is_enabled = ' `Disabled`'

                tunnel_stats = '`Tunnel Room`: ' + current_tunnel[0][2] + \
                    is_password + '\n' + \
                    '`ID`: ' + str(tunnel_id) + is_enabled + '\n' \
                    '`Channels`: ' + str(loop_limit - 1) + \
                    '\n' + '`Channel List`: \n'

                # await sophia.send_message(message.channel, str(loop_count) + ' ' + str(loop_limit))

                while loop_count != loop_limit:
                    tunnel_stats += str(tunnel_type_indicator[current_tunnel[loop_count][1]]) + ' '

                    if loop_count != loop_limit - 1:
                        tunnel_stats += str(current_tunnel[loop_count][0]) + ' `' + \
                                str(current_tunnel[loop_count][0].id) + '` `' + \
                                str(current_tunnel[loop_count][0].server.id) + '`\n'

                        loop_count += 1

                    else:
                        tunnel_stats += str(current_tunnel[loop_count][0]) + ' `' + \
                                str(current_tunnel[loop_count][0].id) + '` `' + \
                                str(current_tunnel[loop_count][0].server.id) + '`\n'

                        loop_count += 1

                await sophia.send_message(message.channel, tunnel_stats)
            else:
                await sophia.send_message(message.channel,
                    'The tunnel room you want to check has already been deleted.')

    else:
        await sophia.send_message(message.channel, 'Tunnel information search failed since the tunnel ID is missing.')


async def tunnel_create(discord, system, sophia, message, tunnel_info):
    channel_id = message.channel.id
    server_id = message.server.id
    message_content = message.content.split(' ', maxsplit=2)
    message_content_length = len(message_content)
    role_permission = await permission_check(system, message)
    usage_allowed = await ban_check(message, tunnel_info, server_id, channel_id)

    if usage_allowed:
        if role_permission:
            if message_content_length >= 2:
                if message_content_length == 3:
                    tunnel_name = message_content[1]
                    tunnel_password = message_content[2]

                else:
                    tunnel_name = message_content[1]
                    tunnel_password = ''

                tunnel_count = len(tunnel_info.tunnel_receive)

                await tunnel_references(discord, message, tunnel_info, tunnel_password, tunnel_count, channel_id,
                    tunnel_name)
                await sophia.send_message(message.channel, str(tunnel_name) +
                    ' has successfully created and linked.\n' +
                    'Your tunnel ID is ' + str(tunnel_count) + '.')
                # await sophia.delete_message(message)

            else:
                await sophia.send_message(message.channel, 'Tunnel room creation failed since ' +
                    'you did not specify a room name nor password.')

        else:
            # await sophia.delete_message(message)
            await sophia.send_message(message.channel, 'Unable to create tunnel room since ' +
                'you do not have sufficient role permissions.')

    else:
        await sophia.send_message(message.channel, 'Your current channel or server is banned ' +
            'from using chat tunneling.')


async def tunnel_leave_process(sophia, message, tunnel_info, channel_point):
    tunnel_id = int(tunnel_info.channel_relation[channel_point][2])
    tunnel_index = tunnel_info.channel_relation[channel_point][1]
    tunnel_channel_link = tunnel_info.channel_linked.index(message.channel.id)
    tunnel_length = len(tunnel_info.tunnel_receive[tunnel_id])

    if tunnel_length > 2 and channel_point is not tunnel_length:
        tunnel_loop = tunnel_index + 1
        channel_loop = 0
        preceding_channels = [None]
        channel_max = len(tunnel_info.channel_relation)

        while tunnel_loop < tunnel_length:
            # await sophia.send_message(message.channel, str(tunnel_id) + " " + str(tunnel_loop))
            preceding_channels.append(tunnel_info.tunnel_receive[tunnel_id][tunnel_loop][0].id)
            tunnel_loop += 1

        loop_counter = 0

        while channel_loop < channel_max:
            if tunnel_info.channel_relation[channel_loop][0] in preceding_channels:
                tunnel_info.channel_relation[channel_loop][1] -= 1
            channel_loop += 1

    del tunnel_info.tunnel_receive[tunnel_id][tunnel_index]
    del tunnel_info.channel_relation[channel_point]
    del tunnel_info.channel_linked[tunnel_channel_link]

    await sophia.send_message(message.channel, 'The channel has successfully left the tunnel room.')


async def tunnel_leave(system, sophia, message, tunnel_info):
    message_content = message.content.split(' ', maxsplit=1)
    channel_point = await current_channel_find(message, tunnel_info)
    role_permission = await permission_check(system, message)

    # await sophia.send_message(message.channel, str(channel_point) + ' ' + str(message_check))
    if channel_point != -1:
        if role_permission:
            tunnel_id = int(tunnel_info.channel_relation[channel_point][2])
            tunnel_settings = tunnel_info.tunnel_receive[tunnel_id][0]

            if tunnel_settings[3] != '':
                if len(message_content) > 1:
                    if message_content[1] == tunnel_settings[3]:
                        await tunnel_leave_process(sophia, message, tunnel_info, channel_point)

                    else:
                        await sophia.send_message(message.channel,
                            'Failed to leave tunnel room since the entered password is invalid.')
                else:
                    await sophia.send_message(message.channel,
                        'Failed to leave the tunnel room since the room password is not entered.')

            else:
                await tunnel_leave_process(sophia, message, tunnel_info, channel_point)

        else:
            await sophia.send_message(message.channel, 'Unable to leave tunnel room since' +
                ' you did not have sufficient role permission.')

    else:
        await sophia.send_message(message.channel, 'The channel is not in a tunnel room.')


async def tunnel_delete_process(asyncio, sophia, tunnel_info, message, channel_point):
    tunnel_id = int(tunnel_info.channel_relation[channel_point][2])
    current_tunnel = tunnel_info.tunnel_receive[tunnel_id]
    loop_count = 1
    loop_max = len(current_tunnel)
    tunnel_channel_relation = []
    tunnel_channel_link = []

    while loop_count != loop_max:
        await sophia.send_message(current_tunnel[loop_count][0] ,
            '\u26A0 The tunnel room manager has initiated tunnel room deletion.\n\n' +
            'All linked channels will be unlinked and ' +
            'the tunnel room will be deleted within 5 seconds.')
        loop_count += 1
    loop_count = loop_max - 1

    await asyncio.sleep(5)

    while loop_count != loop_max:
        tunnel_channel_relation.append(tunnel_info.channel_relation.index(
                [current_tunnel[loop_count][0].id, loop_count, tunnel_id]))
        tunnel_channel_link.append(tunnel_info.channel_linked.index(message.channel.id))

        loop_count += 1
    loop_count = 1

    while loop_count != 0:
        del tunnel_info.channel_relation[tunnel_channel_relation[loop_count - 1]]
        del tunnel_info.channel_linked[tunnel_channel_link[loop_count - 1]]
        del current_tunnel[loop_count]

        loop_count -= 1
    tunnel_info.tunnel_receive[tunnel_id][0][0] = False
    tunnel_info.tunnel_receive[tunnel_id][0][1] = False
    tunnel_info.tunnel_receive[tunnel_id][0][2] = '-'
    tunnel_info.tunnel_receive[tunnel_id][0][3] = ''

    await sophia.send_message(message.channel, 'Tunnel room deletion successful.')


async def tunnel_delete(asyncio, system, sophia, message, tunnel_info):
    message_content = message.content.split(' ', maxsplit=1)
    channel_point = await current_channel_find(message, tunnel_info)
    role_permission = await permission_check(system, message)

    if channel_point != -1:
        tunnel_id = int(tunnel_info.channel_relation[channel_point][2])
        current_tunnel = tunnel_info.tunnel_receive[tunnel_id]

        if message.channel.id == current_tunnel[1][0].id:
            if role_permission:
                if current_tunnel[0][3] != '':
                    if message_content[1] == current_tunnel[0][3]:
                        await tunnel_delete_process(asyncio, sophia, tunnel_info, message, channel_point)

                    else:
                        await sophia.send_message(message.channel, 'The password you have entered is invalid.')

                else:
                    await tunnel_delete_process(asyncio, sophia, tunnel_info, message, channel_point)

            else:
                await sophia.send_message(message.channel, 'Unable to delete tunnel room since ' +
                    'you did not have sufficient role permission.')
        else:
            await sophia.send_message(message.channel, 'Unable to delete tunnel room since ' +
                'this channel is not the manager of this tunnel room.')

    else:
        await sophia.send_message(message.channel, 'This channel is currently not linked to any tunnel room.')


async def tunnel_mode(system, sophia, message, tunnel_info):
    message_content = message.content.split(' ', maxsplit=1)
    channel_point = await current_channel_find(message, tunnel_info)
    role_permission = await permission_check(system, message)

    # await sophia.send_message(message.channel, str(channel_point))
    # await sophia.send_message(message.channel, str(message_content))

    if channel_point != -1:
        if role_permission:
            tunnel_id = int(tunnel_info.channel_relation[channel_point][2])
            channel_position = tunnel_info.channel_relation[channel_point][1]

            if message_content[1] == '3' or message_content[1] == 'all':
                tunnel_info.tunnel_receive[tunnel_id][channel_position][1] = 3
                await sophia.send_message(message.channel,
                    'This channel room now both receive and send messages.')

            elif message_content[1] == '2' or message_content[1] == 'receive':
                tunnel_info.tunnel_receive[tunnel_id][channel_position][1] = 2
                await sophia.send_message(message.channel,
                    'This channel room now only receives messages.')

            elif message_content[1] == '1' or message_content[1] == 'send':
                tunnel_info.tunnel_receive[tunnel_id][channel_position][1] = 1
                await sophia.send_message(message.channel,
                    'This channel room now only sends messages.')

            elif message_content[1] == '0' or message_content[1] == 'none':
                tunnel_info.tunnel_receive[tunnel_id][channel_position][1] = 0
                await sophia.send_message(message.channel,
                    'This channel room now does not receive nor send any messages.')

            else:
                await sophia.send_message(message.channel, 'Failed to change tunnel mode due to invalid option.')
        else:
            await sophia.send_message(message.channel, 'Unable to change tunnel mode since ' +
                'you did not have sufficient role permission.')
    else:
        await sophia.send_message(message.channel, 'This channel is currently not linked to any tunnel room.')

async def current_channel_find(message, tunnel_info):
    channel_max = len(tunnel_info.channel_relation)
    channel_loop = 0
    channel_value = -1

    while channel_loop < channel_max and channel_value == -1:
        if tunnel_info.channel_relation[channel_loop][0] == message.channel.id:
            channel_value = channel_loop
            return channel_value

        else:
            channel_loop += 1

    return -1


async def permission_check(system, message):
    message_author = message.channel.permissions_for(message.author)

    if message_author.administrator or message_author.manage_server or message_author.manage_channels:
        return True

    else:
        if message.author.id in system.ATSUI:
            return True

        else:
            return False


async def ban_check(message, tunnel_info, server_id, channel_id):
    if message.author.id in tunnel_info.banned_user or \
            channel_id in tunnel_info.banned_channel or server_id in tunnel_info.banned_server:
        return False

    else:
        return True

async def chat_tunnel_process(sophia, message, tunnel_info):
    channel_point = await current_channel_find(message, tunnel_info)

    # await sophia.send_message(message.channel, str(channel_point))
    if tunnel_info.tunnel_receive[int(tunnel_info.channel_relation[channel_point][2])][0][1]:
        if channel_point != -1:
            send_allowed = True
            tunnel_id = int(tunnel_info.channel_relation[channel_point][2])
            current_tunnel = tunnel_info.tunnel_receive[tunnel_id]
            channel_id = tunnel_info.channel_relation[channel_point][1]
            loop_max = len(current_tunnel)
            loop_count = 1

            if current_tunnel[channel_id][1] != 0 and current_tunnel[channel_id][1] != 2:
                # await sophia.send_message(message.channel, 'stage 1 pass')
                while loop_count != loop_max and send_allowed:
                    # await sophia.send_message(message.channel, 'stage 2 pass')
                    if current_tunnel[loop_count][1] >= 2:
                        # await sophia.send_message(message.channel, 'stage 3 pass')
                        if loop_count != tunnel_info.channel_relation[channel_point][1]:
                            # await sophia.send_message(message.channel, 'stage 4 pass')
                            if message.channel.id != current_tunnel[loop_count][2]:
                                # await sophia.send_message(message.channel, 'Switched to False')
                                tunnel_info.tunnel_receive[tunnel_id][loop_count][2] = message.channel.id
                                tunnel_info.tunnel_receive[tunnel_id][loop_count][3] = False
                                tunnel_info.tunnel_receive[tunnel_id][loop_count][4] = message.author.id
                                tunnel_info.tunnel_receive[tunnel_id][loop_count][5] = False

                            if current_tunnel[loop_count][3]:
                                if message.author.id != current_tunnel[loop_count][4]:
                                    tunnel_info.tunnel_receive[tunnel_id][loop_count][4] = message.author.id
                                    tunnel_info.tunnel_receive[tunnel_id][loop_count][5] = False

                                if current_tunnel[loop_count][5]:
                                    await sophia.send_message(current_tunnel[loop_count][0],
                                        str(message.timestamp)[11:16] + ' >> ' + str(message.content))

                                else:
                                    await sophia.send_message(current_tunnel[loop_count][0],
                                        str(message.author) + '\n' +
                                        str(message.timestamp)[11:16] + ' >> ' + str(message.content))
                                    tunnel_info.tunnel_receive[tunnel_id][loop_count][5] = True

                            else:
                                await sophia.send_message(current_tunnel[loop_count][0],
                                    '<' + str(message.server) + ' / ' + str(message.channel) + '>\n' +
                                    str(message.author) + '\n' +
                                    str(message.timestamp)[11:16] + ' >> ' + str(message.content))
                                # await sophia.send_message(message.channel, 'Switched to True')
                                tunnel_info.tunnel_receive[tunnel_id][loop_count][3] = True
                                tunnel_info.tunnel_receive[tunnel_id][loop_count][5] = True

                        else:
                            tunnel_info.tunnel_receive[tunnel_id][loop_count][2] = message.channel.id
                            tunnel_info.tunnel_receive[tunnel_id][loop_count][3] = False

                    loop_count += 1
