
# Needed system modules.
import os

# Set the global variables.
pwd = os.getcwd()
settings_path = "wundertool"
settings_main_file = settings_path + "/settings.yml"
local_commands_file = settings_path + "/commands.yml"
default_command_config = {"type": "shell"}
# TODO: Implement the usage of this.
default_shell = "quay.io/wunder/wundertools-image-fuzzy-developershell"
