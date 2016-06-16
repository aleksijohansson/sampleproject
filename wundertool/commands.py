
# Needed system modules.
import subprocess
import os

# Use faker to create random project names.
import faker

# Use PyYAML to parse settings file etc.
import yaml

# Get the submodules.
import wundertool.commands
import wundertool.helpers
import wundertool.handler

# Define some multi-use variables.
current = os.getcwd() + "/"

def init():
    generator = faker.Faker()
    settings = {
        "project": {
            "name": wundertool.helpers.get_alfanum(generator.company())
        }
    }
    settings_file_path = current + "wundertool-settings.yml"
    if not os.path.isfile(settings_file_path):
        with open(settings_file_path, 'w') as outfile:
            outfile.write(yaml.dump(settings, default_flow_style=False, explicit_start=True))
    else:
        print("Project settings file (wundertool-settings.yml) already exists.")

# Start (and create if not existing) the containers.
def up():
    _compose("up", ["-d"])

# Stop the containers.
def stop():
    _compose("stop")

# Stop and remove the containers.
def down():
    if wundertool.helpers.confirm("This will stop and remove the containers. Are you sure?"):
        _compose("down")

def rm():
    if wundertool.helpers.confirm("This will remove stopped containers. Are you sure?"):
        _compose("rm", ["-f", "--all"])

def ps():
    _compose("ps")

def logs():
    _compose("logs")

# Stop and remove all containers on the system.
def cleanup():
    if wundertool.helpers.confirm("This will stop and remove all containers on your system. Are you sure?"):
        containers = subprocess.check_output(["docker", "ps", "-a", "-q"])
        containers = containers.decode().split("\n")
        containers = list(filter(None, containers))
        print("Stopping all containers on the system...")
        _docker("stop", containers)
        print("Removing all containers on the system...")
        _docker("rm", containers)

# Pass commands to docker-compose bin.
def _compose(command, command_args=[], compose_args=[]):
    settings = wundertool.helpers.get_settings()
    project = "-p %s" % settings.get("project").get("name")
    process = subprocess.run(["docker-compose", project] + compose_args + [command] + command_args)

# Pass commands to docker bin.
def _docker(command, args=[]):
    process = subprocess.run(["docker", command] + args)
