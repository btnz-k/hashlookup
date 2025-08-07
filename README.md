# HashLookup Utility

A fast and efficient Python script to look up NTLM hashes from a `ntds.dit` dump against a file of cracked passwords. It can either find the password for a single user or generate a consolidated list of all users with their found passwords or remaining hashes.

This script is a significantly refactored and improved version of an earlier tool, focusing on performance, usability, and correctness.

---

## Features

* **Dual-Mode Operation**:
    * **Single User Lookup (`-u`)**: Quickly find the credentials for a specific user.
    * **Bulk Merge (`-o`)**: Process an entire `ntds.dit` file and create a new file containing `user:password` for cracked hashes and `user:hash` for remaining ones.
* **High Performance**: Uses a dictionary for hash lookups, making it extremely fast even with very large hash lists (O(N+M) complexity). It avoids the slow, nested loops found in the original script.
* **User-Friendly**:
    * Clear, colored output for easy identification of cracked passwords.
    * Verbose mode (`-v`) for detailed status updates.
    * Safe by default: warns before overwriting files.
    * Intelligently skips computer accounts (e.g., `WKSTN01$`).
* **Robust & Readable**: The code is well-structured, commented, and includes error handling for common issues like file I/O errors or malformed lines.

---

## Requirements

* Python 3.x
* `colorama` library for colored terminal output.

---

## Installation

1.  Clone or download the `hashlookup.py` script.
2.  Install the `colorama` dependency using pip:
    ```sh
    pip install colorama
    ```

---

## Usage

The script requires two positional arguments (`dit_file` and `cracked_file`) and one of two mutually exclusive options (`-u` or `-o`).

### Command-Line Help

```
usage: hashlookup.py [-h] -u USER | -o OUTPUT [-v] dit_file cracked_file

A tool to look up cracked passwords from a DIT/NTDS dump.

positional arguments:
  dit_file              Path to the DIT/NTDS file (e.g., ntds.txt).
                        Expected format: user:id:lm_hash:nt_hash:::
  cracked_file          Path to the file of cracked hashes.
                        Expected format: hash:password

options:
  -h, --help            show this help message and exit
  -u USER, --user USER  Username to search for.
  -o OUTPUT, --output OUTPUT
                        Output file to write all users with their cracked passwords or hashes.
  -v, --verbose         Enable verbose informational output.

Example Usage:
  - To find a single user's password:
    python3 hashlookup.py ntds.txt cracked.txt -u John.Doe

  - To create a merged file of all users and their cracked passwords:
    python3 hashlookup.py ntds.txt cracked.txt -o user_pass.txt -v
```

### Examples

**1. Find a Password for a Single User**

To search for the user `Administrator`:

```sh
python3 hashlookup.py ntds_dump.txt cracked_hashes.txt -u Administrator
```

**Possible Outputs:**

*If the hash was found in `cracked_hashes.txt`:*
```
[+] Administrator:P@ssword123
```

*If the hash was not found:*
```
[-] Administrator:1F8E24D7B385F477B7A1A7A23A4ED2B9
```

**2. Create a Merged Output File**

To process all users in `ntds_dump.txt` and write the results to `credentials.txt`, use the `-o` option. Adding `-v` provides helpful status updates.

```sh
python3 hashlookup.py ntds_dump.txt cracked_hashes.txt -o credentials.txt -v
```

**Output to Console:**
```
[i] Attempting to load cracked hashes from 'cracked_hashes.txt'.
[+] Successfully loaded 15021 cracked hashes.
[i] Starting merge process. Output will be written to 'credentials.txt'.
[+] Merge complete. Processed 435 user accounts.
[+] Found and replaced 87 passwords in 'credentials.txt'.
```

**Contents of `credentials.txt`:**
```
Administrator:P@ssword123
John.Doe:Summer2025!
Jane.Smith:8A3D9E2C7B1A6F0E9D4B3C2A1B7E8F9D
...
```

---

## Input File Formats

For the script to work correctly, your input files must be in the following format:

* **DIT/NTDS File (`dit_file`)**: A text file where each line represents a user account, with fields separated by colons (`:`). The script specifically expects the username to be the **1st** field and the NTLM hash to be the **4th** field.
    ```
    user:id:lm_hash:nt_hash:::
    Administrator:500:aad3b435b51404eeaad3b435b51404ee:1f8e24d7b385f477b7a1a7a23a4ed2b9:::
    ```

* **Cracked Hashes File (`cracked_file`)**: A text file where each line contains an NTLM hash and its corresponding password, separated by a colon (`:`).
    ```
    hash:password
    1f8e24d7b385f477b7a1a7a23a4ed2b9:P@ssword123
    ```

---

## License

This project is licensed under the MIT License.
