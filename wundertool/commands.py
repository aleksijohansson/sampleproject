
# Needed system modules.
import subprocess
import os
import inspect

# Docker.
import docker

# Get the submodules
import wundertool.helpers
import wundertool.handler

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

def rm():
    if wundertool.helpers.confirm("This will remove stopped containers. Are you sure?"):
        _compose("rm", ["-f", "--all"])

def ps():
    _compose("ps")

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

def shell():
    settings = wundertool.helpers.get_settings()
    cli = docker.Client()
    containers = cli.containers()
    # Get the containers of this project.
    links = []
    net = "default" # Assume default network.
    for container in containers:
        if container.get("Labels").get("com.docker.compose.project") == settings.get("project").get("name"):
            links.append("--link=" + container.get("Id") + ":" + container.get("Labels").get("com.docker.compose.service") + ".app")
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
        ] + links + [
        settings.get("images").get("shell"),
    ])

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
    process = subprocess.run(["docker-compose", project] + compose_args + [command] + command_args)

# Pass commands to docker bin.
# TODO: Change this to use docker-py Client.
def _docker(command, args=[]):
    process = subprocess.run(["docker", command] + args)
