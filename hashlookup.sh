#!/bin/bash

# Script used to find password for user given cracked hashes, dit file, and username
#
# Written by BTNZ 
# v1.0.2019.09.28
#
####################################################################################################################

# INIT VARS, SET DEFAULT VALUES
DITFILE=""
HASHFILE=""
USERNAME=""
HELP=' HASH LOOKUP SCRIPT

  Flags:
      -?                      Display this help message
      -d <dit file>           Path to NTDS DIT file
      -c <cracked hash file>  Path to cracked hash file
      -u <username>           Designates username/partial username to search for

  Usage:
  ./hashlookup.sh -d client.dit -h cracked_hashes.txt -u admin
        This will search for any usernames that contain the word "admin"
        All fields are required!

'

# BASH COLOR OUTPUT (PRINTF)
BLACK="\e[0;30m";  DKGRAY="\e[1;30m"
RED="\e[0;31m";    LTRED="\e[1;31m"
GREEN="\e[0;32m";  LTGREEN="\e[1;32m"
ORANGE="\e[0;33m"; YELLOW="\e[1;33m"
BLUE="\e[0;34m";   LTBLUE="\e[1;34m"
PURPLE="\e[0;35m"; LTPURPLE="\e[1;35m"
CYAN="\e[0;36m";   LTCYAN="\e[1;36m"
LTGRAY="\e[0;37m"; WHITE="\e[1;37m"
NOCOLOR="\e[0m"

# PULL OPTIONS FROM ARGS AND SET VALUES
while getopts "d:c:u:?" option; do
        case "${option}"
                in
                d) DITFILE=${OPTARG};;
                c) HASHFILE=${OPTARG};;
                u) USERNAME=${OPTARG};;
                \?) printf '\n%s' "$HELP"; exit 0;;
        esac
done

# CHECK TO MAKE SURE REQ VARS ARE SET
[[ -z "$DITFILE" || -z "$HASHFILE" || -z "$USERNAME" ]] && { printf "\n${RED}%s${NOCOLOR}%s\n" " [!] " "Error: Missing Required Parameters!"; printf '\n%s' "$HELP"; exit 1; }

[ ! -f "$DITFILE" ] && { printf "\n${RED}%s${NOCOLOR}%s\n" " [!] " "Error: DIT File Does Not Exist! File: $DITFILE"; printf '\n%s' "$HELP"; exit 1; }
[ ! -f "$HASHFILE" ] && { printf "\n${RED}%s${NOCOLOR}%s\n" " [!] " "Error: Cracked Hash File Does Not Exist! File: $HASHFILE"; printf '\n%s' "$HELP"; exit 1; }

# MAKE SURE USER EXISTS IN DIT
FOUNDUSER=($(cat "$DITFILE" | cut -d":" -f1 | grep -v "\\$" | grep -i "$USERNAME"))
[ "${#FOUNDUSER[@]}" -eq "0" ] && { printf "\n${YELLOW}%s${NOCOLOR}%s\n\n" " [!] " "User does not exist in DIT! Username: $USERNAME"; exit 1; } || { printf "\n%s\n\n" " [-] Found ${#FOUNDUSER[@]} matching usernames!"; }

# LOOP THROUGH FOUND LINES AND PRINT USERNAME AND PASSWORD OR HASH
for r in "${FOUNDUSER[@]}"; do
        LINE=($(grep -iF "$r" "$DITFILE" | cut -d":" -f1,4))
        HASH=($(echo $LINE | cut -d":" -f2))
        USER=($(echo $LINE | cut -d":" -f1))
        PASS=($(grep -iF "$HASH" "$HASHFILE" | cut -d":" -f2))

        # PRINT HASH IF NO PASSWORD FOUND, OTHERWISE PRINT PASSWORD
        [ -z "$PASS" ] && { printf "${YELLOW}%s${NOCOLOR}%s${YELLOW}%s${NOCOLOR}\n" " [/] " "Hash for $USER >> " "$HASH"; } || { printf "${GREEN}%s${NOCOLOR}%s${GREEN}%s${NOCOLOR}\n" " [+] " "Pass for $USER >> " "$PASS"; }
done

echo ""
