#!/usr/bin/env python3

# Include Modules
import argparse
import sys
import os.path
import shutil
import logging
from colorama import Fore, Back, Style, init

# Initiate colorama and vars
init()
opened_dit_file = []
opened_cracked_file = []
found = []
userpass=""

# Initiate the parser
parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=shutil.get_terminal_size()[0]))
parser.add_argument("dit_file", help="Path to DIT/NTDS File")
parser.add_argument("cracked_file", help="Path to Cracked Hash File (hash:pass format)")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-u", "--user", help="Username to Search")
group.add_argument("-o", "--output", help="Output Path for Merged Document")
parser.add_argument("-v","--verbose", help="Increase Verbosity", action="store_const", dest="loglevel", const=logging.INFO, default=logging.WARNING)
args = parser.parse_args()

# Initiate Logger Configuration
WarnSymbol=(Fore.YELLOW + ' [W] ' + Style.RESET_ALL)
ErrorSymbol=(Fore.RED + ' [!] ' + Style.RESET_ALL)
InfoSymbol=(Fore.BLUE + ' [i] ' + Style.RESET_ALL)
SuccessSymbol=(Fore.GREEN + ' [+] ' + Style.RESET_ALL)
HashSymbol=(Fore.YELLOW + ' [-] ' + Style.RESET_ALL)
LoggingFormat='%(message)s'
logging.basicConfig(format=LoggingFormat,level=args.loglevel)

# Display passed variables
logging.info(InfoSymbol + "Passed Arguments:")
logging.info(InfoSymbol + "\tDIT File:      " + str(args.dit_file))
logging.info(InfoSymbol + "\tCracked File:  " + str(args.cracked_file))
logging.info(InfoSymbol + "\tUsername:      " + str(args.user))
logging.info(InfoSymbol + "\tOutput File:   " + str(args.output))
logging.info(InfoSymbol + "\tVerbosity:     " + str(args.loglevel))

# Attempt to open DIT and Cracked files
try:
    logging.info(InfoSymbol + "Attempting to open DIT file (" + args.dit_file + ").")
    with open(args.dit_file) as Df:
        for Dline in Df:
            opened_dit_file.append(Dline)

        logging.info(InfoSymbol + "DIT file (" + args.dit_file + ") successfully opened.")
except IOError:
    logging.error(ErrorSymbol + "Could not open DIT file: " + args.dit_file)
    quit()

try:
    logging.info(InfoSymbol + "Attempting to open cracked file (" + args.cracked_file + ").")
    with open(args.cracked_file) as Cf:
        for Cline in Cf:
            opened_cracked_file.append(Cline)

        logging.info(InfoSymbol + "DIT file (" + args.cracked_file + ") successfully opened.")
except IOError:
    logging.error(ErrorSymbol + "Could not open cracked file: " + args.cracked_file)
    quit()

# Sort lines
opened_dit_file.sort()
opened_cracked_file.sort()

# Check for Output vs User

# If output, merge and quit
    # For merge, check for file exists and ask  for overwrite
    # Copy dit to tmp for processing
    # Strip computer accounts
    # Loop through cracked hash file and modify /tmp dit
    # Copy /tmp dit to correct path
    # Quit script

# Make sure user exists in DIT
foundcount = sum(args.user.lower() in s for s in ([x.lower() for x in  opened_dit_file]))
print ()
# Print Success if Found
if foundcount > 0 :
    logging.warn(SuccessSymbol + "Found " + str(foundcount) + " results!\n")
else:
    logging.warn(ErrorSymbol + "Found " + str(foundcount) + " results!\n")
    quit()

# Loop through the DIT and get the line that has the matching user
for line in opened_dit_file:
    # If the line (converted to lowercase) contains the lowercase username (ne -1)
    if line.lower().find(args.user.lower()) != -1: 
        # Split the line based on the ":" character
        cutline = line.rstrip('\n').split(':')
        # Search for the hash in the cracked file
        for cline in opened_cracked_file:
            if cline.lower().find(cutline[3]) != -1:
                userpass = (cline.rstrip('\n').split(':'))[1]
                break
        # Print the user:hash or user:hash:pass
        if userpass is "":
            userinfo = HashSymbol  + cutline[0] + ":" + Fore.YELLOW + cutline[3] + Style.RESET_ALL
        else:
            userinfo = SuccessSymbol + cutline[0] + ":" + Fore.GREEN + userpass + Style.RESET_ALL
        logging.warn(userinfo)
        userpass=""

print()