#!/usr/bin/env python3

# Include Modules
import argparse

HelpText = ''' HASH LOOKUP SCRIPT'''
#  Flags:
#      -d, --dit <dit file>                  Path to NTDS DIT file
#      -c, --cracked <cracked hash file>     Path to cracked hash file
#      -u, user <username>                   Designates username/partial username to search for
#      -o, --output <filename>               Merges the username and password and exports to <filename>
#                                            in username:hash:password format
#  Usage:
#  ./hashlookup.py -d client.dit -h cracked_hashes.txt -u admin
#        This will search for any usernames that contain the word "admin". All fields are required!
#  ./hashlookup.py -d client.dit -h cracked_hashes.txt -o ./user_pass.txt
#        This will merge the DIT and cracked hash file, in user:hash:pass format



# Initiate the parser
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--cracked", help="Path to cracked hash file")
parser.add_argument("-d", "--dit", help="Path to dit/ntds file")
parser.add_argument("-u", "--user", help="Username to search for")
parser.parse_args()

