import os
import sys
import readline
import shlex
import shutil
from subprocess import Popen, PIPE

# Autocompletion
def completer(text, state):
    options = [i for i in os.listdir('.') if i.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

readline.parse_and_bind("tab: complete")
readline.set_completer(completer)

# Shell prompt
def display_prompt():
    cwd = os.getcwd()
    return f"pyshell:{cwd}$ "

# Parse command with quoting
def parse_command(command):
    return shlex.split(command)

# Handle redirection
def handle_redirection(args):
    input_file = None
    output_file = None
    append_mode = False

    if '>' in args:
        index = args.index('>')
        output_file = args[index + 1]
        args = args[:index]
    if '>>' in args:
        index = args.index('>>')
        output_file = args[index + 1]
        append_mode = True
        args = args[:index]
    if '<' in args:
        index = args.index('<')
        input_file = args[index + 1]
        args = args[:index]

    return args, input_file, output_file, append_mode

def list_directory(args):
    path = args[1] if len(args) > 1 else '.'
    try:
        for entry in os.listdir(path):
            print(entry)
    except FileNotFoundError:
        print(f"Directory not found: {path}")
    except NotADirectoryError:
        print(f"Not a directory: {path}")
    except PermissionError:
        print(f"Permission denied: {path}")

def print_working_directory():
    print(os.getcwd())

def make_directory(args):
    if len(args) < 2:
        print("mkdir: missing operand")
        return
    try:
        os.mkdir(args[1])
    except FileExistsError:
        print(f"mkdir: cannot create directory '{args[1]}': File exists")
    except PermissionError:
        print(f"mkdir: cannot create directory '{args[1]}': Permission denied")

def remove_directory(args):
    if len(args) < 2:
        print("rmdir: missing operand")
        return
    try:
        os.rmdir(args[1])
    except FileNotFoundError:
        print(f"rmdir: failed to remove '{args[1]}': No such file or directory")
    except OSError:
        print(f"rmdir: failed to remove '{args[1]}': Directory not empty or other error")
    except PermissionError:
        print(f"rmdir: failed to remove '{args[1]}': Permission denied")

def remove_file(args):
    if len(args) < 2:
        print("rm: missing operand")
        return
    try:
        os.remove(args[1])
    except FileNotFoundError:
        print(f"rm: cannot remove '{args[1]}': No such file or directory")
    except PermissionError:
        print(f"rm: cannot remove '{args[1]}': Permission denied")

def concatenate_file(args):
    if len(args) < 2:
        print("cat: missing operand")
        return
    try:
        with open(args[1], 'r') as f:
            print(f.read())
    except FileNotFoundError:
        print(f"cat: {args[1]}: No such file or directory")
    except PermissionError:
        print(f"cat: {args[1]}: Permission denied")

def echo_text(args):
    print(' '.join(args[1:]))

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def touch_file(args):
    if len(args) < 2:
        print("touch: missing operand")
        return
    try:
        with open(args[1], 'a'):
            os.utime(args[1], None)
    except PermissionError:
        print(f"touch: cannot touch '{args[1]}': Permission denied")

def move_file(args):
    if len(args) < 3:
        print("mv: missing operand")
        return
    try:
        shutil.move(args[1], args[2])
    except FileNotFoundError:
        print(f"mv: cannot move '{args[1]}': No such file or directory")
    except PermissionError:
        print(f"mv: cannot move '{args[1]}': Permission denied")

def copy_file(args):
    if len(args) < 3:
        print("cp: missing operand")
        return
    try:
        shutil.copy(args[1], args[2])
    except FileNotFoundError:
        print(f"cp: cannot copy '{args[1]}': No such file or directory")
    except PermissionError:
        print(f"cp: cannot copy '{args[1]}': Permission denied")

def head_file(args):
    if len(args) < 2:
        print("head: missing operand")
        return
    try:
        with open(args[1], 'r') as f:
            for _ in range(10):
                line = f.readline()
                if not line:
                    break
                print(line, end='')
    except FileNotFoundError:
        print(f"head: cannot open '{args[1]}': No such file or directory")
    except PermissionError:
        print(f"head: cannot open '{args[1]}': Permission denied")

def tail_file(args):
    if len(args) < 2:
        print("tail: missing operand")
        return
    try:
        with open(args[1], 'r') as f:
            lines = f.readlines()
            for line in lines[-10:]:
                print(line, end='')
    except FileNotFoundError:
        print(f"tail: cannot open '{args[1]}': No such file or directory")
    except PermissionError:
        print(f"tail: cannot open '{args[1]}': Permission denied")

def find_files(args):
    if len(args) < 2:
        print("find: missing operand")
        return
    for root, dirs, files in os.walk('.'):
        for name in files:
            if args[1] in name:
                print(os.path.join(root, name))

# Execute command
def execute_command(args):
    if not args:
        return

    # Handle built-in commands
    if args[0] == "cd":
        if len(args) > 1:
            try:
                os.chdir(args[1])
            except FileNotFoundError:
                print(f"Directory not found: {args[1]}")
            except NotADirectoryError:
                print(f"Not a directory: {args[1]}")
            except PermissionError:
                print(f"Permission denied: {args[1]}")
        else:
            print("cd: missing operand")
        return
    elif args[0] == "exit":
        print("Exiting pyshell.")
        sys.exit(0)
    elif args[0] == "ls":
        list_directory(args)
        return
    elif args[0] == "pwd":
        print_working_directory()
        return
    elif args[0] == "mkdir":
        make_directory(args)
        return
    elif args[0] == "rmdir":
        remove_directory(args)
        return
    elif args[0] == "rm":
        remove_file(args)
        return
    elif args[0] == "cat":
        concatenate_file(args)
        return
    elif args[0] == "echo":
        echo_text(args)
        return
    elif args[0] == "clear":
        clear_screen()
        return
    elif args[0] == "touch":
        touch_file(args)
        return
    elif args[0] == "mv":
        move_file(args)
        return
    elif args[0] == "cp":
        copy_file(args)
        return
    elif args[0] == "head":
        head_file(args)
        return
    elif args[0] == "tail":
        tail_file(args)
        return
    elif args[0] == "find":
        find_files(args)
        return

    # Handle redirection
    args, input_file, output_file, append_mode = handle_redirection(args)

    # Execute external commands
    try:
        if input_file:
            with open(input_file, 'r') as f:
                process = Popen(args, stdin=f, stdout=PIPE, stderr=PIPE)
        else:
            process = Popen(args, stdout=PIPE, stderr=PIPE)

        stdout, stderr = process.communicate()

        if output_file:
            mode = 'a' if append_mode else 'w'
            with open(output_file, mode) as f:
                f.write(stdout.decode())
        else:
            print(stdout.decode(), end='')

        if stderr:
            print(stderr.decode(), end='', file=sys.stderr)

    except FileNotFoundError:
        print(f"Command not found: {args[0]}")

# Main shell loop
def main():
    while True:
        try:
            command = input(display_prompt())
            args = parse_command(command)
            execute_command(args)
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()