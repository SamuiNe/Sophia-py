# coding=utf-8


class TunnelInformations:
    def __init__(self, server_linked, tunnel_receive):
        self.server_linked = server_linked
        self.tunnel_receive = tunnel_receive

async def tunnel_link(discord, sophia, message, message_low, tunnel_info):
    channelid = message.channel.id

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
        await sophia.send_message(message.channel, 'Channel B assignment successful')

async def tunnel_enable(sophia, message, message_low, tunnel_info):
    tunnel_enable_parameter = str(message_low)[16:]
    await sophia.send_message(message.channel, tunnel_enable_parameter)

    if tunnel_enable_parameter == 'yes' or tunnel_enable_parameter == '1':
        tunnel_info.tunnel_enable = True
        await sophia.send_message(message.channel, 'Message tunneling enabled')

    elif tunnel_enable_parameter == 'no' or tunnel_enable_parameter == '0':
        tunnel_info.tunnel_enable = False
        await sophia.send_message(message.channel, 'Message tunneling disabled')
        
async def tunnel_information(sophia, message, tunnel_info):
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
        '\n' + '`Tunnel Boolean`: ' + str(tunnel_info.tunnel_enable))
