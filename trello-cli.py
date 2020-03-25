import sys
import os
import json

from trello import TrelloClient

THE_BOARD_ID='hUIl3E3I'
FRANKFURT_RETRO_2020_03='63fehZ0X'

def trelloCLi():

    #TODO Use Command parser
    #TODO Set the config file in more location and use $HOME env value

    config_file = '/home/mclemenceau/.trello.creds'
    
    try:
        with open(config_file) as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print('Credentials file {} could not be parsed.'.format(config_file))
        return 1

    client = TrelloClient(api_key=config['api_key'],token=config['token'])
    the_board_lanes = {}
    the_board_members = {}
    the_board_cards = []

    # Pick The Board Open Lanes
    the_board = client.get_board(THE_BOARD_ID)
    for lane in the_board.get_lists('open'):
        the_board_lanes[lane.name] = lane.id

    # Capture the board members in a dictionary
    for member in the_board.get_members():
        the_board_members[member.full_name] = member.id
        
    # Capture all the cards from active lane into a dictionary
    for card in the_board.open_cards():
        if card.list_id in the_board_lanes.values():
            the_board_cards.append(card)

    # Print active cards per member/lane
    for member in the_board_members:
        if len(list(filter(lambda x: the_board_members[member] in x.member_id,the_board_cards)))>0:
            print(" ")
            print(member)
            for lane in the_board_lanes:
                card_list = []    
                for card in list(filter(lambda x: the_board_members[member] in x.member_id and 
                                                x.list_id == the_board_lanes[lane],the_board_cards)):
                    card_list.append(card)
                if len(card_list) > 0:
                    print("  {}".format(lane))
                    for c in card_list:
                        print("    * {}".format(c.name))

trelloCLi()