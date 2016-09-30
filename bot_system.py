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

    SystemVariables.server_exclude
        [String]
        Entries of server ID excluded from having trigger commands.

    SystemVariables.previous_playing_message
        String
        Entry of previous playing message. For playing message storage when testing mode is turned on and off."""

    def __init__(self, prefix_qualifier, prefix_question, prefix_information, prefix_debug, test_mode,
            allowed_testing, atsui, server_exclude, previous_playing_message):
        self.prefix_qualifier = prefix_qualifier
        self.prefix_question = prefix_question
        self.prefix_information = prefix_information
        self.prefix_debug = prefix_debug
        self.test_mode = test_mode
        self.allowed_testing = allowed_testing
        self.ATSUI = atsui
        self.server_exclude = server_exclude
        self.previous_playing_message = previous_playing_message

async def prefix_change(system, client, message, message_low):
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
        await client.send_message(message.channel, 'Prefix change failed')
        '''await client.send_message(message.channel, 'Debug information:\n' + str(find_check_before) +
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

        await client.send_message(message.channel, 'Prefix change success')
        '''await client.send_message(message.channel, 'Debug information:\n' + str(find_check_before) +
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
