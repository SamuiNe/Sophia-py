# coding=utf-8
"""Text encoding UTF-8"""

class SystemVariables:
    """SystemVariables(String, String, String, String, Boolean, [String], (String), [String], String)
    Class for constructing required system variables for the bot.

    SystemVariables.prefix_qualifier
        String
        Command qualifier. Intended to be the first character of all command prefix.

    SystemVariables.prefix_question
        String
        Command prefix for question related commands.

    SystemVariables.prefix_information
        String
        Command prefix for information related commands.

    SystemVariables.prefix_debug
        String
        Command prefix for debug related commands.

    SystemVariables.test_mode
        Boolean
        Determines if the bot will start in test mode or not.

    SystemVariables.allowed_testing
        [String]
        Entries of server ID allowed when test mode is enabled.

    SystemVariables.ATSUI
        (String)
        Entries of client ID allowed for debug prefix commands.

    SystemVariables.trigger_include
        [String]
        Entries of server ID excluded from having trigger commands.

    SystemVariables.previous_playing_message
        String
        Entry of previous playing message. For playing message storage when testing mode is turned on and off."""

    def __init__(self, prefix_qualifier, prefix_question, prefix_information, prefix_debug, test_mode,
            allowed_testing, atsui, trigger_include, previous_playing_message, forbidden_eval,
            token_status, custom_filename_status, custom_filename_path, eval_error_message):
        self.prefix_qualifier = prefix_qualifier
        self.prefix_question = prefix_question
        self.prefix_information = prefix_information
        self.prefix_debug = prefix_debug
        self.test_mode = test_mode
        self.allowed_testing = allowed_testing
        self.ATSUI = atsui
        self.trigger_include = trigger_include
        self.previous_playing_message = previous_playing_message
        self.forbidden_eval = forbidden_eval
        self.token_status = token_status
        self.custom_filename_status = custom_filename_status
        self.custom_filename_path = custom_filename_path
        self.eval_error_message = eval_error_message
        self.eval_error_length = len(eval_error_message)

async def command_help(system, sophia, message):
    trigger_status = True
    if message.server.id in system.trigger_include:
        trigger_status = False

    if trigger_status:
        await sophia.send_message(message.channel, 'Here are the commands I recognize at the moment:\n\n' +
            'Question commands (starts with `' + system.prefix_question + '`)\n' +
            '`about`, `help`, `command`, `botversion`, `infocheck`, `tunnelcheck`\n\n' +
            'Information commands (starts with `' + system.prefix_information + '`)\n' +
            '`tunnellink`, `tunnelenable`, `tunnelmode`, `tunnelleave`, `tunnelcreate`, `tunneldelete`\n'+
            '`hello`, `invite`, `ping` (`pong`),' + '`triggertoggle`\n\n' +
            'Trigger commands\n' +
            ':coffee:, :tea:, `cawfee`, `gween tea`, ' +
            '`\u0028\u256f\u00b0\u25a1\u00b0\uff09\u256f\ufe35 \u253b\u2501\u253b`, ' +
            '`\u252c\u2500\u252c\ufeff \u30ce\u0028 \u309c\u002d\u309c\u30ce\u0029`\n' +
            '...with 14 secret commands! \n\n' +
            'For information of individual commands, please enter `' + system.prefix_question +
            'command `*`command`*.')
    else:
        await sophia.send_message(message.channel, 'Here are the commands I recognize at the moment:\n\n' +
            'Question commands (starts with `' + system.prefix_question + '`)\n' +
            '`about`, `help`, `command`, `botversion`, `infocheck`, `tunnelcheck`\n\n' +
            'Information commands (starts with `' + system.prefix_information + '`)\n' +
            '`tunnellink`, `tunnelenable`, `tunnelmode`, `tunnelleave`, `tunnelcreate`, `tunneldelete`\n'+
            '`hello`, `invite`, `ping` (`pong`),' + '`triggertoggle`\n' +
            '...with 14 secret commands! \n\n' +
            'For information of individual commands, please enter `' + system.prefix_question +
            'command `*`command`*.')

