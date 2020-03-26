#!/usr/bin/python3
import sys
import os
import json

from trello import TrelloClient
from optparse import OptionParser

THE_BOARD_ID='hUIl3E3I'
FRANKFURT_RETRO_2020_03='63fehZ0X'

def main():


    # config_file = '/home/mclemenceau/.trello.creds'
    
    parser = OptionParser(
        usage='Usage: %prog [options]')

    #TODO Set the config file in more location and use $HOME env value
    default_config=os.path.expanduser('~')
    parser.add_option(
         '-c', dest='credentials',help='location of the trello credential json file',
         default="{}/.trello.creds".format(default_config))
    parser.add_option(
        '-m', dest='member',help='filter with a specific team member', default='all')
    parser.add_option(
        '-o', dest='orphaned',help='show cards without member assigned to them',action='store_true')

    opts, args = parser.parse_args()

    try:
        with open(opts.credentials) as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print('Credentials file {} could not be parsed.'.format(opts.credentials))
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
    
    poi=opts.member
    if len(poi) > 0 and poi != 'all':
        for name in the_board_members.keys():
            if poi in name:
                poi = name
                break   

    # Capture all the cards from active lane into a dictionary
    for card in the_board.open_cards():
        if card.list_id in the_board_lanes.values():
            the_board_cards.append(card)

    # Show Cards without Owner
    if opts.orphaned:
        for lane in the_board_lanes:
            card_list = []    
            for card in list(filter(lambda x: len(x.member_id) == 0 and 
                                            x.list_id == the_board_lanes[lane],the_board_cards)):
                card_list.append(card)
            if len(card_list) > 0:
                print("  {}".format(lane))
                for c in card_list:
                    print("    * {}".format(c.name))
        print(" ")
    else:
        # Print active cards per member/lane
        for member in the_board_members:
            if poi == "all" or poi == member:
                if len(list(filter(lambda x: the_board_members[member] in x.member_id,the_board_cards)))>0:
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
                    print(" ")

if __name__ == "__main__":
    main()