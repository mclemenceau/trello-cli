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

    # List Boards Available to user
    for board in client.list_boards():
        print(board.name)

    print("---")
    # Pick a Board (Frankfurt and print all the lanes)
    the_board = client.get_board(FRANKFURT_RETRO_2020_03)
    for lane in the_board.get_lists('all'):
        print(lane.name)

    print("---")
    # Pick a Board (The Board and print only active lanes)
    the_board_lanes = {}
    the_board = client.get_board(THE_BOARD_ID)
    for lane in the_board.get_lists('open'):
        the_board_lanes[lane.name] = lane.id
        print(lane.name)

    print(the_board_lanes)

    # Capture the board members in a dictionary
    the_board_members = {}
    for member in the_board.get_members():
        the_board_members[member.full_name] = member.id
        
        
    print("---")
    # Print all the Cards from a specific lane (In Progress)
    the_board = client.get_board(THE_BOARD_ID)
    the_board_cards = the_board.open_cards()
    for card in the_board_cards:
        if card.list_id == the_board_lanes['In Progress']:
            print (card.name)

    print("---")

    # Print all the Cards from a specific lane Assigned to Tiago
    the_board = client.get_board(THE_BOARD_ID)
    the_board_cards = the_board.open_cards()
    for card in the_board_cards:
        if card.list_id == the_board_lanes['In Progress']:
            if the_board_members['Tiago Stürmer Daitx'] in card.member_id:
                print (card.name)

    # for board in board_available.items():
    #     print(board)


    # the_board_cards = the_board.get_cards()

    # the_board_members = the_board.get_members()
   

    # Find all Cards with Member Matthieu
    # For each list
    # If list is not Archived
    # For each card
    # If Card members include Matthieu
    # Print Card

trelloCLi()