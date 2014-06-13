"""
Python version: 2.7
Linux distro: Ubuntu 13.10, Ubuntu 14.04
Dependency: Fabric, pip
	install pip: sudo apt-get install python-pip
	install fabric: sudo pip install fabric

Summary: This script installs python and linux packages for the SpatialCollective Web Platform.


"""
from fabric.api import *
from fabric.contrib.files import exists

#sets up linux packages necessary for geodjango to run
def setup():
	sudo("apt-get install postgresql-9.3 postgresql-server-dev-9.3 postgresql-contrib-9.3 postgresql-9.3-postgis-2.1")
	sudo("apt-get install gdal-bin binutils libgeos-3.4.2 libgeos-c1 libgeos-dev libgdal1-dev libxml2 libxml2-dev")
	sudo("apt-get install python-psycopg2")

def install_python_packages(virtualenv=None):
	if virtualenv:
		sudo("workon %s && pip install -r requirements.txt"% virtualenv)
	else:
		sudo("pip install -r requirements.txt")
