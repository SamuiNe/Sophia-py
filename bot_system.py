# coding=utf-8

async def prefix_change(client, message, message_low):
    process_index = [0, None, None, None, None, None]
    temp_collection = ['<', None, None, None, None]
    exception_check = False
    find_qualifier = ' '
    # find_check_before = 0
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
        prefix_qualifier = temp_collection[0]
        prefix_question = temp_collection[1]
        prefix_information = temp_collection[2]
        prefix_debug = temp_collection[3]

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