async def individual_command_help(system, sophia, message):
    message_qualifier = ' '
    space_position = message.content.find(message_qualifier, 0)

    if space_position != -1:
        message_content = message.content[space_position + 1:]

        if message_content == 'about':
            await sophia.send_message(message.channel, 'Category: Question\n' +
                'Command format: `' + system.prefix_question + 'about`\n\n' +
                'Allows Sophia to greet herself.')

        elif message_content == 'help':
            await sophia.send_message(message.channel, 'Category: Question\n' +
                'Command format: `' + system.prefix_question + 'help`\n\n' +
                'Displays current command list and current amount of secret commands.')

        elif message_content == 'command':
            await sophia.send_message(message.channel, 'Category: Question\n' +
                'Command format: `' + system.prefix_question + 'command `*`command`*\n\n' +
                'Displays detailed help information for individual command.')

        elif message_content == 'botversion':
            await sophia.send_message(message.channel, 'Category: Question\n' +
                'Command format: `' + system.prefix_question + 'botversion`\n\n' +
                'Displays the bot\'s current bot version and last update date.')

        elif message_content == 'infocheck':
            await sophia.send_message(message.channel, 'Category: Question\n' +
                'Command format: `' + system.prefix_question + 'infocheck`\n\n' +
                'Displays the author\'s current discord name, discrim number and ID.\n' +
                'Also displays server ID and channel ID.')

        elif message_content == 'tunnelcheck':
            await sophia.send_message(message.channel, 'Category: Question\n' +
                'Command format: `' + system.prefix_question + 'tunnelcheck `*`tunnel_id`*\n\n' +
                'Displays the tunnel information for the specified tunnel ID.')

        elif message_content == 'roomcheck':
            await sophia.send_message(message.channel, 'Category: Question\n' +
                'Command format: `' + system.prefix_question + 'roomcheck `*`room_id`*\n\n' +
                'Displays the room information for the specified room ID.')

        elif message_content == 'tunnellink':
            await sophia.send_message(message.channel, 'Category: Information\n' +
                'Command format: `' + system.prefix_information + 'tunnellink `*`room_id room_password`*\n' +
                'Required user permission(s): *Administrator* or *Manage Server* or *Manage Channel*.\n\n'+
                'Links the current channel to a tunnel room.')

        elif message_content == 'tunnelenable':
            await sophia.send_message(message.channel, 'Category: Information\n' +
                'Command format: `' + system.prefix_information +
                'tunnelenable `*`room_id option room_password`* \n' +
                'Required user permission(s): *Administrator* or *Manage Server* or *Manage Channel*.\n' +
                'Note: Requires tunnel room manager (currently first channel in the tunnel room list).\n\n' +
                'Toggles the current room\'s tunnel enable option.')

        elif message_content == 'tunnelmode':
            await sophia.send_message(message.channel, 'Category: Information\n' +
                'Command format: `' + system.prefix_information + 'tunnelmode `*`option`* \n' +
                'Required user permission(s): *Administrator* or *Manage Server* or *Manage Channel*.\n' +
                'Available option(s):\n' +
                '`3` or `all` - Sets the channel to both send and receive messages.\n' +
                '`2` or `receive` - Sets the channel to only receive messages.\n' +
                '`1` or `send` - Sets the channel to only send messages.\n' +
                '`0` or `none` - Sets the channel to not receive nor send any messages.\n\n'
                'Changes the current tunnel mode.')

        elif message_content == 'tunnelleave':
            await sophia.send_message(message.channel, 'Category: Information\n' +
                'Command format: `' + system.prefix_information + 'tunnelleave `*`room_password`* \n' +
                'Required user permission(s): *Administrator* or *Manage Server* or *Manage Channel*.\n\n' +
                'Leave the current tunnel room.')

        elif message_content == 'tunnelcreate':
            await sophia.send_message(message.channel, 'Category: Information\n' +
                'Command format: `' + system.prefix_information + 'tunnelcreate `*`room_name room_password`*\n'
                'Note: *`room_password`* is optional. Room ID is autogenerated.\n\n' +
                'Creates a tunnel room with user specified room name.')

        elif message_content == 'tunneldelete':
            await sophia.send_message(message.channel, 'Category: Information\n' +
                'Command format: `' + system.prefix_information + 'tunneldelete `*`room_password`*\n' +
                'Required user permission(s): *Administrator* or *Manage Server* or *Manage Channel*.\n\n' +
                'Note: Requires tunnel room manager (currently first channel in the tunnel room list).\n\n'
                'Deletes a tunnel room.')

        elif message_content == 'hello':
            await sophia.send_message(message.channel, 'Category: Information\n' +
                'Command format: `' + system.prefix_information + 'hello`\n\n' +
                'Allows Sophia to say hello to the user.')

        elif message_content == 'invite':
            await sophia.send_message(message.channel, 'Category: Information\n' +
                'Command format: `' + system.prefix_information + 'invite`\n\n' +
                'Displays Sophia\'s invite link and server link.')

        elif message_content == 'ping' or message_content == 'pong':
            await sophia.send_message(message.channel, 'Category: Information\n' +
                'Command format: `' + system.prefix_information + 'ping` or `' +
                system.prefix_information + 'pong`\n\n' +
                'Ping! Pong!')

        elif message_content == 'roomcreate':
            await sophia.send_message(message.channel, 'Category: ???\n' +
                'Command format: `' + system.prefix_information + 'roomcreate `*`room_name room_password`*\n\n' +
                'Creates a minigame room.')

        elif message_content == 'roomjoin':
            await sophia.send_message(message.channel, 'Category: ???\n' +
                'Command format: `' + system.prefix_information + 'roomjoin `*`room_id room_password`*\n\n' +
                'Join a minigame room.')

        elif message_content == 'roomcheck':
            await sophia.send_message(message.channel, 'Category: ???\n' +
                'Command format: `' + system.prefix_information + 'roomcheck `*`room_id`*\n\n' +
                'Check room information for the specified room ID.')

        elif message_content == 'triggertoggle':
            await sophia.send_message(message.channel, 'Category: Information\n' +
                'Command format: `' + system.prefix_information + 'triggertoggle `*`room_id`*\n'
                'Required user permission(s): *Administrator* or *Manage Server* or *Manage Channel*.\n' +
                'Note: This toggle is server wide.\n\n' +
                'Toggles trigger command.')

        elif message_content == 'sara' or message_content == 'sarachan':
            await sophia.send_message(message.channel, 'Category: ???\n' +
                'Command format: `' + system.prefix_information + 'sara` or `' +
                system.prefix_information + 'sarachan`\n\n' +
                'Be-Music Source (BMS) meme. You have found a secret!')

        else:
            await sophia.send_message(message.channel, 'The command you have specified is invalid or missing ' +
                'help informations.')

    else:
        await sophia.send_message(message.channel, 'Unable to show command help since the command you want is ' +
            'not specified.\n' +
            'Usage: `' + system.prefix_question + 'command `*`command`*')

