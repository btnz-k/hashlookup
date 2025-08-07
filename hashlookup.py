#!/usr/bin/env python3
"""
A refactored script to look up cracked NTLM hashes from a DIT/NTDS dump.
"""

# Include Modules
import argparse
import sys
import os
import logging
from colorama import Fore, Style, init

# Define colored symbols for logging to maintain the original feel
InfoSymbol = f"{Fore.BLUE} [i] {Style.RESET_ALL}"
SuccessSymbol = f"{Fore.GREEN} [+] {Style.RESET_ALL}"
WarnSymbol = f"{Fore.YELLOW} [W] {Style.RESET_ALL}"
ErrorSymbol = f"{Fore.RED} [!] {Style.RESET_ALL}"
HashSymbol = f"{Fore.YELLOW} [-] {Style.RESET_ALL}"

def setup_logging(verbose):
    """Configures the logging format and level."""
    log_level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(level=log_level, format='%(message)s')

def load_cracked_hashes(cracked_file_path):
    """
    Loads cracked hashes from a file into a dictionary for fast lookups.

    Args:
        cracked_file_path (str): Path to the file with cracked hashes (format: hash:password).

    Returns:
        dict: A dictionary mapping a hash to its corresponding password.
    """
    logging.info(f"{InfoSymbol}Attempting to load cracked hashes from '{cracked_file_path}'.")
    cracked_map = {}
    try:
        with open(cracked_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if not line or ':' not in line:
                    continue
                hash_val, password = line.split(':', 1)
                cracked_map[hash_val.lower()] = password
        logging.info(f"{SuccessSymbol}Successfully loaded {len(cracked_map)} cracked hashes.")
        return cracked_map
    except IOError as e:
        logging.error(f"{ErrorSymbol}Could not open or read cracked file: {cracked_file_path}. Error: {e}")
        sys.exit(1)

def lookup_user(dit_file_path, username, cracked_hashes):
    """
    Searches for a specific user in the DIT file and prints their credentials.

    Args:
        dit_file_path (str): Path to the DIT file.
        username (str): The user to search for.
        cracked_hashes (dict): Dictionary of cracked hashes.
    """
    logging.info(f"{InfoSymbol}Searching for user '{username}' in '{dit_file_path}'...")
    user_found = False
    try:
        with open(dit_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if username.lower() in line.lower():
                    try:
                        parts = line.strip().split(':')
                        # Standard ntds.dit dump format is user:id:lm_hash:nt_hash:::
                        if len(parts) > 3 and parts[0].lower() == username.lower():
                            user_found = True
                            user_account = parts[0]
                            nt_hash = parts[3]
                            password = cracked_hashes.get(nt_hash.lower())

                            if password:
                                print(f"{SuccessSymbol}{user_account}:{Fore.GREEN}{password}{Style.RESET_ALL}")
                            else:
                                print(f"{HashSymbol}{user_account}:{Fore.YELLOW}{nt_hash}{Style.RESET_ALL}")
                    except IndexError:
                        logging.warning(f"{WarnSymbol}Skipping malformed line: {line.strip()}")
                        continue
        if not user_found:
            logging.warning(f"{ErrorSymbol}User '{username}' not found in {dit_file_path}.")

    except IOError as e:
        logging.error(f"{ErrorSymbol}Could not open or read DIT file: {dit_file_path}. Error: {e}")
        sys.exit(1)

def merge_and_output(dit_file_path, output_file_path, cracked_hashes):
    """
    Merges DIT file with cracked passwords and writes to a new output file.

    Args:
        dit_file_path (str): Path to the DIT file.
        output_file_path (str): Path for the output file.
        cracked_hashes (dict): Dictionary of cracked hashes.
    """
    logging.info(f"{InfoSymbol}Starting merge process. Output will be written to '{output_file_path}'.")

    if os.path.exists(output_file_path):
        overwrite = input(f"{WarnSymbol}Output file '{output_file_path}' already exists. Overwrite? (y/N): ").lower()
        if overwrite != 'y':
            logging.info(f"{InfoSymbol}Operation cancelled by user.")
            return

    cracked_count = 0
    total_count = 0
    try:
        with open(dit_file_path, 'r', encoding='utf-8', errors='ignore') as infile, \
             open(output_file_path, 'w', encoding='utf-8') as outfile:
            for line in infile:
                line = line.strip()
                if not line:
                    continue
                try:
                    parts = line.strip().split(':')
                    user = parts[0]
                    nt_hash = parts[3]

                    # Skip computer accounts, which typically end with $
                    if user.endswith('$'):
                        continue

                    total_count += 1
                    password = cracked_hashes.get(nt_hash.lower())

                    if password:
                        outfile.write(f"{user}:{password}\n")
                        cracked_count += 1
                    else:
                        outfile.write(f"{user}:{nt_hash}\n")
                except IndexError:
                    logging.warning(f"{WarnSymbol}Skipping malformed line in DIT file: {line}")
                    continue

        logging.info(f"{SuccessSymbol}Merge complete. Processed {total_count} user accounts.")
        logging.info(f"{SuccessSymbol}Found and replaced {cracked_count} passwords in '{output_file_path}'.")

    except IOError as e:
        logging.error(f"{ErrorSymbol}File operation failed. Error: {e}")
        sys.exit(1)

def main():
    """Main function to parse arguments and orchestrate the script."""
    init(autoreset=True)  # Initialize colorama

    parser = argparse.ArgumentParser(
        description="A tool to look up cracked passwords from a DIT/NTDS dump.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="Example Usage:\n"
               "  - To find a single user's password:\n"
               "    python3 hashlookup.py ntds.txt cracked.txt -u John.Doe\n\n"
               "  - To create a merged file of all users and their cracked passwords:\n"
               "    python3 hashlookup.py ntds.txt cracked.txt -o user_pass.txt -v"
    )
    parser.add_argument("dit_file", help="Path to the DIT/NTDS file (e.g., ntds.txt).\nExpected format: user:id:lm_hash:nt_hash:::")
    parser.add_argument("cracked_file", help="Path to the file of cracked hashes.\nExpected format: hash:password")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-u", "--user", help="Username to search for.")
    group.add_argument("-o", "--output", help="Output file to write all users with their cracked passwords or hashes.")

    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose informational output.")

    args = parser.parse_args()

    setup_logging(args.verbose)

    # Load cracked hashes into memory for quick lookups
    cracked_hashes = load_cracked_hashes(args.cracked_file)

    # Execute the chosen mode of operation
    if args.user:
        lookup_user(args.dit_file, args.user, cracked_hashes)
    elif args.output:
        merge_and_output(args.dit_file, args.output, cracked_hashes)

if __name__ == "__main__":
    main()
