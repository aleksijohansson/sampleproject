
# Needed system modules.
import argparse

# Get the submodules.
import wundertool.helpers
import wundertool.commands

# Get the global settings variables.
from wundertool.settings import local_commands_file

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    args, unknown = parser.parse_known_args()
    if not exec_local_command(args.command, unknown):
        try:
            func = getattr(wundertool.commands, args.command)
        except AttributeError:
            # TODO: Print usage instructions here.
            print("Command not found!")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        else:
            func()

def exec_local_command(command, args):
    commands = wundertool.helpers.get_config(local_commands_file)
    if commands:
        if command in commands:
            config = wundertool.helpers.get_cmd_config(command, commands.get(command))
            if config.get("type") == "shell":
                wundertool.commands.shell(config.get("entrypoint"), args)
                return True
            else:
                raise NotImplementedError("Invalid command type.")
    else:
        return False
