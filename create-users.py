#!/usr/bin/python3
# -------------------------------------------------------------
# INET4031 – Lab 8 Part 2: Automating User Creation
# Author: 
# Date: 10/26/2025
# Description:
#   This Python script automates the creation of multiple users
#   and their associated groups on a Linux system. User data is
#   read from standard input (an input file) with fields separated
#   by colons (:). Each line specifies username, password, last name,
#   first name, and group memberships. The script can run in "dry run"
#   mode for testing or in normal mode to actually create users.
# -------------------------------------------------------------

import os      # Allows execution of Linux system commands
import re      # Enables use of regular expressions
import sys     # Used for reading from standard input

def main():
    # Read each line from the input file (via stdin)
    for line in sys.stdin:

        # Ignore comment lines (those starting with '#')
        # 'match' checks whether the current line begins with a '#'
        match = re.match("^#", line)

        # Split line into fields separated by ':' and remove extra spaces
        fields = line.strip().split(':')

        # Skip invalid lines — those that are comments or missing required fields
        if match or len(fields) != 5:
            continue

        # Assign input fields to descriptive variable names
        username = fields[0]      # Username for the new user
        password = fields[1]      # Initial password for the user
        lastname = fields[2]      # User's last name (for GECOS field)
        firstname = fields[3]     # User's first name (for GECOS field)
        groups = fields[4].split(',')  # List of groups to which the user belongs

        # Combine first and last name for the GECOS (comment) field in /etc/passwd
        gecos = "%s %s,,," % (firstname, lastname)

        # Print the command that would be executed to create the account
        print(f"==> Creating account for {username}...")
        cmd = f"/usr/sbin/adduser --disabled-password --gecos '{gecos}' {username}"

        # Dry-run: Print command for verification, comment os.system() to avoid execution
        # Actual run: Uncomment os.system() to create the user
        os.system(cmd)

        # Print and execute the command to set the user's password
        print(f"==> Setting the password for {username}...")
        cmd = f"/bin/echo -ne '{password}\n{password}' | /usr/bin/sudo /usr/bin/passwd {username}"
        os.system(cmd)

        # If user belongs to any groups, assign them
        for group in groups:
            if group != '-':  # '-' indicates no group
                print(f"==> Assigning {username} to the {group} group...")
                cmd = f"/usr/sbin/adduser {username} {group}"
                os.system(cmd)

# Run the main function when executed
if __name__ == "__main__":
    main()

