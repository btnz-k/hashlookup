#!/usr/bin/env python3

# Include Modules
import argparse
import sys
import shutil

# Initiate the parser
parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=shutil.get_terminal_size()[0]))
parser.add_argument("dit_file", help="Path to dit/ntds file")
parser.add_argument("cracked_file", help="Path to cracked hash file (hash:pass format)")
parser.add_argument("-u", "--user", help="Username to search for")
parser.add_argument("-o", "--output", help="Output file for merged document")
parser.add_argument("-v","--verbose", help="Increase Verbosity", action="store_true")
args = parser.parse_args()

if args.verbose:
    print("Passed Args:")
    print("\tDit File:      ", args.dit_file)
    print("\tCracked File:  ", args.cracked_file)
    print("\tUser:          ", args.user)
    print("\tOutput File:   ", args.output)
    print("\tVerbose:       ", args.verbose)


# Check required vars are present
if args.user is None and args.output is None:
    print("Please pass a username to search for (-u or --user <username> ) or an output file to merge to (-o or --output <file>)")
    quit()

# Check file paths valid


# Check for Output vs User

# If output, merge and quit
    # For merge, check for file exists and ask  for overwrite
    # Copy dit to tmp for processing
    # Strip computer accounts
    # Loop through cracked hash file and modify /tmp dit
    # Copy /tmp dit to correct path
    # Quit script

# Make sure user exists in DIT

# Loop through found lines and print user:pass or user:hash


