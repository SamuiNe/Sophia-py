# coding=utf-8
import string

# TODO: Create room settings command
# TODO: Add ability to remove room
# TODO: Add ability to leave from room


class RoomInformations:
    """RoomInformations([String], [[String], [Int]], (String), [[String]])
    Class for constructing player and server data for minigame rooms related commands.

    RoomInformations.player_joined
        [String]
        Lists of player joined at a room.

    RoomInformations.table_limits
        [[String], [Int]]
        Lists current available game and its player limit.

    RoomInformations.room_status
        (String)
        Lists of room statuses.

    RoomInformations.minigame_session
        [[String]]
        Index 0 through 4 are reserved for room information, and stores player data from index 5 and on."""

    def __init__(self, player_joined, table_limits, room_status, minigame_session):
        self.player_joined = player_joined
        self.table_limits = table_limits
        self.room_status = room_status
        self.minigame_session = minigame_session

# minigame_session = [['Testing room', 'Blackjack', 'Testing', '0']]
# table_limits = [['Blackjack'], [6]]
async def room_create(system, room_info, client, message, message_low):
    """Creates a room for players to join and play minigame.

    Syntax: (System.prefix_information + roomcreate) <Room Name> <Game Name> <Password (Optional)>

    This command alters the following variables:
        RoomInformations.minigame_session
        RoomInformations.table_limits"""

    find_qualifier = ' '
    find_room_game = [0, None, None, None, None]
    message_element = ['placeholder', None, None, '0']
    seperator_counter = 1
    element_counter = 0
    room_count = len(room_info.minigame_session)

    while seperator_counter != 5:
        find_room_game[seperator_counter] = message_low.find(find_qualifier, find_room_game[seperator_counter - 1] + 1)
        seperator_counter += 1

    while element_counter != 3:
        if element_counter == 2:
            if find_room_game[element_counter] != -1 and find_room_game[element_counter + 1] != -1:
                message_element[element_counter] = message.content[find_room_game[element_counter + 1] + 1:]
        elif element_counter == 1 and find_room_game[element_counter + 2] == -1:
                message_element[element_counter] = message.content[find_room_game[element_counter + 1] + 1:]
        else:
            message_element[element_counter] = message.content[find_room_game[element_counter + 1] + 1:
                find_room_game[element_counter + 2]]
        element_counter += 1

    message_element[1] = string.capwords(str(message_element[1]))

    # await client.send_message(message.channel, str(find_room_game) + '\n' +
    #   str(message_element) + '\n' +
    #   str(room_info.table_limits[0]) + '\n' +
    #   str(room_count))

    if message_element[1] in room_info.table_limits[0]:
        room_info.minigame_session.append(message_element)
        # await client.send_message(message.channel, str(room_info.minigame_session[room_count]))
        await client.send_message(message.channel, 'Room has successfully created.\n' +
            'Your room ID is ' + str(room_count) + '.')

    else:
        await client.send_message(message.channel, 'Game type is not found.' + '\n' +
            'Please format your message as ' + str(system.prefix_information) + 'roomcreate' +
            ' `Room name` `Game name` `Room Password`')


async def room_check(room_info, client, message, message_low):
    """Checks the current room information.

    Syntax: (System.prefix_information + roomcheck) <Room ID>"""
    find_qualifier = ' '
    find_room_id = message_low.find(find_qualifier, 0)
    room_id = message_low[find_room_id + 1:]
    loop_limit = len(room_info.minigame_session[int(room_id)])
    loop_count = 4
    game_name = room_info.table_limits[0].index(room_info.minigame_session[int(room_id)][1])
    is_password = False

    if room_info.minigame_session[int(room_id)][2] is not None:
        is_password = True

    await client.send_message(message.channel, 'yes')

    room_information = '`Room Name`: ' + room_info.minigame_session[int(room_id)][0] + \
        ' `Password`: ' + str(is_password) + '\n' + \
        '`ID`: ' + str(room_id) + '\n' + \
        '`Status`: ' + str(room_info.room_status[int(room_info.minigame_session[int(room_id)][3])]) + '\n' + \
        '`Minigame`: ' + str(room_info.minigame_session[int(room_id)][1]) + \
        ' `Player`: ' + str(loop_limit - 4) + ' / ' + str(room_info.table_limits[1][game_name]) + \
        '\n' + '`Player List`: \n'

    while loop_count != loop_limit:
        if loop_count != loop_limit - 1:
            room_information += str(room_info.minigame_session[int(room_id)][loop_count]) + ', '
        else:
            room_information += str(room_info.minigame_session[int(room_id)][loop_count])
        loop_count += 1

    await client.send_message(message.channel, room_information)

async def room_join(room_info, client, message, message_low):
    """Allows the player to join a room, provided that the player has not yet joined a room.

    Syntax: (System.prefix_information + roomjoin) <Room ID> <Password(Maybe optional)>

    This command alters the following variables:
        RoomInformations.minigame_session Index 5+
        RoomInformations.player_joined"""
    find_qualifier = ' '
    find_room_id = message_low.find(find_qualifier, 0)
    find_room_password = message_low.find(find_qualifier, find_room_id + 1)
    room_id = message_low[find_room_id + 1: find_room_id + 2]
    room_player_count = len(room_info.minigame_session[int(room_id)]) - 3
    game_name = room_info.table_limits[0].index(room_info.minigame_session[int(room_id)][1])
    roomcapacity = room_info.table_limits[1][game_name]
    is_allowed = True

    if room_info.minigame_session[int(room_id)][1] is not None and \
            room_info.minigame_session[int(room_id)][2] is not None:
        # await client.send_message(message.channel, "Password exists")
        if find_room_password is not -1:
            # await client.send_message(message.channel, "User enters a password")
            if message.content[find_room_password + 1:] != room_info.minigame_session[int(room_id)][2]:
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
            if message.author not in room_info.player_joined:
                # await client.send_message(message.channel, 'yes')
                room_info.minigame_session[int(room_id)].append(message.author)
                room_info.player_joined.append(message.author)
                await client.send_message(message.channel, 'You are now in room ' + str(room_id) + '.')

            else:
                # await client.send_message(message.channel, 'no')
                await client.send_message(message.channel, 'Unable to join since you are in a room.')
        else:
            await client.send_message(message.channel, 'Unable to join since the room is full.')
    else:
        await client.send_message(message.channel, "Invalid room ID or room password.")

# async def room_leave(client, message, message_low, minigame_session, player_joined):
