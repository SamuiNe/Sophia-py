# coding=utf-8
"""Text encoding UTF-8"""


# TODO: Work on tunnel_link to allow multiple channel linking
# TODO: Allow tunnel_enable only to the channel that is in first entry


class TunnelInformations:
    def __init__(self, channel_linked, channel_relation, tunnel_receive):
        self.channel_linked = channel_linked
        self.channel_relation = channel_relation
        self.tunnel_receive = tunnel_receive


async def tunnel_link(discord, sophia, message, tunnel_info):
    message_qualifier = ' '
    message_index = message.content.find(message_qualifier, 0)
    message_password = message.content.find(message_qualifier, message_index + 1)
    channel_id = message.channel.id
    tunnel_password = ''

    if message_password != -1:
        tunnel_id = message.content[message_index + 1: message_password]
        tunnel_password = message.content[message_password + 1:]
    else:
        tunnel_id = message.content[message_index + 1:]

    # await sophia.send_message(message.channel, str(len(tunnel_id)) + ' ' + tunnel_id)

    if tunnel_info.tunnel_receive[int(tunnel_id)] is not None:
        # await sophia.send_message(message.channel, 'Condition Level 1 pass')
        if tunnel_info.tunnel_receive[int(tunnel_id)][2] != '':
            # await sophia.send_message(message.channel, 'Condition Level 2 pass')
            if tunnel_info.tunnel_receive[int(tunnel_id)][2] == tunnel_password:
                # await sophia.send_message(message.channel, 'Condition Level 3 pass')
                if channel_id not in tunnel_info.channel_linked:
                    # await sophia.send_message(message.channel, 'Condition Level 4 pass')
                    tunnel_info.tunnel_receive[int(tunnel_id)].append(
                        discord.utils.get(message.server.channels, id=channel_id))
                    append_point = len(tunnel_info.tunnel_receive[int(tunnel_id)]) - 1
                    tunnel_info.channel_relation.append([message.channel.id, append_point, tunnel_id])
                    tunnel_info.channel_linked.append(message.channel.id)
                    await sophia.send_message(message.channel, 'Channel has successfully linked to tunnel ' +
                        tunnel_id + '.')

                else:
                    await sophia.send_message(message.channel, 'The channel has already linked to an existing tunnel.')

            else:
                await sophia.send_message(message.channel, 'The tunnel password you have entered is invalid.')

        else:
            # await sophia.send_message(message.channel, 'Condition Level 2 failed')
            if channel_id not in tunnel_info.channel_linked:
                # await sophia.send_message(message.channel, 'Condition Level 3b pass')
                tunnel_info.tunnel_receive[int(tunnel_id)].append(
                    discord.utils.get(message.server.channels, id=channel_id))
                append_point = len(tunnel_info.tunnel_receive[int(tunnel_id)]) - 1
                tunnel_info.channel_relation.append([message.channel.id, append_point, tunnel_id])
                tunnel_info.channel_linked.append(message.channel.id)
                await sophia.send_message(message.channel, 'Channel has successfully linked to tunnel ' +
                    tunnel_id + '.')

            else:
                await sophia.send_message(message.channel, 'The channel has already linked to an existing tunnel.')

    else:
        await sophia.send_message(message.channel, 'The tunnel you want to link does not exist.')

    '''Old code
    if str(message_low)[-1:] == 'a':
        # await sophia.send_message(message.channel, 'Debug info: ' + str(message.channel))
        tunnel_info.tunnel_receive_a = discord.utils.get(message.server.channels, id=channelid)
        # await sophia.send_message(message.channel, tunnel_receive_a)
        # await sophia.send_message(tunnel_receive_a, 'Test successful')
        await sophia.send_message(message.channel, 'Channel A assignment successful')

    elif str(message_low)[-1:] == 'b':
        # await sophia.send_message(message.channel, 'Debug info: ' + str(message.channel))
        tunnel_info.tunnel_receive_b = discord.utils.get(message.server.channels, id=channelid)
        # await sophia.send_message(message.channel, tunnel_receive_b)
        # await sophia.send_message(tunnel_receive_b, 'Test successful')
        await sophia.send_message(message.channel, 'Channel B assignment successful')'''

async def tunnel_enable_process(sophia, message, tunnel_info, tunnel_option, tunnel_id):
    if tunnel_option == 'yes' or tunnel_option == '1':
        tunnel_info.tunnel_receive[int(tunnel_id)][0] = True
        await sophia.send_message(message.channel, 'Tunnel ' + tunnel_id + ' is now enabled.')

    elif tunnel_option == 'no' or tunnel_option == '2':
        tunnel_info.tunnel_receive[int(tunnel_id)][0] = False
        await sophia.send_message(message.channel, 'Tunnel ' + tunnel_id + ' is now disabled.')
    else:
        await sophia.send_message(message.channel, 'Unable to change tunnel status since ' +
            'the tunnel status option you have specified is invalid.')

