WATSAN Portal: Kibera
=======

About
=======
This is a web application written almost entirely in free and open source software. The backend is Django, a web framework written in the Python programming language, and deals with all of the server side code. In the front-end we use javascript, jQuery, and Backbone.js for interactivity.  Tuktuk.css is used for making the page layouts responsive. Leaflet.js is an opensource mapping application which we use for the map interactivity and overlaying borders and landmarks. The one non-open source piece that we use is the Google Maps Javascript library. We use this underneath Leaflet because it is the best source of free satellite imagery and has an accurate database of landmarks, which we use for the user searches.

Functionality
=======
Basic
-----
Our target users are officials from NGOs, CBOs and members of the public who wish to connect to the municipal water and sewer infrastructure. The workflow they follow is detailed here. First the user creates a Project. A Project is a facility that they wish to build that needs a water and/or sanitation connection. Each Project can have multiple Sites, which are possible locations for the facility. To choose Sites, the user is taken to a map with satellite imagery, roads, and well known landmarks. The area in which the software can estimate costs and distances is clearly marked out (the pilot area). When a user clicks a location on the map, the tool asks them to save the location. Once saved, the Site is added to the list at the right, which gives information about the estimated cost and distance to the nearest sewer and water lines. The user can also view information about the nearest landmarks and GPS Coordinates. If a user types a location or landmark and searches for it in the search box, they can click on a result, causing the map to zoom to that location. The user can also enter GPS coordinates manually to create a Site. The user can enter and save multiple sites for comparison. If the user returns to the Project page, it lists all of the Sites they have chosen and the related information about costs and locations. Finally, the user can get the information about who they need to talk to at NCWSC, what forms they need to fill in, and what information each form requires.

Administration
--------------
When a user signs up for the platform they enter their name and email address, as well as some basic information about how they discovered the platform and what organization they are from. The user can add additional users to their organization at any time from the settings menu. This will allow multiple users to view the same Projects and Sites.

Installation
=======
The Watsan project is packaged as a Django app and includes a fabfile ( fabfile.py ) that will install all the linux and python packages for you. 


Install packages
----------------
First, install fabric: sudo pip install fabric. If you are not familiar with fabric you can read up on it [here](http://docs.fabfile.org/en/1.8/)

Setting up on your local:
	$ /project-root/ fab setup -H localhost
	$ /project-root/ fab install_python_packages (or if you have a virtualenv and you're using virtualenvwrapper) $ /project-root/ fab install_python_packages('your_virtualenv_name')

	Check fabfile.py for more detail about what packages are being installed.


Setup spatial database
----------------------
Run the following commands:
	$ sudo -u postgres psql
	psql (9.1.9)
	Type "help" for help.

	postgres=# CREATE DATABASE your_database_name;
	CREATE DATABASE
	postgres=#CREATE USER your_user WITH PASSWORD 'your_password' LOGIN; //make sure the user you create is also a linux user
	CREATE USER
	postgres=#GRANT ALL PRIVILEGES ON DATABASE your_database_name to your_user;
	GRANT
	postgres=#\c your_database_name
	your_database_name=#CREATE EXTENSION postgis;
	CREATE EXTENSION
	your_database_name=#CREATE EXTENSION postgis_topology;
	CREATE EXTENSION


Settings and Urls file
----------------------
The settings.py file should have the following apps under INSTALLED_APPS:

	INSTALLED_APPS = (
    'longerusername', # has to come first
    'grappelli', # has to come before django.contrib.admin
    'sorl.thumbnail', 
    'south',
    'djangoplugins',
    'django.contrib.gis',
    'shapes',
    'form_utils',
    'djcelery',
    'watsan',
    'user_control',
 	.......
)

Still in the settings.py file, your DATABASE settings should look like:

	DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'collective_geodjango',
        'USER': 'your_user',
        'PASSWORD': 'your_password'
    },
}

If you're runnning a local development environment ( ./manage.py runserver ), make sure the static and media urls are correct
in the file spatialcollective/urls.py

The urls.py file patterns should include:

	(r'^', include('watsan.urls'))

Make sure you syncdb then run the watsan migration:

	$ python manage.py syncdb
	$ python manage.py migrate watsan

You can now run it locally:

	$ python manage.py runserver





