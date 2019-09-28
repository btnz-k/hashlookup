# hashlookup
HASH LOOKUP SCRIPT

  Flags:
      -?                      Display this help message
      -d <dit file>           Path to NTDS DIT file
      -c <cracked hash file>  Path to cracked hash file
      -u <username>           Designates username/partial username to search for

  Usage:
  ./hashlookup.sh -d client.dit -h cracked_hashes.txt -u admin
        This will search for any usernames that contain the word "admin"
        All fields are required!

