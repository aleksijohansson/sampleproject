
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
    args = parser.parse_args()
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