async def info_check(sophia, message):
    await sophia.send_message(message.channel, '`Author`: ' + str(message.author) +
        ' `' + str(message.author.id) + '`\n' +
        # '`Bot`: ' + str(message.author.bot) + '\n' +
        # '`MessLen`: ' + str(len(message.content)) + '\n' +
        '`Channel`: ' + str(message.channel) + ' `' + str(message.channel.id) + '`\n' +
        '`Server`: ' + str(message.server.name) + ' `' + str(message.server.id) + '`')

async def server_invite(sophia, message):
    await sophia.send_message(message.channel,
        'You can take me to your discord server by clicking the link below.' + '\n' +
        'https://discordapp.com/oauth2/authorize?client_id=229134725569183745&scope=bot&permissions=0' + '\n\n' +
        'Interested in joining my discord guild? You can visit it by using the invite link below!' + '\n' +
        'https://discord.gg/SpTWKDd')

async def testing_mode(system, discord, sophia, message, message_low):
    message_qualifier = ' '
    message_start = message_low.find(message_qualifier, 0)
    testing_mode_parameter = str(message_low)[message_start + 1:]
    # await sophia.send_message(message.channel, testing_mode_parameter)

    if testing_mode_parameter == 'yes' or testing_mode_parameter == '1':
        system.test_mode = True

        await sophia.change_presence(game=discord.Game(name='\u26A0 TEST MODE \u26A0'))
        await sophia.send_message(message.channel, 'Testing mode enabled')

    elif testing_mode_parameter == 'no' or testing_mode_parameter == '0':
        system.test_mode = False

        await sophia.change_presence(game=discord.Game(name=system.previous_playing_message))
        await sophia.send_message(message.channel, 'Testing mode disabled')