async def tunnel_enable(sophia, message, message_low, tunnel_info):
    message_qualifier = ' '
    message_check = [0, None, None]
    message_check[0] = message.content.find(message_qualifier, 0)
    message_check[1] = message.content.find(message_qualifier, message_check[0] + 1)
    message_check[2] = message.content.find(message_qualifier, message_check[1] + 1)
    channel_id = message.channel.id
    tunnel_password = ''
    tunnel_id = message.content[message_check[0] + 1: message_check[1]]

    await sophia.send_message(message.channel, str(len(tunnel_id)) + ' ' + str(tunnel_id))
    await sophia.send_message(message.channel, str(message_check))

    if message_check[2] != -1:
        tunnel_option = message_low[message_check[1] + 1: message_check[2]]
        tunnel_password = message.content[message_check[2] + 1:]
    else:
        tunnel_option = message_low[message_check[1] + 1:]

    await sophia.send_message(message.channel, str(len(tunnel_password)) + tunnel_password)

    if tunnel_info.tunnel_receive[int(tunnel_id)] is not None:
        if tunnel_option != '':
            try:
                tunnel_info.tunnel_receive[int(tunnel_id)][3]
            except IndexError:
                await sophia.send_message(message.channel, 'Unable to change tunnel status since ' +
                    'there is no channel linked in the tunnel room.')
            else:
                if channel_id in tunnel_info.tunnel_receive[int(tunnel_id)][3].id:
                    if tunnel_info.tunnel_receive[int(tunnel_id)][2] != '':
                        # await sophia.send_message(message.channel, 'Tunnel password detected')
                        if tunnel_info.tunnel_receive[int(tunnel_id)][2] == tunnel_password:
                            # await sophia.send_message(message.channel, 'Tunnel password matches')
                            await tunnel_enable_process(sophia, message, tunnel_info, tunnel_option, tunnel_id)

                        else:
                            await sophia.send_message(message.channel, 'Unable to change tunnel status since ' +
                                'the tunnel password you have specified is incorrect.')

                    else:
                        await tunnel_enable_process(sophia, message, tunnel_info, tunnel_option, tunnel_id)

                else:
                    await sophia.send_message(message.channel, 'Unable to change tunnel status since ' +
                        'you are not the manager of the tunnel room.')

        else:
            await sophia.send_message(message.channel, 'Unable to change tunnel status since ' +
                'you did not specify the tunnel option. ')

    else:
        await sophia.send_message(message.channel, 'Unable to change tunnel status since ' +
            'tunnel you want to enable does not exist.')

    '''Old code
    tunnel_enable_parameter = str(message_low)[16:]
    await sophia.send_message(message.channel, tunnel_enable_parameter)

    if tunnel_enable_parameter == 'yes' or tunnel_enable_parameter == '1':
        tunnel_info.tunnel_enable = True
        await sophia.send_message(message.channel, 'Message tunneling enabled')

    elif tunnel_enable_parameter == 'no' or tunnel_enable_parameter == '0':
        tunnel_info.tunnel_enable = False
        await sophia.send_message(message.channel, 'Message tunneling disabled')'''

async def tunnel_information(sophia, message, tunnel_info):
    message_qualifier = ' '
    message_index = message.content.find(message_qualifier, 0)

    tunnel_id = message.content[message_index + 1:]
    is_password = False

    if tunnel_id != '':
        if tunnel_info.tunnel_receive[int(tunnel_id)] is not None:
            if tunnel_info.tunnel_receive[int(tunnel_id)][2] != '':
                is_password = True

            loop_count = 3
            loop_limit = len(tunnel_info.tunnel_receive[int(tunnel_id)])

            tunnel_stats = '`Tunnel Name`: ' + tunnel_info.tunnel_receive[int(tunnel_id)][1] + \
                ' `Password`: ' + str(is_password) + '\n' + \
                '`ID`: ' + str(tunnel_id) + '\n' + \
                '`Tunnel enabled`: ' + str(tunnel_info.tunnel_receive[int(tunnel_id)][0]) + \
                ' `Channels Linked`: ' + str(loop_limit - 3) + \
                '\n' + '`Channel List`: \n'

            # await sophia.send_message(message.channel, str(loop_count) + ' ' + str(loop_limit))

            while loop_count != loop_limit:
                if loop_count != loop_limit - 1:
                    tunnel_stats += str(tunnel_info.tunnel_receive[int(tunnel_id)][loop_count]) + ' `' + \
                        str(tunnel_info.tunnel_receive[int(tunnel_id)][loop_count].id) + '`' + '\n'

                    loop_count += 1

                else:
                    tunnel_stats += str(tunnel_info.tunnel_receive[int(tunnel_id)][loop_count]) + ' `' + \
                        str(tunnel_info.tunnel_receive[int(tunnel_id)][loop_count].id) + '`'

                    loop_count += 1

            await sophia.send_message(message.channel, tunnel_stats)

        else:
            await sophia.send_message(message.channel, 'The tunnel ID you have entered does not exist.')

    else:
        await sophia.send_message(message.channel, 'Tunnel information search failed since the tunnel ID is missing.')

    '''Old code
    if tunnel_info.tunnel_receive_a is not None:
        tunnel_id_a = tunnel_info.tunnel_receive_a.id
    else:
        tunnel_id_a = 'None'

    if tunnel_info.tunnel_receive_b is not None:
        tunnel_id_b = tunnel_info.tunnel_receive_b.id
    else:
        tunnel_id_b = 'None'

    await sophia.send_message(message.channel, '`Linked channel A`: ' +
        str(tunnel_info.tunnel_receive_a) + ' `' + tunnel_id_a + '`' +
        '\n' + '`Linked channel B`: ' + str(tunnel_info.tunnel_receive_b) + ' `' + tunnel_id_b + '`' +
        '\n' + '`Tunnel Boolean`: ' + str(tunnel_info.tunnel_enable))'''
