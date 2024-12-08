import subprocess, readline, argparse, sys, os
from utils.ruleset import check_your_privilege 
from utils.utils import login, create_file, get_metadata, set_metadata
from utils.entities import Subject, Resource
from db.db_tables import load_organization
from utils.organization import SUBJECTS_LIST, RESOURCE_LIST
from db.db_interface import add_subject, add_resource, subject_row, resource_row, password_row

allowed_cmds = ["ls", "pwd", "echo"]
internal_cmds = ["read", "write", "touch"]
current_dir = os.path.dirname(os.path.abspath(__file__))
shell = "caba>"
cmd_history = [""]
command_idx = 0
SUBJECT = Subject()

# history_file = os.path.expanduser(os.path.join(current_dir, "shell_history"))

# # Load history from file
# if os.path.exists(history_file):
#     readline.read_history_file(history_file)

def enter_sandbox():
    """ Changes dir to the sandbox dir where files can be safely created and removed """
    sandbox_dir = os.path.join(current_dir, 'sandbox')
    if not os.path.exists(sandbox_dir):
        os.makedirs(sandbox_dir)
    # use os instead of subprocess function to globally change dir
    os.chdir(sandbox_dir)

def run_shell(args):
    global SUBJECT

    # main loop for the shell
    while True:
        command = input(f"{shell} {cmd_history[command_idx]}")
        cmd_tokens = command.split(" ")
        
        # Add command to history
        if command:
            cmd_history.append(command)

        # exit commands
        if command == "exit" or command == "quit":
            print("Exiting...")
            break
        
        # help menu
        elif cmd_tokens[0] in ["help", "?"]:
            menu = f"\nCOMMANDS:\n" \
                    "help                      -> List commands\n" \
                    "whoami                    -> Print your attributes\n" \
                    "read  <filename>          -> Read file\n" \
                    "write <filename>          -> Opens file for writing in nano\n" \
                    "exit, quit                -> Exits the program\n" \
                    "\nSHELL COMMANDS:\n"\
                    "ls, pwd, echo, touch, rm  -> These commands work like normal"
            print(menu)
            
        elif cmd_tokens[0] == "whoami":
            print(SUBJECT)

        # create a file with our own implementation of 'touch' command 
        elif cmd_tokens[0] == "touch":
            if len(cmd_tokens) > 1:
                path = cmd_tokens[1].split("/")[-1] # currently only allow files in current dir
                create_file(path)
            else:
                print("Please provide a path")

        # remove files in from current dir
        elif cmd_tokens[0] == "rm":
            if len(cmd_tokens) == 2:
                path = cmd_tokens[1]
                if os.path.exists(path):
                    id = get_metadata(path)
                    res = resource_row(id)
                    if res != None:
                        READ, WRITE, EXECUTE, OWN = check_your_privilege(SUBJECT, res)
                        if OWN:
                            try:
                                os.remove(path)
                            except Exception as e:
                                print("Error: Could not remove file")
                        else:
                            print("Error: you lack privileges to remove this file")
                    else:
                        print("Error: no db entry for resource")
                else:
                    print('Error: file does not exist')

        # read a file using the cat command
        elif cmd_tokens[0] == "read":
            if len(cmd_tokens) == 2:
                path = cmd_tokens[1]
                cmd = ["cat", path]
                if os.path.exists(path):
                    id = get_metadata(path)
                    res = resource_row(id)
                    if res != None:
                        READ, WRITE, EXECUTE, OWN = check_your_privilege(SUBJECT, res)
                        if READ:
                            try:
                                subprocess.run(cmd, check=True, text=True)
                            except subprocess.CalledProcessError as e:
                                print(f"Error: {e}")
                        else:
                            print("Error: you do not have READ permissions on this file")
                    else:
                        print("Error: no db entry for resource")
                else:
                    print("File does not exist")
            else:
                print("Error: No path specified")

        # write a file using nano. you can rename if needed
        elif cmd_tokens[0] == "write":
            if len(cmd_tokens) == 2:
                path = cmd_tokens[1]
                id = get_metadata(path)
                res = resource_row(id)
                if res != None:
                    READ, WRITE, EXECUTE, OWN = check_your_privilege(SUBJECT, res)
                    if WRITE:
                        try:
                            success = subprocess.call(['nano', path])
                        except subprocess.CalledProcessError as e:
                            print(f"Error: {e}")
                    else:
                        print("Error: you do not have WRITE permissions")
                else:
                    print('Error: no db entry for resource')
            else:
                print("Error: No path specified")

        # create a new subject
        elif cmd_tokens[0] in ["new-subject","ns"] :
            if len(cmd_tokens) == 2:
                sub_id = cmd_tokens[1]
                if SUBJECT.role == "admin":
                    try:
                        add_subject(sub_id) 
                    except: # TODO: raise an error in the db to indicate specifically that the entry already exists and catch it here
                        print("Error: subject already exists")
                else:
                    print("Error: you lack privileges to create subjects")
            else:
                print("Error: no subject specified")

        # edit an existing subject
        elif cmd_tokens[0] in ["edit-subject", "es"]:
            print("edit an existing subject")
            if len(cmd_tokens) == 2:
                sub = cmd_tokens[1]
                if SUBJECT.role == 'admin':
                    pass
                # TODO: database call to edit the subject
                else:
                    print('Error: cannot modify subjects')
            else:
                print("Error: no subject specified")

        # do nothing
        elif cmd_tokens[0] == "":
            continue

        # run allowed shell commands
        elif cmd_tokens[0] in allowed_cmds:
            try:
                subprocess.run(command, shell=True, check=True, text=True)
            except subprocess.CalledProcessError as e:
                print(f"Error: {e}")
        else:
            print("Command not allowed or recognized.")


if __name__=="__main__":
    """ Main entry point to the CABA_ABAC shell """
    enter_sandbox()

    parser = argparse.ArgumentParser(
                    prog='CABA_ABAC',
                    description='ABAC policy simulator',
                    epilog='Text at the bottom of help')
    parser.add_argument('-d', '--dev', action='store_true', help='Developer mode')
    parser.add_argument('-rl', '--reload', action='store_true', help='Reload Database')
    args = parser.parse_args()

    if args.reload:
        load_organization()

    # check for developer mode
    if args.dev:
        SUBJECT = Subject(id="admin1", role="admin")
    else: 
        SUBJECT = login()
    run_shell(args)