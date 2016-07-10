
# Needed system modules.
import os

# Use ruamel.yaml to parse settings file etc.
import ruamel.yaml

# Use faker to create random project names.
import faker

# Get the global settings variables.
from wundertool.settings import pwd
from wundertool.settings import settings_path
from wundertool.settings import settings_main_file
from wundertool.settings import local_commands_file
from wundertool.settings import default_command_config

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

def create_example(settings_file=False, type="settings"):
    if not settings_file:
        create_example(settings_main_file)
        create_example(local_commands_file, "commands")
    else:
        if type == "settings":
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
        elif type == "commands":
            settings = {
                "drush": {
                    "type": "shell",
                    "entrypoint": "/app/.composer/vendor/bin/drush"
                },
                "wget": None,
            }
        if get_config(settings_file, True, pwd):
            print("Settings file (%s) already exists." % settings_file)
        else:
            if not os.path.exists(pwd + "/" + settings_path):
                os.makedirs(pwd + "/" + settings_path)
            with open(pwd + "/" + settings_file, 'w') as outfile:
                outfile.write(ruamel.yaml.round_trip_dump(settings, explicit_start=True))

def get_alfanum(text):
    from string import ascii_letters, digits
    return "".join([ch for ch in text if ch in (ascii_letters + digits)]).lower()

def get_config(config=settings_main_file, path_only=False, path=pwd):
    config_path = path + "/" + config
    if os.path.isfile(config_path):
        if path_only:
            return config_path
        else:
            return ruamel.yaml.round_trip_load(open(config_path))
    elif path == os.path.abspath(os.sep):
        if path_only:
            return False
        else:
            raise ImportError("Settings file (%s) not found." % config)
    else:
        if path_only:
            return get_config(config, True, os.path.abspath(os.path.join(path, os.pardir)))
        else:
            return get_config(config, os.path.abspath(os.path.join(path, os.pardir)))

def get_cmd_config(command, config):
    if not isinstance(config, dict):
        config = default_command_config
    # Make sure we have everything we need.
    if not config.get("type"):
        config["type"] = default_command_config["type"]
    if not config.get("entrypoint"):
        config["entrypoint"] = "/usr/bin/" + command
    return config