async def prefix_change(system, sophia, message, message_low):
    """Changes the bot's prefix.

    This command alters the following variables:
        SystemVariables.prefix_qualifier
        SystemVariables.prefix_question
        SystemVariables.prefix_information
        SystemVariables.prefix_debug"""
    process_index = [0, None, None, None, None, None]
    temp_collection = ['<', None, None, None, None]
    exception_check = False
    find_qualifier = ' '
    find_check_after = 0
    find_count = 0
    process_count = 1
    temp_counter = 0
    exception_counter = 0

    while find_check_after != -1 and find_count != 5:
        find_check_before = find_check_after
        find_check_after = message_low.find(find_qualifier, find_check_before + 1)

        if find_check_after != -1:
            find_count += 1
            process_index[find_count] = find_check_after

    while process_index[process_count] is not None and process_count != 5:
        if process_count == 4:
            temp_collection[temp_counter] = message_low[process_index[process_count] + 1:]
        else:
            temp_collection[temp_counter] = message_low[process_index[process_count] + 1:
                    process_index[process_count + 1]]

        temp_counter += 1
        process_count += 1

    if temp_collection[exception_counter] is not None and \
            temp_collection[exception_counter + 1] is not None:

        while temp_collection[exception_counter] is not None and exception_counter != 4:

            if temp_collection[0] not in temp_collection[exception_counter]:
                exception_check = True
            exception_counter += 1

    if exception_check:
        await sophia.send_message(message.channel, 'Prefix change failed')
        '''Debug code

        await sophia.send_message(message.channel, 'Debug information:\n' + str(find_check_before) +
            ' ' + str(find_check_after) + ' ' + str(find_count) + ' ' + str(process_count) + ' ' +
            str(temp_counter) + ' ' + str(exception_counter) + '\n' +
            str(exception_check) + '\n' +
            '> ' + str(process_index[0]) + ' ' + str(process_index[1]) + ' ' +
            str(process_index[2]) + ' ' + str(process_index[3]) + ' ' +
            str(process_index[4]) + ' ' + str(process_index[5]) + '\n' +
            '>> ' + str(temp_collection[0]) + ' ' + str(temp_collection[1]) + ' ' +
            str(temp_collection[2]) + ' ' + str(temp_collection[3]) + '\n' +
            'L> ' + str(len(str(temp_collection[0]))) + ', ' + str(len(str(temp_collection[1]))) +
            ', ' + str(len(str(temp_collection[2]))) + ', ' + str(len(str(temp_collection[3]))))
        '''

    else:
        system.prefix_qualifier = temp_collection[0]
        system.prefix_question = temp_collection[1]
        system.prefix_information = temp_collection[2]
        system.prefix_debug = temp_collection[3]

        await sophia.send_message(message.channel, 'Prefix change success')
        '''Debug code

        await sophia.send_message(message.channel, 'Debug information:\n' + str(find_check_before) +
            ' ' + str(find_check_after) + ' ' + str(find_count) + ' ' + str(process_count) + ' ' +
            str(temp_counter) + ' ' + str(exception_counter) + '\n' +
            str(exception_check) + '\n' +
            '> ' + str(process_index[0]) + ' ' + str(process_index[1]) + ' ' +
            str(process_index[2]) + ' ' + str(process_index[3]) + ' ' +
            str(process_index[4]) + ' ' + str(process_index[5]) + '\n' +
            '>> ' + str(temp_collection[0]) + ' ' + str(temp_collection[1]) + ' ' +
            str(temp_collection[2]) + ' ' + str(temp_collection[3]) + '\n' +
            'L> ' + str(len(str(temp_collection[0]))) + ', ' + str(len(str(temp_collection[1]))) +
            ', ' + str(len(str(temp_collection[2]))) + ', ' + str(len(str(temp_collection[3]))))
        '''

async def change_name(sophia, message):
    find_qualifier = ' '
    name_position = message.content.find(find_qualifier, 0)
    name_change = message.content[name_position + 1:]
    # await sophia.send_message(message.channel, str(len(username)) + username)
    await sophia.edit_profile(password='', username=name_change)
    await sophia.send_message(message.channel, 'Bot name has successfully changed.')

async def change_avatar(sophia, message):
    find_qualifier = ' '
    filename_position = message.content.find(find_qualifier, 0)
    filename_change = message.content[filename_position + 1:] + '.png'

    await sophia.send_message(message.channel, filename_change)

    file_point = open(filename_change, 'rb')
    processed_file = file_point.read()

    try:
        await sophia.edit_profile(password='', avatar=processed_file)
    except 'InvalidArgument':
        await sophia.send_message(message.channel, 'Avatar change failed due to missing or bad image file.')
    else:
        await sophia.send_message(message.channel, 'Bot avatar has successfully changed.')


async def trigger_toggle(system, sophia, message, message_low, permission):
    find_qualifier = ' '
    option_position = message.content.find(find_qualifier, 0)

    if permission:
        if find_qualifier != -1:
            option_message = message_low[option_position + 1:]

            if option_message == 'disable' or option_message == 'no' or option_message == '0':
                if message.server.id in system.trigger_include:
                    await sophia.send_message(message.channel, 'The trigger command has already ' +
                        'been disabled for this server.')
                else:
                    system.trigger_include.append(message.server.id)
                    await sophia.send_message(message.channel, 'Trigger command is now disabled for this server.')

            elif option_message == 'enable' or option_message == 'yes' or option_message == '1':
                if message.server.id in system.trigger_include:
                    system.trigger_include.remove(message.server.id)
                    await sophia.send_message(message.channel, 'Trigger command is now enabled for this server.')
                else:
                    await sophia.send_message(message.channel, 'The trigger command has already ' +
                        'been enabled for this server.')

            else:
                await sophia.send_message(message.channel, 'Unable to change trigger command settings ' +
                    'due to invalid option.')

        else:
            await sophia.send_message(message.channel,
                'Unable to change trigger command settings due to missing option.')
    else:
        await sophia.send_message(message.channel,
            'Unable to change trigger command since you do not have sufficient role permissions.')
