# linux-packaging

This is a sample repo with multiple Linux packaging types. Docker, Snap and Flatpak for Python projects.

## Setup

First file you want to create is setup.py for your project if you don't already have one. I usually structure my projects like bin/ project_name/ tests/ where project_name contains libraries for my code and bin is scripts I want to run later. 

touch setup.py
touch requirements.txt
mkdir bin
mkdir project_name # replace this with whatever your project is called
