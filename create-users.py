#!/usr/bin/python3
import sys
import os

# Set this to True for a dry run (no actual commands will run)
DRY_RUN = True

def run_cmd(cmd):
    """Run or print the command depending on dry run mode."""
    if DRY_RUN:
        print(f"[DRY RUN] Would run: {cmd}")
    else:
        os.system(cmd)

for line in sys.stdin:
    line = line.strip()

    # Skip empty or comment lines
    if not line or line.startswith('#'):
        continue

    fields = line.split(':')
    if len(fields) < 5:
        print(f"[DRY RUN] Skipping invalid line: {line}")
        continue

    username, password, lastname, firstname, groups = fields

    if username == '':
        print(f"[DRY RUN] Skipping blank username line: {line}")
        continue

    print(f"==> Creating account for {username}...")

    # Create user
    cmd = f"/usr/sbin/adduser --disabled-password --gecos '{firstname} {lastname},,,' {username}"
    run_cmd(cmd)

    # Set password
    cmd = f"/bin/echo -ne '{password}\n{password}' | /usr/bin/sudo /usr/bin/passwd {username}"
    run_cmd(cmd)

    # Add to groups if any
    if groups != '-' and groups.strip() != '':
        for group in groups.split(','):
            group = group.strip()
            print(f"==> Assigning {username} to the {group} group...")
            cmd = f"/usr/sbin/adduser {username} {group}"
            run_cmd(cmd)

print("\n[DRY RUN COMPLETE]")

    
