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

There are a few ways you can build your package, egg, wheel or using git and doing setup.py install directly

### Advantages

1. Really easy to use
2. Gives good feedback if you are missing something 
3. It's written in python so as a python dev you are going to be comfortable extending it (like I've done to this setup.py)

### Disadvantages

1. Doesn't handle native package dependencies, sometimes your app requires some things that are included on the system itself. The regular python setuptools only handle Python related stuff and not allowing easy running on the system
2. Doesn't handle OS specific things like setting up services, desktop shortcuts, menu shortcuts...etc
3. Updates aren't handled with the rest of your system
4. Python changing with upgrades to your system might break packages (some of the others fix this)

## Snap packages

Canonical made a fairly approachable Linux packaging system called Snap. It is built around a YAML file that describes how to build the snap. For Python packages it is really easy to build just with setup.py and a little info. 

If you want to start from scratch run:

    snapcraft init
    
It will create a folder called /snap in your root directory and in there will be a `snapcraft.yml` file. 

Then to build your package just run:

    snapcraft

It sets up an environment for the build in a VM using a system called multipass. If you want to avoid it using a VM (for things like github actions, AWS' build pipeline...etc) use:

    snapcraft --destructive-mode

### Advantages

1. Snaps are native apps but they have permissions attached. You should figure out what exactly your app needs, be it network connectivity, the ability to bind to a port, removable media...etc when creating your package.
2. It uses setup.py as a base so pointing to your scripts or libraries is an important step, also looking at the requirements.txt to make sure it has what it needs
3. Once it's building you can upload to the snap store, this is run by Canonical and can be both public and private distribution
4. Can be built externally of the main repo
5. Overall is very easy to pick up and go
6. Automatically updated daily for ease of use for users but also rollbacks are allowed if there are issues
7. Very much batteries included, everything you need is included in the package. If it works when you release you are good for a long time
8. Works on all major Linux distros
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
6. Ability to either pin or do automatic updates

### Disadvantages

1. Really massive barrier to entry for new developers. Since it's a whole OS you are in control of most devs have a hard time getting over the barrier.
2. Since it's running in a container, the filesystem is walled off so you have to juggle with volumes and the like. For most app devs it's not very intuitive but it's amazing for service devs

## Flatpak

Flatpak is a competitor to Snap package made by the Linux community. There are a good few differences. Flatpak runs on the basis of SDKs, anyone can make an SDK, some examples include Freedesktop, Gnome and KDE. Whereas Snap usually is running images based on Ubuntu LTS versions. Different approaches for the same problem really. 

Unlike Snap you have to run through a few extra steps to get the Python image working for you. 

First install flathub (a repo for flatpak packages) and the freedesktop platform and sdk

    flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
    flatpak install flathub org.freedesktop.Platform//1.6 org.freedesktop.Sdk//1.6

Then you have to look in the `org.flatpak.AppName.yml` file and make sure everything that is required is in there. In my example setup.py is used to grab the correct packages needed but sometimes extra stuff like postgres will cause some headaches for dependencies.

Then build:

    flatpak-builder build-dir org.flatpak.PackagingDemo.yml --force-clean
    
Since we have a well designed setup.py file the longest part of the build will be pulling Python and building it. 

A lot of other tutorials will suggest running using:

    flatpak-builder --run build-dir org.flatpak.PackagingDemo.yml --force-clean

But that fails for me when I try it because it will try to use the system libs rather than from inside of the package. Instead I had to:

    flatpak-builder build-dir org.flatpak.PackagingDemo.yml --install --force-clean --user
    flatpak run org.flatpak.PackagingDemo

The latter command is how you run any commandline flatpak package. Once the package is working you can ship it if you want. There are a few options here for flatpak that you can look at here https://docs.flatpak.org/en/latest/publishing.html

### Advantages

1. Unlike Snap you don't have to wait for versions of Python because you are deciding what to ship with your app
2. For compiled applications it's an incredible tool
3. You get exactly what you want in the package
4. For massive applications with multiple shared dependencies it is ideal, given you can make a target SDK for your system based on a platform of your choosing and develop based on your own tools.
5. You can join multiple projects grabbing source tarballs/zip...etc build together and check the hash to make sure it's legitimate
6. Regular check and update pattern, similar to RPM and deb
7. Very easy tools to host your own repositories

### Disadvantages

1. For Python specific applications it has a few added hoops that the other options don't have. Snap's runtime comes with Python already installed and there are docker images which maintain the latest version of Python. For flatpak you get the added hoop to pull the right Python version, compile it and then worry about shipping the app.
2. Has to build C/C++ code from scratch rather than taking advantage of pre-built packages (like available in snap)
3. Very fiddly since it uses json (just my opinion but yml is way more forgiving and IDEs are quite friendly with them instead of json)
4. Generates a lot of junk if you are building locally
5. The builder is great since it uses one file but it would be nice if they had an easier way to generate a bundle. Snap packages and app image both spit out a file, while flatpak generates a directory which is then used for a repository. A file is a lot easier to distribute when you are considering shipping code in an enterprise setting but the repo option is also a good thing if you are maintaining a big backend with connected services. 

## RPM

RedHat Package Manager. This format is the default of Fedora and RedHat Enterprise Linux Desktop/Server for a very long time now. Unlike Snap, Flatpak and Docker, RPM is an older format made to replace distributing with tarballs. It's very stripped back and only contains what the package itself needs to run. Rather than the other formats which have either runtimes or are a full batteries included image. 

Build your Python package:

    python3 setup.py bdist_rpm

That is all really. It reads the setup.py file and generates the .rpm file in the `dist/` directory. It even works on Ubuntu if you install rpm from the archive. It also gives you a tarball of what was inside of the package.

### Advantages

1. From a packaging standpoint it's incredibly easy to use, you just ensure the required fields are included and it sorts out the rest
2. Is a proper 100% native package, no containerization

### Disadvantages

1. It's very much tied to RedHat managed distributions. Flatpak, Snap, AppImage and Docker are more targeted at distributing everywhere
2. Containerization and security are concerns for users and the other formats have that included as part of their design. If you are distributing for your own use it's fine but the other approaches work better if you want to get your app out there
3. The build process with Python works for simple apps but requires fiddling to get the right packages installed for more complex apps

## Debian package (deb)

The dpkg packaging system is the default in Ubuntu and Debian as well as derivatives of those like Pop!_OS and Mint. Basically the same advantages and disadvantages as RPM packages but dpkg is a much more popular. 

I'm going to avoid doing the longer approach for building this package and instead give the easiest shortcut. 

Build the package using RPM above (same command) then run:

    python3 setup.py bdist_rpm
    sudo alien dist/packaging-demo-20200625-1.noarch.rpm
    
It's not like the deb packages are too hard to build but the tools to build aren't easy and it doesn't really help the user much. Most of the information needed is available in the setup.py about the authors, license, url...etc but you duplicate that info in the debian folder. Where most other tools pickup and go with what Python offers or at least make an option for you to script it, the tools for deb packages don't. The longer guide is below but I'd recommend steering clear unless you really have to. 

So ignore the above if you want to do it properly but still it's annoying so be warned. 

    mkdir debian # make a folder for the configuration files
    echo "10" > debian/compat # I've been using Ubuntu for more than a decade, they always said this was for historical purposes but never bothered removing it, it's cruft and makes the system look annoying
    dch --create # make a changelog (this is actually a great step for every project)

Then the complex thing to explain. Make a debian/control file. This similarly to the other systems is describing the package overall and what is needed to run it. I basically just copy well made control files from bigger projects and use them as a base changing the information required. You will need to know what is needed to build your software and what is needed to run it. So minimum package versions in the Debian/Ubuntu...etc repo and their names. 

Almost there. Then copy in the debian/rules file from this repo into your debian folder. 

Last check you should now have 4 files, `changelog`, `compat`, `control` and `rules`, that is all the requirements set pretty much. Last command to run is:

    debuild -b -us -uc

Then in the the folder above the folder you are should have a .deb file with all the requirements. 

### Advantages and disadvantages

Same as RPM really.

## AppImage

AppImage is super interesting, it's in short the Apple style of packaging, where it's an app bundle that is runable. It looks like a single file but it runs anywhere on Linux. 

I'm not going to give a tutorial for it more than saying you can use a deb package to create an AppImage which is probably the easiest way. With this guide I wanted mostly to look at the tools surrounding the various packaging systems and compare how easy all they were for a fairly common language (Python obviously) but I think AppImage while it's an interesting idea I think is a fairly poor path for Python devs to ship their software. 

I'll still give my advantages and disadvantages because I did investigate the format quite a bit and I feel like it's worthy of discussion though. 

### Advantages

1. A really easy one but important to say, requires no installation to run the program, it's just a file, the file you can just run in the terminal directly. All the rest require various types of installs but AppImage gives you a runable by default. In terms of zero to working only waiting on a download is a massive thing for a small app.
2. Fairly future proof in design. It just works, no fragmentation between distros, no describing various OS level stuff about installing or whatever, you just run it and mostly could be run just with a "mark as executable" in the file manager and double clicking run
3. You are getting the file directly from the developers of the source rather than through a third party. This is both an advantage and a disadvantage, it's familiar for a Windows user to go to websites to download some application but repositories are the normal thing for Linux distribution. I'd say this is more important as a feature for enterprise; it may be easier to host their own package rather than sign agreements with various distros to get into partner repositories or running the distribution of the package through legal beyond the regular EULA. I know there are devs who would take this route.

### Disadvantages

1. Probably the least developed in terms of tooling around packaging. It may be OK for other languages but Python it doesn't seem very fun to use. Snap and RPM took around 20 minutes total. I played around with deb packages and AppImage for a few days. Flatpak was an hour or two but none I felt like I was struggling with more than deb and AppImage. And note Python tools are very developed and easy to use it's not impossible to write a really easy system, RPM has proven you can just hook into the Python system and Snap uses the setuptools really well too.
2. Documentation isn't very approachable. I complained about deb packages being frustrating in comparison to other formats but deb packaging had at least a lot of documentation and a lot of questions answered in loads of places. Loads of tutorials from devs as well. The others were just easy enough not to require extensive documentation but deb made up for bad tooling with good documentation. AppImage felt a bit meh on both. There is a forum you can ask questions and the devs will answer directly which is great but it would be better if they took some time and some various languages and tried to use their format and do a step by step tutorial on how it works in relation to each. 
3. While it's a slight advantage to be able to download the file and launch it directly it brings three issues. One is updates not being handled well. Two is security, apps are limited to your home directory but there isn't containerization like Snap and Flatpak. The last one is just discoverability not being great. The others all have channels where you can easily search and find the apps. AppImage you are running to Google...etc finding the app and grabbing it, taking care for security and then running it but the others are all doing the centralized approach which has been a Linux thing for decades now. 
