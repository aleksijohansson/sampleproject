
# Needed system modules.
import os

# Use PyYAML to parse settings file etc.
import yaml

# Use faker to create random project names.
import faker

# Define some multi-use variables.
pwd = os.getcwd()
settings_path = "wundertool"
settings_main_file = settings_path + "/settings.yml"

# General function for confirming before continuing.
def confirm(prompt, assume=False, reminder=False, retries=3):
    if assume == True:
        prompt = prompt + " [Y/n] "
    else:
        prompt = prompt + " [y/N] "
    while True:
        response = input(prompt)
        if (assume == True and
            response == ""):
            return True
        elif response == "":
            return False
        elif response in ("n", "no", "N", "No"):
            return False
        elif response in ("y", "ye", "yes", "Y", "Yes"):
            return True
        retries = retries - 1
        if retries == 0:
            raise ValueError("Invalid user response.")
        if reminder != False:
            print(reminder)

# TODO: This might become deprecated when using argparse in the main module.
def usage():
    print("This is how you should use the tool.")

def create_settings():
    generator = faker.Faker()
    settings = {
        "images": {
            "shell": "quay.io/wunder/wundertools-image-fuzzy-developershell",
            "source": "source"
        },
        "project": {
            "name": get_alfanum(generator.company()),
        },
    }
    if get_settings(pwd, True):
        print("Settings file (%s) already exists." % settings_main_file)
    else:
        if not os.path.exists(pwd + "/" + settings_path):
            os.makedirs(pwd + "/" + settings_path)
        with open(pwd + "/" + settings_main_file, 'w') as outfile:
            outfile.write(yaml.dump(settings, default_flow_style=False, explicit_start=True))

def get_settings(path=pwd, path_only=False):
    settings_main_file_path = path + "/" + settings_main_file
    if os.path.isfile(settings_main_file_path):
        if path_only:
            return settings_main_file_path
        else:
            return yaml.load(open(settings_main_file_path))
    elif path == os.path.abspath(os.sep):
        if path_only:
            return False
        else:
            raise ImportError("Settings file (%s) not found." % settings_main_file)
    else:
        if path_only:
            return get_settings(os.path.abspath(os.path.join(path, os.pardir)), True)
        else:
            return get_settings(os.path.abspath(os.path.join(path, os.pardir)))

def get_alfanum(text):
    from string import ascii_letters, digits
    return "".join([ch for ch in text if ch in (ascii_letters + digits)]).lower()
