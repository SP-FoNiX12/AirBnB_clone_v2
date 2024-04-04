#!/usr/bin/python3
"""
Fabric script to create and distribute an archive to web servers
"""

from fabric.api import env, local, put, run, sudo
from datetime import datetime
from os.path import exists, isdir


# Define remote hosts
env.hosts = ["52.91.116.161", "18.207.234.225"]


def do_pack():
    """
    Generates a tgz archive of the web_static folder
    Returns: Path to the created archive, None if unsuccessful
    """
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if not isdir("versions"):
            local("mkdir -p versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception as e:
        print("Failed to pack archive:", e)
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    Args:
        archive_path: Path to the archive to deploy
    Returns: True if deployment is successful, False otherwise
    """
    if not exists(archive_path):
        print("Archive not found:", archive_path)
        return False
    try:
        file_name = archive_path.split("/")[-1]
        no_ext = file_name.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        sudo("mkdir -p {}{}/".format(path, no_ext))
        sudo("tar -xzf /tmp/{} -C {}{}/".format(file_name, path, no_ext))
        sudo("rm /tmp/{}".format(file_name))
        sudo("mv {0}{1}/web_static/* {0}{1}/".format(path, no_ext))
        sudo("rm -rf {}{}/web_static".format(path, no_ext))
        sudo("rm -rf /data/web_static/current")
        sudo("ln -s {}{}/ /data/web_static/current".format(path, no_ext))
        return True
    except Exception as e:
        print("Failed to deploy:", e)
        return False


def deploy():
    """
    Creates and distributes an archive to the web servers
    Returns: True if deployment is successful, False otherwise
    """
    archive_path = do_pack()
    if archive_path:
        return do_deploy(archive_path)
    return False
