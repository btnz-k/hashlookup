# hashlookup
```
 HASH LOOKUP SCRIPT

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
```
