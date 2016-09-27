# coding=utf-8

async def room_create(client, message, message_low, minigame_session, table_limits):
    find_qualifier = ' '
    find_room_id = message_low.find(find_qualifier, 0)

    await client.send_message(message.channel, 'Room created.')

async def room_check(client, message, message_low, table_limits, minigame_session, room_status):
    find_qualifier = ' '
    find_room_id = message_low.find(find_qualifier, 0)
    room_id = message_low[find_room_id + 1:]
    loop_limit = len(minigame_session[int(room_id)])
    loop_count = 4
    game_name = table_limits[0].index(minigame_session[int(room_id)][1])
    is_password = False

    if minigame_session[int(room_id)][1] is not None and minigame_session[int(room_id)][1] != '':
        is_password = True

    await client.send_message(message.channel, 'yes')

    room_information = '`Room Name`: ' + minigame_session[int(room_id)][0] + \
        ' `Password`: ' + str(is_password) + '\n' + \
        '`ID`: ' + str(room_id) + '\n' + \
        '`Status`: ' + str(room_status[int(minigame_session[int(room_id)][3])]) + '\n' + \
        '`Minigame`: ' + str(minigame_session[int(room_id)][1]) + \
        ' `Player`: ' + str(loop_limit - 4) + ' / ' + str(table_limits[1][game_name]) + \
        '\n' + '`Player List`: \n'

    while loop_count != loop_limit:
        if loop_count != loop_limit - 1:
            room_information += str(minigame_session[int(room_id)][loop_count]) + ', '
        else:
            room_information += str(minigame_session[int(room_id)][loop_count])
        loop_count += 1

    await client.send_message(message.channel, room_information)

async def room_join(client, message, message_low, table_limits, minigame_session, player_joined):
    find_qualifier = ' '
    find_room_id = message_low.find(find_qualifier, 0)
    find_room_password = message_low.find(find_qualifier, find_room_id + 1)
    room_id = message_low[find_room_id + 1: find_room_id + 2]
    room_player_count = len(minigame_session[int(room_id)]) - 3
    game_name = table_limits[0].index(minigame_session[int(room_id)][1])
    roomcapacity = table_limits[1][game_name]
    is_allowed = True

    if minigame_session[int(room_id)][1] is not None and minigame_session[int(room_id)][2] != '':
        # await client.send_message(message.channel, "Password exists")
        if find_room_password is not -1:
            # await client.send_message(message.channel, "User enters a password")
            if message.content[find_room_password + 1:] != minigame_session[int(room_id)][2]:
                # await client.send_message(message.channel, \
                # "Password does not match with the room password")
                is_allowed = False
        else:
            # await client.send_message(message.channel, "User dun goofed")
            is_allowed = False
    '''await client.send_message(message.channel, message.content[find_room_password + 1:] +
        str(len(message.content[find_room_password + 1:])) + '\n' +
        minigame_session[int(room_id)][2] + str(len(minigame_session[int(room_id)][2])))'''

    if is_allowed:
        if room_player_count <= roomcapacity:
            if message.author not in player_joined:
                await client.send_message(message.channel, 'yes')
                minigame_session[int(room_id)].append(message.author)
                player_joined.append(message.author)
                await client.send_message(message.channel, 'You are now in room ' + str(room_id) + '.')

            else:
                await client.send_message(message.channel, 'no')
                await client.send_message(message.channel, 'Unable to join since you are in a room.')
        else:
            await client.send_message(message.channel, 'Unable to join since the room is full.')
    else:
        await client.send_message(message.channel, "Invalid room ID or room password.")
