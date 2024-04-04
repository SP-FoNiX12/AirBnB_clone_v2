#!/usr/bin/python3
"""
deployed fabric
"""
from datetime import datetime
from fabric.api import local, task


@task
def do_pack():
    """ A script that generates archive the contents of web_static folder"""
    time = datetime.now()
    archive = 'web_static_' + time.strftime("%Y%m%d%H%M%S") + '.' + 'tgz'
    local('mkdir -p versions')
    create = local('tar -cvzf versions/{} web_static'.format(archive))
    if create.return_code == 0:
        return archive
    else:
        return None
