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

Canonical made a fairly approachable Linux packaging system called Snap. It is built around a YAML file that describes how to build the snap. For Python packages it is really easy to build just with setup.py and a little info. 

If you want to start from scratch run:

    snapcraft init
    
It will create a folder called /snap in your root directory and in there will be a snapcraft.yml file. 

### Advantages

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
11. Since it's built from Ubuntu you have prebuilt deb packages (along with the security of the Ubuntu repo), pip packages.

### Disadvantages

1. App size is fairly big because they bundle everything (similar to Docker in that respect but Flatpak you have the ability to make smaller images if the runtime bundles stuff for you)
2. There is only one centralized store rather than multiple to choose from which some devs might not like. This is a concern but you may also host your own snap packages https://ubuntu.com/blog/howto-host-your-own-snap-store
3. It's easy to use mostly but takes a while to get your head around the concepts

## Docker

Docker is a hugely popular container packaging system. Easiest way to explain it is it's an OS and your apps in a bottle. You can ship that bottle to most modern OSes and architectures. 

To create a Docker image you need to create a Dockerfile. In the repo I have included a simple one you can build from. 

To build a Dockerfile you can run:

docker build . --tag appname:version

To run your docker container after it's built you just specify the tag you defined above:

docker run appname:version

### Advantages

1. Since it's in a container, it is build once run anywhere. If it works on one system it will run on Windows, in the cloud, on Linux, anywhere. 
2. You are under complete control over what goes into the container
3. Amazing for services when using tools like docker-compose, cloud services like ESR, Azure App Service, Kubernetes...etc.  
4. With python it's fairly amazing because you can setup your libraries in the container and run it just with the REPL and have an amazing commandline interface for your app for free
5. Since updates are handled by tag, you have complete control over when/if you update

### Disadvantages

1. Really massive barrier to entry for new developers. Since it's a whole OS you are in control of most devs have a hard time getting over the barrier.
2. Since it's running in a container, the filesystem is walled off so you have to juggle with volumes and the like. For most app devs it's not very intuitive but it's amazing for service devs

## Flatpak

Flatpak is a competitor to Snap package made by the Linux community. There are a good few differences. Flatpak runs on the basis of SDKs, anyone can make an SDK, some examples include Freedesktop, Gnome and KDE. Whereas Snap usually is running images based on Ubuntu LTS versions. Different approaches for the same problem really. 

Unlike Snap you have to run through a few extra steps to get the Python image working for you. 

First install flathub (a repo for flatpak packages) and the freedesktop platform and sdk

    flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
    flatpak install flathub org.freedesktop.Platform//1.6 org.freedesktop.Sdk//1.6

Then you have to look in the `org.flatpak.AppName.json` file and make sure everything that is required is in there. In my example setup.py is used to grab the correct packages needed but sometimes extra stuff like postgres will cause some headaches for dependencies.

Then build:

    flatpak-builder build-dir org.flatpak.PackagingDemo.json --force-clean
    
Since we have a well designed setup.py file the longest part of the build will be pulling Python and building it. 

### Advantages

1. Unlike Snap you don't have to wait for versions of Python because you are deciding what to ship with your app
2. For compiled applications it's an incredible tool
3. You get exactly what you want in the package
4. For massive applications with multiple shared dependencies it is ideal, given you can make a target SDK for your system based on a platform of your choosing and develop based on your own tools.
5. You can join multiple projects grabbing source tarballs/zip...etc build together and check the hash to make sure it's legitimate

### Disadvantages

1. For Python specific applications it's a bit much in comparison to the other options
2. Has to C/C++ code from scratch rather than taking advantage of pre-built packages (like available in snap)
3. Very fiddly since it uses json (just my opinion but yml is way more forgiving and IDEs are quite friendly with them instead of json)
4. Generates a lot of junk if you are building locally
