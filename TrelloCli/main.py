#!/usr/bin/python3
import sys
import os
import json
import getpass

from trello import TrelloClient
from optparse import OptionParser

def drawCards(cardList,label=False):
    if cardList:
        for card in cardList:
            card_labels = ""
            if card.labels and label: card_labels = " ".join("[" +label.name+ "]" for label in card.labels)
            if len(card.name)<70:
                print("    * {} {}".format(card_labels,card.name))
            else:
                print("    * {} {}...".format(card_labels,card.name[:68]))

# Test if any subtring from the listNames is in the Name
# For example   listNames = "bob,brian,mat"
#               Name = matthias
#               True
# There has to be a better way to test this in Python ...
def listInString(listNames,Name):
    if listNames.split(","):
        for s in listNames.split(","):
            if s in Name:
                return True
    return False


def main():
    parser = OptionParser(
        usage='Usage: %prog [options]')

    # look for the config file in ~/.trello.creds JSON
    # Should contain two keys
    #       api-key
    #       token
    default_config=os.path.expanduser('~')
    
    # TODO only shows Cards with a given Labels
    # TODO save current preferences into a config file (prefered board)
    # TODO build unit testing
    
    parser.add_option(
         '-c', dest='credentials',help='location of the trello credential json file (default ~/.trello.creds    ',
         default="{}/.trello.creds".format(default_config))
    parser.add_option(
        '-b','--list-boards', dest='show_boards',help='List all Boards available"',action='store_true')
    parser.add_option(
        '-B'    , dest='board',help='Active Board')
    parser.add_option(
        '-l','--list-lanes', dest='show_lanes',help='List all Lanes available"',action='store_true')
    parser.add_option(
        '-L', dest='lanes',help='show only cards in lanes "Lane1,Lane2,Lane3"')
    parser.add_option(
        '-m','--list-members', dest='show_members',help='List all members available"',action='store_true')
    parser.add_option(
        '-s', dest='show_labels',help='show labels with cards',action='store_true')
    parser.add_option(
        '-M', dest='members',help='filter with a specific team member (Names: coma separated list of names bob,sam,Luk all: display everyone, none: display unassigned cards)')
 
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
    
    # Capture the board members in a dictionary
    for member in the_board.get_members():
        the_board_members[member.full_name] = member.id

    if opts.show_members: 
        for name in the_board_members.keys():
            print(name)
        return 1

    if not opts.show_lanes and not opts.lanes:
        print("Missing lanes information")
        parser.print_help()
        return 1

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

    # Capture all the cards from active lane into a dictionary
    for card in the_board.open_cards():
        if card.list_id in the_board_lanes.values():
            the_board_cards.append(card)
   

    # Simply show all the cards from said Lanes if no member selected 
    if not opts.members:
        for lane in the_board_lanes:
            if the_board_cards : print("  {}".format(lane))
            drawCards(the_board_cards,opts.show_labels)
    elif opts.members.split(",")[0] == "none":
        for lane in the_board_lanes:
            card_list = []
            #Show the card only if nobody assigned to it and the lane is in the list    
            for card in list(filter(lambda x: len(x.member_id) == 0 and 
                                            x.list_id == the_board_lanes[lane],the_board_cards)):
                card_list.append(card)
            if card_list : print("  {}".format(lane))
            drawCards(card_list,opts.show_labels)
    else:
        # Print active cards per member/lane
        for member in the_board_members:
            if opts.members.split(",")[0] == "all" or listInString(opts.members,member):
                if list(filter(lambda x: the_board_members[member] in x.member_id,the_board_cards)):
                    print(member)
                    for lane in the_board_lanes:
                        card_list = []    
                        for card in list(filter(lambda x: the_board_members[member] in x.member_id and 
                                                        x.list_id == the_board_lanes[lane],the_board_cards)):
                            card_list.append(card)
                        if card_list: print("  {}".format(lane))
                        drawCards(card_list,opts.show_labels)
    return 0
