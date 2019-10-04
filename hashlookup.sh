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
OUTFILE=""
SPIN="-"
HELP=' HASH LOOKUP SCRIPT

  Flags:
      -?                      Display this help message
      -d <dit file>           Path to NTDS DIT file
      -c <cracked hash file>  Path to cracked hash file
      -u <username>           Designates username/partial username to search for
      -o <filename>           Merges the username and password and exports to <filename>
                              in username:hash:password format

  Usage:
  ./hashlookup.sh -d client.dit -h cracked_hashes.txt -u admin
        This will search for any usernames that contain the word "admin"
        All fields are required!

  ./hashlookup.sh -d client.dit -h cracked_hashes.txt -o ./user_pass.txt
        This will merge the DIT and cracked hash file, in user:hash:pass format

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
while getopts "d:c:u:o:?" option; do
        case "${option}"
                in
                d) DITFILE=${OPTARG};;
                c) HASHFILE=${OPTARG};;
                u) USERNAME=${OPTARG};;
                o) OUTFILE=${OPTARG};;
                \?) printf '\n%s' "$HELP"; exit 0;;
        esac
done

# CHECK TO MAKE SURE REQ VARS ARE SET
[[ -z "$DITFILE" || -z "$HASHFILE" ]] && { printf "\n${RED}%s${NOCOLOR}%s\n" " [!] " "Error: Missing required parameters!"; printf '\n%s' "$HELP"; exit 1; }
[ ! -f "$DITFILE" ] && { printf "\n${RED}%s${NOCOLOR}%s\n" " [!] " "Error: DIT file does not exist! File: $DITFILE"; printf '\n%s' "$HELP"; exit 1; }
[ ! -f "$HASHFILE" ] && { printf "\n${RED}%s${NOCOLOR}%s\n" " [!] " "Error: Cracked hash file does not exist! File: $HASHFILE"; printf '\n%s' "$HELP"; exit 1; }

# CHECK IF OUTPUT FLAG IS ENABLED
if [ ! -z "$OUTFILE" ]; then
        printf "\n%s\n" " [-] Initiating file merge process"
        # TEST TO SEE THAT PATH TO OUTPUT FILE EXISTS
        if [ -f "$OUTFILE" ]; then
                printf "${YELLOW}%s${NOCOLOR}%s" " [!] " "Output file exists. Overwrite? "
                read -p " " -n 1 -read
                [[ "$REPLY" =~ ^[Yy]$ ]] && exit 1
        fi
        # COPY DIT TO TMP FOR PROCESSING
        printf "%s\n" " [-] Copying file to /tmp"
        [[ "$DITFILE"  == *"/"* ]] && FILENAME=$( echo "$DITFILE" | rev | cut -d"/" -f1 | rev ) || FILENAME="$DITFILE" #<<<< changed this line, need to verify it works
        cat "$DITFILE" | cut -d":" -f1,4 > "/tmp/$FILENAME"
        # BUILD NEW FILE
        printf "%s\r" " [-] Building merged file          "
        # LOOP THROUGH CRACKED HASH FILE AND MODIFY /TMP FILE
        i=0
        for l in $(cat $HASHFILE); do
                ((i=i+1))
                LIMIT=$(cat $HASHFILE | wc -l)
                PERCENT=$(( $i*100/$LIMIT ))
                case "$SPIN" in
                        '-') SPIN='\';;
                        '\') SPIN='|';;
                        '|') SPIN='/';;
                        '/') SPIN='-';;
                esac
                printf "%s\r" " [$SPIN] Building merged file ($PERCENT%)       "
                HASH=($( echo $l | cut -d":" -f1 ))
                PASS=($( echo $l | cut -d":" -f2 ))
                MERGED="$HASH:$PASS"
                #sed -i 's,'"$HASH"','"$MERGED"',g' "/tmp/$FILENAME"
                sed -i 's,'"$HASH"','"${MERGED//&/\\&}"',g' "/tmp/$FILENAME"
        done
        mv -f "/tmp/$FILENAME" "$OUTFILE"
        printf "\n%s\n\n" " [-] Export complete!"
        exit 1
fi

[[ -z "$USERNAME" ]] && { printf "\n${RED}%s${NOCOLOR}%s\n" " [!] " "Error: Missing required parameters!"; printf '\n%s' "$HELP"; exit 1; }

# MAKE SURE USER EXISTS IN DIT
FOUNDUSER=($( cat "$DITFILE" | cut -d":" -f1 | grep -v "\\$" | grep -i "$USERNAME"))
[ "${#FOUNDUSER[@]}" -eq "0" ] && { printf "\n${YELLOW}%s${NOCOLOR}%s\n\n" " [!] " "User does not exist in DIT! Username: $USERNAME"; exit 1; } || { printf "\n%s\n\n" " [-] Found ${#FOUNDUSER[@]} matching usernames!"; }

# LOOP THROUGH FOUND LINES AND PRINT USERNAME AND PASSWORD OR HASH
for r in "${FOUNDUSER[@]}"; do
        LINE=($( grep -iF "$r" "$DITFILE" | cut -d":" -f1,4 ))
        HASH=($( echo $LINE | cut -d":" -f2 ))
        USER=($( echo $LINE | cut -d":" -f1 ))
        PASS=($( grep -iF "$HASH" "$HASHFILE" | cut -d":" -f2 ))

        # PRINT HASH IF NO PASSWORD FOUND, OTHERWISE PRINT PASSWORD
        [ -z "$PASS" ] && { printf "${YELLOW}%s${NOCOLOR}%s${YELLOW}%s${NOCOLOR}\n" " [/] " "Hash for $USER >> " "$HASH"; } || { printf "${GREEN}%s${NOCOLOR}%s${GREEN}%s${NOCOLOR}\n" " [+] " "Pass for $USER >> " "$PASS"; }
done

echo ""
