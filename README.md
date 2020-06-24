# linux-packaging

This is a sample repo with multiple Linux packaging types. Docker, Snap and Flatpak for Python projects.

## Setup

First file you want to create is setup.py for your project if you don't already have one. I usually structure my projects like bin/ project_name/ tests/ where project_name contains libraries for my code and bin is scripts I want to run later. 

    touch setup.py
    touch requirements.txt
    mkdir bin
    mkdir project_name # replace this with whatever your project is called

## Versioning

Big or small I always like to have visual representations of version in the repo somewhere. This in my case is a VERSION file which I usually auto generate but you can do this statically or have it in the setup.py file.

## Setup.py

Setuptools is a great way of packaging stuff just for Pypi or even interally for your project sending wheels or eggs to users of your libraries or scripts but also is the basis of a bunch of other tools so is the first thing you start off with. There are loads of examples of good setup.py files around. For packaging especially outside of wheels, eggs, tarballs they might not need a lot of info in there. I keep just the basics in my setup.py files to not annoy setuptools but feel free to add more if your project needs it. 

The documentation is here for this step: https://packaging.python.org/tutorials/packaging-projects/

## Snap packages

Canonical made a fairly approachable Linux packaging system called Snap. It is built around a .yml file that describes how to build the snap. For Python packages it is really easy to build just with setup.py and a little info. 

If you want to start from scratch run:

    snapcraft init
    
It will create a folder called /snap in your root directory and in there will be a snapcraft.yml file. 

###Advantages

1. Snaps are native apps but they have permissions attached. You should figure out what exactly your app needs, be it network connectivity, the ability to bind to a port, removable media...etc when creating your package.
2. It uses setup.py as a base so pointing to your scripts or libraries is an important step, also looking at the requirements.txt to make sure it has what it needs
3. Once it's building you can upload to the snap store, this is run by Canonical and can be both public and private distribution
4. Can be built externally of the main repo
5. Overall is very easy to pick up and go
6. Automatically updated daily for ease of use for users but also rollbacks are allowed if there are issues
7. Very much batteries included, everything you need is included in the package. If it works when you release you are good for a long time
8. Native packages but available on multiple different Linux distros
9. Strong backing from desktop app devs
10. Can setup services with systemd for you https://snapcraft.io/docs/services-and-daemons

###Disadvantages

1. App size is fairly big because they bundle things per library
2. There is only one centralized store rather than multiple to choose from which some devs might not like
3. It's easy to use mostly but takes a while to get your head around the concepts
