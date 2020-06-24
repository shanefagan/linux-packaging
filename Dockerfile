FROM python:3-alpine

# Put your code into /tmp so it's cleaned after the setuptools moves it to the scripts directory
COPY . /tmp

WORKDIR /tmp

RUN python setup.py install

WORKDIR /

# optional
# if you want to run as a python REPL and not running the app directory just delete/comment out the next line
CMD ["app.py"]
