
# General function for confirming before continuing.
def confirm(prompt, assume=False, reminder=False, retries=3):
    if assume == True:
        prompt = prompt + ' [Y/n] '
    else:
        prompt = prompt + ' [y/N] '
    while True:
        response = input(prompt)
        if (assume == True and
            response == ''):
            return True
        elif response == '':
            return False
        elif response in ('n', 'no', 'N', 'No'):
            return False
        elif response in ('y', 'ye', 'yes', 'Y', 'Yes'):
            return True
        retries = retries - 1
        if retries == 0:
            raise ValueError('invalid user response')
        if reminder != False:
            print(reminder)

# TODO: This might become deprecated when using argparse in the main module.
def usage():
    print("This is how you should use the tool.")
