import subprocess, readline
from utils.db_utils import *

allowed_cmds = ["ls", "pwd", "echo"]
internal_cmds = ["read", "write", "touch"]
current_dir = os.path.dirname(os.path.abspath(__file__))
shell = "caba>"
cmd_history = [""]
command_idx = 0
history_file = os.path.expanduser(os.path.join(current_dir, "shell_history"))

# Load history from file
if os.path.exists(history_file):
    readline.read_history_file(history_file)

def enter_sandbox():
    """ Changes dir to the sandbox dir where files can be safely created and removed """
    sandbox_dir = os.path.join(current_dir, 'sandbox')
    if not os.path.exists(sandbox_dir):
        os.makedirs(sandbox_dir)
    # use os instead of subprocess function to globally change dir
    os.chdir(sandbox_dir)

if __name__=="__main__":
    """ Main entry point to the CABA_ABAC shell """
    enter_sandbox()

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
        
        elif cmd_tokens[0] in ["help", "?"]:
            menu = f"\nCOMMANDS:\n" \
                    "help                      -> List commands\n" \
                    "read  <filename>          -> Read file\n" \
                    "write <filename>          -> Opens file for writing in nano\n" \
                    "exit, quit                -> Exits the program\n" \
                    "\nSHELL COMMANDS:\n"\
                    "ls, pwd, echo             -> These commands work in like normal"
            print(menu)
            
        # only allow files to be created in the current directory. 
        elif cmd_tokens[0] == "touch":
            if len(cmd_tokens) > 1:
                name = cmd_tokens[1].split("/")[-1]
                with open(name, 'w') as file:
                    file.write("")
            else:
                print("Please provide a path")

        # remove files only in current dir
        elif cmd_tokens[0] == "rm":
            if len(cmd_tokens):
                name = cmd_tokens[1].split("/")[-1]
                try:
                    os.remove(name)
                except Exception as e:
                    print("Error: Could not remove file")

        # read a file using the cat command
        elif cmd_tokens[0] == "read":
            if len(cmd_tokens) == 2:
                # TODO: run our read check here 
                cmd = ["cat", cmd_tokens[1]]
                if os.path.exists(cmd_tokens[1]):
                    try:
                        subprocess.run(cmd, check=True, text=True)
                    except subprocess.CalledProcessError as e:
                        print(f"Error: {e}")
                else:
                    print("File does not exist")
            else:
                print("Error: No path specified")

        # write a file using nano. you can rename if needed
        elif cmd_tokens[0] == "write":
            if len(cmd_tokens) == 2:
                try:
                    subprocess.call(['nano', cmd_tokens[1]])
                except subprocess.CalledProcessError as e:
                    print(f"Error: {e}")
            else:
                print("Error: No path specified")

        elif cmd_tokens[0] == "":
            continue
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
