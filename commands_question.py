# coding=utf-8

async def question_process(bot_system, chat_tunnel, system, sophia, message, message_low, tunnel_info, version):
    if message_low == system.prefix_question + 'about':
        await sophia.send_message(message.channel, 'Hello! I am Sophia. Please treat me well!')

    elif message_low == system.prefix_question + 'botversion':
        await sophia.send_message(message.channel, 'My current version is ' + version +
            ', which is last updated at 2016/11/21.')

    elif message.content == system.prefix_question + 'help':
        await bot_system.command_help(system, sophia, message)

    elif message_low.startswith(system.prefix_question + 'command'):
        await bot_system.individual_command_help(system, sophia, message)

    elif message_low == system.prefix_question + 'infocheck':
        await bot_system.info_check(sophia, message)

    elif message_low.startswith(system.prefix_question + 'tunnelcheck'):
        await chat_tunnel.tunnel_information(sophia, message, tunnel_info)
