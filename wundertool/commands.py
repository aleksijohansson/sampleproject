
# Needed system modules.
import subprocess
import os
import inspect

# Docker.
import docker

# Get the submodules
import wundertool.helpers

# Init a wundertool enabled project.
def init():
    wundertool.helpers.create_settings()

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

# Remove stopped containers.
def rm():
    if wundertool.helpers.confirm("This will remove stopped containers. Are you sure?"):
        _compose("rm", ["-f", "--all"])

# List containers of the project.
def ps():
    _compose("ps")

# Show logs from containers of the project.
def logs():
    _compose("logs")

# Stop and remove all containers on the system.
# TODO: Update this to use docker-py Client.
def cleanup():
    if wundertool.helpers.confirm("This will stop and remove all containers on your system. Are you sure?"):
        containers = subprocess.check_output(["docker", "ps", "-a", "-q"])
        containers = containers.decode().split("\n")
        containers = list(filter(None, containers))
        print("Stopping all containers on the system...")
        _docker("stop", containers)
        print("Removing all containers on the system...")
        _docker("rm", containers)

# Start a developer shell mapping source and linking to containers of the project.
# TODO: Change this so that each shell name is unique so that we can run multiple shells at once.
# TODO: Add host volume project mount to this command so that it automatically always mounts the project folder to /app/project
def shell():
    settings = wundertool.helpers.get_settings()
    cli = docker.Client()
    containers = cli.containers(all=True)
    # Get the containers of this project.
    links = []
    volumes = []
    net = "default" # Assume default network.
    for container in containers:
        if container.get("Labels").get("com.docker.compose.project") == settings.get("project").get("name"):
            # Link all the containers in the project.
            name = container.get("Names")
            name = name[0].strip("/")
            # Get volumes from all the containers.
            if container.get("Mounts"):
                volumes.append("--volumes-from=%s" % name)
            links.append("--link=" + name + ":" + container.get("Labels").get("com.docker.compose.service") + ".app")
            # Get the network the project containers use.
            for network in container.get("NetworkSettings").get("Networks"):
                # Assumes project services are in a single network.
                net = network
    _docker("run", [
        "--rm",
        "-t",
        "-i",
        "--name=%s_shell" % settings.get("project").get("name"),
        "--hostname=%s" % settings.get("project").get("name"),
        "--net=%s" % net,
        ] + links + volumes + [
        settings.get("images").get("shell"),
    ])

def build():
    # Get volumes of containers in the project.
    # Generate a Dockerfile where those volumes are added into the image.
    # Build the images with the project name and branch included in the name.
    print("Undefined command.")

def push():
    # Push the built images with their tags.
    print("Undefined command.")

# List available commands.
def commands():
    all_functions = inspect.getmembers(wundertool.commands, inspect.isfunction)
    function_names = []
    for function in all_functions:
        if not "_" in function[0]:
            function_names.append(str(function[0]))
    print("Available commands are:\n%s" % "\n".join(function_names))

# Pass commands to docker-compose bin.
def _compose(command, command_args=[], compose_args=[]):
    settings = wundertool.helpers.get_settings()
    project = "-p %s" % settings.get("project").get("name")
    compose = os.path.join(os.path.dirname(__file__), "compose", "script", "run", "run.sh")
    process = subprocess.run([compose, project] + compose_args + [command] + command_args)

# Pass commands to docker bin.
# TODO: Change this to use docker-py Client.
def _docker(command, args=[]):
    process = subprocess.run(["docker", command] + args)
