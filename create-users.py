------
#!/usr/bin/python3
# ===============================================================
# INET4031 - Automated User Creation Script (Step 10)
# Author: Jinnipakarn Berthiaume
# Date: 10/28/2025
# Purpose: Read user account data from stdin, then create or simulate
#          user accounts and group memberships on a Linux system.
# ===============================================================

import os
import re
import sys

# ---------------------------------------------------------------
# Helper Function: run_cmd()
# Executes or simulates a system command depending on DRY RUN mode.
# ---------------------------------------------------------------
def run_cmd(cmd, dry_run):
    if dry_run:
        print(f"[DRY-RUN] Would run: {cmd}")
    else:
        os.system(cmd)


# ---------------------------------------------------------------
# Main program logic
# ---------------------------------------------------------------
def main():
    print("Run in DRY-RUN mode? [Y/n]: ", end="")
    choice = input().strip().lower()
    dry_run = (choice != "n")

    for raw in sys.stdin:
        line = raw.strip("\n")

        # ---- Skip empty lines ----
        if not line.strip():
            continue

        # ---- Detect comment lines ----
        is_comment = re.match("^#", line) is not None

        # ---- Split colon-delimited fields ----
        # Expected format: username:password:firstname:lastname:group1,group2
        fields = line.strip().split(':')

        # ---- Error / Skip Handling ----
        # Skip comments or lines that don't have exactly 5 fields
        if is_comment or len(fields) != 5:
            if dry_run:
                if is_comment:
                    print(f"[DRY-RUN] Skipping commented line: {line}")
                else:
                    print(f"[DRY-RUN][ERROR] Invalid format (needs 5 fields): {line}")
            continue

        # ---- Extract Fields ----
        username = fields[0]
        password = fields[1]
        first = fields[2]
        last = fields[3]
        gecos = f"{first} {last},,,"
        groups = fields[4].split(',')

        # ---- User Creation ----
        print(f"==> Creating account for {username}...")
        cmd = f"/usr/sbin/adduser --disabled-password --gecos '{gecos}' {username}"
        run_cmd(cmd, dry_run)

        # ---- Password Setup ----
        print(f"==> Setting the password for {username}...")
        cmd = f"/bin/echo -ne '{password}\\n{password}' | /usr/bin/sudo /usr/bin/passwd {username}"
        run_cmd(cmd, dry_run)

        # ---- Group Assignments ----
        for group in groups:
            if group != '-':
                print(f"==> Assigning {username} to the {group} group...")
                cmd = f"/usr/sbin/adduser {username} {group}"
                run_cmd(cmd, dry_run)
            else:
                # Inform if no group assignment is specified
                if dry_run:
                    print(f"[DRY-RUN] No supplemental groups for {username} ('-' specified)")

    # ---- End of processing ----
    print()
    if dry_run:
        print("[DRY-RUN COMPLETE]")
    else:
        print("[USER CREATION COMPLETE]")


# ---------------------------------------------------------------
# Script Entry Point
# ---------------------------------------------------------------
if __name__ == "__main__":
    # The script begins execution here.
    # The DRY-RUN mode ensures safety before making any real system changes.
    main()
