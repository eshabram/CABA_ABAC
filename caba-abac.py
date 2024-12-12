import subprocess, readline, argparse, sys, os, shutil
from utils.ruleset import check_your_privilege 
from utils.utils import login, create_file, get_metadata
from utils.entities import Subject, Resource, ROLES, DEPARTMENTS, COURSES
from db.db_tables import load_organization
from db.db_interface import add_subject, resource_row, print_table, delete_subject, delete_resource, delete_password

allowed_cmds = ["ls", "pwd", "echo", "clear"]
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

def reset_sandbox():
    try:
        sandbox_dir = os.path.join(current_dir, 'sandbox')
        shutil.rmtree(sandbox_dir)
    except Exception as e:
        print(e)
    enter_sandbox()

def run_shell(args):
    global SUBJECT

    # main loop for the shell
    while True:
        command = input(f"{shell} {cmd_history[command_idx]}")
        cmd_tokens = command.split()
        if not command:
            continue
        
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
                    "new-resource <res-name>   -> Create a resource (alias: nr)\n" \
                    "new-subject               -> Create a new subject (alias: ns)\n" \
                    "delete-subject <sub-id>   -> Delete a subject (alias: ds)\n" \
                    "db                        -> Inspect the database. (Admin only)\n" \
                    "exit, quit                -> Exits the program\n" \
                    "\nSHELL COMMANDS:\n"\
                    "ls, pwd, echo, touch, rm  -> These commands work like normal"
            print(menu)
            
        elif cmd_tokens[0] == "whoami":
            print(SUBJECT)

        # create a 'user_file' with our own implementation of 'touch' command 
        elif cmd_tokens[0] == "touch":
            if len(cmd_tokens) > 1:
                path = cmd_tokens[1].split("/")[-1] # currently only allow files in current dir
                create_file(path, SUBJECT, touch=True)
            else:
                print("Please provide a path")

        # create a resource
        elif cmd_tokens[0] in ["new-resource", "nr"]:
            if len(cmd_tokens) > 1:
                path = cmd_tokens[1].split("/")[-1] # currently only allow files in current dir
                create_file(path, SUBJECT)
            else:
                print("Please provide a path")

        # remove files in from current dir
        elif cmd_tokens[0] == "rm":
            if len(cmd_tokens) == 2:
                path = cmd_tokens[1].split("/")[-1]
                if os.path.exists(path):
                    id = get_metadata(path)
                    res = resource_row(id)
                    if res != None:
                        READ, WRITE, EXECUTE, OWN = check_your_privilege(SUBJECT, res)
                        if OWN:
                            deleted = delete_resource(id, path)
                            if deleted:
                                try:
                                    os.remove(path)
                                except Exception as e:
                                    print(f"Error: Could not remove file at path: {path}")
                            else:
                                print(f'Error: no resource in database with name: {path}')
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
                            print("Access Denied: you do not have READ permissions on this file")
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
        elif cmd_tokens[0] in ["new-subject", "ns"]:
            if len(cmd_tokens) == 1:
                if SUBJECT.role == "admin":
                    id = input('Enter id: ')
                    name = input('Enter name: ')

                    print(f'Enter role (0-{len(ROLES) - 1}):')
                    for i, role in enumerate(ROLES):
                        print(f'{i}. {role}')
                    role_input = input('> ').strip()
                    if role_input != '':
                        role = ROLES[int(role_input)]
                    else:
                        role = 'guest'

                    print(f'Enter department (0-{len(DEPARTMENTS)})')
                    for i, dept in enumerate(DEPARTMENTS):
                        print(f'{i}. {dept}')
                    dept_input = input('> ').strip()
                    if dept_input != '':
                        departments = {DEPARTMENTS[int(dept_input)]}
                    else:
                        departments = {}

                    print(f'Enter subdepartments (0-{len(DEPARTMENTS)}) separated by commas')
                    for i, dept in enumerate(DEPARTMENTS):
                        print(f'{i}. {dept}')
                    nums_string = input('> ').split(',')
                    int_list = {int(x) for x in nums_string if x.strip().isdigit() and 0 <= int(x) <= len(DEPARTMENTS) - 1}
                    subdepartments = {DEPARTMENTS[i] for i in int_list}

                    yn = input('Is this the chair of the department (y/n)')
                    is_chair = True if yn in ['y', 'Y', 'yes'] else False

                    print(f'Enter courses taught (0-{len(COURSES)}) separated by commas')
                    for i, course in enumerate(COURSES):
                        print(f'{i}. {course}')
                    nums_string = input('> ').split(',')
                    int_list = {int(x) for x in nums_string if x.strip().isdigit() and 0 <= int(x) <= len(COURSES) - 1}
                    courses_taught = {COURSES[i] for i in int_list}

                    print(f'Enter courses taken (0-{len(COURSES)}) separated by commas')
                    for i, course in enumerate(COURSES):
                        print(f'{i}. {course}')
                    nums_string = input('> ').split(',') 
                    int_list = {int(x) for x in nums_string if x.strip().isdigit() and 0 <= int(x) <= len(COURSES) - 1}
                    courses_taken = {COURSES[i] for i in int_list}

                    sub = Subject(
                        id=id,
                        name=name,
                        role=role,
                        departments=departments,
                        subdepartments=subdepartments,
                        courses_taught=courses_taught,
                        courses_taken=courses_taken
                    )
                    try:
                        add_subject(sub) 
                    except:
                        print("Error: subject already exists")
                else:
                    print("Error: you lack privileges to create subjects")
            else:
                print("Error: no subject specified")

        elif cmd_tokens[0] in ['delete-subject', 'ds']:
            if len(cmd_tokens) == 2:
                if SUBJECT.role == "admin":
                    id = cmd_tokens[1]
                    yn = input('Are you sure? (yn)')
                    if yn in ['y', 'Y', 'yes', 'Yes', 'YES', 'YES!']:
                        delete_subject(id)
                        delete_password(id)
                else:
                    print("Error: you lack privileges to delete subjects")
            else:
                print('Improper arg structure')

        # edit an existing subject
        # elif cmd_tokens[0] in ["edit-subject", "es"]:
        #     print("edit an existing subject")
        #     if len(cmd_tokens) == 2:
        #         sub = cmd_tokens[1]
        #         if SUBJECT.role == 'admin':
        #             pass
        #         # TODO: database call to edit the subject
        #         else:
        #             print('Error: cannot modify subjects')
        #     else:
        #         print("Error: no subject specified")
        
        elif cmd_tokens[0] == "db" and SUBJECT.role == 'admin':
            print_table('Subjects')
            print_table('Resources')

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
        reset_sandbox()
        load_organization()

    # check for developer mode
    if args.dev:
        SUBJECT = Subject(id="admin1", role="admin")
    else: 
        SUBJECT = login()
    run_shell(args)