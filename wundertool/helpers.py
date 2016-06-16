
# Needed system modules.
import os

# Use PyYAML to parse settings file etc.
import yaml

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
            raise ValueError('Invalid user response.')
        if reminder != False:
            print(reminder)

# TODO: This might become deprecated when using argparse in the main module.
def usage():
    print("This is how you should use the tool.")

def get_settings(path):
    settings_file_path = path + "wundertool-settings.yml"
    if os.path.isfile(settings_file_path):
        return yaml.load(open(settings_file_path))
    elif path == os.path.abspath(os.sep):
        raise ImportError('Settings file (wundertool-settings.yml) not found. Run `wundertool init` in your project root folder to generate one.')
    else:
        return get_settings(os.path.abspath(os.path.join(path, os.pardir)))

def get_alfanum(text):
    from string import ascii_letters, digits
    return "".join([ch for ch in text if ch in (ascii_letters + digits)]).lower()
