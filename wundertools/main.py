#!/usr/bin/env python

# Define a general function for confirming before continuing.
# TODO: Add possibility to assume yes or no.
def confirm(prompt, reminder=False, retries=4):
    prompt = prompt + ' [y/N] '
    while True:
        response = input(prompt)
        if response in ('', 'N', 'n', 'no', 'nop', 'nope'):
            return False
        if response in ('Y', 'y', 'ye', 'yes'):
            return True
        retries = retries - 1
        if retries == 0:
            raise ValueError('invalid user response')
        if reminder != False:
            print(reminder)

def print_command(command):
    print("Your command was:", command)

def main():
    import sys
    if confirm('Print your command?'):
        for arg in sys.argv:
            print_command(arg)
