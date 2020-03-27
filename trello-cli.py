#!/usr/bin/python3
import sys
import os
import json

from trello import TrelloClient
from optparse import OptionParser

THE_BOARD_ID='hUIl3E3I'
FRANKFURT_RETRO_2020_03='63fehZ0X'

def main():
    parser = OptionParser(
        usage='Usage: %prog [options]')

    # look for the config file in ~/.trello.creds JSON
    # Should contain two keys
    #       api-key
    #       token
    default_config=os.path.expanduser('~')
    
    # TODO allow to list boards you have access to
    # TODO for a given board, list lanes (Active/Inactive/All)
    # TODO for a given board, list cards per lane/members
    # TODO only shows Cards with a given Labels
    # TODO save current preferences into a config file (prefered board)

    parser.add_option(
         '-c', dest='credentials',help='location of the trello credential json file (default ~/.trello.creds    ',
         default="{}/.trello.creds".format(default_config))
    parser.add_option(
        '-b','--list-boards', dest='show_boards',help='List all Boards available"',action='store_true')
    parser.add_option(
        '-B','--board', dest='board',help='Active Board"')
    parser.add_option(
        '-l','--list-lanes', dest='show_lanes',help='List all Lanes available"',action='store_true')
    parser.add_option(
        '-m','--list-members', dest='show_members',help='List all members available"',action='store_true')
    parser.add_option(
        '-o', dest='orphaned',help='show cards without member assigned to them',action='store_true')
    parser.add_option(
        '-s', dest='show_labels',help='show labels with cards',action='store_true')
    parser.add_option(
        '-L', dest='lanes',help='show only cards in lanes "Lane1,Lane2,Lane3"')
    parser.add_option(
        '-M', dest='member',help='filter with a specific team member', default='all')
 
    opts, args = parser.parse_args()

    try:
        with open(opts.credentials) as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print('Credentials file {} could not be parsed.'.format(opts.credentials))
        return 1

    the_boards = {}
    the_board_lanes = {}
    the_board_members = {}
    the_board_cards = []
    
    #TODO Catch error opening Trello here
    client = TrelloClient(api_key=config['api_key'],token=config['token'])

    # Get the list of boards available to current user
    for board in client.list_boards():
        the_boards[board.name] = board.id
        if opts.show_boards:
            print(board.name)
    
    # Exit after returning the board list
    if opts.show_boards: return 1
    
    #Pick the Active Board
    if opts.board:
        the_board = client.get_board(the_boards[opts.board])
    else:
        print("Active board missing, use -B \"Board Name\"")
        parser.print_help()
        return 0
    
    # Pick The Board Open Lanes
    for lane in the_board.get_lists('open'):
        if opts.show_lanes:
            print(lane.name)
        else:
            if opts.lanes:
                if lane.name in opts.lanes.split(","):
                    the_board_lanes[lane.name] = lane.id
            else:
                the_board_lanes[lane.name] = lane.id

    if opts.show_lanes: return 1

    # Capture the board members in a dictionary
    for member in the_board.get_members():
        the_board_members[member.full_name] = member.id

    if opts.show_members: 
        for name in the_board_members.keys():
            print(name)
        return 1

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
            if card_list:
                print("  {}".format(lane))
                for c in card_list:
                    card_labels = ""
                    if card.labels and opts.show_labels: card_labels = " ".join("[" +label.name+ "]" for label in card.labels)
                    if len(c.name)<70:
                        print("    * {} {}".format(card_labels,c.name))
                    else:
                        print("    * {} {}...".format(card_labels,c.name[:68]))
        print(" ")
    else:
        # Print active cards per member/lane
        for member in the_board_members:
            if poi == "all" or poi == member:
                if list(filter(lambda x: the_board_members[member] in x.member_id,the_board_cards)):
                    print(member)
                    for lane in the_board_lanes:
                        card_list = []    
                        for card in list(filter(lambda x: the_board_members[member] in x.member_id and 
                                                        x.list_id == the_board_lanes[lane],the_board_cards)):
                            card_list.append(card)
                        if card_list:
                            print("  {}".format(lane))
                            for c in card_list:
                                card_labels = ""
                                if card.labels and opts.show_labels: card_labels = " ".join("[" +label.name+ "]" for label in card.labels)
                                if len(c.name)<70:
                                    print("    * {} {}".format(card_labels,c.name))
                                else:
                                    print("    * {} {}...".format(card_labels,c.name[:68]))

                    print(" ")

if __name__ == "__main__":
    main()