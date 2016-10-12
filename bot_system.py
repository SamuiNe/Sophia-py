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

    SystemVariables.trigger_exclude
        [String]
        Entries of server ID excluded from having trigger commands.

    SystemVariables.previous_playing_message
        String
        Entry of previous playing message. For playing message storage when testing mode is turned on and off."""

    def __init__(self, prefix_qualifier, prefix_question, prefix_information, prefix_debug, test_mode,
            allowed_testing, atsui, trigger_exclude, previous_playing_message):
        self.prefix_qualifier = prefix_qualifier
        self.prefix_question = prefix_question
        self.prefix_information = prefix_information
        self.prefix_debug = prefix_debug
        self.test_mode = test_mode
        self.allowed_testing = allowed_testing
        self.ATSUI = atsui
        self.trigger_exclude = trigger_exclude
        self.previous_playing_message = previous_playing_message

async def command_help(system, sophia, message):
    trigger_status = 'Enabled'
    if message.server.id in system.trigger_exclude:
        trigger_status = 'Disabled'

    await sophia.send_message(message.channel, 'Here are the commands I recognize at the moment:\n\n' +
        '*Question commands* (starts with `' + system.prefix_question + '`)\n' +
        '`about`, `help` (`commands`), `botversion`, `infocheck`, `tunnelcheck`, `roomcheck`\n\n' +
        '*Information commands* (starts with `' + system.prefix_information + '`)\n' +
        '`tunnellink`, `tunnelenable`, `tunnelleave`, `tunnelcreate`, `delete`'+
        '`hello`, `sara` (`sarachan`), `invite`, `ping` (`pong`),' +
        ' `roomcreate`, `roomjoin`, `roomcheck`\n\n' +
        '*Trigger commands* ' + trigger_status + '\n' +
        ':coffee:, :tea:, `cawfee`, `gween tea`, ' +
        '`\u0028\u256f\u00b0\u25a1\u00b0\uff09\u256f\ufe35 \u253b\u2501\u253b`, ' +
        '`\u252c\u2500\u252c\ufeff \u30ce\u0028 \u309c\u002d\u309c\u30ce\u0029`\n' +
        '...with 11 secret commands!')

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
            temp_collection[temp_counter] = message_low[(process_index[process_count] + 1):]
        else:
            temp_collection[temp_counter] = message_low[process_index[process_count] + 1:
            process_index[process_count + 1]]

        temp_counter += 1
        process_count += 1
    ''' Old Code
    if process_index[2] is not None:
        tempqualifier = message_low[process_index[1] + 1: \
            (process_index[2] - process_index[1]) - 2]

    if process_index[3] is not None:
        tempquestion = message_low[process_index[2] + 1: \
            (process_index[3] - process_index[2]) - 2]

    if process_index[4] is not None:
        tempinformation = message_low[process_index[3] + 1: \
            (process_index[4] - process_index[3]) - 2]

    if process_index[5] is not None:
        tempdebug = message_low[process_index[4] + 1: \
            (process_index[5] - process_index[4]) - 2]
    '''

    if temp_collection[exception_counter] is not None and \
            temp_collection[exception_counter + 1] is not None:

        while temp_collection[exception_counter] is not None and exception_counter != 4:

            if temp_collection[0] not in temp_collection[exception_counter]:
                exception_check = True
            exception_counter += 1
    ''' Old code
    if tempqualifier is not None and tempquestion is not None:
        if tempquestion is not None and not tempquestion.startswith(tempqualifier):
            exception_check = True

        if tempinformation is not None and not tempinformation.startswith(tempqualifier):
            exception_check = True

        if tempdebug is not None and not tempinformation.startswith(tempqualifier):
            exception_check = True
    '''

    if exception_check:
        await sophia.send_message(message.channel, 'Prefix change failed')
        '''await sophia.send_message(message.channel, 'Debug information:\n' + str(find_check_before) +
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
    await sophia.send_message(message.channel, 'Bot name successfully changed')

async def trigger_exception(system, sophia, message, message_low):
    find_qualifier = ' '
    option_position = message.content.find(find_qualifier, 0)

    if find_qualifier != -1:
        option_message = message_low[option_position + 1:]

        if option_message == 'yes' or option_message == '1':
            if message.server.id in system.trigger_exclude:
                await sophia.send_message(message.channel, 'The trigger command has already' +
                    'been disabled for this server.')
            else:
                system.trigger_exclude.append(message.server.id)
                await sophia.send_message(message.channel, 'Trigger command is now disabled for this server.')

        elif option_message == 'no' or option_message == '0':
            if message.server.id in system.trigger_exclude:
                system.trigger_exclude.remove(message.server.id)
                await sophia.send_message(message.channel, 'Trigger command is now enabled for this server.')
            else:
                await sophia.send_message(message.channel, 'The trigger command has already' +
                    'been disabled for this server.')

        else:
            await sophia.send_message(message.channel, 'Unable to change trigger command settings' +
                'due to invalid option.')

    else:
        await sophia.send_message(message.channel, 'Unable to change trigger command settings due to missing option.')
