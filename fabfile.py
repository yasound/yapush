import os.path
from fabric.api import *
from fabric.utils import puts
from fabric.contrib.files import sed, uncomment, append, exists

def prod():
    global WEBSITE_PATH
    global APP_PATH
    global GIT_PATH
    global BRANCH
    global DJANGO_MODE

    env.forward_agent = 'True'
    env.hosts = [
        'yas-web-01.ig-1.net',
        'yas-web-02.ig-1.net',
        'yas-web-03.ig-1.net',
        'yas-web-04.ig-1.net',
        'yas-web-05.ig-1.net',
        'yas-web-06.ig-1.net',
        'yas-web-07.ig-1.net',
        'yas-web-08.ig-1.net',
        'yas-web-09.ig-1.net',
        'yas-web-10.ig-1.net',
    ]
    env.user = "customer"
    WEBSITE_PATH = "/data/vhosts/y/yapush/root/"
    APP_PATH = "yapush"
    GIT_PATH = "git@github.com:yasound/yapush.git"
    BRANCH = "master"
    DJANGO_MODE = 'production'

def dev():
    global WEBSITE_PATH
    global APP_PATH
    global GIT_PATH
    global BRANCH
    global DJANGO_MODE
    env.forward_agent = 'True'
    env.hosts = [
        'sd-14796.dedibox.fr',
    ]
    env.user = "customer"
    WEBSITE_PATH = "/var/www/push.yasound.com/root/"
    APP_PATH = "yapush"
    GIT_PATH = "git@github.com:yasound/yapush.git"
    BRANCH = "dev"
    DJANGO_MODE = 'development'

def deploy():
    """[DISTANT] Update distant django env
    """
    with cd(WEBSITE_PATH):
        run("git checkout %s" % (BRANCH))
        run("git pull")
        run("./vtenv.sh")
    with cd("%s/%s" % (WEBSITE_PATH, APP_PATH)):
        run("/etc/init.d/yapush stop")
        run("/etc/init.d/yapush start")




def test():
    """[DISTANT] restart services
    """
    with cd("%s/%s" % (WEBSITE_PATH, APP_PATH)):
        run("ls")
