
import subprocess

# Get the submodules.
import wundertool.helpers

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

def ps():
    _compose("ps")

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
    settings = wundertool.handler.settings()
    project = "-p %s" % settings.get("project_name")
    process = subprocess.run(["docker-compose", project] + compose_args + [command] + command_args)

# Pass commands to docker bin.
def _docker(command, args=[]):
    process = subprocess.run(["docker", command] + args)
