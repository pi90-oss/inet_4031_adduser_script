
DRY_RUN = True   # set True for dry-run; set False to execute
def run_cmd(cmd):
    if DRY_RUN:
        print("DRY-RUN: " + cmd)
    else:
        os.system(cmd)
